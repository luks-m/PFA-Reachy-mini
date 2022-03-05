class State :

    def __init__(self, action):
        self.transitions = {}
        self.action = action

    def fill_transitions(self, transitions):
        self.transitions = transitions

    def play_state(self, context):
        context = self.action(context)
        for T in self.transitions:
            if(T.verif(context) == True):
                return T.play_transition(context)
        return self, context