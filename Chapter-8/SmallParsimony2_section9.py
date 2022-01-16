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

def read_input(filename):
    try:
        pass
    except:
        print("Exception caught, file probably doesnt exist")
    input_file = open(filename, "r")
    n = input_file.readline().rstrip('\n')
    n = int(n)

    tree = dict()
    leaf_strings = []
    label = 0
    while True:
        # Read 2 edges at the same time
        edge1 = input_file.readline().rstrip('\n').split('->')
        edge2 = input_file.readline().rstrip('\n').split('->')

        if edge1 == ['']: break # EOF

        start1, end1 = edge1[0], edge1[1]
        start2, end2 = edge2[0], edge2[1]

        # Check if the end of the edges is a digit or a string
        if end1[0].isdigit():
            start1 = int(start1)
            node = Node(id=start1, tag=0, string='', symbol=None, left=int(end1), right=int(end2))
            tree[start1] = node

        # If end is a string
        else:
            # Store the string
            leaf_strings.append(end1)
            leaf_strings.append(end2)

            start1 = int(start1)
            #node1 = Node(id=start1, tag=0, string=None, symbol=None, left=end1, right=end2)
            node1 = Node(id=start1, tag=0, string='', symbol=None, left=label, right=label+1)
            tree[start1] = node1

            #leaf1 = Node(id=end1, tag=0, string=end1, symbol=None)
            #tree[end1] = leaf1
            leaf1 = Node(id=label, tag=0, string='', symbol=None)
            tree[label] = leaf1
            label += 1


            #leaf2 = Node(id=end2, tag=0, string=end2, symbol=None)
            #tree[end2] = leaf2
            leaf2 = Node(id=label, tag=0, string='', symbol=None)
            tree[label] = leaf2
            label += 1

    input_file.close()
    return n, tree, leaf_strings

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
                else:
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
    tree[root].string += alphabet[i]

    # Backtrack and assign a symbol to each internal node
    n = len(tree)-1
    without_leaves = ceil(n/2)
    internal_nodes = [i for i in range(n, without_leaves, -1)]
    for node in internal_nodes:
        daugther_i, son_i = assign_symbols(tree, tree[node].symbol, tree[node].left, tree[node].right)
        tree[tree[node].left].symbol = alphabet[daugther_i]
        tree[tree[node].left].string += alphabet[daugther_i]
        tree[tree[node].right].symbol = alphabet[son_i]
        tree[tree[node].right].string += alphabet[son_i]
    return tree


# Take an adjacency list of a tree with undirected edges and breaks it to directed edges
def directed_edges_adjaceny_list(tree):

    def hamming_distance(genome1, genome2):
        mismatch_count = 0
        for i in range(0, len(genome1)):
            if genome1[i] != genome2[i]:
                mismatch_count += 1
        return mismatch_count

    n = len(tree)-1
    without_leaves = ceil(n/2)
    internal_nodes = [i for i in range(n, without_leaves, -1)]
    directed_tree = []
    for node in internal_nodes:
        start = tree[node].string

        # Get nodes at the end of the edge and the weights
        end1 = tree[tree[node].left].string
        end2 = tree[tree[node].right].string
        w1 = hamming_distance(start, end1)
        w2 = hamming_distance(start, end2)

        # Create directed edge and add it to the tree
        directed_tree.append(start + '->' + end1 + ':' + str(w1))
        directed_tree.append(start + '->' + end2 + ':' + str(w2))
        directed_tree.append(end1 + '->' + start + ':' + str(w1))
        directed_tree.append(end2 + '->' + start + ':' + str(w2))
    return directed_tree

def start():
    n, tree, strings = read_input("dataset.txt")
    m = len(strings[0]) # get length of the strings
    root = max(tree)
    score = 0
    for i in range(m):
        character = ''
        for string in strings:
            character += string[i]

        tree = small_parsimony(tree, character)

        # Keep a record of the score
        score += min(tree[root].scores)
        # Flush and Clean up the tree for another iteration
        for node in tree:
            tree[node].tag = 0
            tree[node].scores.clear()

    output = directed_edges_adjaceny_list(tree)
    #print(score)
    #for edge in output:
    #    print(edge)

    try:
        output_file = open("output.txt", "w")
        output_file.write(str(score) + '\n')
        for e in output:
                output_file.write(e + '\n')
        output_file.close()
        print("Output written successfully to the textfile.")
    except:
        print('File I/O Error...')




if __name__ == '__main__':
    start()
