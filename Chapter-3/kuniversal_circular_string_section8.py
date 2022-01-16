

def read_input(filename):
    try:
        input_file = open(filename, "r")
        k = input_file.readline().strip('\n')
        input_file.close()
    except:
        print("Exception caught, file probably doesnt exist")
    return int(k)

def binary_strings(k):
    if k == 1:
        return ['0', '1']
    elif k > 1:
        binary_patterns= []
        expand_strings = binary_strings(k-1)
        for string in expand_strings:
            added_zero = string + '0'
            added_one = string + '1'
            binary_patterns.append(added_zero)
            binary_patterns.append(added_one)
        return binary_patterns

########### binary strings generator up, db down #################

def prefix(pattern):
    return pattern[:-1]

def suffix(pattern):
    return pattern[1:]

def debruijn_graph(patterns):
    composition_g = []
    small_patterns = []
    for i in range(0, len(patterns)):
        pattern_prefix = prefix(patterns[i])
        pattern_suffix = suffix(patterns[i])
        composition_g.append([pattern_prefix, pattern_suffix])
        small_patterns.append(pattern_prefix)
        small_patterns.append(pattern_suffix)

    unique_patterns = list(dict.fromkeys(small_patterns))
    n = len(unique_patterns)
    debruijn_g = [[0 for i in range(n)] for row in range(n)]

    # Get index of each pattern in matrix (without duplicates)
    pattern_index = dict()
    for i, pattern in enumerate(unique_patterns):
        pattern_index[pattern] = i

    for i in range(0, len(composition_g)):
        idx1 = pattern_index[composition_g[i][0]]
        idx2 = pattern_index[composition_g[i][1]]
        debruijn_g[idx1][idx2] += 1

    # Loop through the debruijn matrix and format the output strings
    output = []
    for i in range(0, n):
        overlapping_patterns = ''
        for j in range(0, n):
            if debruijn_g[i][j] != 0:
                if len(overlapping_patterns) == 0:
                    overlapping_patterns += unique_patterns[j]
                    overlapping_patterns += (',' + unique_patterns[j]) * (debruijn_g[i][j]-1)
                else:
                    overlapping_patterns += (',' + unique_patterns[j]) * (debruijn_g[i][j])
        if len(overlapping_patterns) != 0: # found some compatible patterns
            output.append(unique_patterns[i] + " -> " + overlapping_patterns)

    return output, debruijn_g

########## debruijn code up, eulerian cycle down ###############

def create_cycle(graph):
    # pick first node/edge in graph dictionary
    first_key = next(iter(graph))
    e = next(iter(graph[first_key])) # get first element in set - "conceptually" sets dont have first elements
    cycle = first_key + "->" + e
    graph[first_key].remove(e)

    # If there are no more outgoing edges in that node delete the node from dict
    if len(graph[first_key]) == 0:
        del graph[first_key]

    # Add nodes to the cycle until we find an edge from the final node in the cycle to the first
    while True:
        cycle_nodes = cycle.split('->')
        idx = len(cycle_nodes)-1
        last_n_in_cycle = cycle_nodes[idx]
        try:
            edges = graph[last_n_in_cycle] # get edges from the final node in the cycle
            e = next(iter(edges))
            cycle += "->" + e
            graph[last_n_in_cycle].remove(e)
            if len(graph[last_n_in_cycle]) == 0:
                del graph[last_n_in_cycle]
        except KeyError as e:
            #print('we are probably back at the start so stop here')
            break
    return cycle, graph


def select_new_node(cycle, unexplored_graph):
    try:
        nodes = cycle.split('->')
        length = 0
        for i in range(0, len(nodes)):
            if nodes[i] in unexplored_graph:
                return nodes[i], ((2*i)+length)
            length += len(nodes[i])
    except TypeError as e:
        print(e)


def expand_cycle(new_start, idx, cycle, unexplored_graph):
    # Rearrange the cycle to use the new start index
    nodes = cycle.split('->')
    length = 0
    for i in range(1, len(nodes)):
        if nodes[i] == new_start:
            break
        length += len(nodes[i])

    cycle = cycle[idx:] + "->" + cycle[idx-((2*(i-1))+length):idx] + new_start

    # Add nodes to the cycle until we find an edge from the final node in the cycle to the first
    while True:
        cycle_nodes = cycle.split('->')
        idx = len(cycle_nodes)-1
        last_n_in_cycle = cycle_nodes[idx]
        try:
            edges = unexplored_graph[last_n_in_cycle] # get edges from the final node in the cycle
            e = next(iter(edges))
            cycle += "->" + e
            unexplored_graph[last_n_in_cycle].remove(e)
            if len(unexplored_graph[last_n_in_cycle]) == 0:
                del unexplored_graph[last_n_in_cycle]
        except KeyError as e:
            #print('we are probably back at the start so change start')
            break
    return cycle, unexplored_graph


def eulerian_cycle(graph):
    cycle, unexplored_graph = create_cycle(graph)
    while len(unexplored_graph) != 0:
        new_start, idx = select_new_node(cycle, unexplored_graph)
        cycle, unexplored_graph = expand_cycle(new_start, idx, cycle, unexplored_graph)
    return cycle

################## genome path down, euler up ############

def genome_path(patterns):
    # Get n and k, helps with debugging as well
    n = len(patterns)
    k = len(patterns[0])

    # Build the string
    genome = patterns[0]
    for i in range(1, n):
        genome += patterns[i][k-1]
    return genome

def start():
    k = read_input("dataset.txt")
    binary_patterns = binary_strings(k)

    db, db_graph = debruijn_graph(binary_patterns)

    # Format db output to be exactly like how euler cycle input
    graph_al = dict()
    for string in db:
        graph_al[string.split(' ')[0]] = set(num for num in string[len(string.split(' ')[0])+4:].split(','))

    # find the cycle in the graph
    cycle = eulerian_cycle(graph_al)

    cycle_pataterns = cycle.split('->')
    result = genome_path(cycle_pataterns)
    cut = 2**k
    print('Uncut string is', result)
    print(result[:cut])
    print(len(result[:cut]))

    try:
        output_file = open("output.txt", "w")
        for string in result:
            output_file.write(string[:cut])
        output_file.close()
        print("Output written successfully to the textfile.")
    except:
        print('File I/O Error...')




if __name__ == '__main__':
    start()
