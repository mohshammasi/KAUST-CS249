import numpy as np
from math import ceil

def read_input(filename):
    try:
        input_file = open(filename, "r")
        patterns = input_file.read().splitlines()
        input_file.close()
    except:
        print("Exception caught, file probably doesnt exist")
    return patterns

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
                    overlapping_patterns += (', ' + unique_patterns[j]) * (debruijn_g[i][j]-1)
                else:
                    overlapping_patterns += (', ' + unique_patterns[j]) * (debruijn_g[i][j])
        if len(overlapping_patterns) != 0: # found some compatible patterns
            output.append(unique_patterns[i] + " -> " + overlapping_patterns)

    return output, debruijn_g

def maximal_non_branching_paths(graph):
    # Create a dict of degrees
    degrees = dict.fromkeys(graph.keys(), 0)
    for node in graph:
        degrees[node] = len(graph[node])
        for node2 in graph:
            degrees[node] += graph[node2].count(node)
    print(degrees)

    paths = []
    for node in graph:
        if degrees[node] != 2:
            if node in graph:
                for edge in graph[node]:
                    non_branching_path = node + '->' + edge
                    one_in_one_out_node = True
                    while one_in_one_out_node:
                        non_branching_path_nodes = non_branching_path.split('->')
                        idx = len(non_branching_path_nodes)-1
                        last_n_in_path = non_branching_path_nodes[idx]
                        try:
                            edges = graph[last_n_in_path]
                            print(last_n_in_path)
                            print(degrees[last_n_in_path])
                            if len(edges) == 1 and degrees[last_n_in_path] == 2:
                                e = next(iter(edges))
                                non_branching_path += "->" + e
                            else:
                                one_in_one_out_node = False
                        except KeyError as e:
                            break
                    paths.append(non_branching_path)
    return paths

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
    patterns = read_input("dataset.txt")
    db, db_graph = debruijn_graph(patterns)

    # Format db output to be exactly like how eulerpath input
    graph_al = dict()
    for string in db:
        graph_al[string.split(' ')[0]] = list(num for num in string.split('->')[1][1:].split(', '))

    result = maximal_non_branching_paths(graph_al)

    contigs = []
    for string in result:
        string_patterns = string.split('->')
        contig = genome_path(string_patterns)
        contigs.append(contig)

    for contig in contigs:
        print(contig, end=" ")
    print()


if __name__ == '__main__':
    start()
