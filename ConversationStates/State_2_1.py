# -*- coding: utf-8 -*-

import random
from config import system_response_text, nlu_slots, conversation_states
from helperClasses import Calculator, RecipeSearcher, SystemResponseGenerator
from ConversationStates import State_2_2

# Anne:


# handles different types of restrictions (in h_nlu() at bottom), updates conversation count (in if-elif-conditions)
def handle_conversation_question(context, update, db, nlu, model, details):
    # behandelt dirkete Ja/Nein-Antworten auf die Fragen
    previous_message = model.replied_message
    user_query = update.message.text.lower()
    # handle_binary_and_restricted_answers_on_conversation_stock_questions()
    if previous_message == system_response_text.CUISINE_SOLID:  # Wie stehst du zu deftigem Essen?
        handle_solid_cuisine(model, details, nlu.get_answer(user_query), user_query)
    elif previous_message == system_response_text.EATING_VEGAN:
        handle_vegan(model, details, nlu.get_answer(user_query), user_query)
    elif previous_message == system_response_text.EATING_VEGETARIAN:
        handle_vegetarian(model, details, nlu.get_answer(user_query), user_query)
    elif previous_message == system_response_text.CUISINE_SEASONAL:  # Wie stehst du zu saisonalem Essen?
        handle_seasonal_cuisine(model, details, nlu.get_answer(user_query))
    elif previous_message == system_response_text.RECIPE_SWEET:  # "Magst du etwas süßes Essen?"
        handle_sweet_recipe(model, details, nlu.get_answer(user_query), user_query)
    elif previous_message == system_response_text.CUISINE_REGIONAL:  # "Wie stehst du zu regionaler Küche?"
        handle_regional(model, details, nlu.get_answer(user_query))
    elif previous_message == system_response_text.ALLERGY:  # "Gibt es Allergiker?"
        handle_allergy(model, details, nlu.get_answer(user_query)) # ANNE: nur ja, nein-Antwort möglich -> NUTZER FEEDBACK!
    # ANNE todo: testen ob laktoseintolleranz erkannt wird in handle_nlu
    elif previous_message == (system_response_text.COOKING_SKILLS or system_response_text.COOKING_DIFFICULTY):
        # "Wie würdest du deine Kochfähigkeiten einschätzen?" or "Wie ausgefallen darf das Rezept sein?"
        handle_difficulty(model, details, user_query)
    # Anne: removed several elif, because SERVINGS_NUM, COOKING_PREPARATION_LIKE, CUISINE_COUNTRY, RECIPE_DURATION
    # (and indirectly EATING_HABITS) are in handle_NLU as custom_slot
    system_message = handle_nlu(db, nlu, model, details, update)
    return system_message


# updates the counter of the conversation and ingredient stock (state 2.1 and 2.2)
def update_count(model, slot_name):
    if slot_name == nlu_slots.INGREDIENT_NAME:
        model.ingredients_count += 1
    # updates the count only if the slotName is None
    if (slot_name is None) or (slot_name == []):
        model.conversation_items_count += 1


# sets the sweet value for the query
def handle_solid_cuisine(model, details, quest_answer, user_query):
    update_count(model, details.is_sweet)
    if quest_answer or ("deftig" in user_query or
                        "pikant" in user_query or
                        "herzhaft" in user_query or
                        "salz" in user_query and
                        nlu_slots.NO_VALUE not in user_query and
                        "nicht" not in user_query):
        details.is_sweet = 0
    else:
        details.is_sweet = 1


# previous question gets processed with the current user input
def handle_seasonal_cuisine(model, details, quest_answer):
    if quest_answer:
        season = Calculator.calculate_current_season()
        if ("Frühling" and "Sommer" and "Herbst" and "Winter") not in details.all_categories:
            update_count(model, details.all_categories)
            append_to_all_categories(details, season)


def handle_sweet_recipe(model, details, quest_answer, user_query):
    update_count(model, details.is_sweet)
    if (quest_answer) or ("süß" in user_query and nlu_slots.NO_VALUE not in user_query and "nicht" not in user_query):
        details.is_sweet = 1
    else:
        details.is_sweet = 0


