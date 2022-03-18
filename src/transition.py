class Transition :
    def __init__(self, next_state, action, pred) :
        # string
        self.next_state = next_state
        # string
        self.action = action
        # string
        self.pred = pred
    
    def verif_condition(self, context):
        return globals()[self.pred](context)

    def take_transition(self, context):
        context = globals()[self.action](context)
        return self.next_state, context