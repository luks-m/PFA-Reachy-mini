import vocal_recognition as vr
import cmd
import movement as mv
from reachy_sdk import ReachySDK
import time
import speech_synthesis as speech
import session as ses
import mock

def debug_print(str):
    print("DEBUG : " + str)


reachy = Mock()
r = Session(reachy)


# reachy = ReachySDK(host='localhost')  # Replace with the actual IP

# reachy.head
# for name, joint in reachy.joints.items():
#     print(f'Joint "{name}" position is {joint.present_position} degree.')

# r = mv.Movement(reachy)
# r.motor_on()
# r.head.look_at(1, 0, 0, 2)
# #t = time.time()

command = ""

##################################
####    Main State Machine    ####
##################################

states = {  "RECHERCHE_INTERACTION": 0,
            "INCITATION_INTERACTION": 1,
            "RECHERCHE_PERSONNE" : 2,
            "ATTENTE_ORDRE" : 3,
            "TRAITEMENT_ORDRE" : 4,
            # états concernants la conversation
            "CONVERSATION" : 5,
            # états concernants la photographie
            "PHOTO" : 6,
            "PHOTO_SIMPLE" : 7,
            "PHOTO_GROUPE" : 8,
            "PRISE_PHOTO" : 9,
}

INITIAL_STATE = states["RECHERCHE_INTERACTION"]

actual_state = INITIAL_STATE

def recherche_interaction_func():
    global command
    global actual_state
    while True: 
        command = vr.record_and_transcript()
        if cmd.all_in(command, cmd.set_activation):
            actual_state = states["ATTENTE_ORDRE"]
            break

def incitation_interaction_func():
    return True

def recherche_personne_func():
    return True

def attente_ordre_func():
    global command
    global actual_state
    while True: 
        command = vr.record_and_transcript()
        if(command == "ERROR"):
            debug_print("> Je n'ai pas compris ce que vous venez de dire")
        else:
            actual_state = states["TRAITEMENT_ORDRE"]
            break

def traitement_ordre_func():
    global command
    global actual_state
    if cmd.one_in(command, cmd.set_photo):
        actual_state = states["PHOTO"]
    else:
        actual_state = states["CONVERSATION"]

def conversation_func():
    global command
    global actual_state
    if(cmd.one_in(command, cmd.set_bonjour["e"])):
        conv_bonjour_func()
        return
    if(cmd.one_in(command, cmd.set_cava["e"])):
        conv_cava_func()
        return
    if(cmd.one_in(command, cmd.set_gentil["e"])):
        conv_gentil_func()
        return
    if(cmd.one_in(command, cmd.set_mechant["e"])):
        conv_mechant_func()
        return
    if(cmd.one_in(command, cmd.set_aurevoir["e"])):
        conv_bonjour_func()
        return
    else:
        conv_incomprehension_func()
        return

def photo_func():
    global command
    global actual_state
    if cmd.one_in(command, cmd.set_simple):
        actual_state = states["PHOTO_SIMPLE"]
    elif cmd.one_in(command, cmd.set_groupe):
        actual_state = states["PHOTO_GROUPE"]
    else:
        debug_print("> Veuillez spécifier si vous voulez une photo simple ou de groupe")
        command = vr.record_and_transcript()
        if cmd.one_in(command, cmd.set_simple):
            actual_state = states["PHOTO_SIMPLE"]
        elif cmd.one_in(command, cmd.set_groupe):
            actual_state = states["PHOTO_GROUPE"]
        else: 
            debug_print("> Vous n'avez pas spécifié, je reviens au menu de base")
            actual_state = states["ATTENTE_ORDRE"]

def photo_simple_func():
    global command
    global actual_state
    debug_print("> Je cadre la photo simple")
    actual_state = states["PRISE_PHOTO"]

def photo_groupe_func():
    global command
    global actual_state
    debug_print("> Je cadre la photo de groupe")
    actual_state = states["PRISE_PHOTO"]

def prise_photo_func():
    global command
    global actual_state
    debug_print("> Ok tout est bon")
    debug_print("> 3 ...")
    debug_print("> 2 ...")
    debug_print("> 1 ...")
    debug_print("> CLIIIC")
    actual_state = states["ATTENTE_ORDRE"]

state_machine = {   states["RECHERCHE_INTERACTION"] : recherche_interaction_func,
                    states["INCITATION_INTERACTION"] : incitation_interaction_func,
                    states["RECHERCHE_PERSONNE"] : recherche_personne_func,
                    states["ATTENTE_ORDRE"] : attente_ordre_func,
                    states["TRAITEMENT_ORDRE"] : traitement_ordre_func,
                    states["CONVERSATION"] : conversation_func,
                    states["PHOTO"] : photo_func,
                    states["PHOTO_SIMPLE"] : photo_simple_func,
                    states["PHOTO_GROUPE"] : photo_groupe_func,
                    states["PRISE_PHOTO"] : prise_photo_func  
}

##########################################
####    Conversation Sub Functions    ####
##########################################

def say_one_in_conv_set(set):
    speech.text_to_speech(cmd.one_out(set["s"])) #to say

def conv_bonjour_func():
    global actual_state
    say_one_in_conv_set(cmd.set_bonjour)
    actual_state = states["ATTENTE_ORDRE"]

def conv_cava_func():
    global actual_state
    say_one_in_conv_set(cmd.set_cava)
    actual_state = states["ATTENTE_ORDRE"]
    
def conv_gentil_func():
    global actual_state
    say_one_in_conv_set(cmd.set_gentil)
    r.happy()
    actual_state = states["ATTENTE_ORDRE"]

def conv_mechant_func():
    global actual_state
    say_one_in_conv_set(cmd.set_mechant)
    r.sad()
    actual_state = states["ATTENTE_ORDRE"]

def conv_aurevoir_func():
    global actual_state
    say_one_in_conv_set(cmd.set_aurevoir)
    actual_state = states["RECHERCHE_INTERACTION"]

def conv_incomprehension_func():
    global actual_state
    #say_one_in_conv_set(cmd.set_incomprehension)
    actual_state = states["ATTENTE_ORDRE"]

#############################
####    Main Function    ####
#############################

# while True:
for i in range(2) :
    print("i =", i)
    debug_print(str(actual_state))
    state_machine[actual_state]()

r.motor_off()