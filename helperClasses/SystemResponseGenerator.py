# -*- coding: utf-8 -*-

from config import system_response_text

# Anne: for the dynamic system responses to user (static answers in config.system_response_text.py)


# extra suggestion phrases (ToDo used in main.py)
def get_recipe_recommendation(result):
    return "Wie klingt <b>" + result + "</b> für dich?"


# Anne: detailed Recipe visualization for user (chat)
def define_recipe_text(details):  # called in state 3.2 (if False to show ingred_list) and 3.3 (if True to show recipe)
    recipe = details.current_recipe
    title, description, servings, ingredients, preparartion, difficulty, prep_time = get_recipe_text_items(recipe)
    # Anne: HTML parsing (only <b>old, <i>talic and <a>nchor)
    # -> important for future pictures: telegram interprets links with meta-picture by itself
    system_message = "<b>Rezept: '" + title + "'</b>\n\n<b>Beschreibung</b>\n<i>" + description + "</i>\n\n<b>Portionen: <i>" + servings + "</i></b>\n\n<b>Zutaten</b>\n" + ingredients + "\n\n<b>Zubereitung</b>\n" + preparartion + "\n\n<b>Schwierigkeit: <i>" + difficulty + "</i>\nZeit:</b> " + prep_time
    return system_message


# Anne: returns the recipe items (outsourced for readability)
def get_recipe_text_items(recipe):
    title = str(recipe[1])
    description = str(recipe[2])
    if description == "None":
        description = "keine Angabe"
    servings = str(recipe[9])
    ingredients = str(recipe[10]).replace(":", " ")
    preparation = str(recipe[11])
    difficulty = str(recipe[12])
    prep_time = prep_time_handler(str(recipe[13]))
    return title, description, servings, ingredients, preparation, difficulty, prep_time


# Anne: handles German grammar (Pl./Sg.) and None for recipe time value (as string)
def prep_time_handler(time):
    if time == "None":
        time = "keine Angabe"
    elif time == "1":
        time += " Minute"
    else:
        time += " Minuten"
    return time

########################################################################################################################
# used?


# extra phrases (ANNE: not used?)
def get_part_times(result):
    return "Arbeitszeit: ca. " + result.working_time + " Min. / Koch-/Backzeit: ca. " + result.cooking_time + " Min."


# user input Dauer (ANNE: not used?)
def get_time(result):
    return result + " Minuten"

##################################################
# suggestion stock phrases


def get_recommended_recipe(result, ingredient):
    return "Du hast erwähnt, dass du " + ingredient + " magst, wie klingt <b>" + result + "</b> für dich?"


def get_ingredient_recipe_recommendation(result):
    return "Mithilfe der Zutaten, die du mir genannt hast, habe ich folgendes Rezept gefunden. „" \
           + result + "“ " + system_response_text.RECIPE_INFORMATION
