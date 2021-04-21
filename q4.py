import sys
import json
import numpy as np
import itertools as it

# myhill nerode minimization method

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

list_of_dict = ["start_states","letters","states","transition_function","final_states"]

class Dfa:
    def __init__(self, data):
        self.Print = {}
        self.start_state = data[list_of_dict[0]]
        self.letters = data[list_of_dict[1]]
        self.dire = {}
        self.states = data[list_of_dict[2]]
        self.transition_matrix = data[list_of_dict[3]]
        self.final_state = data[list_of_dict[4]]
      # self.letters = data["letters"]
        self.Nonfinal = []
        self.visited = {}

    def seperate_data(self):
        for state in range(0,len(self.states)):
            if self.states[state] not in self.start_state: self.visited[self.states[state]] = False
            else: self.visited[self.states[state]] = True
        for transition in list(self.transition_matrix):
            if self.visited[transition[2]] == False: self.visited[transition[2]] = True
        for state in range(0,len(self.states)):
            if self.states[state] not in self.final_state: self.Nonfinal.append(self.states[state])
        # print(self.Nonfinal, self.final_state, self.visited)

    def MiniMize(self):
        dire = {}
        for state in range(0,len(self.states)):
            for state1 in range(0,len(self.states)):
                if self.visited[self.states[state]] == True and self.visited[self.states[state1]] == True:
                    if (self.states[state] in self.final_state and self.states[state1] in self.Nonfinal) or ((self.states[state1] in self.final_state and self.states[state] in self.Nonfinal)):
                        dire[self.states[state], self.states[state1]] = True
                        dire[self.states[state1], self.states[state]] = True
                    else:
                        dire[self.states[state], self.states[state1]] = False
                        dire[self.states[state1], self.states[state]] = False
        # print(dire)
        # exit(0)
        End = {}
        Start = {}
        while 1:
            # Start={}

            End = dire
            Start = dire.copy()
            # print(hex(id(Start)))

            # print(hex(id(End)))

            for state in range(0,len(self.states)):
                for state1 in range(0,len(self.states)):
                    if self.visited[self.states[state]] == True and self.visited[self.states[state1]] == True:
                        for letter in self.letters:
                            for transition in self.transition_matrix:
                                if transition[0] == self.states[state] and transition[1] == letter: new_state1 = transition[2]
                                if transition[0] == self.states[state1] and transition[1] == letter: new_state2 = transition[2]
                            # print(new_state1, new_state2)
                            if dire[new_state1, new_state2] == True:
                                End[self.states[state], self.states[state1]] = True
                                End[self.states[state1], self.states[state]] = True
            dire = End
            # print("\n")
            # break
            Flag_val = (End == Start)
            if Flag_val:
                # print("yes")
                self.dire = dire
                break

    def New_state(self):
        Combind = []
        for i, j in self.dire:
            flag2 = (j!=i)
            if self.dire[i, j] == 0 and flag2:
                Combind.append(list([i, j]))
        # print(Combind)
        # for state in self.states:
        #     print(state[0])
        Combind.sort()
        # print(Combind)
        New_States = []
        Visited = [False]*len(Combind)
        # Visited = [False for i in len(Combind)]
        for i in range(0,len(Combind)):
            a_set = set(Combind[i])
            if Visited[i] == False:
                for j in range(len(Combind)):
                    b_set = set(Combind[j])
                    if (a_set & b_set) and (Visited[j] == False):
                        a_set = set(list(set(Combind[i]) | set(Combind[j])))
                        Visited[j] = True
                New_States.append(list(a_set))
        for state in self.states:
            if self.visited[state] == True:
                f = False
                for pre in New_States:
                    if state in pre: f = True
                if f == False: New_States.append([(state)])
        self.Print = {}
        self.Print[list_of_dict[2]] = [list(ss) for ss in New_States]
        self.Print[list_of_dict[1]] = list(self.letters)
        self.Print[list_of_dict[3]] = []
        # print(type(New_States))
        # print(type(self.letters))
        for state in range(0,len(New_States)):
            # state=list(list(ss) for ss in New_States[i])
            # print(state)
            for letter in list(self.letters):
                end = New_States[state][0]
                start = New_States[state][0]
                # print(start)
                # print(list(state))
                # print(end)
                for transition in range(0,len(self.transition_matrix)):
                    if self.transition_matrix[transition][0] == start and self.transition_matrix[transition][1] == letter: end = self.transition_matrix[transition][2]
                for next in range(0,len(New_States)):
                    if end in New_States[next]: self.Print[list_of_dict[3]].append([ list(New_States[state]), letter, (New_States[next])])
        # self.Print()
        new_start_state = set([])
        for state in range(0,len(self.start_state)):
            for check in New_States:
                if self.start_state[state] in check: new_start_state.add(tuple(check))
        self.Print[list_of_dict[0]] = list(new_start_state)
        new_final_state = set([])
        for state in range(0,len(self.final_state)):
            # state=[state]
            # print(self.final_state[state])
            for check in New_States:
                if self.final_state[state] in check: new_final_state.add(tuple(check))

        self.Print[list_of_dict[4]] = list(new_final_state)
        # print(self.Print)

        printout(self.Print)

    def Dump_data(self):
        pass


if __name__ == "__main__":
    input_data = getinput()
    dfa = Dfa(input_data)
    dfa.seperate_data()
    dfa.MiniMize()
    dfa.New_state()

