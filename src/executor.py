
class Executor:
    def __init__(self, initial_state, context) :
        self.current_state = initial_state
        self.context = context  # Dictionnary : session + state_dico + transition_dico
    
    def launch():
        while(True):    # To take as many transitions as needed
            context['states'][current_state]()    # Execute the current state action
            size = len(context['transitions'][current_state])
            trans_index = -1
            while(True):    # To actively verify if one transition can be taken
                trans_index = (trans_index + 1) % size
                trans = context['transitions'][current_state][trans_index]
                if trans.verif_condition(context) :
                    current_state, context = trans.take_transition(context)
                    break