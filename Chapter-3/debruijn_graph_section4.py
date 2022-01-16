import numpy as np
from math import ceil

def read_input(filename):
    try:
        input_file = open(filename, "r")
        k, genome = input_file.read().splitlines()
        input_file.close()
    except:
        print("Exception caught, file probably doesnt exist")
    return int(k), genome

def prefix(pattern):
    return pattern[:-1]

def suffix(pattern):
    return pattern[1:]

def path_graph(patterns):
    # construct a matrix of 0's which is a n x n matrix
    n = len(patterns)
    graph = [[0 for i in range(n)] for row in range(n)]

    for i in range(0, n-1):
        graph[i][i+1] = 1
    return graph

def debruijn_graph(k, genome):
    # Create list of patterns, the 'nodes' of the graph
    patterns = []
    num_of_patterns = len(genome) - k + 2
    for i in range(0, num_of_patterns):
        pattern = genome[i:i+k-1]
        patterns.append(pattern)

    # Construct overlap graph
    path_g= path_graph(patterns)
    #print(np.array(path_g)) # for debug

    # Construct a matrix of 0's which is a n x n matrix of unqiue elements only
    unique_patterns = list(dict.fromkeys(patterns))
    n = len(unique_patterns)
    debruijn_g = [[0 for i in range(n)] for row in range(n)]

    # Get index of each pattern in matrix (without duplicates)
    pattern_index = dict()
    for i, pattern in enumerate(unique_patterns):
        pattern_index[pattern] = i

    #for i, pattern in enumerate(patterns):
    #    for j, pattern_ in enumerate(patterns):
    #        if path_g[i][j] != 0:
    #            idx1 = pattern_index[pattern]
    #            idx2 = pattern_index[pattern_]
    #            debruijn_g[idx1][idx2] += 1

    for i in range(0, len(patterns)-1):
        idx1 = pattern_index[patterns[i]]
        idx2 = pattern_index[patterns[i+1]]
        debruijn_g[idx1][idx2] += 1
    #print(np.array(debruijn_g)) # for debug

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

def start():
    k, genome = read_input("dataset.txt")
    result, graph = debruijn_graph(k, genome)
    try:
        output_file = open("output.txt", "w")
        for string in result:
            output_file.write(string + '\n')
        output_file.close()
        print("Output written successfully to the textfile.")
    except:
        print('File I/O Error...')


if __name__ == '__main__':
    start()
