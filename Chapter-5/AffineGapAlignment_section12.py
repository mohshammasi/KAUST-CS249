import numpy as np
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
def AffineGapAlignmentBacktrack(g1, g2, scoring_matrix):
    # gap opening penalty (sigma) and gap extension penalty (epsilon)
    sigma = 11
    epsilon = 1
    n1 = len(g1)
    n2 = len(g2)
    lower = np.zeros((n1+1, n2+1), dtype=int)
    middle = np.zeros((n1+1, n2+1), dtype=int)
    upper = np.zeros((n1+1, n2+1), dtype=int)
    backtrack = np.zeros((n1+1, n2+1), dtype='object')
    backtrack_lower = np.zeros((n1+1, n2+1), dtype='object')
    backtrack_upper = np.zeros((n1+1, n2+1), dtype='object')

    middle[0][1] = -sigma # start of gap penalty
    middle[1][0] = -sigma
    for i in range(2, n1+1):
        middle[i][0] = middle[i-1][0] - epsilon
    for j in range(2, n2+1):
        middle[0][j] = middle[0][j-1] - epsilon

    # Lower has only vertical edges with weights -epsilon to represent gap extensions in g1
    for i in range(0, n2+1):
        lower[0][i] = -999999
    lower[1][0] = -sigma # start of gap penalty
    for i in range(2, n1+1):
        lower[i][0] = lower[i-1][0] - epsilon

    # Upper has only horizontal edges with weights -epsilon to represent gap extensions in g2
    for i in range(0, n1+1):
        upper[i][0] = -999999
    upper[0][1] = -sigma # start of gap penalty
    for i in range(2, n2+1):
        upper[0][i] = upper[0][i-1] - epsilon

    # add indels until we reach our start point from either side, like traffic control
    # since both alignment strings must be of same length at the end
    # if we lign them partially we will just pad until they are equal
    for i in range(1, n1+1):
        backtrack[i][0] = 'D'
    for j in range(1, n2+1):
        backtrack[0][j] = 'R'

    for i in range(1, n1+1):
        for j in range(1, n2+1):

            lower[i][j] = max(lower[i-1][j]-epsilon, middle[i-1][j]-sigma)
            upper[i][j] = max(upper[i][j-1]-epsilon, middle[i][j-1]-sigma)

            match = 0
            u = 0
            if g1[i-1] == g2[j-1]:
                l_pos = letter_position[g1[i-1]]
                match = scoring_matrix[l_pos][l_pos]
                middle[i][j] = max(lower[i][j], middle[i-1][j-1] + match, upper[i][j])
            else:
                l1_pos = letter_position[g1[i-1]]
                l2_pos = letter_position[g2[j-1]]
                u = scoring_matrix[l1_pos][l2_pos]
                middle[i][j] = max(lower[i][j], middle[i-1][j-1] + u, upper[i][j])

            if middle[i][j] == lower[i][j]:
                backtrack[i][j] = 'L'
                for k in range(i, -1, -1):
                        if lower[k-1][j] == (lower[k][j] + epsilon):
                            backtrack_lower[k][j] = 'D'
                        else:
                            backtrack_lower[k][j] = 'RE' # return to midd
                            break
            elif middle[i][j] == (middle[i-1][j-1] + match):
                backtrack[i][j] = 'M'
            elif middle[i][j] == (middle[i-1][j-1] + u): # remember to flip sign if using scoring matrix
                backtrack[i][j] = 'MM'
            elif middle[i][j] == upper[i][j]:
                backtrack[i][j] = 'U'
                backtrack_upper[i][j] = 'R'
                for k in range(j, -1, -1):
                    if upper[i][k-1] == (upper[i][k] + epsilon):
                        backtrack_upper[i][k] = 'R'
                    else:
                        backtrack_upper[i][k] = 'RE'
                        break

    #print('Lower: ')
    #print(lower)
    #print('Middle: ')
    #print(middle)
    #print('Upper: ')
    #print(upper)
    #print('Backtracking: ')
    #print(backtrack)
    #print(backtrack_lower)
    #print(backtrack_upper)
    return backtrack, backtrack_lower, backtrack_upper, n1, n2, middle[n1][n2]

def OutputAffineGapAlignment(backtrack, backtrack_lower, backtrack_upper, g1, g2, i, j):
    # Base case
    if backtrack[i][j] == 0:
        return '', ''

    # Recursive part
    if backtrack[i][j] == 'L': # Go to lower backtrack matrix
        s1, s2 = BackTrackLowernUpper(backtrack, backtrack_lower, backtrack_upper, g1, g2, i, j)
        return s1, s2
    elif backtrack[i][j] == 'U': # Go to upper backtrack matrix
        s1, s2 = BackTrackLowernUpper(backtrack, backtrack_lower, backtrack_upper, g1, g2, i, j)
        return s1, s2
    elif backtrack[i][j] == 'D':
        s1, s2 = OutputAffineGapAlignment(backtrack, backtrack_lower, backtrack_upper, g1, g2, i-1, j)
        s1 += g1[i-1]
        s2 += '-'
        return s1, s2
    elif backtrack[i][j] == 'R':
        s1, s2 = OutputAffineGapAlignment(backtrack, backtrack_lower, backtrack_upper, g1, g2, i, j-1)
        s1 += '-'
        s2 += g2[j-1]
        return s1, s2
    else:
        s1, s2 = OutputAffineGapAlignment(backtrack, backtrack_lower, backtrack_upper, g1, g2, i-1, j-1)
        s1 += g1[i-1]
        s2 += g2[j-1]
        return s1, s2

def BackTrackLowernUpper(backtrack, backtrack_lower, backtrack_upper, g1, g2, i, j):
    if backtrack_lower[i][j] == 'D':
        s1, s2 = BackTrackLowernUpper(backtrack, backtrack_lower, backtrack_upper, g1, g2, i-1, j)
        s1 += g1[i-1]
        s2 += '-'
        return s1, s2
    elif backtrack_lower[i][j] == 'RE': # means return to middle backtrack matrix
        s1, s2 = OutputAffineGapAlignment(backtrack, backtrack_lower, backtrack_upper, g1, g2, i-1, j)
        s1 += g1[i-1]
        s2 += '-'
        return s1, s2
    elif backtrack_upper[i][j] == 'R':
        s1, s2 = BackTrackLowernUpper(backtrack, backtrack_lower, backtrack_upper, g1, g2, i, j-1)
        s1 += '-'
        s2 += g2[j-1]
        return s1, s2
    elif backtrack_upper[i][j] == 'RE':
        s1, s2 = OutputAffineGapAlignment(backtrack, backtrack_lower, backtrack_upper, g1, g2, i, j-1)
        s1 += '-'
        s2 += g2[j-1]
        return s1, s2

def start():
    genome1, genome2, scoring_matrix = read_input("dataset.txt", "BLOSUM62.txt")
    if len(genome1) < len(genome2):
        backtrack, backtrack_lower, backtrack_upper, n1, n2, score = AffineGapAlignmentBacktrack(genome2, genome1, scoring_matrix)
        s1, s2 = OutputAffineGapAlignment(backtrack, backtrack_lower, backtrack_upper, genome2, genome1, n1, n2)
        print(score)
        print(s2)
        print(s1)
    else:
        backtrack, backtrack_lower, backtrack_upper, n1, n2, score = AffineGapAlignmentBacktrack(genome1, genome2, scoring_matrix)
        s1, s2 = OutputAffineGapAlignment(backtrack, backtrack_lower, backtrack_upper, genome1, genome2, n1, n2)
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
