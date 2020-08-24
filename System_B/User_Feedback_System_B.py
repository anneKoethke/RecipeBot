# -*- coding: utf-8 -*-

from config import system_response_text


# Anne: for System B, i.e. Feedback to User


# returns either a string of liked an disliked ingredients or one of them
# (used in State 2.2: handle_2_2_ingredient_stock_state() )
def concatenate_ingredient_lists_to_string(like_list, dislike_list):
    feedback_message = ""
    if like_list:
        like_feedback = return_ingredients_string(like_list, "like")
        feedback_message += like_feedback
    if dislike_list:
        dislike_feedback = return_ingredients_string(dislike_list, "dislike")
        feedback_message += dislike_feedback
    return feedback_message


# Anne: returns a nice and readable String of the like or dislike list to concatenate_...()
def return_ingredients_string(curr_list, like_value):
    list_string = ""
    if curr_list:
        if len(curr_list) > 1:
            for ingredient in curr_list:
                ingredient = ingredient.capitalize()
                list_string = list_string + ingredient + ", "
            list_string = list_string.rstrip(", ")
            if like_value == "like":
                list_string += " werden bei der Suche als Zutaten berücksichtigt."
            else:
                list_string += " werden bei der Suche als Zutaten vermieden."
        else:
            list_string = curr_list[0].capitalize()
            if like_value == "like":
                list_string += " wird als Zutat der Suche hinzugefügt."
            else:
                list_string += " wird als Zutat bei der Suche vermieden."
        list_string += "\n"
    return list_string


# called in main
def get_all_search_criteria(recipe_data):
    feedback_message = "<b>Folgende Suchkriterien werden verwendet:</b>\n"
    for c in recipe_data:
        if c.get("duration"):
            feedback_message += str(c.get("duration")) + " Minuten. "
        if c.get("servings"):
            feedback_message += str(c.get("servings")) + " Portionen. "
        if c.get("difficulty"):
            feedback_message += "Schwierigkeit: " + str(c.get("difficulty")) + ". "
        if c.get("categories"):
            curr_list = c.get("categories")
            cap_list = [i.capitalize() for i in curr_list]
            feedback_message += "\nKategorie(n): " + ", ".join(cap_list) + ".\n"
        if c.get("class_sweet"):
            if c.get("class_sweet") == 0:
                feedback_message += "Nicht süss. "
            else:
                feedback_message += "Süss. "
        if c.get("ingredients_like"):
            curr_list = c.get("ingredients_like")
            cap_list = [i.capitalize() for i in curr_list]
            feedback_message += "Bevorzuge: " + ", ".join(cap_list) + ".\n"
        if c.get("ingredients_dislike"):
            curr_list = c.get("ingredients_dislike")
            cap_list = [i.capitalize() for i in curr_list]
            feedback_message += "Vermeide: " + ", ".join(cap_list) + ".\n"
    return feedback_message


# called in State 3.3 after 3.2 () was declined
def get_all_ingredients_removed_message(details):
    like_str = ", ".join(details.ingredients_like)
    dislike_str = ", ".join(details.ingredients_dislike)
    feedback_message = None
    if like_str and dislike_str:
        feedback_message = "Bisherige Zutaten (gewollt: " + like_str + ", nicht gewollt: " + dislike_str + \
                           ") wurden als Suchkriterium aus der Suche entfernt.\n<i>" + \
                           system_response_text.INGREDIENT_PREFERENCE + "</i>"
    elif like_str:
        feedback_message = "Bisherige Zutaten (gewollt: " + like_str + \
                           ") wurden als Suchkriterium aus der Suche entfernt.\n<i>" + \
                           system_response_text.INGREDIENT_PREFERENCE + "</i>"
    elif dislike_str:
        feedback_message = "Bisherige Zutaten (nicht gewollt: " + dislike_str + \
                           ") wurden als Suchkriterium aus der Suche entfernt.\n<i>" + \
                           system_response_text.INGREDIENT_PREFERENCE + "</i>"
    else:
        feedback_message = "Bisherige Zutaten wurden als Suchkriterium aus der Suche entfernt.\n<i>" \
                           + system_response_text.INGREDIENT_PREFERENCE + "</i>"
    return feedback_message


# Anne: called in RecipeSearcher
def item_removed_from_modified_recipe(el):
    feedback_message = ""
    if el.get("duration"):
        feedback_message = str(el.get("duration")) + " Minuten"
    if el.get("servings"):
        feedback_message = str(el.get("servings")) + " Portionen"
    if el.get("categories"):
        feedback_message = get_comma_separated_string_from_list(el.get("categories"))
    if el.get("recipe_diet"):
        feedback_message = get_comma_separated_string_from_list(el.get("recipe_diet"))
    if el.get("class_sweet"):
        if el.get("class_sweet") == 1:
            feedback_message = "süß"
        else:
            feedback_message = ""
    return feedback_message


def get_comma_separated_string_from_list(curr_list):
    cap_list = [i.capitalize() for i in curr_list]
    return ", ".join(cap_list) + ". "
