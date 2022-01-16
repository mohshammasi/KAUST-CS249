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
    optimal_path = np.zeros((n, m), dtype=float)
    backtrack = np.zeros((n, m), dtype=int)

    # Fill the values of the first column, from the source node
    first_symbol = string[0]
    for i in range(0, n):
        emission_val = emissions[(states[i], first_symbol)]
        optimal_path[i][0] = (1/n) * emission_val # 1/n to break ties equally

    # Fill the rest of the matrix using the recurrance.
    for i in range(1, m):
        for j in range(0, n):
            # Calculate the values from the previous column
            max = 0
            max_k = 0
            for k in range(0, n):
                emission_val = emissions[(states[j], string[i])]
                transition_val = transitions[(states[k], states[j])]
                weight = transition_val * emission_val
                value = optimal_path[k][i-1] * weight
                if value > max:
                    max = value
                    max_k = k
            optimal_path[j][i] = max
            backtrack[j][i] = max_k

    # See which entry in the last column that has the 'optimal' path
    sink = 0
    sink_i = 0
    for i in range(0, n):
        if optimal_path[i][m-1] > sink:
            sink = optimal_path[i][m-1]
            sink_i = i

    #print(backtrack)
    #print(sink)
    #print(sink_i)
    return backtrack, sink_i, m-1

# Sometimes the strings are different idk why...
def backtracking(backtrack, states, n, m):
    # Base case
    if m == 0:
        return states[n]

    # Recursive case
    hidden_path = backtracking(backtrack, states, backtrack[n][m], m-1)
    hidden_path += states[backtrack[n][m]]
    return hidden_path

def start():
    string, alphabet, states, transitions, emissions = read_input("dataset.txt")
    backtrack, n, m = viterbi_graph(string, alphabet, states, transitions, emissions)
    hidden_path = backtracking(backtrack, states, n, m)
    print(hidden_path)

if __name__ == '__main__':
    start()
