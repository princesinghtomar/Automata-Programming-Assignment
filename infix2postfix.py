import sys

OPERATORS = set(['+','*', '(', ')'])
PRIORITY = {'*':2, '+':1,}

def infix_to_postfix(formula):
    stack = [] # only pop when the coming op has priority 
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


if __name__ == '__main__':
    total = input()
    for i in range(int(total)):
        regex = input()
        print(infix_to_postfix(regex))