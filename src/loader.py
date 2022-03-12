import json
from transition import *

def load(file_path):
    with open(file_path) as file:
    
        def basic_predicat(context):
            return True

        def basic_transition_action(context):
            return context

        j = json.load(file) 
        
        inital_state = j.items()
        states = {}
        transitions = {}

        #initialisation of the arrays
        for i in j.items():
            #initialisation of the states array
            if("action" in i[1]):
                states[i[0]] = i[1]["action"]
            else:
                raise ValueError("a state needs an action")

            #initialisation of the transitions array
            if("transitions" in i[1]):
                transitions[i[0]] = []
                for t in i[1]["transitions"]:

                    if("final" in t):
                        final = t["final"]
                    else:
                        raise ValueError("a transition needs a final state")
                    
                    if("predicat" in t):
                        predicat = t["predicat"]
                    else:
                        predicat = "basic_predicat"

                    if("action" in t):
                        action = t[action]
                    else:
                        action = "basic_transition_action"

                    transitions[i[0]].append(Transition(final, action, predicat))
            else:
                raise ValueError("a state needs transitions")
