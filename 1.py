import numpy as np
import json
import sys

try:
    assert(len(sys.argv)==3)
    # take input from file
    # with open(sys.argv[1],'r') as kbc:
    #     input_regx = json.load(kbc)   # string format it will be a dictionary remember
    input_regx = {"regex":"(a+b)*+ba+c*"}
    
except:
    print("Enter Correct Values")
    exit()



# print in output file
# with open(sys.argv[2],"w") as abc:
#     json.dump(a,abc)