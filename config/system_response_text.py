# -*- coding: utf-8 -*-
"""
This contains all of the text that is used for the bots reply to the user.
"""
########################################################################################################################
# Telegram commands
########################################################################################################################

# in telegram: /start
START = "Mit <b>„Hey Rezeptbot“</b> oder <b>„Hi Bot“</b> kannst du die Suche nach einem Rezept starten." \
        "\nFalls du weitere Fragen hast, kannst du mit <b>/help</b> ein kurzen Hilfe-Text aufrufen, der dir " \
        "einige Funktionen des Bots erklärt."
START_SEARCH = "Mit <b>„Hey rezeptbot“</b> oder <b>„Hey bot“</b> kann eine neue Suche gestartet werden."

# in telegram: /help
HELP = "Ich helfe dir, Rezepte zu finden:\nMit <b>„Hi bot“</b> kannst du jederzeit die Suche nach einem neuem Rezept " \
       "starten. Schreib dann einfach, was du suchst. Falls du noch nicht genau weißt, was du essen möchtest, stelle " \
       "ich dir ein paar Fragen, um deine Suche einzugrenzen.\nWenn du schon den Titel eines Rezeptes weißt, kannst " \
       "du auch einfach den Titel angeben.\nStarte jetzt mit <b>\"Hi Bot\"</b>."

# triggered by wake word (e.g. hi bot, hallo bot etc.)
GREETING = "<b>Hallo und willkommen zum Rezeptbot-Chat!</b>\nFalls du Fragen hast, was man hier tun kann, kannst du " \
           "mit <b>/help</b> eine kleine Einleitung aufrufen. Du kannst aber auch sofort nach einem Rezept suchen." \
           "\n<b>Also: <i>Was kann ich für dich tun?</i></b>"

########################################################################################################################
# recipeCategory
########################################################################################################################
PREFERENCES = "Auf was hast du Lust?"
COOKING_RECIPES = "Zu was für Rezepten greifst du normalerweise, wenn du etwas kochen möchtest?"

RECIPE_HOT = "Magst du etwas scharfes Essen?" # never used?
RECIPE_SWEET = "Magst du etwas süßes Essen?"
CUISINE_SOLID = "Wie stehst du zu deftigem Essen?"
CUISINE_LIGHT = "Wie stehst du zu leichtem Essen?" # never used?

# Season: Frühling, Sommer, Herbst, Winter
CUISINE_SEASONAL = "Wie stehst du zu saisonalem Essen?"

# recipeDifficulty
COOKING_SKILLS = "Wie würdest du deine Kochfähigkeiten einschätzen?"
COOKING_DIFFICULTY = "Wie ausgefallen darf das Rezept sein?" # never used?

# recipeServings
SERVINGS_NUM = "Für wie viele Personen willst du kochen?"

# recipePreparation
COOKING_PREPARATION_LIKE = "Gibt es spezielle Zubereitungsarten, die du magst?"

# recipeOrigin
CUISINE_REGIONAL = "Wie stehst du zu regionaler Küche (z.B. Hamburger oder Allgäuer Küche)?"
CUISINE_COUNTRY = "Welche Länderküche ist dein Favorit, bzw. aus welchem Land soll dein Rezept kommen?"

# recipeDuration and recipeDurationParaphrase
RECIPE_DURATION = "Wie viel Zeit hast du zum Kochen?"

# recipeDiet
ALLERGY = "Gibt es Allergiker?"
EATING_VEGAN = "Gibt es Veganer?"
EATING_VEGETARIAN = "Gibt es Vegetarier?"
EATING_HABITS = "Wie ernährst du dich?"

CONVERSATION_STOCK = [PREFERENCES, SERVINGS_NUM, COOKING_PREPARATION_LIKE,
                      CUISINE_SOLID,
                      CUISINE_SEASONAL,
                      RECIPE_SWEET,
                      COOKING_RECIPES, COOKING_SKILLS,
                      CUISINE_REGIONAL, CUISINE_COUNTRY, EATING_HABITS, RECIPE_DURATION, ALLERGY,
                      EATING_VEGAN, EATING_VEGETARIAN]

##################################################

# ingredient stock phrases
INGREDIENT_NEVER = "Welche Zutaten würdest du niemals benutzen?"
INGREDIENT_FAVORITE = "Was sind deine Lieblingszutaten?"  # für/in Kuchen
INGREDIENT_VEGETABLES = "Welches Gemüse magst du?"
INGREDIENT_CARBOHYDRATES_SOURCE = "Welche Kohlenhydratquelle bevorzugst du normalerweise? Beispielsweise Kartoffeln, " \
                                  "Nudeln oder Reis? Brot?"
INGREDIENT_SPECIAL = "Gibt es spezielle Zutaten, die du magst? Wie beispielsweise Szechuan Pfeffer oder Tamarinde?"
# Anne: changed 'Gibt es Präferenzen bei den Zutaten?' to:
INGREDIENT_PREFERENCE = "Welche Präferenzen gibt es bei den Zutaten?"

INGREDIENT_STOCK = [
    INGREDIENT_NEVER,
    INGREDIENT_FAVORITE, INGREDIENT_VEGETABLES, INGREDIENT_CARBOHYDRATES_SOURCE,
    INGREDIENT_SPECIAL, INGREDIENT_PREFERENCE]


##################################################
# "Möchtest du die Zutaten sehen?"
INGREDIENT_LIST = "Möchtest du die Zutatenliste sehen?"
RECIPE_INFORMATION = "Möchtest du mehr Informationen zu diesem Rezept?"
RECIPE_DISPLAY = "Möchtest du das Rezept sehen?"
##################################################
# error stock phrases
SPELLING_ERROR = "Ich glaube, da war ein Rechtschreibfehler. Was meintest du?"
FORMULATION_ERROR = "Es tut mir leid, das habe ich nicht verstanden. Kannst du es neu formulieren?"
INGREDIENT_ERROR = "Was für Zutaten hast du gemeint?"

# extra error phrase for telefood commands
COMMAND_ERROR = "Es tut mir leid, das Kommando existiert nicht."
RECIPE_ERROR = "Auf Basis deiner Angaben konnte ich leider kein Rezept finden. Bitte starte mit „Hey Bot“ eine neue Rezeptsuche."

##################################################
# rating of ingredients
INGREDIENT_GOOD = "Wie gefallen dir die Zutaten?"
INGREDIENT_LIKE = "Magst du die Zutaten?"
INGREDIENT_RATING = [INGREDIENT_GOOD, INGREDIENT_LIKE]
##################################################
