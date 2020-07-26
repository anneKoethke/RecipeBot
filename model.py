# -*- coding: utf-8 -*-

"""
This class contains the framework_states(to know at which state/point the bot is in),
counter(for db search when condition are fulfilled),
available_questions(conversation and ingredients),
the last message for intent classification for the specific question
the number of recipe searches in that specific session (currently)
"""


class Model:
    # framework model
    def __init__(self):
        self.framework_state = "no_state"
        self.framework_states = []

        self.recipe_num_search = 0

        self.conversation_items_count = 0
        self.ingredients_count = 0

        self.replied_message = None

        self.available_conversation_questions = None  # todo better
        self.available_ingredients_questions = None

        self.conversation_questions = []
        self.ingredients_questions = []

    def reset_model(self):
        self.framework_state = "no_state"
        self.framework_states = []

        self.recipe_num_search += 1

        self.conversation_items_count = 0
        self.ingredients_count = 0

        self.replied_message = None

        self.available_conversation_questions = None
        self.available_ingredients_questions = None

        self.conversation_questions = []
        self.ingredients_questions = []
