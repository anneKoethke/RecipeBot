# -*- coding: utf-8 -*-

# Anne: needed for parse-mode (Markup in chat via bot)
import telegram
from telegram.ext import CommandHandler, Updater, MessageHandler, Filters
# Anne: outsourced CONSTANTS to config directory
from config import bot_token, conversation_states, system_response_text, database_config
from helperClasses import ConvLogger
from helperClasses.ChatFilter import GreetFilter
# States
from ConversationStates import State_0, State_2_1, State_2_2, State_3_1, State_3_2, State_3_3
# everything else
from model import Model
# from db_handler import DatabaseHandler
from Database.db_handler import DatabaseHandler
from telefood_nlu import TelefoodNLU
from recipe_details import RecipeDetails

SYSTEM_B = True
# Anne: FOR LOGGING
conversation = []
curr_user = "no_user"


########################################################################################################################
# DATABASE: saves the current user input and the system response to the database
#           (every turn of the current conversation)
########################################################################################################################

# Anne: outsourced;
def respond_to_user_and_save_conversational_turn(update, context, system_message):
    system_response = context.bot.send_message(chat_id=update.effective_chat.id, text=system_message,
                                               parse_mode=telegram.ParseMode.HTML)
    save_input_to_database(update, system_response)


# Anne: save Conversation (after State 3.4 Title Display State) to DB and JSON
def save_input_to_database(update, system_response):
    result_dict = {"user": {"user_chat_id": update.effective_chat.id, "user_message_id": update.message.message_id,
                            "user_date": str(update.message.date), "user_query": update.message.text},
                   "system": {"system_chat_id": system_response.from_user.id,
                              "system_message_id": system_response.message_id,
                              "system_date": str(system_response.date), "system_response": system_response.text},
                   "state": model.framework_state,
                   "recipe_num_search": model.recipe_num_search}

    # Anne: track conversation outside db
    conversation.append(result_dict)
    # "möchtest du die Zutaten sehen" ? -> "Ja": State 3.3 reached: save current recipe
    if model.framework_state == conversation_states.INGREDIENT_LIST_DISPLAY_STATE:
        conversation.append({"current_recipe": str(details.current_recipe)})
    # current recipe in State 3.4 can be a different recipe, if user declines recipe in State 3.3 (based on ingredients)
    if model.framework_state == conversation_states.RECIPE_DISPLAY_STATE:
        conversation.append({"current_recipe": str(details.current_recipe)})
        conversation.append({"curr_user": curr_user})
        if SYSTEM_B:
            conversation.append({"System": "B"})
        else:
            conversation.append({"System": "A"})
        ConvLogger.save_to_json(conversation)
        conversation.clear()

    db.add_chat_to_db(result_dict)


########################################################################################################################
# State 1 (greeting state): greet user in telegram, empties recipe and model objects, saves the turn o db
########################################################################################################################


def greet_user(update, context):
    system_message = system_response_text.GREETING
    details.reset_details()
    model.reset_model()
    model.replied_message = system_message
    model.available_conversation_questions = system_response_text.CONVERSATION_STOCK.copy()
    model.available_ingredients_questions = system_response_text.INGREDIENT_STOCK.copy()
    model.framework_state = conversation_states.GREETING_STATE
    model.framework_states.append(model.framework_state)
    respond_to_user_and_save_conversational_turn(update, context, system_message)

########################################################################################################################
# DISPATCHER: Intents and Message Handling
########################################################################################################################


def add_slash_handlers(dispatcher):
    dispatcher.add_handler(CommandHandler("start", start_command))
    dispatcher.add_handler(CommandHandler("help", help_command))


def start_command(update, context):
    system_response = context.bot.send_message(chat_id=update.effective_chat.id, text=system_response_text.START,
                                               parse_mode=telegram.ParseMode.HTML)
    save_input_to_database(update, system_response)


def help_command(update, context):
    system_response = context.bot.send_message(chat_id=update.effective_chat.id, text=system_response_text.HELP,
                                               parse_mode=telegram.ParseMode.HTML)
    save_input_to_database(update, system_response)


# von Anne: filters user input for wake word, handles user messages to telegram bot (invocation,
def define_conversational_intents(dispatcher):
    greet_filter = GreetFilter()
    greeting_intent = MessageHandler(greet_filter, greet_user)
    user_input_intent = MessageHandler(Filters.text, handle_user_query)
    unknown_intent = MessageHandler(Filters.command, unknown_command)
    add_intent_handlers(dispatcher, greeting_intent, user_input_intent, unknown_intent)


# von Anne
def add_intent_handlers(dispatcher, greeting_intent, user_input_intent, unknown_intent):
    dispatcher.add_handler(greeting_intent)
    dispatcher.add_handler(user_input_intent)
    dispatcher.add_handler(unknown_intent)


