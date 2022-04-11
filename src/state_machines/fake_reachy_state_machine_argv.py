import loader as ld
import sys
sys.path.append("../session")
# import session
import fake_session as fs

###################################
## Creation of the State Machine ##
###################################

state_machine = ld.load(sys.argv[1])

##########
## Test ##
##########

executeur = state_machine.create_executor(fs.FakeSession())

#try:
executeur.launch()
#except:
    #S.turn_off()