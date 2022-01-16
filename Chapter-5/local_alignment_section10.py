import numpy as np
from numpy import unravel_index
import sys
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

# Edge weights are defined by the scoring matrix and penalties
def LocalAlignmentBacktrack(g1, g2, scoring_matrix):
    # sigma is indel penalty
    sigma = 5
    n1 = len(g1)
    n2 = len(g2)
    longest_path = np.zeros((n1+1, n2+1), dtype=int)
    backtrack = np.zeros((n1+1, n2+1), dtype='object')

    for i in range(1, n1+1):
        for j in range(1, n2+1):
            match = 0
            u = 0
            if g1[i-1] == g2[j-1]:
                l_pos = letter_position[g1[i-1]]
                #match = scoring_matrix[l_pos][l_pos]
                match = 2
                longest_path[i][j] = max(0, longest_path[i-1][j]-sigma, longest_path[i][j-1]-sigma, \
                longest_path[i-1][j-1] + match)
            else:
                l1_pos = letter_position[g1[i-1]]
                l2_pos = letter_position[g2[j-1]]
                #u = scoring_matrix[l1_pos][l2_pos]
                u = -2
                longest_path[i][j] = max(0, longest_path[i-1][j]-sigma, longest_path[i][j-1]-sigma, \
                longest_path[i-1][j-1] + u)

            if longest_path[i][j] == 0:
                backtrack[i][j] = 'F'
            elif longest_path[i][j] == (longest_path[i-1][j]-sigma):
                backtrack[i][j] = 'D'
            elif longest_path[i][j] == (longest_path[i][j-1]-sigma):
                backtrack[i][j] = 'R'
            elif longest_path[i][j] == (longest_path[i-1][j-1] + match):
                backtrack[i][j] = 'M'
            elif longest_path[i][j] == (longest_path[i-1][j-1] + u):
                backtrack[i][j] = 'MM'

    # Find the largest value in the graph
    largest = np.amax(longest_path)
    i, j = unravel_index(longest_path.argmax(), longest_path.shape)
    return longest_path, backtrack, i, j, longest_path[i][j]

def OutputLocalAlignment(backtrack, g1, g2, i, j):
    # Base case
    if i == 0 or j == 0:
        return '', ''
    elif backtrack[i][j] == 'F':
        return '', ''

    if backtrack[i][j] == 'D':
        s1, s2 = OutputLocalAlignment(backtrack, g1, g2, i-1, j)
        s1 += g1[i-1]
        s2 += '-'
        return s1, s2
    elif backtrack[i][j] == 'R':
        s1, s2 = OutputLocalAlignment(backtrack, g1, g2, i, j-1)
        s1 += '-'
        s2 += g2[j-1]
        return s1, s2
    elif backtrack[i][j] == 'M':
        s1, s2 = OutputLocalAlignment(backtrack, g1, g2, i-1, j-1)
        s1 += g1[i-1]
        s2 += g2[j-1]
        return s1, s2
    else:
        s1, s2 = OutputLocalAlignment(backtrack, g1, g2, i-1, j-1)
        s1 += g1[i-1]
        s2 += g2[j-1]
        return s1, s2

def start():
    genome1, genome2, scoring_matrix = read_input("dataset.txt", "PAM250.txt")
    longest_path, backtrack, i, j, score = LocalAlignmentBacktrack(genome1, genome2, scoring_matrix)
    s1, s2 = OutputLocalAlignment(backtrack, genome1, genome2, i, j)
    print(longest_path)
    print(score)
    print(s1)
    print(s2)

    #try:
    #    output_file = open("output.txt", "w")
    #    output_file.write(str(score) + '\n')
    #    output_file.write(s1 + '\n')
    #    output_file.write(s2 + '\n')
    #    output_file.close()
    #    print("Output written successfully to the textfile.")
    #except:
    #    print('File I/O Error...')

if __name__ == '__main__':
    start()
