# -*- coding: utf-8 -*-

from config import conversation_states, system_response_text
from helperClasses import SystemResponseGenerator
from System_B import User_Feedback_System_B

# Anne: ...


def ingredient_list_display_state(system_b, nlu, model, details, user_query):
    quest_answer = nlu.get_answer(user_query)
    if quest_answer:
        # ANNE: show recipe and prepare new search
        model.framework_state = conversation_states.RECIPE_DISPLAY_STATE
        system_message = SystemResponseGenerator.define_recipe_text(details)
    else:
        # reset all ingredients
        reset_all_ingredients(model, details)
        if system_b:
            system_message = User_Feedback_System_B.get_all_ingredients_removed_message(details)
        else:
            system_message = system_response_text.INGREDIENT_PREFERENCE  # "Welche Präferenzen gibt es bei den Zutaten?"
    return system_message


# Anne: is called by state 3.3 (user didn't want that recipe after either title display (3.1)
#       or ingredient display (3.2))
def reset_all_ingredients(model, details):
    # get all ingredient questions
    model.framework_state = conversation_states.INGREDIENT_STOCK_STATE
    # reset all concerning ingredients in recipe_details.py
    details.ingredients = []
    details.ingredients_like = []
    details.ingredients_dislike = []
    # no ingredients -> counter = 0
    model.ingredients_count = 0
    # no current recipe
    details.current_recipe = None
