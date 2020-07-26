# -*- coding: utf-8 -*-

from config import conversation_states, system_response_text
from helperClasses import SystemResponseGenerator

# Anne: State 3.2 - INGREDIENT LIST STATE - displays the ingredients list to user in telegram


# Anne: returns the formatted list of ingredients (State 3.2)
def ingredient_list_state(nlu, model, details, user_query):
    quest_answer = nlu.get_answer(user_query)
    if quest_answer:
        model.framework_state = conversation_states.INGREDIENT_LIST_DISPLAY_STATE  # (state 3.3)
        ingredients = format_ingredients_string(details.current_recipe[10])
        system_message = "<b>Zutaten</b>\n\n" + str(ingredients) + "\n\n<i>" \
                         + system_response_text.RECIPE_DISPLAY + "</i>"
    else:
        model.framework_state = conversation_states.RECIPE_DISPLAY_STATE
        system_message = SystemResponseGenerator.define_recipe_text(details)
    return system_message


# Anne: all ingredients are stored as string in DB 'food_db' -> Table 'kochbar_analysis_recipe'
#       -> Column 'ingredients_string'
# thus, remove ':' as separator between amount and type of ingredient
def format_ingredients_string(ingredients):
    ingredient_string = ""
    for line in ingredients:
        ingredient_string += line.replace(":", " ")
    return ingredient_string
