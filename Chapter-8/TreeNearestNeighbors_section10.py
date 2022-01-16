import numpy as np
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
        while True:
            # Read 2 edges at the same time
            edge1 = input_file.readline().rstrip('\n').split('->')
            edge2 = input_file.readline().rstrip('\n').split('->')
            if edge1 == ['']: break # EOF
            start1, end1 = int(edge1[0]), int(edge1[1])
            tree[start1] = end1

            # If its the edge ab, then ignore it
            if (start1 == ab[0] and end1 == ab[1]) or (start1 == ab[1] and end1 == ab[0]): continue

            if start1 == ab[0]:
                a_adjacent.append(end1)
            elif end1 == ab[0]:
                a_adjacent.append(start1)

            if start1 == ab[1]:
                b_adjacent.append(end1)
            elif end1 == ab[1]:
                b_adjacent.append(start1)
        input_file.close()
    except:
        print("Exception caught, file probably doesnt exist")
    return ab, tree, a_adjacent, b_adjacent


# later
def rearrange(tree, real_parent, new_parent, node):

    # Find the adjacent edges to the node
    adj = []
    for edge in tree:
        if tree[edge] == node:
            adj.append(edge)
        elif edge == node:
            adj.append(tree[edge])

    adj = [i for i in adj if i != real_parent]
    #print(adj)

    # Make sure to also switch the edge that are connected to the nodes we switched
    # deletion
    for e in adj:
        del tree[e]
    # addition
    for e in adj:
        tree[e] = new_parent

    # Go deeper to make the swaps until leafs
    #for e in adj:
    #    tree = rearrange(tree, new_parent,  e)
    return tree



def tree_nearest_neighbors(ab, tree, a_adj, b_adj):
    # make 2 copies of the original tree
    neighbor1 = tree.copy()
    neighbor2 = tree.copy()

    #for e in a_adj:
    #    neighbor1 = rearrange(neighbor1, ab[0], ab[1], e)
    #for e in b_adj:
    #    neighbor2 = rearrange(neighbor2, ab[1], ab[0], e)

    # Neighbor 1 switching
    del neighbor1[a_adj[1]] # delete from a
    del neighbor1[b_adj[0]] # delete from b
    neighbor1[b_adj[0]] = ab[0] # add to a
    neighbor1[a_adj[1]] = ab[1] # add to b

    output1 = directed_edges_adjaceny_list(neighbor1)
    #for e in output1:
    #    print(e)
    #print()

    # Neighbor 2 switching
    if neighbor2[a_adj[1]] == ab[0]:
        del neighbor2[a_adj[1]] # delete from a
        neighbor2[a_adj[1]] = ab[1] # add to b
    else:
        del neighbor2[ab[0]]
        print('Add an edge between ' + str(ab[0]) + ' and ' + str(a_adj[1]))
        
    if neighbor2[b_adj[1]] == ab[1]:
        del neighbor2[b_adj[1]] # delete from b
        neighbor2[b_adj[1]] = ab[0] # add to a
    else:
        del neighbor2[ab[1]]
        # cant add ab[1] as a key and cant add b_adj[1] as a key
        print('Add an edge between ' + str(ab[1]) + ' and ' + str(b_adj[1]))

    output2 = directed_edges_adjaceny_list(neighbor2)
    #for e in output2:
    #    print(e)

    return output1, output2


# Take an adjacency list of a tree with undirected edges and breaks it to directed edges
def directed_edges_adjaceny_list(tree):
    directed_tree = []
    for node in sorted(tree):
        end = tree[node]
        # Create directed edges in both directions and add them to the tree
        directed_tree.append(str(node) + '->' + str(end))
        directed_tree.append(str(end) + '->' + str(node))
    return directed_tree

def start():
    ab, tree, a_adj, b_adj = read_input("dataset.txt")
    output = directed_edges_adjaceny_list(tree)
    print(a_adj)
    print(b_adj)
    tree1, tree2 = tree_nearest_neighbors(ab, tree, a_adj, b_adj)

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
