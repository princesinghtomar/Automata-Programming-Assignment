import sys
import json
import numpy as np
import itertools as it 


arr = ['$','#','+','*']

def printout(DFA):
    with open(sys.argv[2],"w+") as abc:
        json.dump(DFA,abc,indent=4)

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

dfa = getinput()
# made list of dictionary variable so that can change transition_function to transition_matrix
list_of_dict = ["start_states","letters","states","transition_function","final_states"]
gnfa = {}


gnfa[list_of_dict[0]] = 'Start'
gnfa[list_of_dict[4]] = 'End'
gnfa[list_of_dict[2]] = dfa[list_of_dict[2]]
gnfa[list_of_dict[3]] = []
gnfa[list_of_dict[1]] = dfa[list_of_dict[1]]

gnfa[list_of_dict[2]].append('Start')
gnfa[list_of_dict[2]].append('End')

[gnfa[list_of_dict[3]].append(['Start',arr[0],dfa[list_of_dict[0]][i]]) for i in range(0,len(dfa[list_of_dict[0]])) ]
[gnfa[list_of_dict[3]].append([dfa[list_of_dict[4]][i],arr[0],'End']) for i in range(0,len(dfa[list_of_dict[4]])) ]

def transitionFind(delta, s, e):
    for i in range(0,len(delta)):
        if delta[i][0] == s and delta[i][2] == e:
            return delta[i]
    return [0,arr[1],0]

vis = [False]*len(dfa[list_of_dict[3]])

for i in range(len(dfa[list_of_dict[3]])):
    if vis[i]:
        continue
    ini = dfa[list_of_dict[3]][i]
    ex = ''
    ex =ex + str(ini[1])
    for j in range(len(dfa[list_of_dict[3]])):
        fin = dfa[list_of_dict[3]][j]
        if ini[0] is fin[0] and ini[2] is fin[2] and ini[1] is not fin[1]:
            ex = ex + arr[2]
            ex = ex + str(fin[1])
            vis[j] = True
    transition = [ini[0],ex,ini[2]]
    gnfa[list_of_dict[3]].append(transition)
    vis[i] = True
tmp_transition = gnfa[list_of_dict[3]]
for i in gnfa[list_of_dict[2]]:
    if i is 'End':
        continue
    for j in gnfa[list_of_dict[2]]:
        if i==j or j is 'Start':
            continue
        flag = True
        for tr in gnfa[list_of_dict[3]]:
            if tr[0]==i and tr[2]==j:
                flag = False
                break
        if flag:
            transition = [i,arr[1],j]
            tmp_transition.append(transition)
            
gnfa[list_of_dict[3]] = tmp_transition
gnfa[list_of_dict[3]].sort()

while(len(gnfa[list_of_dict[2]])>2):
    select = None
    tmp_transition = []
    for rip in gnfa[list_of_dict[2]]:
        if rip is 'End' or rip is 'Start':
            continue
        elif select == None:
            select=rip
        if rip is select:
            r4 = arr[1]
            r3 = arr[1]
            r2 = arr[1]
            r1 = arr[1]
            ex = ''
            tr = transitionFind(gnfa[list_of_dict[3]],select,select)
            r2 = tr[1]
            r2 = '('+str(r2)+')'+arr[3]
            for i in gnfa[list_of_dict[2]]:
                if i is select or i is 'End':
                    continue
                tr = transitionFind(gnfa[list_of_dict[3]],i,select)
                r1 = tr[1]
                r1 = '('+str(r1)+')'
                for j in gnfa[list_of_dict[2]]:
                    if j is select or i is j or j is 'Start':
                        continue
                    tr = transitionFind(gnfa[list_of_dict[3]],select,j)
                    r3 = tr[1]
                    tr = transitionFind(gnfa[list_of_dict[3]],i,j)
                    r4 = tr[1]
                    r3 = '('+str(r3)+')'
                    if r4 == arr[1]:
                        r4=''
                    else:
                        r4 = arr[2] + '(' + str(r4) + ')'
                    r = r1
                    r = r + r2
                    r = r + r3
                    r = r + r4
                    transition = [i,r,j]
                    tmp_transition.append(transition)
        break
    tmp_state = []
    tmp_transition.sort()
    gnfa[list_of_dict[3]] = tmp_transition
    for i in gnfa[list_of_dict[2]]:
        if i!=select:
            tmp_state.append(i)
    gnfa[list_of_dict[2]] = tmp_state
    
answer = {}
answer['regex'] = gnfa[list_of_dict[3]][0][1]
printout(answer)