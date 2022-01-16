import numpy as np
from numpy import unravel_index

def read_input(filename):
    try:
        input_file = open(filename, "r")
        genome1 = input_file.readline().rstrip('\n')
        genome2 = input_file.readline().rstrip('\n')
        input_file.close()
    except:
        print("Exception caught, file probably doesnt exist")
    return genome1, genome2

def EditDistance(g1, g2):
    n1 = len(g1)
    n2 = len(g2)
    edit_dist = np.zeros((n1+1, n2+1), dtype=int)

    for i in range(1, n1+1):
        edit_dist[i][0] = i
    for j in range(1, n2+1):
        edit_dist[0][j] = j

    for i in range(1, n1+1):
        for j in range(1, n2+1):
            match = 1
            if g1[i-1] == g2[j-1]:
                match = 0
            edit_dist[i][j] = min(1+edit_dist[i-1][j], 1+edit_dist[i][j-1], match+edit_dist[i-1][j-1])
    return edit_dist[n1][n2]

def start():
    genome1, genome2 = read_input("dataset.txt")
    distance = EditDistance(genome1, genome2)
    print(distance)


if __name__ == '__main__':
    start()
