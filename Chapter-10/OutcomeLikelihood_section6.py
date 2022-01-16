import numpy as np

def read_input(filename):
    try:
        input_file = open(filename, "r")
        string = input_file.readline().rstrip('\n')
        seperator1 = input_file.readline()
        alphabet = input_file.readline().rstrip('\n').split(" ")
        seperator2 = input_file.readline()
        states = input_file.readline().rstrip('\n').split(" ")
        seperator3 = input_file.readline()
        notneeded1 = input_file.readline() # this is the first line of the matrix

        # Store the transition matrix as a dictionary with the keys being pairs
        # of states, skipping first line of labels
        transitions = dict()
        for i, line in enumerate(input_file):
            if line == '--------\n':
                break
            else:
                line = line.split()[1:]
                for j, value in enumerate(line):
                    key = (states[i], states[j])
                    transitions[key] = float(value)

        notneeded2 = input_file.readline() # this is the first line of the matrix
        # Store the emission matrix as a dictionary with the keys being pairs
        # of states and alphabet, skipping first line of labels
        emissions = dict()
        for i, line in enumerate(input_file):
            line = line.split()[1:]
            for j, value in enumerate(line):
                key = (states[i], alphabet[j])
                emissions[key] = float(value)
    except:
        print("Exception caught, file probably doesnt exist")
    return string, alphabet, states, transitions, emissions

def viterbi_graph(string, alphabet, states, transitions, emissions):
    n = len(states)
    m = len(string)
    forward = np.zeros((n, m), dtype=float)

    # Fill the values of the first column, from the source node
    first_symbol = string[0]
    for i in range(0, n):
        emission_val = emissions[(states[i], first_symbol)]
        forward[i][0] = (1/n) * emission_val # 1/n to break ties equally

    # Fill the rest of the matrix using the recurrance.
    for i in range(1, m):
        for j in range(0, n):
            # Calculate the values from the previous column
            total = 0
            for k in range(0, n):
                emission_val = emissions[(states[j], string[i])]
                transition_val = transitions[(states[k], states[j])]
                weight = transition_val * emission_val
                total += (forward[k][i-1] * weight)
            forward[j][i] = total

    # See which entry in the last column that has the 'optimal' path
    sink = 0
    for i in range(0, n):
        sink += forward[i][m-1]
    return sink

def start():
    string, alphabet, states, transitions, emissions = read_input("dataset.txt")
    outcome_likelihood = viterbi_graph(string, alphabet, states, transitions, emissions)
    print(outcome_likelihood)

if __name__ == '__main__':
    start()
