
from matplotlib.pyplot import get
from datetime import datetime

# This class is made to execute a specified state machine, this is the State machine that creates its own Executor
class Executor:
    # constructor : initialization of the attributes
    def __init__(self, initial_state, context, state_machine) :
        # the executed state machine
        self.state_machine = state_machine 

        # the initial state of the machine
        self.current_state = initial_state

        # Dictionnary : session + state_dico + transition_dico + modules
        self.context = context 

        # the executor imports the functions it will use after
        self.module = __import__(self.state_machine.module)

        # the Executor need the actual time to test if there is a timeout
        self.time = datetime.now() 

    # subfunction to verify if in the actual context, the predicat "pred" is True or False
    def __verif_predicat(self, pred, context):
        # if the state don't have transitions it has the default transition that quit the program
        if(pred == "quit_program"):
            quit()
        # if the transition don't have predicat it is the default predicat which returns always True
        if(pred == "basic_predicat"):
            return True
        else:
            return getattr(self.module, pred)(context)

    # subfunction to take a transition  
    def __take_transition(self, transition, context):
        action = transition["action"]
        # if a transition hasn't an action it is the default action which only returns the context
        if(action == "basic_transition_action"):
            return context
        else: 
            return getattr(self.module, action)(context)

    # subfunction that executes one time the state machine so just does a state action, 
    # tests transitions predicats and returns the next state with the associate context
    def __execute_once(self, state, context = {}):
        save = state
        # search and execute the action associate to the state
        func_name = self.state_machine.state_dico[state]
        context = getattr(self.module, func_name)(context)
        # verify the predicat for all transition and execute the first that returns true
        for T in self.state_machine.transition_dico[state]:
            if self.__verif_predicat(T["pred"], context):
                context = self.__take_transition(T, context)
                if(save != T["next_state"]): 
                    self.time = datetime.now()
                return T["next_state"], context
            else:
                # verif if there is a timeout
                diff = datetime.now() - self.time
                # if no timeout is set it is just "infinite"
                if self.state_machine.outtime[state]["time"] != "infinite":
                    if diff.seconds >= self.state_machine.outtime[state]["time"]:
                        state = self.state_machine.outtime[state]["next_state"]
        # loop on the actual state if none transition predicat is verified
        return state, context

    # main function of the executor, it launches the executor on its state machine
    # if iteration is > 0 for example n, it will execute n states
    # else it will be executed till infinity
    def launch(self, iteration = 0):
        if(iteration <= 0):
            while(True):
                print("state " + self.current_state)
                self.current_state, self.context = self.__execute_once(self.current_state, self.context)
        else:
            for i in range(iteration - 1):
                self.current_state, self.context = self.__execute_once(self.current_state, self.context)
