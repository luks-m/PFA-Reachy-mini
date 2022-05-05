from jinja2 import contextfilter, contextfunction
import time
from datetime import datetime
import sys
sys.path.append("..")
sys.path.append("../detection")
sys.path.append("../speech")
import movement as mv
import face_detection as facedet
from reachy_sdk import ReachySDK
import state_machine_obj as stm
import vocal_recognition as vr
import cmd
import advanced_conversation as advconv
import speech_synthesis_gtt as speech
import random

def debug_print(str):
    print("DEBUG : " + str)

#############################################
## Auxiliary Functions of the state machine ##
#############################################

# a function that return a string corresponding to a photo name format
def __picture_noun():
    t = datetime.now()
    return f"{t.year}_{t.month}_{t.day}_{t.hour}_{t.minute}_{t.second}"

####################
## States Actions ##
####################

# This function initialize the used values of the context
def __init_context(context):
    context["aruco"] = None
    context["time"] = datetime.now()
    context["command"] = ""
    context["advanced_command"] = ""
    context["activation"] = False 
    (context["recognizer"], context["micro"]) = vr.init_record()
    return context

# This function execute the function the robot need when it is turned on 
def allumage_robot_func(context):
    context = __init_context(context)
    mv.motor_on(context["session"])
    mv.move_to(context["session"], 0.5, 90, 0, 0.5)
    speech.start_voice()
    return context

# state action of Recherche d'Interaction
def recherche_interaction_func(context):
    mv.reset_antennas(context["session"])
    #reset the context for advanced conversation
    context["advanced_command"] = "Ceci est une conversation entre une Intelligence artificielle et un Humain. Nous allons parler en français et nous sommes dans une école d'ingénieurs. Actuellement c'est la soirée partenaire de l'école, il y a des élèves et des entreprises qui se rencontrent. Tu es un robot de démonstration, donne ton maximum pour les impressionner.\n Human:Bonjour, j'espère que tu es heureux d'avoir été invité à la soirée partenaire de l'école.\nAI:Bonjour, c'est super je suis content d'y avoir été invité\n"
    context["activation"] = vr.hey_reachy_detection()
    return context

# state action of Recherche d'Interaction but in the case where there is only Aruco detection
def recherche_interaction__only_aruco_func(context):
    mv.reset_antennas(context["session"])
    angle = facedet.smart_give_angle(context["session"], 15, facedet.n_closest_angle, 1, True)
    mv.update_position(context["session"], angle.v, angle.h, 0.5)
    #reset the context for advanced conversation
    context["advanced_command"] = "Ceci est une conversation entre une Intelligence artificielle et un Humain. Nous allons parler en français et nous sommes dans une école d'ingénieurs. Actuellement c'est la soirée partenaire de l'école, il y a des élèves et des entreprises qui se rencontrent. Tu es un robot de démonstration, donne ton maximum pour les impressionner.\n Human:Bonjour, j'espère que tu es heureux d'avoir été invité à la soirée partenaire de l'école.\nAI:Bonjour, c'est super je suis content d'y avoir été invité\n"
    context["aruco"] = facedet.smart_get_aruco_code(context["session"], 3)
    return context

# state action of Recherche de Personne
def recherche_de_personne_func(context):
    context["deteced"] = False
    angle = facedet.smart_give_angle(context["session"], 15, facedet.n_closest_angle, 1, True)
    context["detected"] = (angle.h != 0 or angle.v != 0)

    return context

# state action of Incitation d'Interaction
def incitation_interaction_func(context):
    mv.incentive(context["session"])
    return context

# state action of Incitation d'interaction but in the case where there is only Aruco detection
def incitation_aruco_func(context):
    mv.incentive(context["session"])
    speech.text_to_speech("Si vous voulez communiquer avec moi il faut me montrer les code Aruco qui sont devant vous")
    return context

# state action of Attente d'Ordre
def attente_ordre_func(context):
    mv.listen(context["session"])
    r1 = random.randint(1, 4)
    if(r1 == 1):
        speech.attente_ordre_speech()
    context["command"] = vr.record_and_transcript(context["recognizer"], context["micro"])
    return context

# state action of Attente d'Ordre but in the case where there is only Aruco detection
def attente_ordre_only_aruco_func(context):
    mv.listen(context["session"])
    speech.attente_ordre_aruco_speech()
    context["aruco"] = None
    context["aruco"] = facedet.smart_get_aruco_code(context["session"], 3)
    return context

# state action of Traitement d'ordre 
def traitement_ordre_func(context):
    mv.thinking(context["session"])
    return context

# state action of Traitement d'ordre but in the case where there is only Aruco detection
def traitement_ordre_only_aruco_func(context):
    mv.thinking(context["session"])
    return context

