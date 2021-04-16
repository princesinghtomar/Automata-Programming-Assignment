import numpy as np
import json
import sys

global_stack = []  # start and end states and letters or operation
state_count = 0
states = []
letters = []
transition_mat = []
start_state= []
final_state = []
SameState = []

OPERATORS = ['+','*', '(', ')','?']
PRIORITY = {'*':3, '+':2,'?':1}

def infix_to_postfix(formula):
    stack = []
    output = ''
    for ch in formula:
        if ch not in OPERATORS:
            output += ch
        elif ch == '(':
            stack.append('(')
        elif ch == ')':
            while stack and stack[-1] != '(':
                output += stack.pop()
            stack.pop() # pop '('
        else:
            while stack and stack[-1] != '(' and PRIORITY[ch] <= PRIORITY[stack[-1]]:
                output += stack.pop()
            stack.append(ch)
    # leftover
    while stack: output += stack.pop()
    return output

def getinput():
    try:
        assert(len(sys.argv)==1)
        # take input from file
        # with open(sys.argv[1],'r') as kbc:
        #     input_regx = json.load(kbc)   # string format it will be a dictionary remember
        input_regx = {"regex":"(a*b)*+ba+c*"}
        return input_regx["regex"]
    except:
        print("Enter Correct Values")
        exit(1)

def printout(output):
    with open(sys.argv[2],"w") as abc:
        json.dump(a,abc)

def rQState(num):
    return 'Q' + str(num)

def rStartState(state):
    s = []
    for i in state:
        if(i[3] == 0):
            s.append(i)
    return s

def rEndState(state):
    s = []
    for i in state:
        if(i[3] == 1):
            s.append(i)
    return s

def nfa_creation(infix_string):
    for i in infix_string:
        if(i in OPERATORS):
            if(i=='*'):
                # print("Here do i==* Stuff")
                state_temp = []
                popState = stack.pop()
                start_S = rStartState(popState)
                end_S = rEndState(popState)
                transition_mat.append([rQState(state_count),'$',rQState(state_count+1)])
                transition_mat.append([end_S[0],'$',start_S[0]])
                popState.append([rQState(state_count)  , [start_S[0]], i,0])
                popState.append([rQState(state_count+1)  , [1], i,1])
                state_count += 2
                for i in popState:
                    if(i[0] == start_S[0]):
                        i[3] = -1
                    if(i[0] == end_S[0]):
                        i[3] = -1
                states.append(popState)

            elif(i=='+'):
                # print("Here do i==+ Stuff")
                popState1 = stack.pop()
                popState2 = stack.pop()
                start_S1 = rStartState(popState1)
                end_S1 = rEndState(popState1)
                start_S2 = rStartState(popState2)
                end_S2 = rEndState(popState2)
                transition_mat.append([rQState(state_count),'$',start_S1[0]])
                transition_mat.append([rQState(state_count),'$',start_S1[0]])
                transition_mat.append([end_S1[0],'$',rQState(state_count+1)])
                transition_mat.append([end_S2[0],'$',rQState(state_count+1)])
                popState.append([rQState(state_count)  , [start_S[0]], i,0])
                popState.append([rQState(state_count+1)  , [1], i,1])
                state_count += 2
                for i in popState1:
                    if(i[0] == start_S1[0]):
                        i[3] = -1
                    if(i[0] == end_S1[0]):
                        i[3] = -1
                for i in popState2:
                    if(i[0] == start_S2[0]):
                        i[3] = -1
                    if(i[0] == end_S2[0]):
                        i[3] = -1
                states.append(popState)
            elif(i=='?'):
                popState1 = stack.pop()
                popState2 = stack.pop()
                start_S1 = rStartState(popState1)
                end_S1 = rEndState(popState1)
                start_S2 = rStartState(popState2)
                end_S2 = rEndState(popState2)
                transition_mat.append([end_S2[0],'$',start_S1[0]])
                for i in popState1:
                    if(i[0] == start_S1[0]):
                        i[3] = -1
                for i in popState2:
                    if(i[0] == end_S2[0]):
                        i[3] = -1
            else:
                print("No such operation is handled so Fuck off")
                exit(1)
        else:
            if(i not in letter)
                letters.append(i)
            # tuple[0] passed gives number of that state
            # tuple[1] passed gives the states that can be reached from that state in that direction else -1
            # tuple[2] passed gives the character if present else -1
            # tuple[3] passed gives the if its start or end state else -1
            state_temp = []
            transition_mat.append([rQState(state_count),i,rQState(state_count+1)])
            state_temp.append([rQState(state_count)  , [1], i,0])
            state_temp.append([rQState(state_count+1),[-1],-1,1])
            stack.append(state_temp)
            state_count+=2

if __name__ == "__main__":
    regex_string = getinput()
    # print(regex_string)
    infix_string = infix_to_postfix(regex_string)
    # print(infix_string)
    nfa_creation(infix_string)

