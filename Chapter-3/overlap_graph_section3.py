

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

def overlap_graph(patterns):
    # construct a count matrix of 0's which is a n x n matrix
    n = len(patterns)
    graph = [[0 for i in range(n)] for row in range(n)]

    output = []
    for i, pattern in enumerate(patterns):
        overlapping_patterns = ''
        for j, pattern_ in enumerate(patterns):
            if suffix(pattern) == prefix(pattern_):
                graph[i][j] = 1
                if len(overlapping_patterns) == 0:
                    overlapping_patterns += pattern_
                else:
                    overlapping_patterns += ', ' + pattern_
        if len(overlapping_patterns) != 0: # found some compatible patterns
            output.append(pattern + " -> " + overlapping_patterns)

    return output, graph

def start():
    patterns = read_input("example_ds.txt")
    result, graph = overlap_graph(patterns)
    for string in result:
        print(string)



if __name__ == '__main__':
    start()
