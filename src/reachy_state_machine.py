import executeur as extr
import state_machine_obj as stm
import state as st
import transition as tr

import vocal_recognition as vr
import cmd
# import movement as mv
# from reachy_sdk import ReachySDK
import time
# import speech_synthesis as speech

def debug_print(str):
    print("DEBUG : " + str)

# reachy = ReachySDK(host='localhost')  # Replace with the actual IP

# reachy.head
# for name, joint in reachy.joints.items():
#     print(f'Joint "{name}" position is {joint.present_position} degree.')

# r = mv.Movement(reachy)
# r.motor_on()
# r.head.look_at(1, 0, 0, 2)

####################
## States Actions ##
####################

# state action of Recherche d'Interaction
def recherche_interaction_func(context):
    context["command"] = vr.record_and_transcript()
    return context

# state action of Attente d'Ordre
def attente_ordre_func(context):
    context["command"] = vr.record_and_transcript()
    return context

# state action of Traitement d'ordre
def traitement_ordre_func(context):
    return context

# state action of Conversation
def conversation_func(context):
    return context

# state action of Bonjour
def bonjour_func(context):
    # speech.text_to_speech(cmd.one_out(cmd.set_bonjour["s"]))
    debug_print(cmd.one_out(cmd.set_bonjour["s"]))
    return context

# state action of Ca Va
def cava_func(context):
    # speech.text_to_speech(cmd.one_out(cmd.set_cava["s"]))
    debug_print(cmd.one_out(cmd.set_cava["s"]))
    return context

# state action of Au Revoir
def aurevoir_func(context):
    # speech.text_to_speech(cmd.one_out(cmd.set_aurevoir["s"]))
    debug_print(cmd.one_out(cmd.set_aurevoir["s"]))
    return context

# state action of Gentil
def gentil_func(context):
    # speech.text_to_speech(cmd.one_out(cmd.set_gentil["s"]))
    debug_print(cmd.one_out(cmd.set_gentil["s"]))
    # r.happy()
    return context

# state action of Mechant
def mechant_func(context):
    # speech.text_to_speech(cmd.one_out(cmd.set_mechant["s"]))
    debug_print(cmd.one_out(cmd.set_mechant["s"]))
    # r.sad()
    return context

#####################
## States Creation ##
#####################

# create the state Recherche d'Interaction
recherche_interaction = st.State(recherche_interaction_func)

# create the state Attente d'Ordre
attente_ordre = st.State(attente_ordre_func)

# create the state Traitement d'ordre
traitement_ordre = st.State(traitement_ordre_func)

# create the state Conversation
conversation = st.State(conversation_func)

# create the state Bonjour
bonjour = st.State(bonjour_func)

# create the state Ca Va
cava = st.State(cava_func)

# create the state Au Revoir
aurevoir = st.State(aurevoir_func)

# create the state Gentil
gentil = st.State(gentil_func)

# create the state Mechant
mechant = st.State(mechant_func)

########################
## Transitions Action ##
########################

# transition action between Recherche d'Interaction and Attente d'Ordre
def RI_to_AO_func(context):
    return context

# transition action between  Attente d'Ordre and Traitement d'Ordre
def AO_to_TO_func(context):
    return context

# transition action between Traitement d'Ordre and Conversation
def TO_to_C_func(context):
    return context

# transition action between Conversation and Bonjour
def C_to_B_func(context):
    return context

# transition action between Bonjour and Attente d'ordre
def B_to_AO_func(context):
    context["command"] = ""
    return context

# transition action between Conversation and Ca Va
def C_to_CV_func(context):
    return context

# transition action between Ca Va and Attente d'ordre
def CV_to_AO_func(context):
    context["command"] = ""
    return context

# transition action between Conversation and Au Revoir
def C_to_AR_func(context):
    return context

# transition action between Au Revoir and Attente d'ordre
def AR_to_RI_func(context):
    context["command"] = ""
    return context

# transition action between Conversation and Gentil
def C_to_G_func(context):
    return context

# transition action between Gentil and Attente d'ordre
def G_to_AO_func(context):
    context["command"] = ""
    return context

# transition action between Conversation and Mechant
def C_to_M_func(context):
    return context

# transition action between Mechant and Attente d'ordre
def M_to_AO_func(context):
    context["command"] = ""
    return context

# transition action between Conversation and Attente d'ordre
def C_to_AO_func(context):
    context["command"] = ""
    return context

###########################
## Transitions Condition ##
###########################

# transition verif function between Recherche d'Interaction and Attente d'Ordre
def RI_to_AO_verif(context):
    return cmd.all_in(context["command"], cmd.set_activation)

# transition verif function between  Attente d'Ordre and Traitement d'Ordre
def AO_to_TO_verif(context):
    return (context["command"] != "ERROR")

# transition verif function between Traitement d'Ordre and Conversation
def TO_to_C_verif(context):
    return True

# transition verif function between Conversation and Bonjour
def C_to_B_verif(context):
    return (cmd.one_in(context["command"], cmd.set_bonjour["e"]))


# transition verif function between Bonjour and Attente d'ordre
def B_to_AO_verif(context):
    return True

# transition verif function between Conversation and Ca Va
def C_to_CV_verif(context):
    return (cmd.one_in(context["command"], cmd.set_cava["e"]))

# transition verif function between Ca Va and Attente d'ordre
def CV_to_AO_verif(context):
    return True

