import numpy as np
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

# BFS to find the paths from a certain node in the tree
def breadth_first_search_find_insert_position(graph, i, k, x):
    q = [i]
    visited = dict()
    visited[i] = True

    path = dict()
    path[i] = [i]
    edges = dict()
    edges[i] = [0]
    while len(q) != 0:
        v = q.pop(0)
        visited[v] = True
        # Edges are stored as tuples with weights, e[0] is the node, e[1] is the weight
        for edge in graph[v]:
            # Dont care about other paths, break once we find k
            if edge[0] == k:
                path[edge[0]] = path[v] + [edge[0]]
                edges[edge[0]] = edges[v] + [edge[1]]
                break

            if edge[0] not in visited:
                q.append(edge[0])
                path[edge[0]] = path[v] + [edge[0]]
                edges[edge[0]] = edges[v] + [edge[1]]

    path_ik = path[k] # path from i to k
    edges_ik = edges[k]
    distance = 0
    for k in range(len(path_ik)):
        i = path_ik[k]
        j = path_ik[k+1]
        weight = edges_ik[k+1]
        if (distance + weight) > x:
            return i, j, (x-distance), (distance+weight)-x
        distance += weight

def total_distance(i, n, D):
    total_dist = 0
    for j in range(n):
        total_dist += D[i][j]
    return total_dist

def neighbor_joining(n, D, m1, m2, nodes):
    if n == 2:
        tree = dict()
        tree.setdefault(nodes[0], []).append((nodes[1], "%.2f" % D[0][1]))
        tree.setdefault(nodes[1], []).append((nodes[0], "%.2f" % D[0][1]))
        return tree, m1, m2

    # D* ← neighbor-joining matrix constructed from the distance matrix D
    D_star = np.zeros((n, n), dtype='float64')
    for i in range(n):
        for j in range(n):
            if i == j:
                D_star[i][j] = 0
            else:
                D_star[i][j] = (n-2) * D[i][j] - total_distance(i, n, D) - total_distance(j, n, D)

    print(D_star)

    # Iterate through D* to find the minimum element
    i, j = 0, 0
    minimum = float('inf')
    for idx1 in range(n):
        for idx2 in range(n):
            if (D_star[idx1][idx2] < minimum) and (idx1 != idx2):
                minimum = D_star[idx1][idx2]
                i, j = idx1, idx2

    # find elements i and j such that D*i,j is a minimum non-diagonal element of D*
    #indices = np.where(D_star==np.amin(D_star))[0] # only get the first ele
    #indices2 = np.where(D_star==np.amin(D_star))[1]
    #i, j = indices[0], indices[1]
    #if i == j:
    #    i, j = indices2[0], indices2[1]

    # Δ ← (TotalDistanceD(i) - TotalDistanceD(j)) /(n - 2)
    difference = ( (total_distance(i, n, D) - total_distance(j, n, D))/(n-2) )

    limb_i = (1/2) * (D[i][j] + difference)
    limb_j = (1/2) * (D[i][j] - difference)

    # remove the rows and columns of D corresponding to j, overwrite i as new col/row
    D_copy = D
    D = np.delete(D, j, 1) # col j
    D = np.delete(D, j, 0) # row j
    n = n - 1

    # store nodes list at this stage
    this_recurs_nodes = nodes.copy()

    # keep track of the nodes at this stage
    nodes.remove(nodes[j])
    nodes.remove(nodes[i])
    nodes.insert(i, m1)
    copy = m1
    m1 += 1


    # Iterate through the col and compute new values
    for k in range(n):
        if i == k:
            D[i][k] = 0 # main diagonal
        else:
            # compute values such that Dk,m = Dm,k = (1/2)(Dk,i + Dk,j - Di,j) for any k
            if k >= j:
                D[k][i] = (1/2) * (D_copy[k+1][i] + D_copy[k+1][j] - D_copy[i][j])
                D[i][k] = D[k][i]
            else:
                D[k][i] = (1/2) * (D_copy[k][i] + D_copy[k][j] - D_copy[i][j])
                D[i][k] = D[k][i]
    print('After TRANSFORMATION: ')
    print(D)

    tree, m1, m2 = neighbor_joining(n, D, m1, m2, nodes)

    # Now growing the damn tree back is hard
    print('----')
    print(nodes)
    print(i)
    print(j)
    print(tree)
    print(D)
    #print(m)
    print(n)
    tree.setdefault(copy, []).append((this_recurs_nodes[i], "%.2f" % limb_i))
    tree.setdefault(this_recurs_nodes[i], []).append((copy, "%.2f" % limb_i))
    tree.setdefault(copy, []).append((this_recurs_nodes[j], "%.2f" % limb_j))
    tree.setdefault(this_recurs_nodes[j], []).append((copy, "%.2f" % limb_j))
    print(tree)
    print('***')
    m2 -= 1
    return tree, m1, m2


# Take an adjacency list of a tree with undirected edges and breaks it to directed edges
def directed_edges_adjaceny_list(tree):
    directed_tree = []
    for node in sorted(tree):
        for e in tree[node]:
            # Get node at the end of the edge and the weight
            node2, weight = e[0], e[1]

            # Create directed edge and add it to the tree
            directed_tree.append(str(node) + '->' + str(node2) + ':' + str(weight))
    return directed_tree


if __name__ == '__main__':
    n, d_matrix = read_input("dataset.txt")
    # Keep track of the nodes
    nodes = []
    for i in range(n):
        nodes.append(i)

    tree, placeholder, placeholder2 = neighbor_joining(n, d_matrix, n, n, nodes)
    result = directed_edges_adjaceny_list(tree)
    for e in result:
        print(e)

    try:
        output_file = open("output.txt", "w")
        for e in result:
                output_file.write(e + '\n')
        output_file.close()
        print("Output written successfully to the textfile.")
    except:
        print('File I/O Error...')
