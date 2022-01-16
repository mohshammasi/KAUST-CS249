import numpy as np
import sys
sys.setrecursionlimit(1500)

def read_input(filename, scoring_file):
    try:
        input_file = open(filename, "r")
        genome1 = input_file.readline().rstrip('\n')
        genome2 = input_file.readline().rstrip('\n')
        genome3 = input_file.readline().rstrip('\n')
        input_file.close()
    except:
        print("Exception caught, file probably doesnt exist")
    return genome1, genome2, genome3

# Edge weights are defined by the scoring matrix and penalties
def MultipleLCS(g1, g2, g3):
    n1 = len(g1)
    n2 = len(g2)
    n3 = len(g3)
    longest_path = np.zeros((n1+1, n2+1, n3+1), dtype=int)
    backtrack = np.zeros((n1+1, n2+1, n3+1), dtype='object')

    # Traffic control
    for i in range(1, n1+1):
        backtrack[i][0][0] = 'D'
    for j in range(1, n2+1):
        backtrack[0][j][0] = 'R'
    for k in range(1, n3+1):
        backtrack[0][0][k] = 'I'

    for i in range(1, n1+1):
        for j in range(1, n2+1):
            backtrack[i][j][0] = 'DR'

    for i in range(1, n1+1):
        for k in range(1, n3+1):
            backtrack[i][0][k] = 'DI'

    for j in range(1, n2+1):
        for k in range(1, n3+1):
            backtrack[0][j][k] = 'RI'

    for i in range(1, n1+1):
        for j in range(1, n2+1):
            for k in range(1, n3+1):
                match = 0
                if g1[i-1] == g2[j-1] and g1[i-1] == g3[k-1]:
                    match = 1

                longest_path[i][j][k] = max(longest_path[i-1][j][k],
                                            longest_path[i][j-1][k], \
                                            longest_path[i][j][k-1], \
                                            longest_path[i-1][j-1][k], \
                                            longest_path[i-1][j][k-1], \
                                            longest_path[i][j-1][k-1], \
                                            longest_path[i-1][j-1][k-1] + match \
                )

                if longest_path[i][j][k] == longest_path[i-1][j][k]:
                    backtrack[i][j][k] = 'D'
                elif longest_path[i][j][k] == longest_path[i][j-1][k]:
                    backtrack[i][j][k] = 'R'
                elif longest_path[i][j][k] == longest_path[i][j][k-1]:
                    backtrack[i][j][k] = 'I'
                elif longest_path[i][j][k] == longest_path[i-1][j-1][k]:
                    backtrack[i][j][k] = 'DR'
                elif longest_path[i][j][k] == longest_path[i-1][j][k-1]:
                    backtrack[i][j][k] = 'DI'
                elif longest_path[i][j][k] == longest_path[i][j-1][k-1]:
                    backtrack[i][j][k] = 'RI'
                elif longest_path[i][j][k] == (longest_path[i-1][j-1][k-1] + match):
                    backtrack[i][j][k] = 'M'
    return backtrack, n1, n2, n3, longest_path[n1][n2][n3]

def OutputMultipleLCS(backtrack, g1, g2, g3, i, j, k):
    # Base case
    if backtrack[i][j][k] == 0:
        return '', '', ''

    # Recursive part
    if backtrack[i][j][k] == 'D':
        s1, s2, s3 = OutputMultipleLCS(backtrack, g1, g2, g3, i-1, j, k)
        s1 += g1[i-1]
        s2 += '-'
        s3 += '-'
        return s1, s2, s3
    elif backtrack[i][j][k] == 'R':
        s1, s2, s3 = OutputMultipleLCS(backtrack, g1, g2, g3, i, j-1, k)
        s1 += '-'
        s2 += g2[j-1]
        s3 += '-'
        return s1, s2, s3
    elif backtrack[i][j][k] == 'I':
        s1, s2, s3 = OutputMultipleLCS(backtrack, g1, g2, g3, i, j, k-1)
        s1 += '-'
        s2 += '-'
        s3 += g3[k-1]
        return s1, s2, s3
    elif backtrack[i][j][k] == 'DR':
        s1, s2, s3 = OutputMultipleLCS(backtrack, g1, g2, g3, i-1, j-1, k)
        s1 += g1[i-1]
        s2 += g2[j-1]
        s3 += '-'
        return s1, s2, s3
    elif backtrack[i][j][k] == 'DI':
        s1, s2, s3 = OutputMultipleLCS(backtrack, g1, g2, g3, i-1, j, k-1)
        s1 += g1[i-1]
        s2 += '-'
        s3 += g3[k-1]
        return s1, s2, s3
    elif backtrack[i][j][k] == 'RI':
        s1, s2, s3 = OutputMultipleLCS(backtrack, g1, g2, g3, i, j-1, k-1)
        s1 += '-'
        s2 += g2[j-1]
        s3 += g3[k-1]
        return s1, s2, s3
    else: # match
        s1, s2, s3 = OutputMultipleLCS(backtrack, g1, g2, g3, i-1, j-1, k-1)
        s1 += g1[i-1]
        s2 += g2[j-1]
        s3 += g3[k-1]
        return s1, s2, s3

def start():
    genome1, genome2, genome3 = read_input("dataset.txt", "BLOSUM62.txt")
    backtrack, n1, n2, n3, score = MultipleLCS(genome1, genome2, genome3)
    s1, s2, s3 = OutputMultipleLCS(backtrack, genome1, genome2, genome3, n1, n2, n3)
    print(score)
    print(s1)
    print(s2)
    print(s3)

if __name__ == '__main__':
    start()
