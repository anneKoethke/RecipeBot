import json
# from telefood_nlu_controller import NluController
# from telefood_nlu_handler import NLUHandler
from snips_nlu import SnipsNLUEngine
from config import nlu_intents, nlu_slots

"""
Telefood NLU handles user input to telegram:
    - nlu enging is initialized: init()
    - recognizese Search Intent: parse_user_query()
    - recognizes Ingredient Intent: get_ingredients_intents()
    - recognizes yes/no answers: get_answer()
    
    - Claudia: one fits all strategy: parse_user_query2() -> no yet used
"""


class TelefoodNLU:

    def __init__(self):
        self.nlu_engine = SnipsNLUEngine.from_path("./nlu_engine")

    # used for all the users answers in the conversation stock -> to be able to realize other outputs too
    def parse_user_query(self, user_input):  # gets the top most intent with the respected slots
        parsing = self.nlu_engine.parse(user_input, intents=[nlu_intents.SEARCH_RECIPE,
                                                             nlu_intents.MISC_QUESTION], top_n = 1)
        return parsing

    # returns the top_n ingredients intents (accept | decline) and slots
    def get_ingredients_intents(self, user_input):
        ingredients_intent = self.nlu_engine.parse(user_input, intents=[nlu_intents.ACCEPT_INGREDIENTS,
                                                                        nlu_intents.DECLINE_INGREDIENTS], top_n=1)
        print("\n### NLU:\t ingred_intent: "+str(ingredients_intent)+" ###\n")
        return ingredients_intent

    # returns True for a positive answer and false for a negative answer or not classified one
    def get_answer(self, user_input):
        ingredients_intent = self.nlu_engine.parse(user_input, intents=[nlu_intents.CONFIRM_QUESTION,
                                                                        nlu_intents.DECLINE_QUESTION], top_n=1)
        intent_name = ingredients_intent[0]["intent"]["intentName"]
        if intent_name is None:
            return False
        else:
            if intent_name == nlu_intents.CONFIRM_QUESTION:
                return True
            if intent_name == nlu_intents.DECLINE_QUESTION:
                return False

####################################################################################################################

    # Anne: so far NOT USED in main.py (?!) -> one query for all intents
    def parse_user_query2(self, user_input):  # gets the top most intent with the respected slots
        parsing = self.nlu_engine.parse(user_input, intents=[nlu_intents.SEARCH_RECIPE, nlu_intents.MISC_QUESTION,
                                                             nlu_intents.ACCEPT_INGREDIENTS,
                                                             nlu_intents.DECLINE_INGREDIENTS],
                                        top_n=1)  # top_n get the topmost intents with the highest probability
        # result is a list with [0] it is a dictionary # intents=[for intent_filters]
        return parsing
