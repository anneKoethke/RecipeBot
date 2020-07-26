# -*- coding: utf-8 -*-

import random
import telegram
from config import system_response_text, nlu_intents, nlu_slots
from helperClasses import RecipeSearcher
from System_B import User_Feedback_System_B

# Anne:


#
def ingredient_stock_state(context, update, system_b, db, nlu, model, details, user_query):
    # get intent and slots from user message
    ingredient_data = nlu.get_ingredients_intents(user_query)
    intent = ingredient_data[0]["intent"]["intentName"]
    slots = ingredient_data[0]["slots"]
    # Anne: None intent == don't increase ingredient count
    #       -> take a new question (removed from handle_ingredients and handle_never_ingredients)
    print("intent in 2.2")
    print(intent)
    if intent is None:
        system_message = select_ingredient_question(model)
    else:
        if model.replied_message == system_response_text.INGREDIENT_NEVER:
            # "Welche Zutaten würdet du niemals benutzen?"
            handle_never_ingredients(model, details, intent, slots)
        else:
            # Anne: all ingredient questions except INGREDIENT_NEVER (see above)
            handle_ingredients(model, details, intent, slots)
        if system_b:
            feedback_message = \
                User_Feedback_System_B.concatenate_ingredient_lists_to_string(details.ingredients_like,
                                                                              details.ingredients_dislike)
            context.bot.send_message(chat_id=update.effective_chat.id, text=feedback_message,
                                     parse_mode=telegram.ParseMode.HTML)
        # gather whether enough information were extracted from user
        system_message = select_ingredient_question_or_search_for_recipe(context, update, system_b, db, model, details)
    return system_message


#
def handle_never_ingredients(model, details, intent, slots):
    for slot in slots:
        if intent == nlu_intents.ACCEPT_INGREDIENTS or intent == nlu_intents.DECLINE_INGREDIENTS:
            slot_value = slot["value"]["value"]
            # current slot is not in the dislike list and not 'kein' -> append to dislike list, count up
            if (slot_value not in details.ingredients_dislike) and slot_value != nlu_slots.NO_VALUE:
                append_to_ingredient_list_and_update_count(model, details, "dislike", slot_value)
            # Anne: removed sys_msg from for loop for better performance,
            # because could also be handled at calling def handle_user_query()
        # Anne: removed else (because no other intent reaches here)
    # Anne: removed if slots == [], because this is handled in telefood_nlu.py -> get_ingredients_intents()


#
def handle_ingredients(model, details, intent, slots):
    # (if intent is None) has had no influence on program flow, therefore removed
    test_negative = False
    for slot in slots:
        curr_slot_value = slot["value"]["value"]
        if (intent == nlu_intents.ACCEPT_INGREDIENTS) and (
                curr_slot_value not in details.ingredients_like) and (
                curr_slot_value not in details.ingredients_dislike):
            append_to_ingredient_list_and_update_count(model, details, "like", curr_slot_value)
        if intent == nlu_intents.DECLINE_INGREDIENTS:
            # ausgelöst durch Kohlenhydrate-Frage und Verneinung bei Lieblingzutaten
            # NO_VALUE = "kein
            if curr_slot_value == nlu_slots.NO_VALUE:
                test_negative = True
            # last slot was 'kein' (test_negative), current slot is not 'kein' (curr_slot_value != NO_VALUE_SLOT),
            # and current slot is neither in like nor dislike list, so add current slot to dislike list
            if test_negative and curr_slot_value != nlu_slots.NO_VALUE and (
                    curr_slot_value not in details.ingredients_like) and (
                    curr_slot_value not in details.ingredients_dislike):
                append_to_ingredient_list_and_update_count(model, details, "dislike", curr_slot_value)
            # last slot was NOT 'kein' and isn't in like or dislike list
            elif (not test_negative) and (
                    curr_slot_value not in details.ingredients_like) and (
                    curr_slot_value not in details.ingredients_dislike):
                append_to_ingredient_list_and_update_count(model, details, "like", curr_slot_value)


# handler for appending ingredients to like or dislike list in details + increase ingredient counter in model
def append_to_ingredient_list_and_update_count(model, details, list_type, slot):
    if list_type == "like":
        details.ingredients_like.append(slot)
    else:
        # list_type == "dislike"
        details.ingredients_dislike.append(slot)
    model.ingredients_count += 1


# Anne: handles if enough info for search found, else new question needed, called by state 2.2
def select_ingredient_question_or_search_for_recipe(context, update, system_b, db, model, details):
    system_message = ""
    if model.ingredients_count <= 1:
        system_message = select_ingredient_question(model)
    elif model.ingredients_count > 1:
        system_message = RecipeSearcher.search_for_recipe(context, update, system_b, db, model, details)
    return system_message


# selects the available questions for ingredients
def select_ingredient_question(model):
    # if all questions from INGREDIENT_STOCK were asked -> reset questions and restart
    if not model.available_ingredients_questions:
        model.available_ingredients_questions = system_response_text.INGREDIENT_STOCK.copy()
        # ANNE geändert : return select_ingredient_question()
        select_ingredient_question(model)
    # take a random question of the list
    question = random.choice(model.available_ingredients_questions)
    # remove it from the list
    model.available_ingredients_questions.remove(question)
    model.replied_message = question
    return question
