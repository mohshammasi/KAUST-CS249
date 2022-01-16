import numpy as np

def read_input(filename):
    try:
        input_file = open(filename, "r")
        outcome = input_file.readline().rstrip('\n')
        seperator1 = input_file.readline()
        theta, pseudocount = input_file.readline().rstrip('\n').split(" ")
        theta = float(theta)
        pseudocount = float(pseudocount)
        seperator2 = input_file.readline()
        alphabet = input_file.readline().rstrip('\n').split(" ")
        seperator3 = input_file.readline()
        alignment = input_file.read().splitlines()

        # Create the alignment matrix
        n = len(alignment)
        m = len(alignment[0])
        alignment_matrix = np.zeros((n, m), dtype='object')
        for i, string in enumerate(alignment):
            alignment_matrix[i] = list(string)
    except:
        print("Exception caught, file probably doesnt exist")
    return outcome, theta, pseudocount, alphabet, alignment_matrix

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

def pseudocounts_and_normalisation(transition_m, emission_m, pseudocount, d, m, alphabet):
    # Get the list of nodes
    nodes_to_idx = create_idx_map(m)
    nodes = list(nodes_to_idx.keys())
    idx_to_node = create_key_map(nodes_to_idx)

    # Simply by observing the matrices we can infer the pattern for the edges
    # between the nodes
    # add the edges outgoing from the nodes 'S' and 'I0' independently, special case
    edges = []
    source_i = nodes_to_idx['S']
    i0_i = nodes_to_idx['I0']
    edges.append((source_i, i0_i))
    edges.append((i0_i, i0_i))
    m1_i = nodes_to_idx['M1']
    edges.append((source_i, m1_i))
    edges.append((i0_i, m1_i))
    d1_i = nodes_to_idx['D1']
    edges.append((source_i, d1_i))
    edges.append((i0_i, d1_i))

    for i in range(2, d):
        start = idx_to_node[i]
        start_i = nodes_to_idx[start]

        if i == d-1:
            break
        elif i >= (d-4):
            k = 1
        else:
            k = 0

        if start[0] == 'M':
            for j in range(i+2, i+5-k):
                end = idx_to_node[j]
                end_i = nodes_to_idx[end]
                edges.append((start_i, end_i))
        elif start[0] == 'D':
            for j in range(i+1, i+4-k):
                end = idx_to_node[j]
                end_i = nodes_to_idx[end]
                edges.append((start_i, end_i))
        elif start[0] == 'I':
            for j in range(i, i+3-k):
                end = idx_to_node[j]
                end_i = nodes_to_idx[end]
                edges.append((start_i, end_i))

    # add pseudocounts to the edges cells and normalise
    for edge in edges:
        transition_m[edge[0]][edge[1]] += pseudocount
    row_sums = transition_m.sum(axis=1)
    for i in range(d):
        for j in range(d):
            if transition_m[i][j] != 0:
                transition_m[i][j] = round(transition_m[i][j]/row_sums[i], 3)

    # Emission matrix pseudocount and normalisati
    # If the row in the matrix is an insertion row or a row that has emission
    # values then we add pseudocounts to the entire row
    row_sums = emission_m.sum(axis=1)
    for i in range(d):
        start = idx_to_node[i]
        if start[0] == 'I':
            emission_m[i] += pseudocount
        elif row_sums[i] > 0:
            emission_m[i] += pseudocount
    row_sums = emission_m.sum(axis=1)
    for i in range(d):
        for j in range(len(alphabet)):
            if emission_m[i][j] != 0:
                emission_m[i][j] = round(emission_m[i][j]/row_sums[i], 3)
    return transition_m, emission_m


def profile_hmm_with_pseudocounts(theta, alphabet, alignment, pseudocount):
    alignment_star, shaded_columns = seed_alignment(theta, alignment)
    m = len(alignment_star[0]) # num of columns
    d = m * 3 + 3 # number of nodes in our HMM, dimension of the matrix

    # Compute the transition matrix
    transition_m, emission_m = HMM_matrices(alignment, d, m, alphabet, shaded_columns)

    # Add the pseudocounts to both matrices and normalise
    transition_m, emission_m = pseudocounts_and_normalisation(transition_m, emission_m, pseudocount, d, m, alphabet)

    # for the sake of formatting
    headers = create_idx_map(m)

    return transition_m, emission_m, headers, d

##################################################################################


