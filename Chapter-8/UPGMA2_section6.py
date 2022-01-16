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
            d_matrix.append(list(map(int, line.rstrip('\n').split(' ')))) # convert to int
        d_matrix = np.array(d_matrix)
        d_matrix = d_matrix.astype('float64')
        input_file.close()
    except:
        print("Exception caught, file probably doesnt exist")
    return int(n), d_matrix

# Function to find the distance between 2 clusters
def cluster_distance(ci, cj, D, idx1, idx2):
    d_ci_cj = 0
    for ei in ci:
        for ej in cj:
            d_ci_cj += D[idx1][idx2]
    d_ci_cj = (d_ci_cj/(len(ci)*len(cj)))
    return d_ci_cj

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

def UPGMA(n, D, m):
    clusters = [[i] for i in range(n)]

    tree = dict()
    for i in range(n):
        tree.setdefault(i, [])

    age = dict()
    for node in tree:
        age[node] = 0

    # Used to map each node in the tree with its cluster
    map = []
    for i in range(n):
        map.append(i)

    while len(clusters) > 1:
        # Find the two closest clusters Ci and Cj 
        indices = np.where(D==np.min(D[np.nonzero(D)]))[0] # only get the first ele
        i, j = indices[0], indices[1]
        ci = clusters[i]
        cj = clusters[j]

        d_ci_cj = cluster_distance(ci, cj, D, i, j)

        # merge new cluster, add new node and edges with weight to the tree
        c = ci + cj
        weight_i = round(((d_ci_cj/2) - age[map[i]]), 2)
        weight_j = round(((d_ci_cj/2) - age[map[j]]), 2)
        tree.setdefault(m, []).append((map[i], "%.2f" % weight_i))
        tree.setdefault(m, []).append((map[j], "%.2f" % weight_j))

        # map cluster index from D/clusters to nodes in the tree
        del map[j] # order is important
        del map[i]
        map.insert(i, m)

        # new age
        age[m] = (d_ci_cj/2)
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
        increase_k = False
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
    return tree

# Take an adjacency list of a tree with undirected edges and formats it to a directed
# edges list of string to output
def directed_edges_adjaceny_list(tree):
    directed_tree = []
    edges = dict()
    for node in sorted(tree):
        for e in tree[node]:
            # Get node at the end of the edge and the weight
            node2, weight = e[0], e[1]

            # Create directed edge and add it to the tree
            s1 = str(node) + '->' + str(node2) + ':' + str(weight)
            s2 = str(node2) + '->' + str(node) + ':' + str(weight)
            edges.setdefault(node, []).append(s1)
            edges.setdefault(node2, []).append(s2)

            #directed_tree.append(str(node) + '->' + str(node2) + ':' + str(weight))
            #directed_tree.append(str(node2) + '->' + str(node) + ':' + str(weight))
    for edge in sorted(edges):
        directed_tree.append(edges[edge])
    directed_tree = list(itertools.chain.from_iterable(directed_tree))
    return directed_tree


if __name__ == '__main__':
    n, d_matrix = read_input("dataset.txt")
    tree = UPGMA(n, d_matrix, n)
    result = directed_edges_adjaceny_list(tree)
    #print('----')
    #for e in result:
    #    print(e)

    try:
        output_file = open("output.txt", "w")
        for e in result:
                output_file.write(e + '\n')
        output_file.close()
        print("Output written successfully to the textfile.")
    except:
        print('File I/O Error...')
