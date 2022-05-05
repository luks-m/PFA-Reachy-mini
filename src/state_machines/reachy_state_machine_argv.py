import loader as ld
import sys
sys.path.append("../session")
# import session
import reachy_session as rs

###################################
## Creation of the State Machine ##
###################################

# create the State Machine from the json file specified in arguments
state_machine = ld.load(sys.argv[1])

##########
## Test ##
##########

# create an executor with a true session in order to work with Reachy
executeur = state_machine.create_executor(rs.ReachySession())

# lauch the Executor / State Machine
executeur.launch()