def sequence_alignment(string, theta, pseudocount, alphabet, alignment):
    transitions, emissions, headers, d = profile_hmm_with_pseudocounts(theta, alphabet, alignment, pseudocount)
    rows = int(len(headers)/3)-1

    alphabet_dict = dict()
    for i, letter in enumerate(alphabet):
        alphabet_dict[letter] = i

    # The extra column in both the 'I' and 'M' matrices is useless, just to make
    # it possible to loop through all the matrices at once to fill them
    I = [[0 for i in range(len(string)+1)] for i in range(rows)]
    M = [[0 for i in range(len(string)+1)] for i in range(rows)]
    D = [[0 for i in range(len(string)+1)] for i in range(rows)]

    # Fill in the first row 'I0' of the viterbi graph
    for i in range(1, len(string)+1):
        if i == 1:
            I[0][i] = max(transitions[headers['S']][headers['I0']]*emissions[headers['I0']][alphabet_dict[string[i-1]]],
                        transitions[headers['S']][headers['I0']]*emissions[headers['I0']][alphabet_dict[string[i-1]]],
                        transitions[headers['S']][headers['I0']]*emissions[headers['I0']][alphabet_dict[string[i-1]]])
        else:
            I[0][i] = max(I[0][i-1]*transitions[headers['I0']][headers['I0']]*emissions[headers['I0']][alphabet_dict[string[i-1]]],
                        I[0][i-1]*transitions[headers['I0']][headers['I0']]*emissions[headers['I0']][alphabet_dict[string[i-1]]],
                        I[0][i-1]*transitions[headers['I0']][headers['I0']]*emissions[headers['I0']][alphabet_dict[string[i-1]]])

    # Fill in the first column of silent states 'the Ds' of the viterbi graph, ignoring col pos 0,0
    for i in range(1, rows):
        if i == 1:
            D[i][0] = transitions[headers['S']][headers['D'+str(i)]]
        else:
            D[i][0] = D[i-1][0]*transitions[headers['D'+str(i-1)]][headers['D'+str(i)]]

    # Fill in the remaining 'I', 'M' and 'D' of the viterbi graph
    for j in range(1, rows):
        for i in range(1, len(string)+1):
            if (j-1 == 0) and i == 1: # first col and first row, from initial state
                M[j][i] = max(transitions[headers['S']][headers['M1']]*emissions[headers['M'+str(j)]][alphabet_dict[string[i-1]]],
                            transitions[headers['S']][headers['M1']]*emissions[headers['M'+str(j)]][alphabet_dict[string[i-1]]],
                            transitions[headers['S']][headers['M1']]*emissions[headers['M'+str(j)]][alphabet_dict[string[i-1]]])
                D[j][i] = I[j-1][i]*transitions[headers['I'+str(j-1)]][headers['D'+str(j)]]
                I[j][i] = max(D[j][i-1]*transitions[headers['D'+str(j)]][headers['I'+str(j)]]*emissions[headers['I'+str(j)]][alphabet_dict[string[i-1]]],
                            M[j][i-1]*transitions[headers['M'+str(j)]][headers['I'+str(j)]]*emissions[headers['I'+str(j)]][alphabet_dict[string[i-1]]],
                            I[j][i-1]*transitions[headers['I'+str(j)]][headers['I'+str(j)]]*emissions[headers['I'+str(j)]][alphabet_dict[string[i-1]]])
            elif j-1 == 0: # first row
                M[j][i] = I[j-1][i-1]*transitions[headers['I'+str(j-1)]][headers['M'+str(j)]]*emissions[headers['M'+str(j)]][alphabet_dict[string[i-1]]]
                D[j][i] = I[j-1][i]*transitions[headers['I'+str(j-1)]][headers['D'+str(j)]]
                I[j][i] = max(D[j][i-1]*transitions[headers['D'+str(j)]][headers['I'+str(j)]]*emissions[headers['I'+str(j)]][alphabet_dict[string[i-1]]],
                            M[j][i-1]*transitions[headers['M'+str(j)]][headers['I'+str(j)]]*emissions[headers['I'+str(j)]][alphabet_dict[string[i-1]]],
                            I[j][i-1]*transitions[headers['I'+str(j)]][headers['I'+str(j)]]*emissions[headers['I'+str(j)]][alphabet_dict[string[i-1]]])
            else:
                M[j][i] = max(I[j-1][i-1]*transitions[headers['I'+str(j-1)]][headers['M'+str(j)]]*emissions[headers['M'+str(j)]][alphabet_dict[string[i-1]]],
                            D[j-1][i-1]*transitions[headers['D'+str(j-1)]][headers['M'+str(j)]]*emissions[headers['M'+str(j)]][alphabet_dict[string[i-1]]],
                            M[j-1][i-1]*transitions[headers['M'+str(j-1)]][headers['M'+str(j)]]*emissions[headers['M'+str(j)]][alphabet_dict[string[i-1]]])
                D[j][i] = max(I[j-1][i]*transitions[headers['I'+str(j-1)]][headers['D'+str(j)]],
                            M[j-1][i]*transitions[headers['M'+str(j-1)]][headers['D'+str(j)]],
                            D[j-1][i]*transitions[headers['D'+str(j-1)]][headers['D'+str(j)]])
                I[j][i] = max(I[j][i-1]*transitions[headers['I'+str(j)]][headers['I'+str(j)]]*emissions[headers['I'+str(j)]][alphabet_dict[string[i-1]]],
                            D[j][i-1]*transitions[headers['D'+str(j)]][headers['I'+str(j)]]*emissions[headers['I'+str(j)]][alphabet_dict[string[i-1]]],
                            M[j][i-1]*transitions[headers['M'+str(j)]][headers['I'+str(j)]]*emissions[headers['I'+str(j)]][alphabet_dict[string[i-1]]])

    # Backtracking to obtain the optimal hidden path
    res = []
    state = rows-1
    seq = len(string)
    max_value = 0
    max_state = ('', 0, 0)
    next_state = 'E'
    while seq>0:
        if I[state][seq] > max_value:
            max_value =  I[state][seq]*transitions[headers['I'+str(state)]][headers[next_state]]
            max_state = ('I', state, seq)
        if M[state][seq] > max_value:
            max_value =  M[state][seq]*transitions[headers['M'+str(state)]][headers[next_state]]
            max_state = ('M', state, seq)
        if D[state][seq] > max_value:
            max_value =  D[state][seq]*transitions[headers['D'+str(state)]][headers[next_state]]
            max_state = ('D', state, seq)

        res.insert(0, max_state[0]+str(max_state[1]))
        next_state = res[0]
        if max_state[0] == 'I':
            seq -= 1
        if max_state[0] == 'D':
            state -= 1
        if max_state[0] == 'M':
            seq -= 1
            state -= 1
    return res


def start():
    string, theta, pseudocount, alphabet, alignment = read_input("dataset.txt")
    sequence = sequence_alignment(string, theta, pseudocount, alphabet, alignment)
    for s in sequence:
        print(s, end=" ")
    print()

if __name__ == '__main__':
    start()
