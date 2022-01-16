import re, ast


def read_input(filename):
    try:
        input_file = open(filename, "r")
        k, d = input_file.readline().strip().split(" ")
        kdmers = input_file.read().splitlines()
        input_file.close()
    except:
        print("Exception caught, file probably doesnt exist")
    return int(k), int(d), kdmers


############################################################

def genome_path(patterns):
    # Get n and k, helps with debugging as well
    n = len(patterns)
    k = len(patterns[0])

    # Build the string
    genome = patterns[0]
    for i in range(1, n):
        genome += patterns[i][k-1]
    return genome

def string_spelled_by_gapped_patterns(kdmers, k, d):
    # Split the kdmers in to first_patterns and second_patterns
    first_patterns = []
    second_patterns = []
    for kdmer in kdmers:
        kdmer = kdmer[1:-1]
        kdmer = kdmer.split('|')
        first_patterns.append(kdmer[0])
        second_patterns.append(kdmer[1])

    prefix_string = genome_path(first_patterns)
    suffix_string = genome_path(second_patterns)

    for i in range(k+d+1, len(prefix_string)):
        if prefix_string[i] != suffix_string[i-k-d]:
            return 'There is no string spelled by the gapped patterns'
    prefix_string += suffix_string[-(k+d):]
    return prefix_string

################################################################

def prefix(pattern):
    return pattern[:-1]

def suffix(pattern):
    return pattern[1:]

def paired_debruijn_graph(kdmers):
    # Break down each kdmer in patterns and store it as a list of lists
    patterns = []
    for kdmer in kdmers:
        kdmer = kdmer.split('|')
        patterns.append(kdmer)

    # Building our PairedCompositionGraph and Getting all 'Nodes' in the graph
    composition_g = []
    small_patterns = []
    for i in range(0, len(patterns)):
        pair_pattern_prefix = (prefix(patterns[i][0]), prefix(patterns[i][1]))
        pair_pattern_suffix = (suffix(patterns[i][0]), suffix(patterns[i][1]))
        composition_g.append([pair_pattern_prefix, pair_pattern_suffix])
        small_patterns.append(pair_pattern_prefix)
        small_patterns.append(pair_pattern_suffix)

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
                    overlapping_patterns += '(' + unique_patterns[j][0] + '|' + unique_patterns[j][1] + ')'
                    overlapping_patterns += (' ' + '(' + unique_patterns[j][0] + '|' + unique_patterns[j][1] + ')') * (debruijn_g[i][j]-1)
                else:
                    overlapping_patterns += (' ' + '(' + unique_patterns[j][0] + '|' + unique_patterns[j][1] + ')') * (debruijn_g[i][j])
        if len(overlapping_patterns) != 0: # found some compatible patterns
            output.append('(' + unique_patterns[i][0] + '|' + unique_patterns[i][1] + ')' + " -> " + overlapping_patterns)

    return output, debruijn_g

################## PairedDeBruijn Up, Euler path down ###################

def create_path(graph):
    # Create a dict of degrees
    degrees = dict.fromkeys(graph.keys(), 0)
    for node in graph:
        degrees[node] = len(graph[node])
        for node2 in graph:
            if node in graph[node2]:
                degrees[node] += 1

    # Pick the node with odd degree as starting node since its unbalanced
    for node in degrees:
        if (degrees[node] % 2) != 0:
            first_node = node
            break

    # pick first node/edge in graph dictionary
    e = next(iter(graph[first_node]))
    path = first_node + "->" + e
    graph[first_node].remove(e)

    # If there are no more outgoing edges in that node delete the node from dict
    if len(graph[first_node]) == 0:
        del graph[first_node]

    # Add nodes to the path until we find an edge from the final node in the path to the first
    while True:
        path_nodes = path.split('->')
        idx = len(path_nodes)-1
        last_n_in_path = path_nodes[idx]
        try:
            edges = graph[last_n_in_path] # get edges from the final node in the path
            e = next(iter(edges))
            path += "->" + e
            graph[last_n_in_path].remove(e)
            if len(graph[last_n_in_path]) == 0:
                del graph[last_n_in_path]
        except KeyError as e:
            #print('we are probably back at the start so stop here')
            break
    return path, graph