def handle_allergy(model, details, quest_answer):
    if quest_answer:
        if "Allergien und Unverträglichkeiten" not in details.all_categories:
            append_to_all_categories(details, "Allergien und Unverträglichkeiten")
        if "laktosfrei" not in details.all_categories:
            append_to_all_categories(details, "laktosefrei")
    model.conversation_items_count += 1


def handle_difficulty(model, details, user_query):
    if ("gut" or "ok") in user_query:
        details.recipe_difficulty = "mittel"  # 17.237 recipes in DB
    # Anne: added other difficulty levels
    elif "schlecht" in user_query:
        details.recipe_difficulty = "leicht"  # 2.921.273 recipes in DB
    elif ("super" or "exzellent") in user_query:
        details.recipe_difficulty = "schwer"  # 849 recipes in DB
    update_count(model, details.recipe_difficulty)


def handle_regional(model, details, quest_answer):
    if quest_answer:
        if "Regionale Küche" not in details.all_categories:
            append_to_all_categories(details, "Regionale Küche")
    model.conversation_items_count += 1


def handle_vegan(model, details, quest_answer, user_query):
    if quest_answer:
        if "Vegan" not in details.all_categories or "Vegan" in user_query:
            append_to_all_categories(details, "Vegan")
            model.available_conversation_questions.remove(system_response_text.EATING_VEGETARIAN)
            model.available_conversation_questions.remove(system_response_text.EATING_HABITS)
    model.conversation_items_count += 1


def handle_vegetarian(model, details, quest_answer, user_query):
    if quest_answer:
        if "Vegetarisch" not in details.all_categories or "vegetarisch" in user_query or "vegetarier" in user_query:
            details.recipe_diet.append("Vegetarisch")
            append_to_all_categories(details, "Vegetarisch")
            model.available_conversation_questions.remove(system_response_text.EATING_VEGAN)
            model.available_conversation_questions.remove(system_response_text.EATING_HABITS)
    model.conversation_items_count += 1


# if the slot value for the categories doesn't exists in all categories the value is added
def append_to_all_categories(details, value):
    if value not in details.all_categories:
        details.all_categories.append(value)


# ANNE TODO HANDLE NLU durchtesten! -> wo wird curr_rec beschrieben?!
def handle_nlu(db, nlu, model, details, update):
    nlu_data = nlu.parse_user_query(update.message.text)
    model.framework_state = conversation_states.CONVERSATION_STOCK_STATE
    for intents in nlu_data:
        intent = intents["intent"]["intentName"]
        all_slots = intents["slots"]
        slot_minutes = 0
        if intent is None:
            pass
        for slot in all_slots:
            slot_value = slot["value"]
            # Claudia: entity uses built_in names
            slot_name = slot["slotName"]
            if slot_value["kind"] == nlu_slots.SNIPS_SERVINGS_NUMBER:
                # Claudia: alternative use slotName == "recipeServings"
                handle_number_of_servings_slot(model, details, slot_value)
            elif slot_value["kind"] == nlu_slots.SNIPS_DURATION:
                # Claudia: alternative use slotName == "recipeDuration"
                slot_minutes = handle_duration_slot(model, slot_minutes, slot_value)
            elif slot_value["kind"] == "Custom":  # custom entities
                handle_custom_slot(update, db, nlu, model, details, slot_value, slot_name)
        if slot_minutes > 0:  # has to be separate
            update_count(model, details.recipe_duration)
            details.recipe_duration = slot_minutes
    # Anne: changed for clarification (no returning of another method)
    system_message = get_system_message(model, details)
    return system_message

