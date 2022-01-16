import numpy as np
import sys
sys.setrecursionlimit(5000)

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
def GlobalAlignmentBacktrack(g1, g2, scoring_matrix):
    # sigma is indel penalty
    sigma = 4
    n1 = len(g1)
    n2 = len(g2)
    longest_path = np.zeros((n1+1, n2+1), dtype=int)
    backtrack = np.zeros((n1+1, n2+1), dtype='object')

    for i in range(1, n1+1):
        longest_path[i][0] = longest_path[i-1][0] - sigma
    for j in range(1, n2+1):
        longest_path[0][j] = longest_path[0][j-1] - sigma

    for i in range(1, n1+1):
        for j in range(1, n2+1):
            match = 0
            u = 0
            if g1[i-1] == g2[j-1]:
                l_pos = letter_position[g1[i-1]]
                #match = scoring_matrix[l_pos][l_pos]
                match = 1
                longest_path[i][j] = max(longest_path[i-1][j]-sigma, longest_path[i][j-1]-sigma, \
                longest_path[i-1][j-1] + match)
            else:
                l1_pos = letter_position[g1[i-1]]
                l2_pos = letter_position[g2[j-1]]
                #u = scoring_matrix[l1_pos][l2_pos]
                u = -1
                longest_path[i][j] = max(longest_path[i-1][j]-sigma, longest_path[i][j-1]-sigma, \
                longest_path[i-1][j-1] + u)

            if longest_path[i][j] == (longest_path[i-1][j]-sigma):
                backtrack[i][j] = 'D'
            elif longest_path[i][j] == (longest_path[i][j-1]-sigma):
                backtrack[i][j] = 'R'
            elif longest_path[i][j] == (longest_path[i-1][j-1] + match):
                backtrack[i][j] = 'M'
            elif longest_path[i][j] == (longest_path[i-1][j-1] + u):
                backtrack[i][j] = 'MM'
    return longest_path, backtrack, n1, n2, longest_path[n1][n2]

def OutputGlobalAlignment(backtrack, g1, g2, i, j):
    # Base case
    if i == 0 and j == 0:
        return '', ''
    elif i == 0:
        return '-', '' + g2[j-1]
    elif j == 0:
        return '' + g1[i-1], '-'

    # Recursive part
    if backtrack[i][j] == 'D':
        s1, s2 = OutputGlobalAlignment(backtrack, g1, g2, i-1, j)
        s1 += g1[i-1]
        s2 += '-'
        return s1, s2
    elif backtrack[i][j] == 'R':
        s1, s2 = OutputGlobalAlignment(backtrack, g1, g2, i, j-1)
        s1 += '-'
        s2 += g2[j-1]
        return s1, s2
    elif backtrack[i][j] == 'M':
        s1, s2 = OutputGlobalAlignment(backtrack, g1, g2, i-1, j-1)
        s1 += g1[i-1]
        s2 += g2[j-1]
        return s1, s2
    else:
        s1, s2 = OutputGlobalAlignment(backtrack, g1, g2, i-1, j-1)
        s1 += g1[i-1]
        s2 += g2[j-1]
        return s1, s2

def start():
    genome1, genome2, scoring_matrix = read_input("dataset.txt", "BLOSUM62.txt")
    longest_path, backtrack, n1, n2, score = GlobalAlignmentBacktrack(genome1, genome2, scoring_matrix)
    s1, s2 = OutputGlobalAlignment(backtrack, genome1, genome2, n1, n2)
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
