import numpy as np
from math import log, ceil

alphabet = ['A', 'C', 'G', 'T']

class Node(object):
    def __init__(self, id, tag, string, symbol, left=None, right=None, middle=None):
        self.id = id
        self.tag = tag
        self.string = string
        self.scores = []
        self.symbol = symbol

        # children
        self.left = left
        self.right = right
        self.middle = middle

    def __str__(self):
        return "ID: %s, tag: %s, string: %s, symbol: %s, left: %s, right: %s, middle: %s, scores: %s" \
               % (self.id, self.tag, self.string, self.symbol, self.left, self.right, self.middle, self.scores)

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
    pairs = []
    label = 0
    while True:
        # Read 1 edge first, several cases
        edge1 = input_file.readline().rstrip('\n').split('->')

        if edge1 == ['']:
            break # EOF
        start1, end1 = edge1[0], edge1[1]

        # If we are still at the strings part, then read 3 more edges
        if start1[0].isalpha():
            edge2 = input_file.readline().rstrip('\n').split('->')
            edge3 = input_file.readline().rstrip('\n').split('->')
            edge4 = input_file.readline().rstrip('\n').split('->')

            start2, end2 = edge2[0], edge2[1]
            #start3, end3 = edge3[0], edge3[1] # simple no need to do processing for this
            start4, end4 = edge4[0], edge4[1]

            # Create a node for the number and set the 2 strings as leafs
            # Store the string
            leaf_strings.append(end2)
            leaf_strings.append(end4)

            start2 = int(start2)
            node1 = Node(id=start2, tag=0, string='', symbol=None, left=label, right=label+1)
            tree[start2] = node1

            leaf1 = Node(id=label, tag=0, string='', symbol=None)
            tree[label] = leaf1
            label += 1

            leaf2 = Node(id=label, tag=0, string='', symbol=None)
            tree[label] = leaf2
            label += 1

        # If its a digit then we probably done readin the leaves
        else:
            edge2 = input_file.readline().rstrip('\n').split('->')
            start1, end1 = int(start1), int(end1)
            #start2, end2 = edge2[0], edge2[1] # simply not needed

            # Store pairs of internal node
            pairs.append((start1, end1))

            # Only add NEW internal nodes or nodes that are the 'third' child
            if start1 in tree:
                # Find an empty edge for the new node, (left, right or middle)
                if tree[start1].left is None:
                    tree[start1].left = end1
                elif tree[start1].right is None:
                    tree[start1].right = end1
                elif tree[start1].middle is None:
                    tree[start1].middle = end1
                else:
                    print('SOMETHING IS DAMN WEIRD IN HERE')

            if end1 not in tree:
                node = Node(id=end1, tag=0, string='', symbol=None, left=start1)
                tree[end1] = node
            else:
                # Find a place for it, (right or middle)
                if tree[end1].right is None:
                    tree[end1].right = start1
                elif tree[end1].middle is None:
                    tree[end1].middle = start1
                else:
                    print('SOMETHING IS DAMN WEIRD IN HERE22222')
    input_file.close()
    return n, tree, leaf_strings, pairs

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
    directed_tree = set() # use a set to cheese adding duplicate edges lol
    for node in internal_nodes:
        start = tree[node].string

        # Get nodes at the end of the edge and the weights
        end1 = tree[tree[node].left].string
        end2 = tree[tree[node].right].string
        end3 = tree[tree[node].middle].string
        w1 = hamming_distance(start, end1)
        w2 = hamming_distance(start, end2)
        w3 = hamming_distance(start, end3)

        # Create directed edge and add it to the tree
        directed_tree.add(start + '->' + end1 + ':' + str(w1))
        directed_tree.add(start + '->' + end2 + ':' + str(w2))
        directed_tree.add(start + '->' + end3 + ':' + str(w3))
        directed_tree.add(end1 + '->' + start + ':' + str(w1))
        directed_tree.add(end2 + '->' + start + ':' + str(w2))
    return directed_tree


