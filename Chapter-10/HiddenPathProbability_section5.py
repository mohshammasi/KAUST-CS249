
def read_input(filename):
    try:
        input_file = open(filename, "r")
        hidden_path = input_file.readline().rstrip('\n')
        seperator1 = input_file.readline()
        states = input_file.readline().rstrip('\n').split(" ")
        seperator2 = input_file.readline()
        notneeded = input_file.readline()

        # Store the transition matrix as a dictionary with the keys being pairs
        # of states, skipping first line of labels
        transitions = dict()
        for i, line in enumerate(input_file):
            line = line.split()[1:]
            for j, value in enumerate(line):
                key = (states[i], states[j])
                transitions[key] = float(value)
    except:
        print("Exception caught, file probably doesnt exist")
    return hidden_path, states, transitions

def probability_of_hidden_path(hidden_path, transitions):
    n = len(hidden_path)
    probability = 0.5 # start with 0.5 because of the 'silent' initial state
    for i in range(0, n-1):
        transition_val = transitions[(hidden_path[i], hidden_path[i+1])]
        probability = probability * transition_val
    return probability

def start():
    hidden_path, states, transitions = read_input("dataset.txt")
    hidden_path_probability = probability_of_hidden_path(hidden_path, transitions)
    print(hidden_path_probability)

if __name__ == '__main__':
    start()
