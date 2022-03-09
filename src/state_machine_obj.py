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
    
    def call_state(self, state, context) :
        context = state.play_state(context)
        for T in self.transition_table[str(state)]:
            if(T.verif_condition(context) == True):
                return T.take_transition(context)
        return state, context
    
    def get_initial_state(self) :
        return self.initial_state
