import numpy as np

def read_input(filename):
    try:
        input_file = open(filename, "r")
        n = input_file.readline().rstrip('\n')
        j = input_file.readline().rstrip('\n')
        d_matrix = []
        for line in input_file:
            d_matrix.append(list(map(int, line.rstrip('\n').split(' ')))) # convert to int
        d_matrix = np.array(d_matrix)
        input_file.close()
    except:
        print("Exception caught, file probably doesnt exist")
    return int(n), int(j), d_matrix

def limb_length(n, j, d_matrix):
    # Make a list of the leaves excluding our leaf j
    leaves = [i for i in range(n) if i != j]

    # List to store computed values of (Dij + Djk - Dik)/2 over all pairs of leaves
    # i and k, iterate 'lC2' times, which is the number of pairs of leaves
    values = []
    l = len(leaves)
    for i in range(0, l):
        for k in range(1, l):
            values.append((d_matrix[leaves[i]][j] + d_matrix[j][leaves[k]] \
                                                - d_matrix[leaves[i]][leaves[k]])/2)
    return int(min(values))

def start():
    n, j, d_matrix = read_input("dataset.txt")
    result = limb_length(n, j, d_matrix)
    print(result)

if __name__ == '__main__':
    start()
