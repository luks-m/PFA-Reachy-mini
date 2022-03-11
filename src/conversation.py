import cmd
import movement as mv

robot = None

def init_robot(reachy):
    global robot
    robot = reachy

def detect_say_move(str, set_name):
    if(cmd.one_in(str, set_name["e"])):
        print(cmd.one_out(set_name["s"])) #todo, change to speech
        return True
    return False

# the state machine conversation function
def conversation(command):
    #bonjour
    if(detect_say_move(command, cmd.set_bonjour)):
        return 
    #ça va
    if(detect_say_move(command, cmd.set_cava)):
        return
    #gentil
    if(detect_say_move(command, cmd.set_gentil)):
        robot.happy()
        return
    #méchant
    if(detect_say_move(command, cmd.set_mechant)):
        robot.sad()
        return
    else:
        #todo replace the print by a "say" function and a "move" function
        print(cmd.one_in(cmd.set_incomprehension))
        return