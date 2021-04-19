#!/usr/bin/python -tt

# ELEMENTS OF NFA
import json
import sys

f = open(sys.argv[1])
regexExp = json.load(f)


class Conversion:
    def __init__(self, capacity):
        self.top = -1
        self.capacity = capacity
        self.array = []
        self.output = []
        self.precedence = {'+': 1, '#': 2, '*': 3}

    def isEmpty(self):
        return True if self.top == -1 else False

    def peek(self):
        return self.array[-1]

    def pop(self):
        if not self.isEmpty():
            self.top -= 1
            return self.array.pop()
        else:
            return "$"

    def push(self, op):
        self.top += 1
        self.array.append(op)

    def isOperand(self, c):
        if c >= 'a' and c <= 'z':
            return True
        elif c >= '0' and c <= '9':
            return True

    def notGreater(self, i):
        try:
            a = self.precedence[i]
            b = self.precedence[self.peek()]
            return True if a <= b else False
        except KeyError:
            return False

    def infixToPostfix(self, exp):

        for i in exp:
            # print(self.array)
            if self.isOperand(i):
                # print("i",i)
                self.output.append(i)
            elif i == '(':
                self.push(i)
            elif i == ')':
                while((not self.isEmpty()) and
                      self.peek() != '('):
                    a = self.pop()
                    self.output.append(a)
                if (not self.isEmpty() and self.peek() != '('):
                    return -1
                else:
                    self.pop()

            elif i == '*':
                self.output.append(i)

            else:
                while(not self.isEmpty() and self.notGreater(i)):
                    self.output.append(self.pop())
                self.push(i)

        while not self.isEmpty():
            self.output.append(self.pop())
        print(self.output)
        return self.output

# Driver program to test above function


def is_alphabet(c):
    if c >= 'a' and c <= 'z':
        return True
    elif c >= '0' and c <= '9':
        return True


def add_hash(exp):
    changed_index = []
    for i in range(0, len(exp)-1):
        if exp[i] == ')' and is_alphabet(exp[i+1]):
            changed_index.append(i)
        if is_alphabet(exp[i]) and exp[i+1] == '(':
            changed_index.append(i)
        if is_alphabet(exp[i]) and is_alphabet(exp[i+1]):
            changed_index.append(i)
        if exp[i] == ')' and exp[i+1] == '(':
            changed_index.append(i)
        if exp[i] == '*' and is_alphabet(exp[i+1]):
            changed_index.append(i)
        if exp[i] == '*' and exp[i+1] == '(':
            changed_index.append(i)

    changed_regex = exp

    for i in range(0, len(changed_index)):
        changed_regex = changed_regex[:changed_index[i] +
                                      i+1] + "#" + changed_regex[changed_index[i]+i+1:]
    return changed_regex


class component:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def getStart(self):
        return self.start

    def getEnd(self):
        return self.end


states = []
letters = []
transition_function = []
start_states = []
final_states = []
statesUsed = 0
exp = regexExp["regex"]
if exp == "":
    states.append("Q0")
    start_states.append("Q0")
    NFA = {
        "states": states,
        "letters": letters,
        "transition_matrix": transition_function,
        "start_states": start_states,
        "final_states": final_states
    }
    with open(sys.argv[2], "w") as outfile:
        json.dump(NFA, outfile)
    exit(0)

exp = add_hash(exp)
print(exp)
obj = Conversion(len(exp))
exp = obj.infixToPostfix(exp)
componentList = []
for i in exp:
    if is_alphabet(i):
        letters.append(i)
        tmp1 = component([statesUsed], [statesUsed+1])
        states.append(statesUsed)
        states.append(statesUsed+1)
        transition_function.append(
            [f"Q{statesUsed}", f"{i}", f"Q{statesUsed+1}"])
        # transition_function.append((statesUsed,i,statesUsed+1))
        statesUsed += 2
        componentList.append(tmp1)
    else:
        componentList.append(i)

# print(exp)


