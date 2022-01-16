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

def start():
    patterns = read_input("dataset.txt")
    result, graph = debruijn_graph(patterns)
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
