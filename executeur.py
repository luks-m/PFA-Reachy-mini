class Executeur :

    def __init__(self, state_machine):
        self.state_machine = state_machine
        self.actual_state = state_machine.get_initial_state()

    def __execute_once(self, state, context = {}):
        return self.state_machine.call_state(state, context)

    def execute(self, initial_context = {}, iteration = 0):
        initial_state = self.state_machine.get_initial_state()
        state, context = self.__execute_once(initial_state, initial_context)
        if(iteration == 0):
            while(True):
                state, context = self.__execute_once(state, context)
        else:
            for i in range(iteration - 1):
                state, context = self.__execute_once(state, context)