# state action of Conversation
def conversation_func(context):
    mv.move_back(context["session"])
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
    speech.happy_voice()
    mv.happy(context["session"])
    speech.text_to_speech(cmd.one_out(cmd.set_gentil["s"]))
    debug_print("(R) " + cmd.one_out(cmd.set_gentil["s"]))
    return context

# state action of Mechant
def mechant_func(context):
    speech.sad_voice()
    mv.sad(context["session"])
    return context

# state actoin of Eteindre, this is the function the robot needs when it is turned off
def eteindre_func(context):
    mv.move_back(context["session"])
    mv.thanking(context["session"])
    speech.turn_of_voice()
    mv.motor_off(context["session"])
    return context

# state action of Incomprehension
def incomprehension_func(context):
    sentence = context["command"]
    context["advanced_command"] += f"Human:{sentence} \n"
    context["advanced_command"] = advconv.openai_speech(context["advanced_command"])
    debug_print(context["advanced_command"])
    return context

# state action of Photo
def photo_func(context):
    debug_print("(R) Quel type de photo voulez vous ? simple ou de groupe ?")
    speech.photo_speech()
    context["command"] = vr.record_and_transcript(context["recognizer"], context["micro"])
    return context

# state action of Photo Simple
def photo_simple_func(context):
    mv.move_back(context["session"])
    debug_print("(R) cadrage de la photo simple")
    speech.cadrage_speech()
    angle = facedet.smart_give_angle(context["session"], 30, facedet.n_closest_angle, 1, False)
    mv.update_position(context["session"], angle.v, angle.h, 0.5)
    return context

# state action of Photo Groupe
def photo_groupe_func(context):
    mv.move_back(context["session"])
    debug_print("(R) cadrage de la photo de groupe")
    speech.cadrage_speech()
    angle = facedet.smart_give_angle(context["session"], 30, facedet.framing_for_group_photo_angle, 99, False)
    mv.update_position(context["session"], angle.v, angle.h, 0.5)
    return context

# state action of Prise Photo
def prise_photo_func(context):
    debug_print("(R) 3... 2... 1... cheese !!")
    speech.prise_de_photo1()
    facedet.take_picture(context["session"], __picture_noun())
    speech.prise_de_photo2()
    return context

def filtre_func(context):
    speech.filtre_speech()
    context["command"] = vr.record_and_transcript(context["recognizer"], context["micro"])
    return context

def face_swap_prise_photo_func(context):
    debug_print("(R) 3... 2... 1... cheese !!")
    speech.prise_de_photo1()
    facedet.take_swapped_faces_picture(context["session"], __picture_noun(), 10)
    speech.prise_de_photo2()
    return context

def noir_et_blanc_prise_photo_func(context): 
    return context

# state action when no one is detected after a timeout   
def triste_recherche_func(context):
    mv.sad(context["session"])
    return context

########################
## Transitions Actions ##
########################

# transition action to reset the command key of the context
def reset_for_attente_ordre(context):
    mv.move_back(context["session"])
    context["command"] = ""
    enregistrer_date(context)
    return context

# transition action to reset the context when it returns to Recherche dI'nteraction
def reset_for_recherche_interaction(context):
    mv.update_position(context["session"], 90, 0, 0.5)
    (context["recognizer"], context["micro"]) = vr.init_record()
    return context

# transition action to reset the activation key of the context
def reset_activation(context):
    mv.listen(context["session"])
    context["activation"] = False
    return context

# transition action when it is almost timeout
def temps_presque_ecoule_func(context):
    speech.temps_presque_ecoule_speech()
    debug_print("(R) Le temps est presque écoulé")
    return context

# transition action when it is timeout
def temps_ecoule_func(context):
    speech.temps_ecoule_speech()
    debug_print("(R) Le temps est écoulé")
    return context

# transition action to save the actual date (especialy the hour, minute and second)
def enregistrer_date(context):
    context["time"] = datetime.now()
    return context

# transition action to reset the context when it returns to Incitation d'Interaction
def reset_for_incitation_interaction(context):
    return context

###########################
## Transition predicats ##
###########################

# transition predicat to detect activation keywords
def activation_detection(context):
    return context["activation"] == True

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

# transition predicat to detect the eteindre set's keywords
def eteindre_set_detection(context):
    return (cmd.one_in(context["command"], cmd.set_eteindre["e"]))

# transition predicat to detect if it is almost timeout
def temps_presque_ecoule(context):
    temps = datetime.now() - context["time"]
    return (temps.total_seconds() > 15 and temps.total_seconds() < 20)

# transition predicat to detect if it is timeout
def temps_ecoule(context):
    temps = datetime.now() - context["time"]
    return (temps.total_seconds() > 30)

# transition predicat to detect the photo set's keywords
def photo_set_detection(context):
    return (cmd.one_in(context["command"], cmd.set_photo))

# transition predicat to detect the simple set's keywords
def simple_set_detection(context):
    return (cmd.one_in(context["command"], cmd.set_simple))

