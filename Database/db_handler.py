# -*- coding: utf-8 -*-
import mysql.connector
import random


# Anne: remodeled db_handler, because of numerous database error concerning category table in DB
#       and how the sql statement was created


class DatabaseHandler:
    # class variables: DB Tables
    RECIPE_TABLE = "kochbar_analysis_recipe"
    INGREDIENT_TABLE = "kochbar_analysis_ingredient_de"
    REC_INGRED_TABEL = "kochbar_analysis_recipe_ingredient_de"
    CATEGORY_TABLE = "kochbar_recipes_category"
    # class variables: fetch limits # MySQL Workbench LIMIT is always <= 1000 (default value for mySQL connector)
    # for performance reasons
    LIMIT_1000 = " LIMIT 0,1000;"
    LIMIT_100 = " LIMIT 0,100;"
    LIMIT_50 = " LIMIT 0,50;"
    LIMIT_30 = " LIMIT 0,30;"
    LIMIT_10 = " LIMIT 0,10;"
    LIMIT_3 = " LIMIT 0,3;"

    def __init__(self, host, name, user, password):
        self.host = host
        self.name = name
        self.user = user
        self.password = password
        self.db = mysql.connector.connect(host=self.host, database=self.name, user=self.user, password=self.password)
        self.cursor = self.db.cursor(buffered=True)

    ####################################################################################################################
    # TITLE ONLY SEARCH

    # Anne: changed name to 'get_recipe_by_title_only' # old: get_only_title_recipe
    def get_recipe_by_title_only(self, recipe_name):
        sql = "SELECT * FROM " + self.RECIPE_TABLE + " WHERE title='" + recipe_name + "'"
        # self.cursor.execute(sql) # Claudia
        # result = self.cursor.fetchone() # Claudia
        # Anne: sourced out to
        result = self.execute_sql_fetch_one_for_recipe(sql)
        return result

    ####################################################################################################################
    # RECIPE SEARCH

    # Anne: main search structure; rebuilt
    # get n recipe ids by el[key] -> compare the lists -> found one for all? return rec : mod rec
    def get_recipe(self, data):
        print("\n GET_RECIPE: data")
        print(data)
        # data-example = [
        #  {'servings': 3}, {'categories': ['Suppen/Eintöpfe']}, {'ingredients_like': ['tomaten', 'basilikum']}
        #  ]
        result_recipe = None
        rec_table_list, cat_table_list, like_ingred_table_list, dislike_ingred_table_list = None, None, None, None
        rec_constraints_list = []
        cat_constraints_list = []
        ingred_like_list = []
        ingred_dislike_list = []
        for el in data:
            # search in RECIPE TABLE: servings, duration, difficulty, sweet
            #                         -> get 1000 rec_ids (here: hrefs)
            if el.get("duration"):
                rec_constraints_string = "duration <= " + str(el.get("duration"))
                rec_constraints_list.append(rec_constraints_string)
            if el.get("servings"):
                rec_constraints_string = "servings = " + str(el.get("servings"))
                rec_constraints_list.append(rec_constraints_string)
            if el.get("difficulty"):
                rec_constraints_string = "difficulty = '" + el.get("difficulty") + "'"
                rec_constraints_list.append(rec_constraints_string)
            if el.get("is_sweet"):
                rec_constraints_string = "class_sweet = " + str(el.get("is_sweet"))
                rec_constraints_list.append(rec_constraints_string)
            # search in CATEGORY TABLE: categories, all_categories, recipe_category etc.
            #                           -> get 1000 rec_ids (here: hrefs)
            if el.get("categories"):
                for cat in el.get("categories"):
                    cat_constraints_list.append(cat)
            if el.get("recipe_category"):
                for cat in el.get("recipe_category"):
                    cat_constraints_list.append(cat)
            if el.get("recipe_preparation"):
                for cat in el.get("recipe_preparation"):
                    cat_constraints_list.append(cat)
            if el.get("recipe_origin"):
                for cat in el.get("recipe_origin"):
                    cat_constraints_list.append(cat)
            if el.get("recipe_diet"):
                for cat in el.get("recipe_diet"):
                    cat_constraints_list.append(cat)
            if el.get("all_categories"):
                for cat in el.get("all_categories"):
                    cat_constraints_list.append(cat)
            # search in INGREDIENT TABLE and RECIPExINGREDIENT TABLE: like, dislike -> get 1000 rec_ids (here: hrefs)
            if el.get("ingredients_like"):
                like_ingred_table_list = self.select_from_ingredient_table(liked=True, list=el.get("ingredients_like"))
            if el.get("ingredients_dislike"):
                dislike_ingred_table_list = self.select_from_ingredient_table(liked=False,
                                                                              list=el.get("ingredients_dislike"))
        # cat_constraints_list : ['Vegan', 'Abendessen']
        if cat_constraints_list:
            cat_table_list = self.handle_category_table_search(cat_constraints_list)
        # rec_constraints_list : [{'duration': 240}, {'servings': 3}, {'difficulty': 'leicht'}]
        if rec_constraints_list:
            rec_table_list = self.handle_recipe_table_search(rec_constraints_list)

        # compare the lists and return those, which fulfill all user restraints
        result = self.compare_lists(rec_table_list, cat_table_list, like_ingred_table_list, dislike_ingred_table_list)

        print("\nDB RESULT: ")  # 1000 or less
        print(len(result))

        result_recipe = self.get_result_recipe(result, result_recipe, rec_table_list, cat_table_list,
                                        like_ingred_table_list, dislike_ingred_table_list)

        # else: couldn't find a SINGLE recipe for user -> modify_recipe_search
        return result_recipe

    def get_result_recipe(self, result, result_recipe=None, rec_table_list=None, cat_table_list=None,
                          like_ingred_table_list=None, dislike_ingred_table_list=None):
        # handle differnet outcomes: (1) one result (2) many results (3) None result
        if result and result != []:
            random.shuffle(result)
            print(result[0])
            if len(result) == 1:
                print("\nIN IF: result 1")
                result_recipe = self.get_recipe_by_rec_id(result[0])
            elif len(result) > 1 and result_recipe is None:
                print("\nIN ELIF: result many")
                for item in result:
                    result_recipe = self.get_recipe_by_rec_id(item)
                    if result_recipe:
                        break
        else:
            print("\nIN ELSE: result None")
            if cat_table_list:
                print("cat")
                result_recipe = self.get_result_recipe(cat_table_list)
            elif like_ingred_table_list:
                print("like")
                result_recipe = self.get_result_recipe(like_ingred_table_list)
            elif rec_table_list:
                result_recipe = self.get_result_recipe(rec_table_list)
                # not with dislike
        return result_recipe

    # Anne: called by get_recipe to get recipe values for current recipe
    def get_recipe_by_rec_id(self, curr_id):
        # SELECT * FROM kochbar_analysis_recipe WHERE recipe_href = '/rezept/319156/Geschmortes-mediterranes-Ofengemuese.html';
        sql = "SELECT * FROM " + self.RECIPE_TABLE + " WHERE recipe_href = '" + str(curr_id) + "';"
        result = self.execute_sql_fetch_one_for_recipe(sql)
        return result

    ####################################################################################################################
    # COMPARING THE RESULT LISTS of the different tables

    # compare table_list (rec, cat, ingred): (called by get_recipe)
    # first: compare two lists:
    # -> if they don't share items, no need to compare third list
    # -> else: compare intermediary list to third list
    def compare_lists(self, rec_list=None, cat_list=None, like_list=None, dislike_list=None):
        intermed_list_1, intermed_list_2 = None, None
        result_list = []
        # 1st if: there is either rec_list or cat_list or both
        if rec_list and cat_list:
            print("\nrec_list, length: " + str(len(rec_list)))
            print("cat_list, length:" + str(len(cat_list)))
            intermed_list_1 = self.compare_two_lists(rec_list, cat_list)
            print(len(intermed_list_1))
        elif rec_list:
            print("\nrec_list, length: " + str(len(rec_list)))
            intermed_list_1 = rec_list.copy()
        elif cat_list:
            print("\ncat_list, length:" + str(len(cat_list)))
            intermed_list_1 = cat_list.copy()
        # 2nd if: there is either like_list or dislike_list or both
        if like_list and dislike_list:
            print("\nlike_list, length:" + str(len(like_list)))
            print("dislike_list, length:" + str(len(dislike_list)))
            intermed_list_2 = self.compare_two_lists(like_list, dislike_list)
            print(len(intermed_list_2))
        elif like_list:
            print("\nlike_list, length:" + str(len(like_list)))
            intermed_list_2 = like_list.copy()
        elif dislike_list:
            print("\ndislike_list, length:" + str(len(dislike_list)))
            intermed_list_2 = dislike_list.copy()
        # 3rd if: (merge of rec and cat) and (merge of like and dislike)
        if intermed_list_1 and intermed_list_2:
            result_list = self.compare_two_lists(intermed_list_1, intermed_list_2)
        # no like or dislike: merge of rec and cat (or only one of those)
        elif intermed_list_1:
            result_list = intermed_list_1
        # no cat or rec: merge of like and dislike (or only one of those)
        elif intermed_list_2:
            result_list = intermed_list_2

        # disklike_list and rec_list are hurting result
        print("\ncompare_lists - result_list final length: ")
        print(len(result_list))
        return result_list

    # table_lists should have same length (i.e. LIMIT 0,1000), but for future changes..
    def compare_two_lists(self, list_1, list_2):
        result_list = []
        # for sort() the lists must be copied (else reference error - not shown)
        l1, l2 = list_1.copy(), list_2.copy()
        # sort lists alphabetically
        l1.sort()
        l2.sort()
        counter_1 = 0
        counter_2 = 0
        # derived from: Elsweiler, lecture2_indexing.pdf, Introduction to IR, page 33,
        #               'Intersecting two postings lists' (pseudo code)
        while counter_1 < len(l1) and counter_2 < len(l2):
            if l1[counter_1] == l2[counter_2]:
                result_list.append(l1[counter_1])
                counter_1 += 1
                counter_2 += 1
            # works, because signs ('letters') of each string are compared stepwise and per 'Unicode' value
            # (rather ASCII?)
            # [see: https://www.thecoderpedia.com/blog/python-string-comparison/ -> More String Comparison Operators]
            elif l1[counter_1] > l2[counter_2]:
                counter_2 += 1
            elif l1[counter_1] < l2[counter_2]:
                counter_1 += 1

        print("\nCOMPARE TWO LISTS")
        print(result_list)

        return result_list

    ####################################################################################################################
    # DURATION, DIFFICULTY, SERVINGS, CLASS_SWEET SQL STAMTEMENTS

    def select_from_recipe_table(self, list):
        # sql = SELECT recipe_href FROM kochbar_analysis_recipe WHERE duration <= (int) AND servings = (int)
        #       AND difficulty = '(string)' AND class_sweet = (0|1) LIMIT 0,1000;
        counter = 0
        sql_start = "SELECT recipe_href FROM " + self.RECIPE_TABLE + " WHERE "
        sql_end = self.LIMIT_1000
        for i in list:
            if counter < len(list) - 1:
                sql_start += i + " AND "
            else:
                sql_start += i
            counter += 1
        sql_start += sql_end

        print("\nRECIPE TABLE, sql: ")
        print(sql_start)

        curr_list = self.execute_sql_fetch_all(sql_start)
        return curr_list

    ####################################################################################################################
    # CATEGORY SQL STATEMENTS

    def select_from_category_table_via_category_list(self, category_list):
        cat_counter = 0
        cat_length = len(category_list)
        # sql: "SELECT href_link FROM kochbar_recipe_catgories WHERE category_label = '(string)'
        #       AND category_label = '(string)' (...) LIMIT 0,1000"
        sql_start = "SELECT link_href FROM " + self.CATEGORY_TABLE + " WHERE "
        sql_end = self.LIMIT_1000
        for cat in category_list:
            cat_counter += 1
            sql_start += "category_label = '" + str(cat) + "' "
            if cat_length > 1 and cat_counter < cat_length:
                sql_start += " AND "
        sql_start += sql_end

        print("\nCATEGORY TABLE, sql: ")
        print(sql_start)

        curr_list = self.execute_sql_fetch_all(sql_start)
        return curr_list

    ####################################################################################################################
    # INGREDIENTS SQL STATEMENTS:

    def select_from_ingredient_table(self, liked, list):
        # single like
        if list and len(list) < 2:
            result = self.select_from_ingredient_table_single_ingredient(liked, list)
            if not result:
                # TODO chatbot msg to USER
                if liked:
                    print("Es gibt keine Rezepte mit " + str(list[0]).capitalize() + ".")
                else:
                    # might never happen, but who knows with that db...
                    print("Es gibt keine Rezepte ohne " + str(list[0]).capitalize() + ".")
        # multi item list
        else:
            counter = 0
            sql = "SELECT distinct t0.recipe_href FROM "
            sql_table_part = ""
            sql_where = " WHERE "
            sql_not = ""
            sql_ingred_id = ""
            sql_rec_id = ""
            id_list = self.loop_for_ids(list)
            for i in id_list:
                sql_table_part += self.REC_INGRED_TABEL + " t" + str(counter)
                sql_ingred_id += "t" + str(counter) + ".ingredient_id = " + str(i) + " "
                if counter < len(id_list) - 1:
                    sql_table_part += ", "
                    if liked:
                        sql_ingred_id += "AND "  # AND NOT
                    else:
                        sql_ingred_id += "AND NOT "
                if counter > 0:
                    sql_rec_id += " AND t" + str(counter - 1) + ".recipe_href = t" + str(counter) + ".recipe_href"
                counter += 1
            sql += sql_table_part + sql_where + sql_not + sql_ingred_id + sql_rec_id + self.LIMIT_1000

            print("\n INGREDIENT TABLE, sql")
            print(sql)

            result = self.execute_sql_fetch_all(sql)
        return result

    def select_from_ingredient_table_single_ingredient(self, wanted, ingred):
        # SELECT distinct recipe_href FROM kochbar_analysis_recipe_ingredient_de
        #   INNER JOIN kochbar_analysis_ingredient_de
        #       ON kochbar_analysis_ingredient_de.ingredient_id = kochbar_analysis_recipe_ingredient_de.ingredient_id
        # WHERE kochbar_analysis_ingredient_de.name = "Eier" LIMIT 0,1000;
        ingred = ingred[0]
        sql_not = ""
        if not wanted:
            sql_not = "NOT "
        sql = "SELECT distinct recipe_href FROM " + self.REC_INGRED_TABEL + \
              " INNER JOIN " + self.INGREDIENT_TABLE + \
              " ON " + self.INGREDIENT_TABLE + ".ingredient_id = " + self.REC_INGRED_TABEL + ".ingredient_id" + \
              " WHERE " + sql_not + self.INGREDIENT_TABLE + ".name = '" + ingred + "'" + self.LIMIT_1000

        print("\nINGREDIENT TABLE, single, sql: ")
        print(sql)

        result = self.execute_sql_fetch_all(sql)
        return result

    def loop_for_ids(self, ingred_list):
        result_list = []
        for item in ingred_list:
            item_id = self.get_ingredient_id(item)
            if item_id:
                result_list.append(item_id)
            else:
                # TODO an Nutzer: ingredient not in db
                print(item.capitalize() + " ist nicht in der Datenbank enthalten.")
        return result_list

    # ANNE: DIFFERENCE between this and Claudia_s db_handler -> here: fetchone, not fetchall
    # looping through lists in loop_for_ids
    def get_ingredient_id(self, ingredient):
        sql = "SELECT ingredient_id FROM " + self.INGREDIENT_TABLE + " WHERE name = '" + ingredient + "';"
        result = self.execute_sql_fetch_one_for_ingredient_id(sql)
        return result

    ####################################################################################################################
    # TABLE SEARCH HANDLERS: preparation for sql queries (ingredients see above)

    # RECIPE TABLE: kochbar_analysis_recipe
    def handle_recipe_table_search(self, curr_list):
        # list of sql parts
        rec_table_list = None
        rec_table_list = self.select_from_recipe_table(curr_list)
        return rec_table_list

    # CATEGORY TABLE: kochbar_recipes_category
    def handle_category_table_search(self, cat_list):
        cat_table_list = None
        cat_table_list = self.select_from_category_table_via_category_list(cat_list)
        return cat_table_list

    ####################################################################################################################
    # FETCHER DEFS

    # used for get_ingredient_id
    def execute_sql_fetch_one_for_ingredient_id(self, sql):
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        # Anne: result is Tuple of int values (ingredient_id)
        if isinstance(result, tuple):
            result = result[-1]
        return result

    def execute_sql_fetch_one_for_recipe(self, sql):
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        return result

    # used for list defs (tables)
    def execute_sql_fetch_all(self, sql):
        result_list = []
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        for line in result:
            # result is a list of tuples, therefore
            result_list.append(line[-1])
        return result_list

    ####################################################################################################################
    # saves user input to DB
    def add_chat_to_db(self, result_dict):
        sql_query = "INSERT INTO telegram_chat_data (" \
                    "user_chat_id, system_chat_id, user_message_id, system_message_id, user_time, system_time, " \
                    "user_query, system_response, state, recipe_num_search) VALUES (%s, %s, %s, %s, NOW(), " \
                    "NOW(), %s, %s, %s, %s)"
        data = (result_dict.get("user").get("user_chat_id"), result_dict.get("system").get("system_chat_id"),
                result_dict.get("user").get("user_message_id"), result_dict.get("system").get("system_message_id"),
                result_dict.get("user").get("user_query"),
                result_dict.get("system").get("system_response"),
                result_dict.get("state"),
                result_dict.get("recipe_num_search"))
        self.cursor.execute(sql_query, data)
        self.db.commit()

    ####################################################################################################################
    # reconnects the database
    def reconnect_db(self):
        self.db.commit()
        self.close_db()
        self.db = mysql.connector.connect(host=self.host, database=self.name, user=self.user, password=self.password)
        self.cursor = self.db.cursor()

    # closes the database
    def close_db(self):
        self.db.commit()
        self.db.close()