class RegexToNFA:
    def __init__(self, statesUsed):
        self.top = -1
        # self.capacity = capacity
        self.array = []
        self.output = []
        self.statesUsed = statesUsed

    def isEmpty(self):
        return True if self.top == -1 else False

    def peek(self):
        return self.array[-1]

    def pop(self):
        if not self.isEmpty():
            self.top -= 1
            return self.array.pop()
        else:
            return "$"

    def push(self, op):
        self.top += 1
        self.array.append(op)

    def isOperand(self, ch):
        return ch.isalpha()

    def is_alphabet(c):
        if c >= 'a' and c <= 'z':
            return True
        elif c >= '0' and c <= '9':
            return True

    def concatenation(self, tmp1, tmp2):
        start1 = tmp1.getStart()
        end1 = tmp1.getEnd()
        start2 = tmp2.getStart()
        end2 = tmp2.getEnd()
        for i in end1:
            for j in start2:
                transition_function.append([f"Q{i}", "$", f"Q{j}"])
                # transition_function.append((i,'$',j))
        tmp3 = component(start1, end2)
        return tmp3

    def union(self, tmp1, tmp2):
        states.append(self.statesUsed)
        start1 = tmp1.getStart()
        end1 = tmp1.getEnd()
        start2 = tmp2.getStart()
        end2 = tmp2.getEnd()
        end3 = end1+end2
        for i in start1:
            transition_function.append([f"Q{self.statesUsed}", "$", f"Q{i}"])

            # transition_function.append((statesUsed,'$',i))
        for i in start2:
            transition_function.append([f"Q{self.statesUsed}", "$", f"Q{i}"])

            # transition_function.append((statesUsed,'$',i))
        start3 = [self.statesUsed]
        tmp3 = component(start3, end3)
        self.statesUsed += 1
        return tmp3

    def khneel(self, tmp1):
        start1 = tmp1.getStart()
        end1 = tmp1.getEnd()
        for i in end1:
            for j in start1:
                transition_function.append([f"Q{i}", "$", f"Q{j}"])

        start3 = [self.statesUsed]
        end3 = [self.statesUsed+1]
        for i in start1:
            transition_function.append([f"Q{self.statesUsed}", "$", f"Q{i}"])

        for i in end1:
            transition_function.append([f"Q{i}", "$", f"Q{self.statesUsed+1}"])

        transition_function.append(
            [f"Q{self.statesUsed}", "$", f"Q{self.statesUsed+1}"])

        states.append(self.statesUsed)
        states.append(self.statesUsed+1)
        self.statesUsed += 2

        tmp3 = component(start3, end3)
        return tmp3

    def regToNFA(self, exp):
        for i in exp:
            if i == '#':
                tmp2 = self.peek()
                self.pop()
                tmp1 = self.peek()
                self.pop()
                tmp3 = self.concatenation(tmp1, tmp2)
                self.push(tmp3)
            elif i == '*':
                tmp1 = self.peek()
                self.pop()
                tmp2 = self.khneel(tmp1)
                self.push(tmp2)
            elif i == '+':
                tmp2 = self.peek()
                self.pop()
                tmp1 = self.peek()
                self.pop()
                tmp3 = self.union(tmp1, tmp2)
                self.push(tmp3)
            else:
                self.push(i)
        return self.peek()


# print(componentList)
obj = RegexToNFA(statesUsed)
FinalComponent = obj.regToNFA(componentList)
start_states = FinalComponent.getStart()
final_states = FinalComponent.getEnd()
for i in range(len(start_states)):
    start_states[i] = f"Q{start_states[i]}"
for i in range(len(final_states)):
    final_states[i] = f"Q{final_states[i]}"

letters = list(dict.fromkeys(letters))
# print("letters",letters)

States = []
for i in states:
    States.append(f"Q{i}")
# print("States",States)


# for i in transition_function:
# 	print(i[0],i[1],i[2])

NFA = {
    "states": States,
    "letters": letters,
    "transition_matrix": transition_function,
    "start_states": start_states,
    "final_states": final_states
}

with open(sys.argv[2], "w") as outfile:
    json.dump(NFA, outfile)
