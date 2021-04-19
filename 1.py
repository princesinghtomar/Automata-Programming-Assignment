import json
import sys
import numpy as np
import itertools as it

def getinput():
    try:
        assert(len(sys.argv)==3)
        with open(sys.argv[1],'r') as kbc:
            input_nfa = json.load(kbc)
        return input_nfa
    except:
        print("Enter Correct Values")
        exit(1)

def printout(DFA):
    with open(sys.argv[2],"w+") as abc:
        json.dump(DFA,abc)

regularExpression = getinput()

precedence = {'+': 1, '#': 2, '*': 3}
start_states = []
NullState = "$"
final_states = []
tstates = 0
NFA = {}
transition_function = []
states = []
letters = []
exp = regularExpression["regex"]
componentList = []
nfrextop = -1
nfrexarra = []
converse_top = -1
converse_array = []
converse_output = []

def convisEmpty():
    global converse_top
    if(converse_top + 1):
        return False
    else:
        return True

def convph(op):
    global converse_top
    converse_top = 1 + converse_top
    converse_array.append(op)

def convisoperand(c):
    if (c>='0' and c<='9') or (c>='a' and c<='z'):
        return True

def convpeek():
    if(len(converse_output)>0):
        return converse_array[-1]
    else:
        return ""

def checkgreat(i):
    global precedence
    try:
        b = precedence[convpeek()]
        a = precedence[i]
        if(a>b):
            return False
        if(a<=b):
            return True
    except KeyError:
        return False    

def convp():
    global converse_top
    if not convisEmpty():
        converse_top = converse_top - 1
        return converse_array.pop()
    else:
        return NullState

def infixToPostfix(exp):
    global converse_output
    for i in range(0,len(exp)):
        if convisoperand(exp[i]):
            converse_output += exp[i]
        elif exp[i] == '(':
            convph(exp[i])
        elif exp[i] == ')':
            while( (not convisEmpty()) and convpeek() != '('):
                converse_output += convp()
            if (not convisEmpty() and convpeek() != '('):
                return -1
            else:
                convp()
        
        elif exp[i] == '*':
            converse_output += exp[i]
        
        else:
            while(not convisEmpty() and checkgreat(exp[i])):
                converse_output += convp()
            convph(exp[i])

    while not convisEmpty():
        converse_output += convp()
    return converse_output

class other:
    def __init__(self,exp):
        self.changed_index = []
        self.changed_regex = ""
        self.exp = exp

    def is_alphabet(self,c):
        if (c>='0' and c<='9') or (c<='z' and c>='a'):
            return True
        else:
            return False

    def add_hash(self):
        for i in range(0,len(self.exp)-1):
            if self.exp[i] is ')' and self.is_alphabet(self.exp[i+1]):
                self.changed_index.append(i)
            if self.is_alphabet(self.exp[i]) and self.exp[i+1] is '(':
                self.changed_index.append(i)
            if self.is_alphabet(self.exp[i]) and self.is_alphabet(self.exp[i+1]):
                self.changed_index.append(i)
            if self.exp[i] is ')' and self.exp[i+1] is '(':
                self.changed_index.append(i)
            if self.exp[i] is '*' and self.is_alphabet(self.exp[i+1]):
                self.changed_index.append(i)
            if self.exp[i] is '*' and self.exp[i+1] is '(':
                self.changed_index.append(i)
        
        self.changed_regex = self.exp
        
        for i in range(0,len(self.changed_index)):
            self.changed_regex = self.changed_regex[:self.changed_index[i]+i+1] + "#" + self.changed_regex[self.changed_index[i]+i+1:]
        return self.changed_regex

class compo:
    def __init__(self,start,end):
        self.start,self.end = start,end
        
    def ENd(self):
        return self.end
    
    def STEN(self):
        return [self.start,self.end]

    def STart(self):
        return self.start

if len(exp) == 0:
    states.append("Q0")
    start_states.append("Q0")
    NFA["states"]=states
    NFA["letters"]=letters
    NFA["transition_matrix"]=transition_function
    NFA["start_states"]=start_states
    NFA["final_states"]=final_states
    printout(NFA)
    exit(1)

