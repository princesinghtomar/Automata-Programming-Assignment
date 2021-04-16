import numpy as np
import json
import sys

def getinput():
    try:
        assert(len(sys.argv)==3)
        # take input from file
        with open("./NFA.json",'r') as kbc:
            input_nfa = json.load(kbc)
        return input_nfa
    except:
        print("Enter Correct Values")
        exit(1)

def rstatestring(s):
    st = ""
    if(type(s) is not str):
        for i in range(0,len(s)):
            if(i == 0):
                st += s[i]
            else:
                st += " " + s[i]
        return st

def printout(output):
    with open(sys.argv[2],"w") as abc:
        json.dump(a,abc)

if __name__ == "__main__":
    nfa = getinput()
    lett = {}
    state_dict = {}
    for i in range(0,len(nfa['letters'])):
        lett[nfa['letters'][i]] = i
    states = [['$']]
    table = [['$']]
    for i in lett: table[0].append([])
    for i in nfa['states']:
        states.append([i])
        table.append([i])
        for i in lett: table[-1].append([])
    for i in range(0,len(states)):
        state_dict[rstatestring(states[i])] = i
    print(table)
    print(states)
    print(lett)
    done_states = len(states)
    print(state_dict)
    for i in nfa['transition_function']:
        table[int(i[0][1])+1][lett[i[1]]+1].append(i[2])
    print(table)
    for i in table:
        for j in i:
            if len(j)==0:
                j.append('$')
    print(rstatestring(['Q1','Q0']))
    print(table)
    print(states)
    flag = True
    total_states = len(states)
    while(flag):
        flag = not flag
        for i in table:
            # print(i)
            for j in i:
                # print("i : " + str(i) + " | j :  "+ str(j))
                if(rstatestring(j) in state_dict or rstatestring(j) is None or j == []):
                    # print(rstatestring(j))
                    pass
                else:
                    # print(i,j)
                    total_states += 1
                    state_dict[rstatestring(j)] = len(state_dict)
                    states.append(j)
                    table.append([j])
                    # print(table)
                    for i in lett: table[-1].append([])
        for i in range(done_states,total_states):
            done_states +=1
    print("--")
    print(states)
    print(table)
    print(state_dict)