# Make the children of a node use their 'middle' edge to connect with it
def fix_tree(tree, node):
    # Fix the stuff
    daugther = tree[node].left
    son = tree[node].right

    if tree.get(daugther) != None:
        if tree.get(daugther).left == node:
            temp = tree[daugther].left
            tree[daugther].left = tree[daugther].middle
            tree[daugther].middle = temp
        elif tree.get(daugther).right == node:
            temp = tree[daugther].right
            tree[daugther].right = tree[daugther].middle
            tree[daugther].middle = temp

    if tree.get(son) != None:
        if tree.get(son).left == node:
            temp = tree[son].left
            tree[son].left = tree[son].middle
            tree[son].middle = temp
        elif tree.get(son).right == node:
            temp = tree[son].right
            tree[son].right = tree[son].middle
            tree[son].middle = temp

    # recurse
    if daugther != None:
        tree = fix_tree(tree, tree[node].left)
    if son != None:
        tree = fix_tree(tree, tree[node].right)

    return tree


def start():
    n, tree, strings, pairs = read_input("dataset.txt")

    # Get the label of the 'new' node that we will add to ROOT the tree
    root = max(tree)
    extra = root+1


    min_score = float('inf')
    best_tree = None
    m = len(strings[0]) # get length of the strings
    for pair in pairs:
        # Create new node which will be the root
        node = Node(id=extra, tag=0, string='', symbol=None, left=pair[0], right=pair[1])
        tree[extra] = node

        # clean the strings from last rooted tree iteration, for some weird reason
        # the strings exist in the OLD copied tree
        for node in tree:
            tree[node].string = ''

        # Make sure that every node from the root point has their middle edge 'towrads' the root
        # Reorient the edges of the tree around this rooted tree
        fixed_tree = tree.copy()
        node1 = pair[0]
        node2 = pair[1]

        left1 = fixed_tree[node1].left
        left2 = fixed_tree[node2].left
        right1 = fixed_tree[node1].right
        right2 = fixed_tree[node2].right
        middle1 = fixed_tree[node1].middle
        middle2 = fixed_tree[node2].middle

        if fixed_tree[node1].left == node2:
            fixed_tree[node1].left = middle1 # switch left and middle
            fixed_tree[node1].middle = left1 # left is in fact node2
        elif fixed_tree[node1].right == node2:
            fixed_tree[node1].right = middle1
            fixed_tree[node1].middle = right1

        # Do the same thing for node2
        if fixed_tree[node2].left == node1:
            fixed_tree[node2].left = middle2 # switch left and middle
            fixed_tree[node2].middle = left2 # left is in fact node2
        elif fixed_tree[node2].right == node1:
            fixed_tree[node2].right = middle2
            fixed_tree[node2].middle = right2

        # Fix everything else in the tree as well
        fixed_tree = fix_tree(fixed_tree, node1)
        fixed_tree = fix_tree(fixed_tree, node2)

        score = 0

        # Now find the small parsimony score for this rooted tree
        for i in range(m):
            character = ''
            for string in strings:
                character += string[i]

            fixed_tree = small_parsimony(fixed_tree, character)

            # Keep a record of the score
            score += min(fixed_tree[extra].scores)
            # Flush and Clean up the tree for another iteration
            for node in fixed_tree:
                fixed_tree[node].tag = 0
                fixed_tree[node].scores.clear()

        # Record score and update if necessary
        if score < min_score:
            min_score = score
            best_tree = fixed_tree

    # Remove the root
    del best_tree[extra]

    output = directed_edges_adjaceny_list(best_tree)
    #print(min_score)
    #for edge in output:
    #    print(edge)

    try:
        output_file = open("output.txt", "w")
        output_file.write(str(min_score) + '\n')
        for e in output:
                output_file.write(e + '\n')
        output_file.close()
        print("Output written successfully to the textfile.")
    except:
        print('File I/O Error...')

if __name__ == '__main__':
    start()
