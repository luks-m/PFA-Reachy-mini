from jinja2 import contextfilter
import state_machine_obj as stm
import vocal_recognition as vr
import cmd
import movement as mv
import face_detection as facedet
# from reachy_sdk import ReachySDK
import time
from datetime import datetime
import advanced_conversation as advconv

import speech_synthesis as speech

def debug_print(str):
    print("DEBUG : " + str)

###############################################
## Fonctions Auxiliaires de la State Machine ##
###############################################

def __picture_noun():
    t = datetime.now()
    return f"{t.year}_{t.month}_{t.day}_{t.hour}_{t.minute}_{t.second}"

####################
## States Actions ##
####################

def allumage_robot_func(context):
    #TODO
    #facedet.initiate_reachy_camera(context["session"])
    mv.motor_on(context["session"])
    mv.move_to(context["session"], 0.5, 90, 0, 0.5)
    return context

# state action of Recherche d'Interaction
def recherche_interaction_func(context):
    context["command"] = vr.record_and_transcript()
    return context

def recherche_de_personne_func(context):
    #TODO
    return context

def incitation_interaction_func(context):
    #TODO
    return context

# state action of Attente d'Ordre
def attente_ordre_func(context):
    mv.listen(context["session"])
    context["command"] = vr.record_and_transcript()
    return context

def traitement_ordre_func(context):
    return context

# state action of Conversation
def conversation_func(context):
    return context

# state action of Bonjour
def bonjour_func(context):
    mv.incentive(context["session"])
    speech.text_to_speech(cmd.one_out(cmd.set_bonjour["s"]))
    debug_print("(R) " + cmd.one_out(cmd.set_bonjour["s"]))
    return context

# state action of Au Revoir
def aurevoir_func(context):
    mv.thanking(context["session"])
    speech.text_to_speech(cmd.one_out(cmd.set_aurevoir["s"]))
    debug_print("(R) " + cmd.one_out(cmd.set_aurevoir["s"]))
    return context

# state action of Ca va
def cava_func(context):
    speech.text_to_speech(cmd.one_out(cmd.set_cava["s"]))
    debug_print("(R) " + cmd.one_out(cmd.set_cava["s"]))
    return context

# state action of Gentil
def gentil_func(context):
    mv.happy(context["session"])
    speech.text_to_speech(cmd.one_out(cmd.set_gentil["s"]))
    debug_print("(R) " + cmd.one_out(cmd.set_gentil["s"]))
    return context

# state action of Mechant
def mechant_func(context):
    mv.sad(context["session"])
    speech.text_to_speech(cmd.one_out(cmd.set_mechant["s"]))
    debug_print("(R) " + cmd.one_out(cmd.set_mechant["s"]))
    return context

def eteindre_func(context):
    speech.text_to_speech(cmd.one_out(cmd.set_eteindre["s"]))
    debug_print("(R) " + cmd.one_out(cmd.set_eteindre["s"]))
    mv.thanking(context["session"])
    mv.motor_off(context["session"])
    return context

# state action of Incomprehension
def incomprehension_func(context):
    advconv.openai_speech(context["command"])
    return context

def photo_func(context):
    #TODO
    debug_print("(R) Quel type de photo voulez vous ? simple ou de groupe ?")
    context["command"] = vr.record_and_transcript()
    return context

def photo_simple_func(context):
    debug_print("(R) cadrage de la photo simple")
    # penser a enlever le True de test
    angle = facedet.smart_give_angle(context["session"], 10, facedet.n_closest_angle, 1, True)
    mv.update_position(context["session"], angle.v, angle.h, 0.5)
    return context

def photo_groupe_func(context):
    debug_print("(R) cadrage de la photo de groupe")
    # penser a enlever le True de test
    angle = facedet.smart_give_angle(context["session"], 10, facedet.framing_for_group_photo_angle, 25, True)
    # ajouter movement
    return context

def prise_photo_func(context):
    debug_print("(R) 3... 2... 1... clic !!")
    facedet.take_picture(context["session"], __picture_noun())
    return context
    
########################
## Transitions Action ##
########################

# transition action to reset the command key of the context
def reset_for_attente_ordre(context):
    context["command"] = ""
    enregistrer_date(context)
    return context

def temps_presque_ecoule_func(context):
    #speech.text_to_speech(TODO)
    debug_print("(R) Le temps est presque écoulé")
    return context

def temps_ecoule_func(context):
    #speech.text_to_speech(TODO)
    debug_print("(R) Le temps est écoulé")
    return context

def enregistrer_date(context):
    context["time"] = datetime.now()
    return context

def reset_for_incitation_interaction(context):
    #TODO
    return context

###########################
## Transition predicats ##
###########################

# transition predicat to detect activation keywords
def activation_detection(context):
    return cmd.all_in(context["command"], cmd.set_activation)

# transition predicat function to verify if the command is not an ERROR
def command_verif(context):
    return (context["command"] != "ERROR")

# transition predicat to detect the bonjour set's keywords
def bonjour_set_detection(context):
    return (cmd.one_in(context["command"], cmd.set_bonjour["e"]))

# transition predicat to detect the aurevoir set's keywords
def aurevoir_set_detection(context):
    return (cmd.one_in(context["command"], cmd.set_aurevoir["e"]))

# transition predicat to detect the cava set's keywords
def cava_set_detection(context):
    return (cmd.one_in(context["command"], cmd.set_cava["e"]))

# transition predicat to detect the gentil set's keywords
def gentil_set_detection(context):
    return (cmd.one_in(context["command"], cmd.set_gentil["e"]))

# transition predicat to detect the mechant set's keywords
def mechant_set_detection(context):
    return (cmd.one_in(context["command"], cmd.set_mechant["e"]))

def eteindre_set_detection(context):
    return (cmd.one_in(context["command"], cmd.set_eteindre["e"]))

def temps_presque_ecoule(context):
    temps = datetime.now() - context["time"]
    return (temps.total_seconds() > 15 and temps.total_seconds() < 20)

def temps_ecoule(context):
    temps = datetime.now() - context["time"]
    return (temps.total_seconds() > 30)

def photo_set_detection(context):
    return (cmd.one_in(context["command"], cmd.set_photo))

def simple_set_detection(context):
    return (cmd.one_in(context["command"], cmd.set_simple))

def groupe_set_detection(context):
    return (cmd.one_in(context["command"], cmd.set_groupe))

def photo_simple_sets_detection(context):
    return (photo_set_detection(context) and simple_set_detection(context)) 

def photo_groupe_sets_detection(context):
    return (photo_set_detection(context) and groupe_set_detection(context)) 

def detection_personne(context):
    #TODO
    return context