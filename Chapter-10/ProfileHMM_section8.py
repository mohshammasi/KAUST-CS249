import numpy as np

def read_input(filename):
    try:
        input_file = open(filename, "r")
        theta = input_file.readline().rstrip('\n')
        theta = float(theta)
        seperator1 = input_file.readline()
        alphabet = input_file.readline().rstrip('\n').split(" ")
        seperator2 = input_file.readline()
        alignment = input_file.read().splitlines()

        # Create the alignment matrix
        n = len(alignment)
        m = len(alignment[0])
        alignment_matrix = np.zeros((n, m), dtype='object')
        for i, string in enumerate(alignment):
            alignment_matrix[i] = list(string)
    except:
        print("Exception caught, file probably doesnt exist")
    return theta, alphabet, alignment_matrix

def seed_alignment(theta, alignment):
    # Transpose the alignment to count the spaces in each column
    transposed_alignment = alignment.T.tolist()
    n = len(transposed_alignment)

    # Use count() to count '-' occurances in each column
    # Very classic while loop iteration because we are deleting elements while iterating
    col_len = len(transposed_alignment[0])
    shaded_columns = set()
    i = 1
    while n-i >= 0:
        spaces_ratio = transposed_alignment[n-i].count('-')/col_len
        if spaces_ratio > theta:
            transposed_alignment.pop(n-i)
            shaded_columns.add(n-i)
        i += 1

    #transposed_alignment = [col for col in transposed_alignment if (col.count('-')/col_len) < theta]
    return np.array(transposed_alignment).T, shaded_columns

def create_idx_map(m):
    index_map = dict()
    index_map['S'] = 0
    index_map['I0'] = 1
    idx = 2
    for i in range(1, m+1):
        index_map['M' + str(i)] = idx
        index_map['D' + str(i)] = idx+1
        index_map['I' + str(i)] = idx+2
        idx += 3
    index_map['E'] = idx
    return index_map

def create_key_map(index_map):
    key_map = dict()
    for key in index_map:
        key_map[index_map[key]] = key
    return key_map

def create_count_map(m):
    count = dict()
    count['S'] = 0
    count['I0'] = 0
    for i in range(1, m+1):
        count['M' + str(i)] = 0
        count['D' + str(i)] = 0
        count['I' + str(i)] = 0
    count['E'] = 0
    return count

S M1


def HMM_matrices(alignment, d, m, alphabet, shaded_columns):
    # Create a 'count' matrix of the alignment which we will 'normalize' to the
    # transition matrix
    transition_m = np.zeros((d, d), dtype=float)
    index_map = create_idx_map(m)
    count = create_count_map(m)
    key_map = create_key_map(index_map)

    # Create the emission matrix
    emission_m = np.zeros((d, len(alphabet)), dtype=float)
    alphabet_dict = dict()
    for i, letter in enumerate(alphabet):
        alphabet_dict[letter] = i

    # Iterate through the strings in the alignment and count the number of times
    # we pass by each node in our HMM, *graph not existent jokes*
    n = len(alignment)
    m = len(alignment[0])
    for i in range(0, n):
        l_idx = 0
        shaded_seen = 0
        for j in range(0, m):
            c = alignment[i][j]

            # Check if the character is in the 'shaded' columns
            if j in shaded_columns:
                if c == '-':
                    shaded_seen += 1
                    if j == m-1:
                        ending_key = 'E'
                        transition_m[l_idx][index_map[ending_key]] += 1
                    continue
                else: # inserted char
                    if j == m-1:
                        key = 'I' + str(j-shaded_seen)
                        ending_key = 'E'
                        transition_m[index_map[key]][index_map[ending_key]] += 1
                    else:
                        key = 'I' + str(j-shaded_seen)
                shaded_seen += 1 # increment the number of shaded colums we encountered

            # Very last letter in the string
            elif j == m-1:
                if c == '-':
                    key = 'D' + str(j-shaded_seen+1)
                else:
                    key = 'M' + str(j-shaded_seen+1)
                ending_key = 'E'
                transition_m[index_map[key]][index_map[ending_key]] += 1

            # Regular cases
            elif c == '-':
                key = 'D' + str(j+1-shaded_seen)
            else:
                key = 'M' + str(j+1-shaded_seen)

            # Increment the count in the 'count-transition' matrix
            idx = index_map[key]
            transition_m[l_idx][idx] += 1
            l_idx = idx
            count[key] += 1

            # Emission matrix
            if c != '-':
                letter_idx = alphabet_dict[c]
                emission_m[l_idx][letter_idx] += 1

    # Divide by the frequency of visiting each state or node for the transition matrix
    count['S'] = n # we pass by the S and E nodes n times for each string in alignment
    count['E'] = n
    for i in range(0, d):
        for j in range(0, d):
            if transition_m[i][j] != 0:
                node = key_map[i]
                if count[node] != 0:
                    transition_m[i][j] = round(transition_m[i][j]/count[node], 3)

    # Divide by the frequency of visiting each state or node for the emission matrix
    for i in range(0, d):
        for j in range(0, len(alphabet)):
            if emission_m[i][j] != 0:
                node = key_map[i]
                if count[node] != 0:
                    emission_m[i][j] = round(emission_m[i][j]/count[node], 3)
    return transition_m, emission_m


def profile_hmm(theta, alphabet, alignment):
    alignment_star, shaded_columns = seed_alignment(theta, alignment)
    m = len(alignment_star[0]) # num of columns
    d = m * 3 + 3 # number of nodes in our HMM, dimension of the matrix

    # Compute the transition matrix
    transition_m, emission_m = HMM_matrices(alignment, d, m, alphabet, shaded_columns)

    # for the sake of formatting
    headers = create_idx_map(m)

    return transition_m, emission_m, headers, d


def start():
    theta, alphabet, alignment = read_input("dataset.txt")
    transitions, emissions, headers, d = profile_hmm(theta, alphabet, alignment)

    # Formatting the damn output
    transitions = transitions.astype('object')
    emissions = emissions.astype('object')

    # Transition matrix first
    headers_with_empty = list(headers.keys())
    headers_with_empty.insert(0, '')
    headers = list(headers.keys())
    result1 = np.insert(transitions, 0, headers, axis=0)
    result1 = np.insert(result1, 0, headers_with_empty, axis=1)
    for i in range(d+1):
        for j in range(d+1):
            print(result1[i][j], end="\t")
        print()

    print('--------')

    # Emissions matrix
    result2 = np.insert(emissions, 0, alphabet, axis=0)
    result2 = np.insert(result2, 0, headers_with_empty, axis=1)
    for i in range(d+1):
        for j in range(len(alphabet)+1):
            print(result2[i][j], end="\t")
        print()



if __name__ == '__main__':
    start()


# The given example
# 0.35
# --------
# A C D E F
# --------
# ACDEFACADF
# AFDA---CCF
# A--EFD-FDC
# ACAEF--A-C
# ADDEFAAADF
