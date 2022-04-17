
from matplotlib.pyplot import get
from datetime import datetime

class Executor:
    def __init__(self, initial_state, context, state_machine) :
        self.state_machine = state_machine
        self.current_state = initial_state
        self.context = context  # Dictionnary : session + state_dico + transition_dico + modules
        # the executor imports the functions it will use after
        self.module = __import__(self.state_machine.module)
        self.time = datetime.now()

    def __verif_predicat(self, pred, context):
        if(pred == "quit_program"):
            quit()
        if(pred == "basic_predicat"):
            return True
        else:
            return getattr(self.module, pred)(context)

    def __take_transition(self, transition, context):
        action = transition["action"]
        if(action == "basic_transition_action"):
            return context
        else: 
            return getattr(self.module, action)(context)

    def __execute_once(self, state, context = {}):
        save = state
        # search and execute the action associate to the state
        func_name = self.state_machine.state_dico[state]
        context = getattr(self.module, func_name)(context)
        # verify the predicat for all transition and execute the first that returns true
        for T in self.state_machine.transition_dico[state]:
            if self.__verif_predicat(T["pred"], context):
                context = self.__take_transition(T, context)
                if(save != T["next_state"]): 
                    self.time = datetime.now()
                return T["next_state"], context
            else:
                diff = datetime.now() - self.time
                #print("diff = " + str(diff))
                if self.state_machine.outtime[state]["time"] != "infinite":
                    if diff.seconds >= self.state_machine.outtime[state]["time"]:
                        state = self.state_machine.outtime[state]["next_state"]
        # loop on the actual state if none transition predicat is verified
        return state, context

    def launch(self, iteration = 0):
        if(iteration <= 0):
            while(True):
                print("state " + self.current_state)
                self.current_state, self.context = self.__execute_once(self.current_state, self.context)
        else:
            for i in range(iteration - 1):
                self.current_state, self.context = self.__execute_once(self.current_state, self.context)
   
    # def launch(self):
    #     while(True):    # To take as many transitions as needed
    #         func_name = self.context['states'][str(self.current_state)]
    #         globals(func_name)    # Execute the current state action
    #         size = len(self.context['transitions'][self.current_state])
    #         trans_index = -1
    #         while(True):    # To actively verify if one transition can be taken
    #             trans_index = (trans_index + 1) % size
    #             trans = self.context['transitions'][self.current_state][trans_index]
    #             if trans.verif_condition(self.context) :
    #                 self.current_state, self.context = trans.take_transition(self.context)
    #                 break