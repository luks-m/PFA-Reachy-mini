from state import *
from transition import * 

class State_Machine :
    def __init__(self, object_table, initial_state, context) :
        self.states = object_table
        self.initial_state = initial_state
        self.context = context # key-value dictionary
    
    def get_context(self) :
        return self.context
    
    def call_state(self, state, context) :
        return state.play_state(context)
    
    def get_initial_state(self) :
        return self.initial_state