# transition verif function between Conversation and Au Revoir
def C_to_AR_verif(context):
    return (cmd.one_in(context["command"], cmd.set_aurevoir["e"]))

# transition verif function between Au Revoir and Attente d'ordre
def AR_to_RI_verif(context):
    return True

# transition verif function between Conversation and Gentil
def C_to_G_verif(context):
    return (cmd.one_in(context["command"], cmd.set_gentil["e"]))

# transition verif function between Gentil and Attente d'ordre
def G_to_AO_verif(context):
    return True

# transition verif function between Conversation and Mechant
def C_to_M_verif(context):
    return (cmd.one_in(context["command"], cmd.set_mechant["e"]))

# transition verif function between Mechant and Attente d'ordre
def M_to_AO_verif(context):
    return True

# transition verif function between Conversation and Attente d'ordre
def C_to_AO_verif(context):
    return True
##########################
## Transitions Creation ##
##########################

# create the transition between Recherche d'Interaction and Attente d'Ordre
RI_to_AO = tr.Transition(attente_ordre, RI_to_AO_func, RI_to_AO_verif)

# create the transition between  Attente d'Ordre and Traitement d'Ordre
AO_to_TO = tr.Transition(traitement_ordre, AO_to_TO_func, AO_to_TO_verif)

# create the transition between Traitement d'Ordre and Conversation
TO_to_C = tr.Transition(conversation, TO_to_C_func, TO_to_C_verif)

# create the transition between Conversation and Bonjour
C_to_B = tr.Transition(bonjour, C_to_B_func, C_to_B_verif)

# create the transition between Bonjour and Attente d'ordre
B_to_AO = tr.Transition(attente_ordre, B_to_AO_func, B_to_AO_verif)

# create the transition between Conversation and Ca Va
C_to_CV = tr.Transition(cava, C_to_CV_func, C_to_CV_verif)

# create the transition between Ca Va and Attente d'ordre
CV_to_AO = tr.Transition(attente_ordre, CV_to_AO_func, CV_to_AO_verif)

# create the transition between Conversation and Au Revoir
C_to_AR = tr.Transition(aurevoir, C_to_AR_func, C_to_AR_verif)

# create the transition between Au Revoir and Attente d'ordre
AR_to_RI = tr.Transition(recherche_interaction, AR_to_RI_func, AR_to_RI_verif)

# create the transition between Conversation and Gentil
C_to_G = tr.Transition(gentil, C_to_G_func, C_to_G_verif)

# create the transition between Gentil and Attente d'ordre
G_to_AO = tr.Transition(attente_ordre, G_to_AO_func, G_to_AO_verif)

# create the transition between Conversation and Mechant
C_to_M = tr.Transition(mechant, C_to_M_func, C_to_M_verif)

# create the transition between Mechant and Attente d'ordre
M_to_AO = tr.Transition(attente_ordre, M_to_AO_func, M_to_AO_verif)

# create the transition between Conversation and Attente d'ordre
C_to_AO = tr.Transition(attente_ordre, C_to_AO_func, C_to_AO_verif, True)

##############################
## Transition sets Creation ##
##############################

# create the transition set of Recherche d'Interaction
recherche_interaction_transitions = {RI_to_AO}

# create the transition set of Attente d'Ordre
attente_ordre_transitions = {AO_to_TO}

# create the transition set of Traitement d'ordre
traitement_ordre_transitions = {TO_to_C}

# create the transition set of Conversation
conversation_transitions = {C_to_B, C_to_CV, C_to_AR, C_to_G, C_to_M, C_to_AO}

# create the transition set of Bonjour
bonjour_transitions = {B_to_AO}

# create the transition set of Ca Va
cava_transitions = {CV_to_AO}

# create the transition set of Au Revoir
aurevoir_transitions = {AR_to_RI}

# create the transition set of Gentil
gentil_transitions = {G_to_AO}

# create the transition set of Mechant
mechant_transitions = {M_to_AO}   

#################################################
## Filling Transition sets in transition_table ##
#################################################
transition_table = {}

# filling the transitions of Recherche d'Interaction
transition_table[str(recherche_interaction)] = recherche_interaction_transitions

# filling the transitions of Attente d'Ordre
transition_table[str(attente_ordre)] = attente_ordre_transitions

# filling the transitions of Traitement d'ordre
transition_table[str(traitement_ordre)] = traitement_ordre_transitions

# filling the transitions of Conversation
transition_table[str(conversation)] = conversation_transitions

# filling the transitions of Bonjour
transition_table[str(bonjour)] = bonjour_transitions

# filling the transitions of Ca Va
transition_table[str(cava)] = cava_transitions

# filling the transitions of Au Revoir
transition_table[str(aurevoir)] = aurevoir_transitions

# filling the transitions of Gentil
transition_table[str(gentil)] = gentil_transitions

# filling the transitions of Mechant
transition_table[str(mechant)] = mechant_transitions

##########################
## Create the State set ##
##########################

states = {  recherche_interaction, 
            attente_ordre,
            traitement_ordre,
            conversation,
            bonjour,
            cava,
            aurevoir,
            gentil,
            mechant
}

###################################
## Creation of the State Machine ##
###################################

context ={"command" : ""}

state_machine = stm.State_Machine(states, transition_table, recherche_interaction, context)

##########
## Test ##
##########

executeur = extr.Executeur(state_machine)

executeur.execute(context)