
class Machine_etat :
    def __init__(self, object_table, initial_state, context) :
        self.obj_tab = object_table
        self.init_state = initial_state
        self.context = context # key-value dictionary
    
    def get_context() :
        return context
    
    def call_state(state, context) :
        return state.action(context)
    
    def get_initial_state() :
        return init_state

class Transition :
    def __init__(next_state, action, cond) :
        self.next_state = next_state
        self.action = action
        self.cond = cond
    
    def verif_condition(context):
        return bool

    def take_transition(context) :
        context = action(context)
        return next_state, context