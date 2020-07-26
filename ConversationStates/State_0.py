# -*- coding: utf-8 -*-

from config import conversation_states, system_response_text

# Anne: State 0 == ERROR State


# ANNE: TODO never used so far: wenn alles aus mod_rel_rec entfernt wurde und immer noch NULL, dann das schicken
def show_no_recipe_found(model):
    model.framework_state = conversation_states.ERROR_STATE
    # system_response_text.RECIPE_ERROR = "Auf Basis deiner Angaben konnte ich leider kein Rezept finden.
    #                                       Bitte starte mit „Hi Bot“ eine neue Rezeptsuche."
    return system_response_text.RECIPE_ERROR