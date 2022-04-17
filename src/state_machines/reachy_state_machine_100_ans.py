import loader as ld
import sys
sys.path.append("../session")
sys.path.append("..")
import reachy_session as rs

###################################
## Creation of the State Machine ##
###################################

context ={"command" : ""}

state_machine = ld.load("../../assets/json/state_machine_100_ans.json")

##########
## Test ##
##########

executeur = state_machine.create_executor(rs.ReachySession())

executeur.launch()