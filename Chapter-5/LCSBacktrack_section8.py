import numpy as np
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

# In here all edges weights are 0 in the alignment graph
def LCSBacktrack(g1, g2):
    n1 = len(g1)
    n2 = len(g2)
    longest_path = np.zeros((n1+1, n2+1), dtype=int)
    backtrack = np.zeros((n1+1, n2+1), dtype='object')

    for i in range(1, n1+1):
        for j in range(1, n2+1):
            match = 0
            if g1[i-1] == g2[j-1]:
                match = 1
            longest_path[i][j] = max(longest_path[i-1][j], longest_path[i][j-1], \
            longest_path[i-1][j-1] + match)

            if longest_path[i][j] == longest_path[i-1][j]:
                backtrack[i][j] = 'D'
            elif longest_path[i][j] == longest_path[i][j-1]:
                backtrack[i][j] = 'R'
            elif longest_path[i][j] == (longest_path[i-1][j-1] + match):
                backtrack[i][j] = 'M'
    return backtrack, n1, n2

def OutputLCS(backtrack, g1, i, j):
    if i == 0 or j == 0:
        return ''
    if backtrack[i][j] == 'D':
        return OutputLCS(backtrack, g1, i-1, j)
    elif backtrack[i][j] == 'R':
        return OutputLCS(backtrack, g1, i, j-1)
    else:
        return OutputLCS(backtrack, g1, i-1, j-1) + g1[i-1]


def start():
    genome1, genome2 = read_input("dataset.txt")
    backtrack, n1, n2 = LCSBacktrack(genome1, genome2)
    result = OutputLCS(backtrack, genome1, n1, n2)
    print(result)

if __name__ == '__main__':
    start()