o = other(exp)
exp = o.add_hash()
exp = infixToPostfix(exp)
for i in range(0,len(exp)):
    if not o.is_alphabet(exp[i]):
        componentList.append(exp[i])
    else:
        tmp1 = compo([tstates],[tstates+1])
        componentList.append(tmp1)
        states.append(tstates)
        states.append(tstates+1)
        letters.append(exp[i])
        transition_function.append([f"Q{tstates}",f"{exp[i]}",f"Q{tstates+1}"])
        tstates = 2 + tstates

nfrextstates = tstates

def nfrexpk():
    if(len(nfrexarra)>0):
        return nfrexarra[-1]
    else:
        return ""

def nfrexconcat(tmp1,tmp2):
    start2 = tmp2.STart()
    start1 = tmp1.STart()
    end2 = tmp2.ENd()
    end1 = tmp1.ENd()
    [transition_function.append( [f"Q{i}",NullState,f"Q{j}"] ) for j in start2 for i in end1]
    tmp3 = compo(start1,end2)
    return tmp3

def nfrexnempt():
    global nfrextop
    if(nfrextop + 1):
        return False
    else:
        return True

def nfrextempwork(tmp1):
    global nfrextstates
    end1 = tmp1.ENd()
    start1 = tmp1.STart()
    [transition_function.append( [f"Q{i}",NullState,f"Q{j}"] ) for j in start1 for i in end1]
    start3 = [nfrextstates]
    end3 = [1 + nfrextstates]
    [transition_function.append( [f"Q{nfrextstates}",NullState,f"Q{i}"] ) for i in start1 ]
    [transition_function.append( [f"Q{i}",NullState,f"Q{nfrextstates+1}"] ) for i in end1 ]
    transition_function.append( [f"Q{nfrextstates}",NullState,f"Q{nfrextstates+1}"] )
    states.append(nfrextstates)
    states.append(nfrextstates+1)
    nfrextstates = 2 + nfrextstates
    tmp3 = compo(start3,end3)
    return tmp3

def nfrexpp():
    global nfrextop
    if not nfrexnempt():
        nfrextop = nfrextop - 1
        return nfrexarra.pop()
    else:
        return NullState

def nfrexmerge(tmp1,tmp2):
    global nfrextstates
    states.append(nfrextstates)
    end1 = tmp1.ENd()
    end2 = tmp2.ENd()
    start2 = tmp2.STart()
    start1 = tmp1.STart()
    end3 = end1+end2
    [transition_function.append( [f"Q{nfrextstates}",NullState,f"Q{i}"] ) for i in start1]
    [transition_function.append( [f"Q{nfrextstates}",NullState,f"Q{i}"] ) for i in start2]
    start3 = [nfrextstates]
    tmp3 = compo(start3,end3)
    nfrextstates = 1 + nfrextstates
    return tmp3

def nfrexpushit(op):
    global nfrextop
    nfrextop = 1 + nfrextop
    nfrexarra.append(op)

def regToNFA(exp):
    for i in range(0,len(exp)):
        if exp[i] is "#":
            tmp2 = nfrexpk()
            nfrexpp()
            tmp1 = nfrexpk()
            nfrexpp()
            tmp3 = nfrexconcat(tmp1,tmp2)
            nfrexpushit(tmp3)
        elif exp[i] is "*":
            tmp1 = nfrexpk()
            nfrexpp()
            tmp2 = nfrextempwork(tmp1)
            nfrexpushit(tmp2)
        elif exp[i] is "+":
            tmp2 = nfrexpk()
            nfrexpp()
            tmp1 = nfrexpk()
            nfrexpp()
            tmp3 = nfrexmerge(tmp1,tmp2)
            nfrexpushit(tmp3)
        else:
            nfrexpushit(exp[i])
    return nfrexpk()

FinalComponent = regToNFA(componentList)
start_states = FinalComponent.STart()
start_states = [f"Q{start_states[i]}" for i in range(0,len(start_states))]
final_states = FinalComponent.ENd()
final_states = [f"Q{final_states[i]}" for i in range(0,len(final_states))]
letters = [i for i in dict.fromkeys(letters)]

States = []
[States.append(f"Q{states[i]}") for i in range(0,len(states))]

NFA["states"]= States
NFA["letters"]= letters
NFA["transition_matrix"]= transition_function
NFA["start_states"]= start_states
NFA["final_states"]= final_states

printout(NFA)
