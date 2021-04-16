string = input()
stack = []
if(len(string) == 0):
    exit()    
operators = ['(',')','*','+','?']
priorty = {"*":5,"+":4,"?":3}

final_string = ""

for i in string():
    if(i in operators):
        # stack.append(i)
        if(len(stack) == 0):
            stack.append(i)
        elif(stack[-1] == '(' and i != ')'):
            stack.append(i)
        elif(i == ')'):
            while(stack.pop()!='(')
                val = stack.pop()
                stack.append(val)
        else:

    else:
        final_string+=i

for i in stack:
    final_string+=i