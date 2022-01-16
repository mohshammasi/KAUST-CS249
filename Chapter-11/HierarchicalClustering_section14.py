import numpy as np
import itertools
from numpy import unravel_index
from operator import itemgetter

def read_input(filename):
    try:
        input_file = open(filename, "r")
        n = input_file.readline().rstrip('\n')
        d_matrix = []
        for line in input_file:
            d_matrix.append(list(map(float, line.rstrip('\n').split(' '))))
        d_matrix = np.array(d_matrix)
        input_file.close()
    except:
        print("Exception caught, file probably doesnt exist")
    return int(n), d_matrix

# Function to find the distance between 2 clusters
def new_cluster_distance(c_new, c2, D, n, idx1, idx2, idx3, ci_len):
    d_cnew_other = 0
    crossed = False
    for i in range(0, len(c_new)):
        for j in range(0, len(c2)):
            if i > ci_len-1:
                crossed = True

            if crossed:
                d_cnew_other += D[idx2][idx3]
            else:
                d_cnew_other += D[idx1][idx3]
    d_cnew_other = (d_cnew_other/(len(c_new)*len(c2)))
    return d_cnew_other

def hierarchical_clustering(n, D, m):
    clusters = [[i] for i in range(1, n+1)]

    tree = dict()
    for i in range(1, n+1):
        tree.setdefault(i, [])

    # Used to map each node in the tree with its cluster
    map = []
    for i in range(1, n+1):
        map.append(i)

    while len(clusters) > 1:
        # Find the two closest clusters Ci and Cj 
        indices = np.where(D==np.min(D[np.nonzero(D)]))[0] # only get the first ele
        i, j = indices[0], indices[1]
        ci = clusters[i]
        cj = clusters[j]

        #d_ci_cj = cluster_distance(ci, cj, D, i, j)

        # merge new cluster, add new node and edges with weight to the tree
        c = ci + cj
        for e in c:
            print(e, end=" ")
        print()

        # map cluster index from D/clusters to nodes in the tree
        del map[j] # order is important
        del map[i]
        map.insert(i, m)
        m += 1

        # remove the rows and columns of D corresponding to Cj 
        D_copy = D
        D = np.delete(D, j, 1) # col j
        D = np.delete(D, j, 0) # row j
        n = n - 1

        # remove the merged clusters from clusters
        clusters.remove(ci)
        clusters.remove(cj)
        clusters.insert(i, c)

        # iterate through the new column and compute the values
        for k in range(n):
            if i == k:
                D[i][k] = 0 # main diagonal
            else:
                # compute the distance between the new cluster C and other clusters
                c_other = clusters[k]

                if k >= j:
                    d_cnew_other = new_cluster_distance(c, c_other, D_copy, n+1, i, j, k+1, len(ci))
                else:
                    d_cnew_other = new_cluster_distance(c, c_other, D_copy, n+1, i, j, k, len(ci))
                D[i][k] = d_cnew_other # column
                D[k][i] = d_cnew_other # row


if __name__ == '__main__':
    n, d_matrix = read_input("dataset.txt")
    hierarchical_clustering(n, d_matrix, n)
