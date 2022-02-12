from distutils.log import debug
import vocal_recognition as vr
import cmd
#import movement as mv

def debug_print(str):
    print("DEBUG : " + str)

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

actual_state = states["RECHERCHE_INTERACTION"]

command = ""

#reachy = ReachySDK(host='localhost')  # Replace with the actual IP

#reachy.head

#for name, joint in reachy.joints.items():
#    print(f'Joint "{name}" position is {joint.present_position} degree.')

#mouv = mv.Mouvement()

def recherche_interaction_func():
    global command
    global actual_state
    while True: 
        command = vr.record_and_transcript()
        if cmd.all_in(command, cmd.set_activation):
            #mouv.content()
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
    if cmd.one_in(command, ["bonjour", "salut"]):
        debug_print("> Bonjour")
    else:
        debug_print("> Je ne connais pas cette commande")
    actual_state = states["ATTENTE_ORDRE"]

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

while True:
    debug_print(str(actual_state))
    state_machine[actual_state]()

