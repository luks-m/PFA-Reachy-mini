import loader as ld
import session
import reachy_session as rs

###################################
## Creation of the State Machine ##
###################################

context ={"command" : ""}

state_machine = ld.load("../assets/json/state_machine_sans_recherche.json")

##########
## Test ##
##########

S = rs.ReachySession()

executeur = state_machine.create_executor(S)

executeur.launch()