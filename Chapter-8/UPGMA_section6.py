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

def new_cluster_distance(ci, cj, D, index, n):
    #d_ci_cj = 0
    #ci_max = max(ci)
    #cj_max = max(cj)
    #for ei in ci:
    #    for ej in cj:
    #        if ci_max >= n:
    #            d_ci_cj += D[idx1][ej]
    #        elif cj_max >= n:
    #            d_ci_cj += D[ei][idx2]
    #        elif (ci_max >= n) and (cj_max >= n):
    #            d_ci_cj += D[idx1][idx2]
    #        else:
    #            d_ci_cj += D[ei][ej]
    #d_ci_cj = (d_ci_cj/(len(ci)*len(cj)))

    d_ci_cj = 0
    for ei in ci:
        for ej in cj:
            d_ci_cj += D[index[ei]][index[ej]]
    d_ci_cj = (d_ci_cj/(len(ci)*len(cj)))
    return d_ci_cj

def UPGMA(n, D):
    # Used to store the clusters that we are merging
    clusters = dict()
    for i in range(n):
        clusters[i] = [i]

    # Used to store the entire tree (nodes and edges)
    tree = dict()
    for i in range(n):
        tree.setdefault(i, [])

    # Used to record the age of each node in the tree
    age = dict()
    for node in tree:
        age[node] = 0

    # Used to map each node in the tree with its cluster
    map = dict()
    for i in range(n):
        map[i] = i

    m = n # used for internal nodes labeling
    clusters_count = n-1
    while len(clusters) > 1:
        print('ITERATION')
        # Find the two closest clusters Ci and Cj 
        indices = np.where(D==np.min(D[np.nonzero(D)]))[0] # only get the first ele
        i, j = indices[0], indices[1]
        ci = clusters[i]
        cj = clusters[j]

        # Find the distance between the 2 clusters
        print('Picked Ci and Cj:')
        print(ci)
        print(cj)
        d_ci_cj = cluster_distance(ci, cj, D, i, j)
        print('D between ci and cj is ')
        print(d_ci_cj)

        # merge Ci and Cj into a new cluster Cnew with |Ci| + |Cj| elements
        # remove Ci and Cj from Clusters  and add Cnew to Clusters
        del clusters[i]
        del clusters[j]
        c_new = ci + cj
        clusters[i] = c_new

        # Create an index dictionary to map each value in the new cluster to
        # its correct index in the Distance matrix
        # example: [0] merged with [2 3] we get [0 2 3], at this stage n = 3
        # so the mapping is 0->0, 2->2, 3->2 when indexing D
        index = dict()
        for element in range(len(ci)):
            if ci[element] >= n:
                index[ci[element]] = ci[0] # first in cluster
            else:
                index[ci[element]] = ci[element] # itself

        for element in range(len(cj)):
            if cj[element] >= n:
                index[cj[element]] = cj[0] # first in cluster
            else:
                index[cj[element]] = cj[element] # itself

        # add a new node labeled by cluster Cnew to T and connect node Cnew to Ci
        # and Cj by directed edges 
        #del tree[i]
        #del tree[j]

        tree.setdefault(map[i], []).append((m, round(((d_ci_cj/2)-age[map[i]]), 2)))
        tree.setdefault(map[j], []).append((m, round(((d_ci_cj/2)-age[map[j]]), 2)))

        # decrement the key integers for all values above the deleted key
        for key in list(clusters.keys()):
            if key > j:
                clusters[key-1] = clusters[key]
                del clusters[key]

        # map cluster index from D/clusters to nodes in the tree
        del map[i]
        del map[j]
        map[i] = m
        for key in list(map.keys()):
            if key > j:
                map[key-1] = map[key]
                del map[key]

        # Age(Cnew) ← DCi, Cj / 2
        #del age[i]
        #del age[j]
        age[m] = d_ci_cj/2
        m += 1
        print('After FIRST transformation in iteration')
        print(map)
        print(clusters)
        print(tree)
        print(age)
        print(D)

        # remove the rows and columns of D corresponding to Cj 
        D_copy = D
        D = np.delete(D, j, 1) # col j
        D = np.delete(D, j, 0) # row j
        n = n - 1

        # iterate through the new column and compute the values
        for k in range(n):
            if i == k:
                D[i][k] = 0 # main diagonal
            else:
                # compute the distance between the new cluster C and other clusters
                c_other = clusters[k]

                # Create an index dictionary to map each value in the new cluster to
                # its correct index in the Distance matrix
                # example: [0] merged with [2 3] we get [0 2 3], at this stage n = 3
                # so the mapping is 0->0, 2->2, 3->2 when indexing D
                print(c_new)
                print(c_other)
                for element in range(len(c_other)):
                    if c_other[element] >= (n+1):
                        index[c_other[element]] = c_other[0]
                    else:
                        index[c_other[element]] = c_other[element]
                print(index)
                print(n+1)

                d_cnew_other = new_cluster_distance(c_new, c_other, D_copy, index, n+1)
                print('D between cnew and other is', d_cnew_other)
                D[i][k] = d_cnew_other

        # iterate through the new row and compute the values
        for k in range(n):
            if i == k:
                D[k][i] = 0 # main diagonal
            else:
                # compute the distance between the new cluster C and other clusters
                c_other = clusters[k]

                for element in range(len(c_other)):
                    if c_other[element] >= (n+1):
                        index[c_other[element]] = c_other[0]
                    else:
                        index[c_other[element]] = c_other[element]

                d_cnew_other = new_cluster_distance(c_new, c_other, D_copy, index, n+1)
                D[k][i] = d_cnew_other

        print('After second transformation in iteration')
        print(map)
        print(clusters)
        print(tree)
        print(age)
        print(D)
        #print(D.dtype)
        #break
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
    tree = UPGMA(n, d_matrix)
    result = directed_edges_adjaceny_list(tree)
    print('----')
    for e in result:
        print(e)


    #try:
    #    output_file = open("output.txt", "w")
    #    for e in result:
    #            output_file.write(e + '\n')
    #    output_file.close()
    #    print("Output written successfully to the textfile.")
    #except:
    #    print('File I/O Error...')
