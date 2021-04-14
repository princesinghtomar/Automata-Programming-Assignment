import numpy as np
import json
import sys

stack = []  # start and end states and letters or operation
state_count = 0
states = []
letters = []
transition_mat = []
start_state= []
final_state = []
operation = '\()+*'

try:
    assert(len(sys.argv)==1)
    # take input from file
    # with open(sys.argv[1],'r') as kbc:
    #     input_regx = json.load(kbc)   # string format it will be a dictionary remember
    input_regx = {"regex":"(a+b)*+ba+c*"}
    regex_string = input_regx["regex"]
except:
    print("Enter Correct Values")
    exit()

for i in regex_string:
    val = operation.find(i)
    if(val > 0):
        print("f")
        # do operation
    else:
        # new letter is introduced
        letters.append(i)
        # tuple[0] passed gives the states that can be reached from that state in that direction else -1
        # tuple[1] passed gives the character if present else -1
        # tuple[2] passed gives the if its start or end state else -1
        state_temp = []
        state_temp.append([(1,i,0)])
        state_temp.append([(-1,-1,1)])
        stack.append(state_temp)

print(stack)

# print in output file
# with open(sys.argv[2],"w") as abc:
#     json.dump(a,abc)