# return True if one of the words in set is in str, False otherwise
def one_in(str, set):
    for i in set:
        if i in str:
            return True
    return False

# return True if n of the words in set are in str, False otherwise
def n_in(str, set, n):
    r = 0
    for i in set:
        if i in str:
            r += 1
    return r >= n

# return True if all the words in set are in str, False otherwise
def all_in(str, set):
    for i in set:
        if i not in str:
            return False
    return True

def how_many_in(str, set):
    r = 0
    for i in set:
        if i in str:
            r += 1
    return r

# open the file "file", search for a command "cmd" :
#       - if it exists return the array of associate keywords
#       - otherwise return an error 
def transcript_cmd(file, cmd):
    f = open(file)
    data = f.readlines()
    for i in range(len(data)):
        if "cmd : " in data[i]:
            #extraction of the command name without "cmd : ", without spaces and without "\n"
            command_name = data[i][6:].replace("\n", "").replace(" ", "")
            if(cmd == command_name):
                #extraction of the command keywords
                keywords = []
                for j in range(i+1, len(data)):
                    #if the command list is ended
                    if "..." in data[j]:
                        return keywords
                    #if the command lists don't fit the format
                    if "." not in data[j]:
                        return "ERROR"
                    #add the keyword without the ". ", without spaces and without "\n"
                    keywords.append(data[j][2:].replace("\n", "").replace(" ", ""))
    return "ERROR"

set_activation = transcript_cmd("./cmd/state_cmd.txt", "activation")

set_photo = transcript_cmd("./cmd/state_cmd.txt", "photo")

set_simple = transcript_cmd("./cmd/state_cmd.txt", "simple")

set_groupe = transcript_cmd("./cmd/state_cmd.txt", "groupe")

