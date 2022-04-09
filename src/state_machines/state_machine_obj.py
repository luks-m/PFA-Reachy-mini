import string

from numpy import character
# from state import *
from executor import *

class State_Machine :
    def __init__(self, state_dico, transition_dico, initial_state, module) :
        self.state_dico = state_dico
        self.transition_dico = transition_dico
        self.initial_state = initial_state
        self.module = module
    
    def create_executor(self, session):
        context = {
            "session" : session,
            "states" : self.state_dico,
            "transitions" : self.transition_dico,
            "module" : self.module
        }
        return Executor(self.initial_state, context)
    
    # def get_context(self) :
    #     return self.context
    
    # def __take_default_transition(self, state, context):
    #     for T in self.transition_table[str(state)]:
    #         if(T.default == True):
    #             return T.take_transition(context)
    #     return state, context

    # def call_state(self, state, context) :
    #     print(str(state), context)
    #     context = state.play_state(context)
    #     for T in self.transition_table[str(state)]:
    #         if((T.default == False) and (T.verif_condition(context) == True)):
    #             return T.take_transition(context)
    #     return self.__take_default_transition(state, context)
    
    # def get_initial_state(self) :
    #     return self.initial_statess

