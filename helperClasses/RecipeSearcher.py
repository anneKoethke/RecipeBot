# -*- coding: utf-8 -*-

import telegram
from config import conversation_states, recipe_keys, system_response_text
from System_B import User_Feedback_System_B
from helperClasses import SystemResponseGenerator

# Anne:


#
def search_only_title_recipe_details(db, details):
    recipe_name = details.recipe_name
    result_data = db.get_recipe_by_title_only(recipe_name)
    details.current_recipe = result_data


# Anne: called by State 2.2 and if 2 or more ingredients where identified
#       (independent from conversation questions count)
def search_for_recipe(context, update, system_b, db, model, details):
    # details.current_recipe = result_data
    search_recipe_details(context, update, system_b, db, details)
    # database search returned NULL
    print(details.current_recipe)
    if details.current_recipe is None:
        details.modify_recipe_found = False
        # returns copy of current_recipe (ranking non-relevant -> to more relevant)
        modified_recipe_details = details.get_modified_recipe_details()
        # Anne: removed sys_msg_tmp, because not needed!
        if system_b:
            feedback_message = "Mit den aktuellen Suchkriterien konnte kein Rezept gefunden werden. Folgende Kriterien werden entfernt: "
            context.bot.send_message(chat_id=update.effective_chat.id, text=feedback_message,
                                     parse_mode=telegram.ParseMode.HTML)
        system_message = modify_recipe_search(context, update, system_b, db, model, details, modified_recipe_details)
        if system_message is None:
            model.framework_state = conversation_states.TITLE_DISPLAY_STATE
            system_message = SystemResponseGenerator.get_recipe_recommendation(details.current_recipe[1])
    else:
        model.framework_state = conversation_states.TITLE_DISPLAY_STATE
        system_message = SystemResponseGenerator.get_recipe_recommendation(details.current_recipe[1])
    return system_message


# gets the recipe details (durations, servings, difficulty, title, categories, ingred_like und ingred_dislike,
# class_sweet) from recipe object, searches in db, write db result to recipe object
def search_recipe_details(context, update, system_b, db,  details):
    recipe_data = details.get_relevant_details()
    if system_b:
        feedback_message = User_Feedback_System_B.get_all_search_criteria(recipe_data)
        context.bot.send_message(chat_id=update.effective_chat.id, text=feedback_message,
                                 parse_mode=telegram.ParseMode.HTML)
    result_data = db.get_recipe(recipe_data)
    details.current_recipe = result_data


# Anne: removed system message from parenthesis; called in
def modify_recipe_search(context, update, system_b, db, model, details, modified_recipe_details):
    # print("mod_rec_search\nfound, details, el")
    # print(details.modify_recipe_found)
    # print(modified_recipe_details)
    # if details.modify_recipe_found is False:
    # Anne: removed, because it's always False initially and controlled in the later ifs
    for el in modified_recipe_details:
        # if details.modify_recipe_found is False: # Anne: removed (see above two lines above for reasons)
        for key in el:
            print("el in mod_rec_search")
            print(el)
            if not details.modify_recipe_found:
                if system_b:
                    feedback_message = User_Feedback_System_B.item_removed_from_modified_recipe(el)
                    print(feedback_message)
                    context.bot.send_message(chat_id=update.effective_chat.id, text=feedback_message,
                                             parse_mode=telegram.ParseMode.HTML)
                if key in [recipe_keys.RECIPE_PREPARATION, recipe_keys.RECIPE_ORIGIN, "servings", "duration",
                           "difficulty", "ingredients_like", "ingredients_dislike", recipe_keys.RECIPE_CATEGORY,
                           recipe_keys.RECIPE_DIET]:
                    # todo: remove current element from a list (currently whole list is droped)
                    if key.get("ingredients_like"):
                        list = key.get("ingredients_like")
                        print("\n LIST")
                        print(list)

                    modified_recipe_details.remove(el)
                    # search DB for result
                    result_data = db.get_recipe(modified_recipe_details)
                    # result exists -> write in curr_rec
                    # removed: is not none
                    print("result_data")
                    print(result_data)
                    if result_data:
                        print("in if result_data")
                        details.current_recipe = result_data
                        model.framework_state = conversation_states.TITLE_DISPLAY_STATE
                        details.modify_recipe_found = True
                        modified_rec_title = SystemResponseGenerator.get_recipe_recommendation(details.current_recipe[1])
                        return modified_rec_title
                    else:
                        print("in else")
                        details.modify_recipe_found = False
                        modify_recipe_search(context, update, system_b, db, model, details, modified_recipe_details)
