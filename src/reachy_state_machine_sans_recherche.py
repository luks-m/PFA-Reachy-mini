import loader as ld

###################################
## Creation of the State Machine ##
###################################

context ={"command" : ""}

state_machine = ld.load("../assets/json/state_machine_sans_recherche.json")

##########
## Test ##
##########

executeur = state_machine.create_executor(0)

executeur.launch()