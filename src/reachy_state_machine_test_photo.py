from email.policy import default
import loader as ld
import session
import reachy_session as rs

###################################
## Creation of the State Machine ##
###################################

context ={"command" : ""}

state_machine = ld.load("../assets/json/state_machine_test_photo.json")

##########
## Test ##
##########

S = rs.ReachySession()

executeur = state_machine.create_executor(S)

try:
    executeur.launch()
except:
    S.turn_off()