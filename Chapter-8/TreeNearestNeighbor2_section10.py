import numpy as np
from copy import deepcopy
from math import log, ceil

def read_input(filename):
    try:
        input_file = open(filename, "r")
        ab = input_file.readline().rstrip('\n').split(" ")
        ab = [int(i) for i in ab]
        ab = tuple(ab)

        tree = dict()
        a_adjacent = []
        b_adjacent = []
        for line in input_file:
            edge = line.rstrip('\n').split('->')
            start, end = int(edge[0]), int(edge[1])
            tree.setdefault(start, []).append(end)

            # If its the edge ab, then ignore it
            if (start == ab[0] and end == ab[1]) or (start == ab[1] and end == ab[0]): continue

            if start == ab[0]:
                a_adjacent.append(end)

            if start == ab[1]:
                b_adjacent.append(end)
        input_file.close()
    except:
        print("Exception caught, file probably doesnt exist")
    return ab, tree, a_adjacent, b_adjacent


def tree_nearest_neighbors(ab, tree, a_adj, b_adj):
    # 1ST NEIGHBOR
    # Deletion
    neighbor1 = deepcopy(tree)
    neighbor1[a_adj[1]].remove(ab[0]) # remove from a, 1 direction
    neighbor1[ab[0]].remove(a_adj[1]) # other direction
    neighbor1[b_adj[0]].remove(ab[1]) # remove from b, 1 direction
    neighbor1[ab[1]].remove(b_adj[0]) # other direction

    # Addition
    neighbor1[ab[1]].append(a_adj[1]) # add to b, 1 direction
    neighbor1[a_adj[1]].append(ab[1]) # other direction
    neighbor1[ab[0]].append(b_adj[0]) # add to a, 1 direction
    neighbor1[b_adj[0]].append(ab[0]) # other direction

    # 2ND NEIGHBOR
    # Deletion
    neighbor2 = deepcopy(tree)
    neighbor2[a_adj[1]].remove(ab[0]) # remove from a, 1 direction
    neighbor2[ab[0]].remove(a_adj[1]) # other direction
    neighbor2[b_adj[1]].remove(ab[1]) # remove from b, 1 direction
    neighbor2[ab[1]].remove(b_adj[1]) # other direction

    # Addition
    neighbor2[ab[1]].append(a_adj[1]) # add to b, 1 direction
    neighbor2[a_adj[1]].append(ab[1]) # other direction
    neighbor2[ab[0]].append(b_adj[1]) # add to a, 1 direction
    neighbor2[b_adj[1]].append(ab[0]) # other direction

    return neighbor1, neighbor2


# Take an adjacency list of a tree with undirected edges and breaks it to directed edges
def directed_edges_adjaceny_list(tree):
    directed_tree = []
    for node in sorted(tree):
        for e in tree[node]:
            # Create directed edges in both directions and add them to the tree
            directed_tree.append(str(node) + '->' + str(e))
    return directed_tree

def start():
    ab, tree, a_adj, b_adj = read_input("dataset.txt")
    tree1, tree2 = tree_nearest_neighbors(ab, tree, a_adj, b_adj)
    tree1 = directed_edges_adjaceny_list(tree1) # format the output
    tree2 = directed_edges_adjaceny_list(tree2)

    try:
        output_file = open("output.txt", "w")
        for e in tree1:
                output_file.write(e + '\n')
        output_file.write('\n')
        for e in tree2:
            output_file.write(e + '\n')
        output_file.close()
        print("Output written successfully to the textfile.")
    except:
        print('File I/O Error...')

if __name__ == '__main__':
    start()
