import numpy as np
from numpy import unravel_index
from math import floor
import sys
sys.setrecursionlimit(1500)

def read_input(filename):
    try:
        input_file = open(filename, "r")
        genome1 = input_file.readline().rstrip('\n')
        genome2 = input_file.readline().rstrip('\n')
        input_file.close()
    except:
        print("Exception caught, file probably doesnt exist")
    return genome1, genome2

def FittingAlignmentBacktrack(g1, g2):
    # sigma is indel penalty
    sigma = 5
    n1 = len(g1)
    n2 = len(g2)
    longest_path = np.zeros((n1+1, n2+1), dtype=int)
    backtrack = np.zeros((n1+1, n2+1), dtype='object')

    for i in range(1, n1+1):
        longest_path[i][0] = longest_path[i-1][0] - sigma
    for j in range(1, n2+1):
        longest_path[0][j] = 0

    for i in range(1, n1+1):
        for j in range(1, n2+1):
            match = 0
            u = 0
            if g1[i-1] == g2[j-1]:
                match = 2
                longest_path[i][j] = max(longest_path[i-1][j]-sigma, longest_path[i][j-1]-sigma, \
                longest_path[i-1][j-1] + match)
            else:
                u = -2
                longest_path[i][j] = max(longest_path[i-1][j]-sigma, longest_path[i][j-1]-sigma, \
                longest_path[i-1][j-1] + u) # +/- u depending on values

            if longest_path[i][j] == (longest_path[i-1][j]-sigma):
                backtrack[i][j] = 'D'
            elif longest_path[i][j] == (longest_path[i][j-1]-sigma):
                backtrack[i][j] = 'R'
            elif longest_path[i][j] == (longest_path[i-1][j-1] + match):
                backtrack[i][j] = 'M'
            elif longest_path[i][j] == (longest_path[i-1][j-1] + u): # +/- u depending on values
                backtrack[i][j] = 'MM'

    #print(longest_path)
    # Find the largest value in the graph
    largestInLastRow= np.amax(longest_path[n1])
    idx1 = n1 # switch to n1 when I flip
    idx2 = np.argmax(longest_path[n1])
    return longest_path, backtrack, idx1, idx2, longest_path[idx1][idx2]

def OutputFittingAlignment(backtrack, g1, g2, i, j):
    # Base case
    if i == 0 or j == 0:
        return '', ''

    if backtrack[i][j] == 'D':
        s1, s2 = OutputFittingAlignment(backtrack, g1, g2, i-1, j)
        s1 += g1[i-1]
        s2 += '-'
        return s1, s2
    elif backtrack[i][j] == 'R':
        s1, s2 = OutputFittingAlignment(backtrack, g1, g2, i, j-1)
        s1 += '-'
        s2 += g2[j-1]
        return s1, s2
    elif backtrack[i][j] == 'M':
        s1, s2 = OutputFittingAlignment(backtrack, g1, g2, i-1, j-1)
        s1 += g1[i-1]
        s2 += g2[j-1]
        return s1, s2
    else:
        s1, s2 = OutputFittingAlignment(backtrack, g1, g2, i-1, j-1)
        s1 += g1[i-1]
        s2 += g2[j-1]
        return s1, s2

def start():
    genome1, genome2 = read_input("dataset.txt")
    longest_path, backtrack, idx1, idx2, score = FittingAlignmentBacktrack(genome2, genome1)
    s1, s2 = OutputFittingAlignment(backtrack, genome2, genome1, idx1, idx2)
    print(longest_path)
    print(score)
    print(s2)
    print(s1)


    #try:
    #    output_file = open("output.txt", "w")
    #    output_file.write(str(score) + '\n')
    #    output_file.write(s2 + '\n')
    #    output_file.write(s1 + '\n')
    #    output_file.close()
    #    print("Output written successfully to the textfile.")
    #except:
    #    print('File I/O Error...')

if __name__ == '__main__':
    start()
