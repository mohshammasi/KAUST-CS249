import numpy as np
import sys
from math import floor
sys.setrecursionlimit(1500)

# scoring matrix string
s = 'ACDEFGHIKLMNPQRSTVWY' # string is useless just here for illustration
letter_position = { 'A': 0, 'C': 1, 'D': 2, 'E': 3, 'F': 4, 'G': 5, 'H': 6, 'I': 7, \
'K': 8, 'L': 9, 'M': 10, 'N': 11, 'P': 12, 'Q': 13, 'R': 14, 'S': 15, 'T': 16, 'V': 17, \
'W': 18, 'Y': 19 }

def read_input(filename, scoring_file):
    try:
        input_file = open(filename, "r")
        genome1 = input_file.readline().rstrip('\n')
        genome2 = input_file.readline().rstrip('\n')
        scoring_matrix = np.loadtxt(scoring_file, usecols=range(20))
        input_file.close()
    except:
        print("Exception caught, file probably doesnt exist")
    return genome1, genome2, scoring_matrix

def flip_string(string):
    flipped_string = ''
    n = len(string)
    for i in range(0, n):
        flipped_string += string[n-1-i]
    return flipped_string

# Edge weights are defined by the scoring matrix and penalties
def MiddleEdge(g1, g2, scoring_matrix, toSink=False):
    # sigma is indel penalty
    sigma = 5
    n1 = len(g1)
    n2 = len(g2)
    middle = floor(n1/2)
    longest_path = np.zeros((n2+1, 2), dtype=int)

    for i in range(1, n2+1):
        longest_path[i][0] = longest_path[i-1][0] - sigma
    #print(longest_path)

    edges = []
    middle_col = []
    # j acts as index for g2
    for j in range(1, middle+1):
        for i in range(1, n2+1):
            longest_path[0][1] = longest_path[0][0] - sigma
            match = 0
            u = 0
            if g2[i-1] == g1[j-1]:
                l_pos = letter_position[g2[i-1]]
                match = scoring_matrix[l_pos][l_pos]
                #match = 1
                longest_path[i][1] = max(longest_path[i-1][1]-sigma, longest_path[i][0]-sigma, \
                longest_path[i-1][0] + match)
            else:
                l1_pos = letter_position[g2[i-1]]
                l2_pos = letter_position[g1[j-1]]
                u = scoring_matrix[l1_pos][l2_pos]
                #u = -1
                longest_path[i][1] = max(longest_path[i-1][1]-sigma, longest_path[i][0]-sigma, \
                longest_path[i-1][0] + u)

            # If this is the last column i.e. the middle column store the values and return them
            if j == middle and i == 1:
                middle_col.append(longest_path[0][1]) # also append the first element in the col
                edges.append('R')
            if j == middle:
                middle_col.append(longest_path[i][1])

                # info about incoming edges
                if toSink:
                    if longest_path[i][1] == (longest_path[i-1][0] + match):
                        edges.append('M') # represents diagonals
                    elif longest_path[i][1] == (longest_path[i-1][0] + u):
                        edges.append('M') # represents diagonals
                    elif longest_path[i][1] == (longest_path[i-1][1]-sigma):
                        edges.append('D')
                    elif longest_path[i][1] == (longest_path[i][0]-sigma):
                        edges.append('R')

        longest_path = np.roll(longest_path, 1, axis=1)
        #print(longest_path)
    if toSink:
        return middle_col, edges
    else:
        return middle_col

def start():
    genome1, genome2, scoring_matrix = read_input("dataset.txt", "BLOSUM62.txt")
    _1genome = flip_string(genome1)
    _2genome = flip_string(genome2)

    from_source = MiddleEdge(genome1, genome2, scoring_matrix)
    #print(from_source)
    #print('----')
    to_sink, edges = MiddleEdge(_1genome, _2genome, scoring_matrix, True)
    j = floor(len(genome1)/2)
    print('middle col index: ', j)
    #print(to_sink)


    n = len(from_source)
    length = []
    for i in range(0, n):
        length.append((from_source[i] + to_sink[i]))
    print(length)
    print(max(length))

    # get row index of middle node
    i = length.index(max(length))

    # get middle edge using index and edges list
    edge = edges[i]
    print(edge)
    middle_edge = None
    if edge == 'R':
        middle_edge = (i, j+1)
    elif edge == 'D':
        middle_edge = (i+1, j)
    elif edge == 'M':
        middle_edge = (i+1, j+1)
    print('(' + str(i) + ', ' + str(j) + ') ' + str(middle_edge))


if __name__ == '__main__':
    start()
