import numpy as np
from operator import itemgetter

def read_input(filename):
    try:
        input_file = open(filename, "r")
        n = input_file.readline().rstrip('\n')
        d_matrix = []
        for line in input_file:
            d_matrix.append(list(map(int, line.rstrip('\n').split(' ')))) # convert to int
        d_matrix = np.array(d_matrix)
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

def additive_phylogeny(n, d_matrix, m):
    if n == 2:
        tree = dict()
        tree.setdefault(0, []).append((1, d_matrix[0][1]))
        tree.setdefault(1, []).append((0, d_matrix[0][1]))
        return tree, m

    limb_len = limb_length(n, n-1, d_matrix)
    for j in range(0, n-1):
        d_matrix[j][n-1] = d_matrix[j][n-1] - limb_len # last column
        d_matrix[n-1][j] = d_matrix[j][n-1] # last row

    # Find a pair of leaves i,k such that Dik = Din + Dnk
    pair = None
    for i in range(0, n):
        for k in range(1, n):
            if d_matrix[i][k] == d_matrix[i][n-1] + d_matrix[n-1][k]:
                pair = (i, k)
                found_pair = True
                break
        else:
            continue # only executred if the inner loop did not break
        break # only executed if the inner loop DID break

    x = d_matrix[pair[0]][n-1]
    d_matrix = d_matrix[:-1, :-1] # shave last col and last row of matrix
    t, m = additive_phylogeny(n-1, d_matrix, m)

    # Find the position to insert the new node in the tree along the path from i
    # to k. Note that this position could be along an edge which we should create
    # a new node at that point or it could be at an already existing node which we
    # attach our new leaf to.
    i, j, i_to_n_dist, n_to_k_dist = breadth_first_search_find_insert_position(t, *pair, x)
    # n-1 is the new leaf vertex
    # m+1 is the new internal vertex
    v = i

    # check if there is an already existing node exactly where the new leaf should be attached
    if i_to_n_dist != 0:
        v = m
        m += 1
        # Remove the old edge by 'Breaking' the edge into 2, to add node to the tree
        t[i].remove((j, i_to_n_dist+n_to_k_dist))
        t[j].remove((i, i_to_n_dist+n_to_k_dist))
        t.setdefault(i, []).append((v, i_to_n_dist))
        t.setdefault(v, []).append((i, i_to_n_dist))
        t.setdefault(j, []).append((v, n_to_k_dist))
        t.setdefault(v, []).append((j, n_to_k_dist))

    # Attach the removed leaf back with limb edge weight to the tree and output tree
    t.setdefault(v, []).append((n-1, limb_len))
    t.setdefault(n-1, []).append((v, limb_len))
    return t, m

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
    tree, placeholder = additive_phylogeny(n, d_matrix, n)
    result = directed_edges_adjaceny_list(tree)
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
