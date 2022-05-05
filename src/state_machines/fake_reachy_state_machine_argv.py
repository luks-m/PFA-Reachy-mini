import loader as ld
import sys
sys.path.append("../session")
import fake_session as fs

###################################
## Creation of the State Machine ##
###################################

# create the State Machine from the json file specified in arguments
state_machine = ld.load(sys.argv[1])

##########
## Test ##
##########

# create an executor with a fake session in order to work without Reachy
executeur = state_machine.create_executor(fs.FakeSession())

# lauch the Executor / State Machine
executeur.launch()
