import loader as ld
import sys
sys.path.append("../session")
sys.path.append("..")
import reachy_session as fs

###################################
## Creation of the State Machine ##
###################################

context ={"command" : ""}

state_machine = ld.load("../../assets/json/state_machine_avec_Aruco.json")

##########
## Test ##
##########

# S = rs.ReachySession()
F = fs.ReachySession()

# executeur = state_machine.create_executor(S)
executeur = state_machine.create_executor(F)


executeur.launch()