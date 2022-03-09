import string

from numpy import character
from state import *
from transition import * 

class State_Machine :
    def __init__(self, states, transition_table, initial_state, context) :
        self.states = states
        self.transition_table = transition_table
        self.initial_state = initial_state
        self.context = context # key-value dictionary
    
    def get_context(self) :
        return self.context
    
    def __take_default_transition(self, state, context):
        for T in self.transition_table[str(state)]:
            if(T.default == True):
                return T.take_transition(context)
        return state, context

    def call_state(self, state, context) :
        print(str(state), context)
        context = state.play_state(context)
        for T in self.transition_table[str(state)]:
            if((T.default == False) and (T.verif_condition(context) == True)):
                return T.take_transition(context)
        return self.__take_default_transition(state, context)
    
    def get_initial_state(self) :
        return self.initial_state

