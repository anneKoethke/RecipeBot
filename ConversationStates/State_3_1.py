# -*- coding: utf-8 -*-

from config import conversation_states, system_response_text

# Anne:


def title_display_state(nlu, model, details, user_query):
    quest_answer = nlu.get_answer(user_query)
    if quest_answer:
        model.framework_state = conversation_states.INGREDIENT_LIST_STATE  # (state 3.2)
        system_message = system_response_text.INGREDIENT_LIST  # "Möchtest du die Zutatenliste sehen?"
    else:
        model.framework_state = conversation_states.INGREDIENT_STOCK_STATE  # (state 2.2)
        # Anne: needed for modify_recipe_search() ins RecipeSearcher
        details.modify_recipe_found = False
        model.replied_message = system_response_text.INGREDIENT_NEVER
        system_message = system_response_text.INGREDIENT_NEVER  # "Welche Zutaten würdest du niemals benutzen?"
    return system_message