# ANNE: TODO sollte vielleicht in Response Generator oder MAin
def get_system_message(model, details):
    print("\t conversation count: " + str(model.conversation_items_count))
    print("\t ingredients count: " + str(model.ingredients_count))
    if details.current_recipe is not None:
        model.framework_state = conversation_states.TITLE_DISPLAY_STATE # (3.1)
        system_message = SystemResponseGenerator.get_recipe_recommendation(details.current_recipe[1])
        return system_message
    elif model.ingredients_count > 0 or model.conversation_items_count > 2:
        # Anne: conversation benchmark reached
        # (2.2) -> ask for ingredients
        model.framework_state = conversation_states.INGREDIENT_STOCK_STATE
        curr_ingredient_question = State_2_2.select_ingredient_question(model)
        print(curr_ingredient_question)
        return curr_ingredient_question
    elif model.conversation_items_count <= 2:
        curr_conversation_question = select_conversation_question(model)
        print(curr_conversation_question)
        return curr_conversation_question


# selects the available questions for conversation
def select_conversation_question(model):
    if not model.available_conversation_questions:
        model.framework_state = conversation_states.INGREDIENT_STOCK_STATE
        # return select_ingredient_question() # in state 2.2
        # Anne: removed return, because internally handled in model
        State_2_2.select_ingredient_question(model)  # in state 2.2
    question = random.choice(model.available_conversation_questions)
    model.available_conversation_questions.remove(question)
    model.replied_message = question
    return question

############################## number of servings, duration=prep_time, custom slots ####################################


def handle_number_of_servings_slot(model, details, slot_value):
    update_count(model, details.recipe_servings)
    details.recipe_servings = slot_value["value"]
    if system_response_text.SERVINGS_NUM in model.available_conversation_questions:
        model.available_conversation_questions.remove(system_response_text.SERVINGS_NUM)


def handle_duration_slot(model, slot_minutes, slot_value):
    slot_minutes += Calculator.calculate_minutes(slot_value)
    if system_response_text.RECIPE_DURATION in model.available_conversation_questions:
        model.available_conversation_questions.remove(system_response_text.RECIPE_DURATION)
    return slot_minutes


# big switch: fine grain difference in slot values or sth.. (anne) update, db, nlu, slot_value, slot_name
def handle_custom_slot(update, db, nlu, model, details, slot_value, slot_name):
    slot_real_value = slot_value["value"]
    if slot_name == nlu_slots.RECIPE_DIET:
        slot_is_diet(model, details, slot_real_value)
    elif slot_name == nlu_slots.RECIPE_SERVINGS_PARAPHRASE:
        slot_paraphrases_servings(model, details, )
    elif slot_name == nlu_slots.RECIPE_PREPARATION:
        slot_is_preparation(model, details, slot_real_value)
    elif slot_name == nlu_slots.RECIPE_ORIGIN:
        slot_is_regional_or_country_origin(model, details, slot_real_value)
    elif slot_name == nlu_slots.RECIPE_DIFFICULTY:
        slot_is_difficulty(model, details, slot_real_value)
    elif slot_name == nlu_slots.RECIPE_NAME:
        handle_recipe_name_slot(db, model, details, slot_real_value)
    elif slot_name == nlu_slots.RECIPE_DURATION_PARAPHRASE:
        slot_paraphrases_duration(model, details)
    elif slot_name == nlu_slots.RECIPE_CATEGORY:
        handle_recipe_category_slot(model, details, slot_real_value)
    elif slot_name == nlu_slots.INGREDIENT_NAME:
        slot_is_ingredient(nlu, model, details, slot_real_value, update)
    elif slot_name == nlu_slots.RECIPE_OTHER:
        handle_recipe_other_slot(model, details, slot_real_value)


###################################### 'switch' defs in handle_custom_slot() ###########################################
#
def slot_is_diet(model, details, slot_real_value):
    update_count(model, details.recipe_diet)
    if slot_real_value not in details.recipe_diet:
        details.recipe_diet.append(slot_real_value)
        append_to_all_categories(details, slot_real_value)
    if system_response_text.ALLERGY in model.available_conversation_questions:
        model.available_conversation_questions.remove(system_response_text.ALLERGY)
    if system_response_text.EATING_VEGAN in model.available_conversation_questions:
        model.available_conversation_questions.remove(system_response_text.EATING_VEGAN)
    if system_response_text.EATING_VEGETARIAN in model.available_conversation_questions:
        model.available_conversation_questions.remove(system_response_text.EATING_VEGETARIAN)


