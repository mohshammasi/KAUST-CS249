import numpy as np
from math import log, ceil

alphabet = ['A', 'C', 'G', 'T']

class Node(object):
    def __init__(self, id, tag, string, symbol, left=None, right=None):
        self.id = id
        self.tag = tag
        self.string = string
        self.scores = []
        self.symbol = symbol

        # children
        self.left = left
        self.right = right

    def __str__(self):
        return "ID: %s, tag: %s, string: %s, symbol: %s, left: %s, right: %s, scores: %s" \
               % (self.id, self.tag, self.string, self.symbol, self.left, self.right, self.scores)


#default_score = {'A': float('inf'), 'C': float('inf'), 'G': float('inf'), 'T': float('inf')}
default_score = {}

def string_tree(string):
    # Store created nodes in a list
    #tree = []
    tree = dict()

    # Create leaf nodes from each character in the string
    label = 1
    for c in string:
        node = Node(id=label, tag=0, string=None, symbol=None)
        #tree.append(node)
        tree[label] = node
        label += 1

    num_of_leafs = len(tree)
    depth = int(log(len(tree), 2))
    layer = num_of_leafs
    for i in range(0, depth):
        num_of_nodes_on_previous_layer = layer
        layer = int(layer/2)
        for j in range(0, layer):
            left = label - num_of_nodes_on_previous_layer + j # calculate left child
            right = label - num_of_nodes_on_previous_layer + j + 1 # calculate right child
            node = Node(id=label, tag=0, string=None, symbol=None, left=left, right=right)
            #tree.append(node)
            tree[label] = node
            label += 1
    return tree

def get_ripe_nodes(tree):
    # while there exist ripe nodes in T
    ripe_nodes = []
    for node in tree:
        node_not_tagged = False
        daugther_tagged = False
        son_tagged = False
        ripe = False
        if tree[node].tag == 0: node_not_tagged = True
        daugther = tree.get(tree[node].left)
        if daugther is not None:
            if daugther.tag == 1: daugther_tagged = True
        son = tree.get(tree[node].right)
        if son is not None:
            if son.tag == 1: son_tagged = True
        if node_not_tagged and daugther_tagged and son_tagged: ripe = True

        if ripe:
            ripe_nodes.append(node) # store node id
    return ripe_nodes

def check(s1, s2):
    if s1 == s2:
        return 0
    else:
        return 1

def small_parsimony_recurrance(tree, k, daugther, son):
    # Get the scores of the daugther and son
    daugther_scores = tree[daugther].scores
    son_scores = tree[son].scores

    #print('Computed scores:')
    daugther_scores = [s + check(alphabet[i], k) for i, s in enumerate(daugther_scores)]
    son_scores = [s + check(alphabet[i], k) for i, s in enumerate(son_scores)]
    #print(daugther_scores)
    #print(son_scores)

    min_parsimony_k = min(daugther_scores) + min(son_scores)
    #print(min_parsimony_k)

    return min_parsimony_k

def assign_symbols(tree, k, daugther, son):
    # Get the scores of the daugther and son
    daugther_scores = tree[daugther].scores
    son_scores = tree[son].scores

    daugther_scores = [s + check(alphabet[i], k) for i, s in enumerate(daugther_scores)]
    son_scores = [s + check(alphabet[i], k) for i, s in enumerate(son_scores)]

    # in here I get the indices of the symbols of the alphabet
    daugther_i = daugther_scores.index(min(daugther_scores))
    son_i = son_scores.index(min(son_scores))

    return daugther_i, son_i

def small_parsimony(tree, character):
    nodes_score = {}
    for node in tree:
        if tree[node].left == None: # no children, a leaf
            tree[node].tag = 1 # tag it
            for k in alphabet:
                if character[node] == k:
                    tree[node].scores.append(0)
                    #nodes_score.setdefault(node, {})[k] = 0
                else:
                    #nodes_score.setdefault(node, {})[k] = float('inf')
                    tree[node].scores.append(float('inf'))

    ripe_nodes = get_ripe_nodes(tree)
    while len(ripe_nodes) != 0:
        for ripe_n in ripe_nodes:
            tree[ripe_n].tag = 1
            for k in alphabet:
                tree[ripe_n].scores.append(small_parsimony_recurrance(tree, k, tree[ripe_n].left, tree[ripe_n].right))
        ripe_nodes = get_ripe_nodes(tree) # get the leftover ripe nodes (newly generated)

    # root symbol is simply the minium value across all letters in the alphabet
    root = max(tree)
    i = tree[root].scores.index(min(tree[root].scores))
    tree[root].symbol = alphabet[i]

    # Backtrack and assign a symbol to each internal node
    n = len(tree)
    without_leaves = ceil(n/2)
    internal_nodes = [i for i in range(n, without_leaves, -1)]
    #print(internal_nodes)
    for node in internal_nodes:
        daugther_i, son_i = assign_symbols(tree, tree[node].symbol, tree[node].left, tree[node].right)
        tree[tree[node].left].symbol = alphabet[daugther_i]
        tree[tree[node].right].symbol = alphabet[son_i]

    for node in tree:
        print(tree[node])

def read_input(filename):
    try:
        pass
    except:
        print("Exception caught, file probably doesnt exist")
    input_file = open(filename, "r")
    n = input_file.readline().rstrip('\n')
    n = int(n)

    tree = []
    while True:
        # Read 2 edges at the same time
        edge1 = input_file.readline().rstrip('\n').split('->')
        edge2 = input_file.readline().rstrip('\n').split('->')

        if edge1 == ['']: break # EOF

        start1, end1 = edge1[0], edge1[1]
        start2, end2 = edge2[0], edge2[1]

        # Check if the end of the edges is a digit or a string
        if end1[0].isdigit():
            node = Node(id=int(start1), tag=0, string=None, symbol=None, left=int(end1), right=int(end2))
            tree.append(node)

        # If its a string, build trees of both strings (subtree of big tree)
        else:
            tree1_nodes = string_tree(end1)
            tree2_nodes = string_tree(end2)
            print('Going into small parsimony')
            print('----')

            # Run Small Parsimony on these subtrees
            end1 = ' ' + end1 # pad first since node labels start at 1
            end2 = ' ' + end2
            subtree1_root = small_parsimony(tree1_nodes, end1) # the root summarises everything
            break
            #subtree2_root = small_parsimony()

            # Add the data of the node connecting these 2 subtrees
            #node = Node(id=start1, )
            #tree.append(node)
    input_file.close()
    return n, tree

def start():
    n, trees = read_input("dataset.txt")
    #for tree in trees:
        #result = small_parsimony(tree, )
    #result = distance_matrix(n, graph, degrees)

if __name__ == '__main__':
    start()