def unknown_command(update, context):
    system_response = context.bot.send_message(chat_id=update.effective_chat.id,
                                               text=system_response_text.COMMAND_ERROR)
    save_input_to_database(update, system_response)


# Anne: outsourched from main()
def add_error_handling(dispatcher):
    dispatcher.add_error_handler(dispatcher_error_raised)


# von ANNE
def dispatcher_error_raised(context):
    print("\n!!! DISPATCHER ERROR - context.error:")
    print(context.error)
    # ANNE: wenn hier die Datenbank abspackt, muss das Programm auch neugestartet werden
    # save_input_to_database(update, system_response={}, dispatcher_error=True, context_error=context.error)
    # -> never reached because of dispatcher error

########################################################################################################################
# THE STATE HANDLER: handles states (the whole conversation), responds to user and save to db
########################################################################################################################


# Anne: theoretically reachable states: '0','1','2.1','2.2','3.1','3.2','3.3','3.4','5','no_state'
#       reached states: 0, 1, 2.1, 2.2, 3.1, 3.2, 3.3, 3.4
def handle_user_query(update, context):
    print("\tframework state: " + str(model.framework_state))
    # Anne: system_message MUST be None!
    system_message = None
    user_query = update.message.text
    # start of conversation (state: 1) or asking conversational questions - everything not ingredient (state 2.1)
    if model.framework_state is not conversation_states.NO_STATE and (
            model.framework_state == conversation_states.GREETING_STATE or
            model.framework_state == conversation_states.CONVERSATION_STOCK_STATE):
        system_message = State_2_1.handle_conversation_question(context, update, db, nlu, model, details)
    elif model.framework_state == conversation_states.INGREDIENT_STOCK_STATE:
        # (state 2.2): asking for specific ingredients
        system_message = State_2_2.ingredient_stock_state(context, update, SYSTEM_B, db, nlu, model, details, user_query)
    elif model.framework_state == conversation_states.TITLE_DISPLAY_STATE:
        # show recipe title: "Wie klingt <Title> für dich?"
        system_message = State_3_1.title_display_state(nlu, model, details, user_query)
    elif model.framework_state == conversation_states.INGREDIENT_LIST_STATE:
        # get feedback on showing ingredient list: "Zutaten: ...,...,... Möchtest du das Rezept sehen?"
        system_message = State_3_2.ingredient_list_state(nlu, model, details, user_query)
    elif model.framework_state == conversation_states.INGREDIENT_LIST_DISPLAY_STATE:
        # show ingredient list, get feedback on recipe display: "Rezept: <Title> Beschreibung: ...."
        system_message = State_3_3.ingredient_list_display_state(SYSTEM_B, nlu, model, details, user_query)
    elif model.framework_state == conversation_states.RECIPE_DISPLAY_STATE:
        print("\nEND of SEARCH")
        # "Mit 'hey <BOTNAME>' kann eine neue Suche gestartet werden"
        system_message = system_response_text.START_SEARCH
    elif model.framework_state == conversation_states.ERROR_STATE:
        # State 0 : Error State
        # Anne: seems to be never reached
        system_message = State_0.show_no_recipe_found(model)
    elif model.framework_state == conversation_states.MISC_QUESTION_STATE:
        # Anne: seems to be never reached
        system_message = "Ich bin im State 5 MISC QUESTION"
    elif model.framework_state == conversation_states.NO_STATE:
        system_message = "Hoppla, ein Fehler ist aufgeteten. " + system_response_text.START_SEARCH
    else:
        system_message = "nicht null: " + system_response_text.START_SEARCH
    model.framework_states.append(model.framework_state)
    respond_to_user_and_save_conversational_turn(update, context, system_message)


def main():
    print("\nNutzer kann loslegen\n")
    # frontend to telegram.Bot:
    # receives updates from Telegram and delivers them to the dispatcher (the bot-uuid, using context based callbacks)
    updater = Updater(token=bot_token.BOT_TOKEN, use_context=True)
    # updates from Updater are dispatched to their registered handlers via dispatcher (registers the handlers)
    dispatcher = updater.dispatcher
    # Dispatcher sub_defs (Anne: outsourced, see above):
    # dispatcher registers slash-commands in dialog (/help, /start)
    add_slash_handlers(dispatcher)
    # which intents can be matched ()
    define_conversational_intents(dispatcher)
    add_error_handling(dispatcher)
    # Updater:
    # start pulling updates from telegram
    updater.start_polling()
    # sth. to manually stop the bot from console (why ever Claudia put that there)
    updater.idle()


if __name__ == "__main__":
    model = Model()
    details = RecipeDetails()
    db = DatabaseHandler(database_config.HOST, database_config.NAME, database_config.USER, database_config.PASSWORD)
    nlu = TelefoodNLU()
    main()