# transition predicat to detect the groupe set's keywords
def groupe_set_detection(context):
    return (cmd.one_in(context["command"], cmd.set_groupe))

# transition predicat to detect the photo set's and simple set's keywords
def photo_simple_sets_detection(context):
    return (photo_set_detection(context) and simple_set_detection(context)) 

# transition predicat to detect the photo set's and groupe set's keywords
def photo_groupe_sets_detection(context):
    return (photo_set_detection(context) and groupe_set_detection(context)) 

def filtre_set_detection(context):
    return (cmd.all_in(context["command"], cmd.set_filtre))

def filtre_face_swap_sets_detection(context):
    return (face_swap_set_detection(context) and filtre_set_detection(context))

def filtre_noir_et_blanc_sets_detection(context):
    return (noir_et_blanc_set_detection(context) and filtre_set_detection(context))

def face_swap_set_detection(context):
    return (cmd.all_in(context["command"], cmd.set_face_swap))

def noir_et_blanc_set_detection(context):
    return (cmd.all_in(context["command"], cmd.set_noir_et_blanc))

# transition predicat to detect if someone is seen 
def detection_personne(context):
    return context["detected"] == True

###########################
##### ARUCO Functions #####
###########################

# transition predicats to detect if there is an ARUCO detected
def aruco_verif(context):
    return context["aruco"] != None

# transition predicats to detect if there is the "activation" ARUCO detected
def activation_aruco_det(context):
    return context["aruco"] == 1

# transition predicats to detect if there is the "prend moi en photo" ARUCO detected
def photo_simple_aruco_det(context):
    return context["aruco"] == 2

# transition predicats to detect if there is the "prend une photo de groupe" ARUCO detected
def photo_groupe_aruco_det(context):
    return context["aruco"] == 3

# transition predicats to detect if there is the "Eteins-toi" ARUCO detected
def eteindre_aruco_det(context):
    return context["aruco"] == 4

# transition predicats to detect if there is the "Bonjour" ARUCO detected
def bonjour_aruco_det(context):
    return context["aruco"] == 5

# transition action if there is the "Bonjour" ARUCO detected
def bonjour_aruco_action(context):
    context["command"] = "bonjour"
    return context

# transition predicats to detect if there is the "Comment vas-tu" ARUCO detected
def cava_aruco_det(context):
    return context["aruco"] == 6

# transition action if there is the "Comment vas-tu" ARUCO detected
def cava_aruco_action(context):
    context["command"] = "comment vas-tu"
    return context

# transition predicats to detect if there is the "Je vais bien" ARUCO detected
def bien_aruco_det(context):
    return context["aruco"] == 7

# transition action if there is the "Je vais bien" ARUCO detected
def bien_aruco_action(context):
    context["command"] = "je vais bien"
    return context

# transition predicats to detect if there is the "Je vais moyennement bien" ARUCO detected
def moyennement_aruco_det(context):
    return context["aruco"] == 8

# transition action if there is the "Je vais moyennement bien" ARUCO detected
def moyennement_aruco_action(context):
    context["command"] = "je vais moyennement bien"
    return context

# transition predicats to detect if there is the "ça ne va pas trop" ARUCO detected
def pas_trop_aruco_det(context):
    return context["aruco"] == 9

# transition action if there is the "ça ne va pas trop" ARUCO detected
def pas_trop_aruco_action(context):
    context["command"] = "ça ne va pas trop"
    return context

# transition predicats to detect if there is the "Raconte moi une histoire" ARUCO detected
def histoire_aruco_det(context):
    return context["aruco"] == 10

# transition action if there is the "Raconte moi une histoire" ARUCO detected
def histoire_aruco_action(context):
    context["command"] = "raconte moi une histoire"
    return context

# transition predicats to detect if there is the "Au revoir" ARUCO detected
def aurevoir_aruco_det(context):
    return context["aruco"] == 11

# transition action if there is the "Au revoir" ARUCO detected
def aurevoir_aruco_action(context):
    context["command"] = "au revoir"
    return context

# transition predicats to detect if there is the "Tu es mignon" ARUCO detected
def mignon_aruco_det(context):
    return context["aruco"] == 12

# transition action if there is the "Tu es mignon" ARUCO detected
def mignon_aruco_action(context):
    context["command"] = "tu es mignon"
    return context

# transition predicats to detect if there is the "Tu es moche" ARUCO detected
def moche_aruco_det(context):
    return context["aruco"] == 13

# transition action if there is the "Tu es moche" ARUCO detected
def moche_aruco_action(context):
    context["command"] = "tu es moche"
    return context

# transition predicats to detect if there is the "Continue" ARUCO detected
def continue_aruco_det(context):
    return context["aruco"] == 14

# transition action if there is the "Continue" ARUCO detected
def continue_aruco_action(context):
    context["command"] = "continue"
    return context
