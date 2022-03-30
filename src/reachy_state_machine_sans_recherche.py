import loader as ld
import session
#import reachy_session as rs
import fake_session as fs

###################################
## Creation of the State Machine ##
###################################

context ={"command" : ""}

state_machine = ld.load("../assets/json/state_machine_sans_recherche.json")

##########
## Test ##
##########

# S = rs.ReachySession()
F = fs.FakeSession()

# executeur = state_machine.create_executor(S)
executeur = state_machine.create_executor(F)


executeur.launch()