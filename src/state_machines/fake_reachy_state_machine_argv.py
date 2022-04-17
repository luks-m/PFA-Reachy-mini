import loader as ld
import sys
sys.path.append("../session")
import reachy_session as rs

###################################
## Creation of the State Machine ##
###################################

state_machine = ld.load(sys.argv[1])

##########
## Test ##
##########

executeur = state_machine.create_executor(rs.ReachySession())

#try:
executeur.launch()
#except:
    #S.turn_off()