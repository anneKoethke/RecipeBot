# -*- coding: utf-8 -*-

from config import system_response_text


# Frage nach System: 'System B verwenden?'
def ask_for_system_state(nlu, user_query):
    quest_answer = nlu.get_answer(user_query)
    if quest_answer:  # ja -> verwendet B
        system_message = system_response_text.USE_SYSTEM_B + "\n" + system_response_text.GREETING
        use_system_B = True
    else:  # nein oder None -> verwendet A
        system_message = system_response_text.USE_SYSTEM_A + "\n" + system_response_text.GREETING
        use_system_B = False
    return [system_message, use_system_B]
