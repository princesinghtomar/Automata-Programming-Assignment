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

OPERATORS = ['+','*', '(', ')']
PRIORITY = {'*':2, '+':1,}

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
        exit()

def printout(output):
    with open(sys.argv[2],"w") as abc:
        json.dump(a,abc)

def nfa_creation(infix_string):
    for i in infix_string:
        

if __name__ == "__main__":
    regex_string = getinput()
    # print(regex_string)
    infix_string = infix_to_postfix(regex_string)
    # print(infix_string)
    nfa_creation(infix_string)

