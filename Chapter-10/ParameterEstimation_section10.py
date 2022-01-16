import numpy as np

def read_input(filename):
    try:
        input_file = open(filename, "r")
        outcome = input_file.readline().rstrip('\n')
        seperator1 = input_file.readline()
        alphabet = input_file.readline().rstrip('\n').split(" ")
        seperator2 = input_file.readline()
        hidden_path = input_file.readline().rstrip('\n')
        seperator3 = input_file.readline()
        states = input_file.readline().rstrip('\n').split(" ")
    except:
        print("Exception caught, file probably doesnt exist")
    return outcome, alphabet, hidden_path, states

def parameter_estimation(string, alphabet, path, states):
    # Create transition matrix
    transition = {}
    for i in states:
         transition[i] = dict((x,0) for x in states)

    # Create emission matrix
    emission = {}
    for i in states:
         emission[i] = dict((x,0) for x in alphabet)
    for i in range(len(path)):
        if i+1<len(path):
            transition[path[i]][path[i+1]] += 1
        emission[path[i]][string[i]] += 1

    # Estimate the transition values using the equation on 10.10.3
    for i in transition:
        total = sum(transition[i].values())
        for j in transition[i]:
            if total>0:
                transition[i][j] = 1.0* transition[i][j]/total
            else:
                transition[i][j] = 1.0/len(states)

    # Estimate the emission values using the equation on 10.10.3
    for i in emission:
        total = sum(emission[i].values())
        for j in emission[i]:
            if total >0:
                emission[i][j] = 1.0*emission[i][j]/total
            else:
                emission[i][j] = 1.0/len(alphabet)
    return transition, emission

def start():
    string, alphabet, hidden_path, states = read_input("dataset.txt")
    transitions, emissions = parameter_estimation(string, alphabet, hidden_path, states)

    # Format the output
    print('  ', end="")
    print(' '.join(states))
    for i in states:
        print(i, end=" ")
        for j in states:
            print(transitions[i][j], end=" ")
        print()

    print('--------')
    print('  ', end="")
    print(' '.join(alphabet))
    for i in states:
        print(i, end=" ")
        for j in alphabet:
            print(emissions[i][j], end=" ")
        print()

if __name__ == '__main__':
    start()
