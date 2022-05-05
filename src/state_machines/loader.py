import json
from socket import timeout
from state_machine_obj import State_Machine

# function that take a json file path, open the file and transform it into a State Machine
def load(file_path):
    # prepare the dictionaries
    states = {}
    transitions = {}
    outtime = {}
    # open the file 
    with open(file_path) as file:
        # load the json file with the json librairy
        j = json.load(file) 

        # travel all the objects in key "states"
        for i in j["states"].items():

            # filling the states array
            if("action" in i[1]):
                states[i[0]] = i[1]["action"]
            #if there is no action the program raises an error because a state needs an action
            else:
                raise ValueError("a state needs an action")

            if("transitions" in i[1]):
                transitions[i[0]] = []
                # travel all the transition objects of a state and fill the 
                # associate transition array
                for t in i[1]["transitions"]:
                    # a transition needs a next state
                    if("target" in t):
                        final = t["target"]
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
            #if there is no transition for this state, stop the program after its action
            else:
                transitions[i[0]] = [{"next_state":"quit_program", "action":"quit_program", "pred":"quit_program"}]

            tmp = {}
            # if there is a timeout it specifies it into the State Machine
            if("timeout" in i[1]):
                tmp = {}
                tmp["time"] = i[1]["timeout"]["time"]
                tmp["next_state"] = i[1]["timeout"]["target"]
            #if there is no timeout it specifies it into the State Machine by adding "inifite" instead
            else:
                tmp["time"] = "infinite"
                tmp["next_state"] = ""
            
            # filling the timeout dictionary
            outtime[i[0]] = tmp
    
    # specifiying the initial state of the State Machine
    initial_state = list(states)[0]
    
    # fill the module argument, it is the file where to find the 
    # implementation of the transition predicats, transitions functions and state functions
    module = j["module"]

    # initialise the state machine with the informations of the json file
    return State_Machine(states, transitions, initial_state, outtime, module)