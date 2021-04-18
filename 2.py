import sys
import json
import numpy as np
import itertools as it

def printout(DFA):
    with open(sys.argv[2],"w+") as abc:
        json.dump(DFA,abc)

def getinput():
    try:
        assert(len(sys.argv)==3)
        # take input from file
        with open(sys.argv[1],'r') as kbc:
            input_nfa = json.load(kbc)
        return input_nfa
    except:
        print("Enter Correct Values")
        exit(1)

def bfs(vis,i,epsilon):
    if vis[i] == 1: return epsilon[i]
    if(vis[i] != 1): vis[i]=1
    for j in range(0,len(transition_matrix[i][k])): epsilon[i] =epsilon + bfs(vis,mapp_states[transition_matrix[i][k][j]],epsilon)
    return epsilon[i]

if __name__ == '__main__':
    NFA = getinput()
    states = NFA["states"].copy()
    letters = NFA["letters"].copy()
    final_letters = letters.copy()
    letters.append('$')
    transition_function = NFA["transition_matrix"].copy()
    start_states = NFA["start_states"].copy()
    end_states = NFA["final_states"].copy()
    epsilon = []
    transition_matrix = []
    final_start_state = []
    final_states = []
    final_end_states = []
    final_start_state = final_start_state + start_states 
    mapp_letters = {}
    mapp_states = {}
    final_end_states = []
    final_transition_function = []
    for r in range(0,len(states)+1):
        combinations_list = [list(ele) for ele in list(it.combinations(states, r))]
        final_states = final_states + combinations_list
    for i in range(0,len(states)): 
        tmp = []
        mapp_states[states[i]] = i
        for j in range(0,len(letters)): tmp.append([])
        transition_matrix.append(tmp)
    for i in range(0,len(letters)): mapp_letters[letters[i]] = i
    k = mapp_letters['$']
    for i in range(0,len(transition_function)):
        input_letter = mapp_letters[transition_function[i][1]]
        initial_state = mapp_states[transition_function[i][0]]
        transition_matrix[initial_state][input_letter].append(transition_function[i][2])
    for i in range(0,len(states)): epsilon.append(transition_matrix[i][k])
    vis = list(it.repeat(0,len(states)))
    for i in range(0,len(states)): epsilon[mapp_states[states[i]]] = bfs(vis,mapp_states[states[i]],epsilon)
    for i in range(0,len(epsilon)): epsilon[i] = list(dict.fromkeys(epsilon[i]))
    for i in range(0,len(states)):
        transition_matrix[mapp_states[states[i]]][k] = transition_matrix[mapp_states[states[i]]][k] + epsilon[mapp_states[states[i]]]
        transition_matrix[mapp_states[states[i]]][k] = list(dict.fromkeys(transition_matrix[mapp_states[states[i]]][k]))
    flen = len(final_states)
    flett = len(final_letters)
    for i in range(0,flen):
        for t in range(0,flett):
            ans = []
            tt=mapp_letters[final_letters[t]]
            for j in final_states[i]:
                ans = ans + transition_matrix[mapp_states[j]][tt]
                for ll in transition_matrix[mapp_states[j]][tt]: ans = ans + epsilon[mapp_states[ll]]
                for h in epsilon[ mapp_states[j] ]:
                    ans=ans + transition_matrix[mapp_states[h]][tt]
                    for kk in transition_matrix[mapp_states[h]][tt]: ans=ans + epsilon[mapp_states[kk]]
            ans = list(dict.fromkeys(ans))
            final_transition_function.append([final_states[i],f"{final_letters[t]}",ans])
    for i in range(0,len(start_states)): final_start_state += epsilon[mapp_states[start_states[i]]]
    total_fstate = len(final_states)
    total_estate = len(end_states)
    for i in range(0,total_fstate):
        for j in range(0,total_estate):
            if end_states[j] in final_states[i]:
                final_end_states.append(final_states[i])
                break
    DFA = {
        "states":final_states,
        "letters":final_letters,
        "transition_function":final_transition_function,
        "start_states": [final_start_state],
        "final_states": final_end_states
    }            
    printout(DFA)
