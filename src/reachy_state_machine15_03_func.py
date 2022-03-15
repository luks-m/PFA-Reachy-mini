import state_machine_obj as stm

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

def allumage_robot_func(context):
    #motor.on
    return context

# state action of Recherche d'Interaction
def recherche_interaction_func(context):
    context["command"] = vr.record_and_transcript()
    return context

# state action of Attente d'Ordre
def attente_ordre_func(context):
    context["command"] = vr.record_and_transcript()
    return context

# state action of Conversation
def conversation_func(context):
    return context

# state action of Bonjour
def bonjour_func(context):
    # speech.text_to_speech(cmd.one_out(cmd.set_bonjour["s"]))
    debug_print("(R) " + cmd.one_out(cmd.set_bonjour["s"]))
    return context

# state action of Au Revoir
def aurevoir_func(context):
    # speech.text_to_speech(cmd.one_out(cmd.set_aurevoir["s"]))
    debug_print("(R) " + cmd.one_out(cmd.set_aurevoir["s"]))
    return context

# state action of Ca va
def cava_func(context):
    # speech.text_to_speech(cmd.one_out(cmd.set_cava["s"]))
    debug_print("(R) " + cmd.one_out(cmd.set_cava["s"]))
    return context

# state action of Gentil
def gentil_func(context):
    # speech.text_to_speech(cmd.one_out(cmd.set_gentil["s"]))
    debug_print("(R) " + cmd.one_out(cmd.set_gentil["s"]))
    return context

# state action of Mechant
def mechant_func(context):
    # speech.text_to_speech(cmd.one_out(cmd.set_mechant["s"]))
    debug_print("(R) " + cmd.one_out(cmd.set_mechant["s"]))
    return context

# state action of Incomprehension
def incomprehension_func(context):
    # speech.text_to_speech(cmd.one_out(cmd.set_incomprehension["s"]))
    debug_print("(R) " + cmd.one_out(cmd.set_incomprehension))
    return context


########################
## Transitions Action ##
########################

# transition action to reset the command key of the context
def reset_command(context):
    context["command"] = ""
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

