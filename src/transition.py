from state import *

class Transition :
    def __init__(self, next_state, action, pred) :
        self.next_state = next_state
        self.action = action
        self.pred = pred
    
    def verif_condition(self, context):
        return self.pred(context)

    def take_transition(self, context) :
        context = self.action(context)
        return self.next_state, context