
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
        seperator4 = input_file.readline()
        notneeded = input_file.readline() # this is the first line of the matrix

        # Store the transition matrix as a dictionary with the keys being pairs
        # of states, skipping first line of labels
        emissions = dict()
        for i, line in enumerate(input_file):
            line = line.split()[1:]
            for j, value in enumerate(line):
                key = (states[i], alphabet[j])
                emissions[key] = float(value)
    except:
        print("Exception caught, file probably doesnt exist")
    return outcome, alphabet, hidden_path, states, emissions

def probability_of_outcome_given_path(outcome, hidden_path, emissions):
    n = len(outcome)
    probability = 1
    for i in range(0, n):
        emission_val = emissions[(hidden_path[i], outcome[i])]
        probability *= emission_val
    return probability

def start():
    outcome, alphabet, hidden_path, states, emissions = read_input("dataset.txt")
    outcome_probability = probability_of_outcome_given_path(outcome, hidden_path, emissions)
    print(outcome_probability)

if __name__ == '__main__':
    start()
