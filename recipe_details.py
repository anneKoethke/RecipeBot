# -*- coding: utf-8 -*-


# only for testing tmp todo save in database and do queries

# Model for RecipeDetails
""" saves all of the relevant data # to later search for a recipe in the database """


class RecipeDetails:

    # ANNE: Recipe object has 20 attributes
    def __init__(self):
        self.recipe_other = None # wat?!
        self.photo_url = None # not important in this bot
        # Recipe Details as gathered from user input (telegram conversation)
        self.is_sweet = None
        self.recipe_duration = None
        self.recipe_servings = None
        self.recipe_difficulty = None
        self.recipe_name = None  # = []
        self.recipe_category = []
        self.recipe_diet = []
        self.recipe_preparation = None  # = []
        self.recipe_origin = None  # = []
        self.all_categories = []
        self.recipe_details = []  # Claudia: dictionary?
        # if DB can't find a recipe with the above, the items are reduced untill it finds a modified recipe
        self.modified_recipe_details = []
        self.modify_recipe_found = False
        self.modified_recipe_title = ""
        # ingredients
        self.ingredients = []
        self.ingredients_like = []
        self.ingredients_dislike = []
        # what?
        self.current_recipe = None

    # ANNE: changed name of method ('relevant' for DB search)
    def get_relevant_details(self):
        relevant_details = []
        if self.recipe_duration is not None:
            relevant_details.append({"duration": int(self.recipe_duration)})
        if self.recipe_servings is not None:
            relevant_details.append({"servings": int(self.recipe_servings)})
        if self.recipe_difficulty is not None:
            relevant_details.append({"difficulty": self.recipe_difficulty})
        if self.recipe_name is not None:
            relevant_details.append({"title": self.recipe_name})
        if len(self.all_categories) > 0:
            relevant_details.append({"categories": self.all_categories})
        if len(self.ingredients_like) > 0:
            relevant_details.append({"ingredients_like": self.ingredients_like})
        if len(self.ingredients_dislike) > 0:
            relevant_details.append({"ingredients_dislike": self.ingredients_dislike})
        if self.is_sweet is not None:
            relevant_details.append({"class_sweet": self.is_sweet})
        return relevant_details

    # Claudia: ranking non-relevant -> to more relevant
    # Anne: not important for SQL, but defines order in which the items are removed from list while searching th db,
    # also lists categories in a more defined way (preparation, origin, diet instead of only all?categories,
    # compare with above)
    def get_modified_recipe_details(self):
        relevant_details = []
        if self.recipe_servings is not None:
            relevant_details.append({"servings": int(self.recipe_servings)})
        if self.recipe_duration is not None:
            relevant_details.append({"duration": int(self.recipe_duration)})
        if self.recipe_difficulty is not None:
            relevant_details.append({"difficulty": self.recipe_difficulty})
        if self.recipe_preparation is not None:
            relevant_details.append({"recipe_preparation": self.recipe_preparation})
        if self.recipe_origin is not None:
            relevant_details.append({"recipe_origin": self.recipe_origin})
        if len(self.recipe_category) > 0:
            relevant_details.append({"recipe_category": self.recipe_category})
        if len(self.recipe_diet) > 0:
            relevant_details.append({"recipe_diet": self.recipe_diet})
        if len(self.ingredients_like) > 0:
            relevant_details.append({"ingredients_like": self.ingredients_like})
        if len(self.ingredients_dislike) > 0:
            relevant_details.append({"ingredients_dislike": self.ingredients_dislike})
        if self.is_sweet is not None:
            relevant_details.append({"class_sweet": self.is_sweet})
        return relevant_details

    def reset_details(self):
        self.recipe_other = None
        self.photo_url = None
        self.is_sweet = None
        self.recipe_duration = None
        self.recipe_servings = None
        self.recipe_difficulty = None
        self.recipe_name = None  # = []
        self.recipe_category = []
        self.recipe_diet = []  # = []
        self.recipe_preparation = None  # = []
        self.recipe_origin = None  # = []
        self.all_categories = []
        self.recipe_details = []  # {"recipe_diet": None, }
        self.modified_recipe_details = []  # new
        self.modify_recipe_found = False
        self.modified_recipe_title = ""
        # ingredients
        self.ingredients = []
        self.ingredients_like = []
        self.ingredients_dislike = []
        self.current_recipe = None

    ####################################################################################################################
    # GETTER (von Anne)
    ####################################################################################################################

    def get_name(self):
        return self.recipe_name

    def get_sweetness(self):
        return self.is_sweet

    def get_duration(self):
        return self.recipe_duration

    def get_servings(self):
        return self.recipe_servings

    def get_difficulty(self):
        return self.recipe_difficulty

    def get_all_categories(self):
        return self.all_categories

    def get_category(self):
        return self.recipe_category

    def get_diet(self):
        return self.recipe_diet

    def get_preparation(self):
        return self.recipe_preparation

    def get_origin(self):
        return self.recipe_origin

    def get_details(self):
        return self.recipe_details

    def get_modified_details(self):
        return self.modified_recipe_details

    def get_modified_recipe_found(self):
        return self.modify_recipe_found

    def get_modified_title(self):
        return self.modified_recipe_title

    def get_all_ingredients(self):
        return self.ingredients

    def get_liked_ingredients(self):
        return self.ingredients_like

    def get_disliked_ingredients(self):
        return self.ingredients_dislike

    def get_current_recipe(self):
        return self.current_recipe
