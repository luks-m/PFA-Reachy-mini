
class Machine_etat :
    def __init__(self, object_table, initial_state, context) :
        self.obj_tab = object_table
        self.init_state = initial_state
        self.context = context # key-value dictionary
    
    def get_context() :
        return context
    
    def call_state(state) :
        return state.action(context)
    
    def get_initial_state() :
        return init_state

class Transition :
    def __init__(action, next_state) :
        self.next_state = next_state
        self.action = action
    
    def action(context) :
        context = action(context)
        return next_state, context