#
def slot_paraphrases_servings(model, details):
    update_count(model, details.recipe_servings)
    if system_response_text.SERVINGS_NUM in model.available_conversation_questions:
        model.available_conversation_questions.remove(system_response_text.SERVINGS_NUM)
    if details.recipe_servings is None:
        details.recipe_servings = 1
    else:
        details.recipe_servings += 1


#
def slot_is_preparation(model, details, slot_real_value):
    update_count(model, details.recipe_preparation)
    details.recipe_preparation = slot_real_value
    append_to_all_categories(details, slot_real_value)
    if system_response_text.COOKING_PREPARATION_LIKE in model.available_conversation_questions:
        model.available_conversation_questions.remove(system_response_text.COOKING_PREPARATION_LIKE)


#
def slot_is_regional_or_country_origin(model, details, slot_real_value):
    update_count(model, details.recipe_origin)
    details.recipe_origin = slot_real_value
    append_to_all_categories(details, slot_real_value)
    if system_response_text.CUISINE_COUNTRY in model.available_conversation_questions:
        model.available_conversation_questions.remove(system_response_text.CUISINE_COUNTRY)
    if system_response_text.CUISINE_REGIONAL in model.available_conversation_questions:
        model.available_conversation_questions.remove(system_response_text.CUISINE_REGIONAL)


#
def slot_is_difficulty(model, details, slot_real_value):
    update_count(model, details.recipe_difficulty)
    details.recipe_difficulty = slot_real_value
    if system_response_text.COOKING_DIFFICULTY in model.available_conversation_questions:
        model.available_conversation_questions.remove(system_response_text.COOKING_DIFFICULTY)
    if system_response_text.COOKING_SKILLS in model.available_conversation_questions:
        model.available_conversation_questions.remove(system_response_text.COOKING_SKILLS)


# searches for the whole recipe title with the current user input data
def handle_recipe_name_slot(db, model, details, slot_real_value):
    # Regex für Milchreisrezept nicht möglich wegen Slot
    model.framework_state = conversation_states.TITLE_DISPLAY_STATE
    details.recipe_name = slot_real_value
    RecipeSearcher.search_only_title_recipe_details(db, details)


#
def slot_paraphrases_duration(model, details):
    update_count(model, details.recipe_duration)
    details.recipe_duration = 20  # 20 minutes is still fast


#
def handle_recipe_category_slot(model, details, slot_real_value):
    if slot_real_value not in details.recipe_category:
        update_count(model, details.recipe_category)
        details.recipe_category.append(slot_real_value)
        # details.all_categories.append(slot_real_value)
        append_to_all_categories(details, slot_real_value)


# todo nlu
def slot_is_ingredient(nlu, model, details, slot_real_value, update):
    nlu_ingredient = nlu.get_ingredients_intents(update.message.text)
    intent = nlu_ingredient[0]["intent"]["intentName"]
    slots = nlu_ingredient[0]["slots"]
    State_2_2.handle_ingredients(model, details, intent, slots)
    if slot_real_value not in details.ingredients_like:
        details.ingredients_like.append(slot_real_value)
        model.ingredients_count += 1
    model.framework_state = conversation_states.INGREDIENT_STOCK_STATE


#
def handle_recipe_other_slot(model, details, slot_real_value):
    # Claudia: mediterran (in recipe name because extra category for it does not exists in database)
    if slot_real_value == "mediterran":
        pass
    elif slot_real_value == "scharf":
        details.ingredients_like.append("schärfe")
    # Claudia: kuchen (should be recipe name cause category uses torte/kuchen)
    elif slot_real_value == "kuchen":
        pass
    elif slot_real_value == "saisonal":
        # Anne: never used?!
        season = Calculator.calculate_current_season()
        handle_recipe_category_slot(slot_real_value)
    else:
        update_count(model, details.is_sweet)
        # deftig (herzhaft, pikant)
        if slot_real_value == "deftig":
            details.is_sweet = 0
        elif slot_real_value == "süß":
            details.is_sweet = 1
