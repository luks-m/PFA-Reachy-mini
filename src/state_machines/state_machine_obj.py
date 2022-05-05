import string

from numpy import character
# from state import *
from executor import *

# a class that represents a Stae Machine with States and Transitions
class State_Machine :
    def __init__(self, state_dico, transition_dico, initial_state, outtime,  module) :
        # states dictionnary with state name as key and state function as value
        self.state_dico = state_dico 

        # transitions dictionnary with state name as key and array of dictionnaries as value (target, predicat, action)
        self.transition_dico = transition_dico 

        # name of the initial state
        self.initial_state = initial_state 

        # path of the python file with the functions implementation
        self.module = module 

        # dictionnary with state name as key and timeout in seconds as value
        self.outtime = outtime   

    # function to create the executor of the State Machine, needed because it is the only way to launch a State  Machine
    def create_executor(self, session):
        context = { "session" : session}
        return Executor(self.initial_state, context, self)