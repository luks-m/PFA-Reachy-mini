from state import *

class Transition :
    def __init__(self, next_state, action, cond) :
        self.next_state = next_state
        self.action = action
        self.verif = cond
    
    def verif_condition(self, context):
        return self.verif(context)

    def take_transition(self, context) :
        context = self.action(context)
        return self.next_state, context