import json
from state_machine_obj import State_Machine
from transition import *

def load(file_path):
    
    # prepare the dictionaries
    states = {}
    transitions = {}
    
    with open(file_path) as file:

        j = json.load(file) 

        # travel all the objects in key "states"
        for i in j["states"].items():

            # filling the states array
            # a state needs an action to be valid 
            if("action" in i[1]):
                states[i[0]] = i[1]["action"]
            #if there is no action the program raises an error
            else:
                raise ValueError("a state needs an action")

            if("transitions" in i[1]):
                transitions[i[0]] = []
                # travel all the transition objects of a state and fill the 
                # associate transition array
                for t in i[1]["transitions"]:
                    # a transition needs a next state
                    if("final" in t):
                        final = t["final"]
                    else:
                        raise ValueError("a transition needs a final state")
                    
                    # if there is no predicat it replaces it with the default one
                    if("predicat" in t):
                        predicat = t["predicat"]
                    else:
                        predicat = "basic_predicat"

                    # if there is no action it replaces it with the default one
                    if("action" in t):
                        action = t["action"]
                    else:
                        action = "basic_transition_action"

                    # fillin the transition dictionary
                    transitions[i[0]].append({"next_state":final, "action":action, "pred":predicat})
            #a state needs at least one transition in our model (no sink state)
            else:
                raise ValueError("a state needs transitions")
    
    initial_state = list(states)[0]
    
    # fill the module argument, it is the file where to find the 
    # implemantation of the transition and state functions
    module = j["module"]

    # initialise the state machine withe the informations of the json file
    return State_Machine(states, transitions, initial_state, module)