def select_new_node(path, graph):
    try:
        # Create a dict of degrees
        degrees = dict.fromkeys(graph.keys(), 0)
        for node in graph:
            degrees[node] = len(graph[node])
            for node2 in graph:
                if node in graph[node2]:
                    degrees[node] += 1

        # Pick the node with odd degree as starting node since its unbalanced
        i=0
        for node in degrees:
            if (degrees[node] % 2) != 0:
                i+=1
                print('returning ', node)
                return node

        # if the code reaches this point that means that no odds were found
        # grab anything that has an edge to the first thing in our path
        path_nodes = path.split('->')
        first_node = path_nodes[0]
        for node in graph:
            if first_node in graph[node]:
                return node

    except TypeError as e:
        print('no odds found', e)
        print(i)


def expand_back_path(first_node, path, graph):
    # pick first node/edge in graph dictionary
    e = next(iter(graph[first_node]))
    path = first_node + "->" + e
    graph[first_node].remove(e)

    # If there are no more outgoing edges in that node delete the node from dict
    if len(graph[first_node]) == 0:
        del graph[first_node]
    return path, graph

def expand(path, graph):
    # Add nodes to the path until we find an edge from the final node in the path to the first
    while True:
        path_nodes = path.split('->')
        idx = len(path_nodes)-1
        last_n_in_path = path_nodes[idx]
        try:
            edges = graph[last_n_in_path] # get edges from the final node in the path
            e = next(iter(edges))
            path += "->" + e
            graph[last_n_in_path].remove(e)
            if len(graph[last_n_in_path]) == 0:
                del graph[last_n_in_path]
        except KeyError as e:
            #print('we are probably back at the start so change start')
            break
    return path, graph

def brute_expand(path, graph):
    path_nodes = path.split('->')
    length = 0
    for i in range(0, len(path_nodes)):
        if path_nodes[i] in graph:
            e = next(iter(graph[path_nodes[i]]))
            sub_path = path_nodes[i] + "->" + e
            graph[path_nodes[i]].remove(e)
            if len(graph[path_nodes[i]]) == 0:
                del graph[path_nodes[i]]
            expanded_sub_path, graph = expand(sub_path, graph)

            # insert it where it belongs in the path
            path = path[:((2*i)+length)] + expanded_sub_path + path[((2*i)+length)+len(path_nodes[i]):]
            break
        length += len(path_nodes[i])
    return path, graph

def eulerian_path(graph):
    path, graph = create_path(graph)
    while len(graph) != 0:
        path, graph = brute_expand(path, graph)
        new_start = select_new_node(path, graph)
        if new_start is not None:
            expanded_path, graph = expand_back_path(new_start, path, graph)
            expanded_nodes = expanded_path.split('->')
            idx = len(expanded_nodes)-1
            l = len(expanded_nodes[idx])
            path = expanded_path[:-(l)] + path
    return path

#################### Euler path Up, Start down ####################

def start():
    k, d, kdmers = read_input("dataset.txt")
    db, db_graph = paired_debruijn_graph(kdmers)

    # Format db output to be exactly like how eulerpath input
    graph_al = dict()
    for string in db:
        graph_al[string.split('->')[0][:-1]] = set()
        edges = str(string.split('->')[1][1:])
        edges = edges.split(' ')
        for tuple in edges:
            graph_al[string.split('->')[0][:-1]].add(tuple)

    path = eulerian_path(graph_al)
    # Format the path to be exactly like the input for string spelled by gapped patterns
    kdmers = path.split('->')

    result = string_spelled_by_gapped_patterns(kdmers, k, d)
    print(result)


if __name__ == '__main__':
    start()
