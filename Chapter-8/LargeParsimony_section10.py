import numpy as np
from copy import deepcopy
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
        input_file = open(filename, "r")
        n = input_file.readline().rstrip('\n')
        n = int(n)

        tree = dict()
        leaf_strings = []
        pairs = []
        label = 0
        add = True
        while True:
            # Read 1 edge first, several cases
            edge1 = input_file.readline().rstrip('\n').split('->')

            if edge1 == ['']:
                break # EOF
            start1, end1 = edge1[0], edge1[1]

            # If we are still at the mixed strings/nodes part then read 4 more edges
            if start1[0].isalpha():
                edge2 = input_file.readline().rstrip('\n').split('->')
                edge3 = input_file.readline().rstrip('\n').split('->')
                edge4 = input_file.readline().rstrip('\n').split('->')
                edge5 = input_file.readline().rstrip('\n').split('->')

                #start2, end2 = edge2[0], edge2[1] # simple no need to do processing for this
                start3, end3 = edge3[0], edge3[1]
                start4, end4 = edge4[0], edge4[1]
                end1 = int(end1)
                start4, end4 = int(start4), int(end4)

                # Store pairs of internal node
                pairs.append((start4, end4))

                # Create a node for the number and set the 2 strings as leafs
                # Store the string
                leaf_strings.append(start1)
                leaf_strings.append(end3)

                node1 = Node(id=end1, tag=0, string='', symbol=None, left=label, right=label+1, middle=end4)
                tree[end1] = node1

                leaf1 = Node(id=label, tag=0, string='', symbol=None)
                tree[label] = leaf1
                label += 1

                leaf2 = Node(id=label, tag=0, string='', symbol=None)
                tree[label] = leaf2
                label += 1

            # If its a digit then we probably done readin the leaves with strings
            else:
                edge2 = input_file.readline().rstrip('\n').split('->')
                edge3 = input_file.readline().rstrip('\n').split('->')
                start1, end1 = int(start1), int(end1)
                start2, end2 = int(edge2[0]), int(edge2[1])
                start3, end3 = int(edge3[0]), int(edge3[1])


                # Store pairs of internal node
                if add:
                    pairs.append((start3, end3))
                    add = False # alternate between adding
                else:
                    add = True

                # Create 1 new node and link it to its 3 children
                node = Node(id=start1, tag=0, string='', symbol=None, left=end1, right=end2, middle=end3)
                tree[start1] = node
        input_file.close()
    except:
        print("Exception caught, file probably doesnt exist")
    return n, tree, leaf_strings, pairs


##############################################################
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

    daugther_scores = [s + check(alphabet[i], k) for i, s in enumerate(daugther_scores)]
    son_scores = [s + check(alphabet[i], k) for i, s in enumerate(son_scores)]

    min_parsimony_k = min(daugther_scores) + min(son_scores)
    return min_parsimony_k

def assign_symbols(tree, k, daugther, son):
    # Get the scores of the daugther and son
    daugther_scores = tree[daugther].scores
    son_scores = tree[son].scores

    daugther_scores = [s + check(alphabet[i], k) for i, s in enumerate(daugther_scores)]
    son_scores = [s + check(alphabet[i], k) for i, s in enumerate(son_scores)]

    # in here I get the indices of the symbols of the alphabet
    #print(son)
    #for node in tree:
    #    print(tree[node])
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
        #directed_tree.add(end3 + '->' + start + ':' + str(w3))
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


def unrooted_small_parsimony(n, tree, strings, pairs):
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
        fixed_tree = deepcopy(tree)
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

    # Remove the root of the best tree we found
    del best_tree[extra]
    return min_score, best_tree
##############################################################


##############################################################
# NEAREST TREE NEIGHBORS CODE SECTION10

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

##############################################################

# Finds all internal edges in a tree, these are the edges with degree 3
def find_internal_edges(n, tree):
    # Check if the node has degree 3, then it is an internal node, from that
    # find internal edges which are edges connected to non-leafs
    internal_edges = []
    for node in tree:
        has_degree_3 = False
        left = tree[node].left
        right = tree[node].right
        middle = tree[node].middle
        if (left != None) and (right != None) and (middle != None):
            has_degree_3 = True

        if has_degree_3:
            # If the other endpoint is labelled >= n then its an internal node
            if left >= n:
                internal_edges.append(frozenset({node, left}))
            if right >= n:
                internal_edges.append(frozenset({node, right}))
            if middle >= n:
                internal_edges.append(frozenset({node, middle}))
    internal_edges = [tuple(edge) for edge in internal_edges]
    #print(internal_edges)
    return internal_edges

# Find the adjacent nodes of a node except for a specific node
def find_adjacent_nodes(tree, node, avoid):
    adjacent_nodes = []
    if tree[node].left != avoid:
        adjacent_nodes.append(tree[node].left)
    if tree[node].right != avoid:
        adjacent_nodes.append(tree[node].right)
    if tree[node].middle != avoid:
        adjacent_nodes.append(tree[node].middle)
    return adjacent_nodes

# Reformats the tree from the form of the unrooted_small_parsimony problem to the
# form of the tree nearest neighbor
def to_nearest_neighbor(n, tree):
    formatted_tree = dict()
    for node in tree:
        # check if the node is leaf, then we skip it
        if tree[node].left == None:
            continue

        # If the node is not a leaf, but it is connected to a leaf node then we
        # add the leaf node. a leaf has label < n
        if tree[node].left < n:
            formatted_tree.setdefault(tree[node].left, []).append(node)
        if tree[node].right < n:
            formatted_tree.setdefault(tree[node].right, []).append(node)
        if tree[node].middle < n:
            formatted_tree.setdefault(tree[node].middle, []).append(node)
        formatted_tree.setdefault(node, []).append(tree[node].left)
        formatted_tree.setdefault(node, []).append(tree[node].right)
        formatted_tree.setdefault(node, []).append(tree[node].middle)
    return formatted_tree

# Reformats the tree from the form of the nearest neighbor problem to the form of
# the unrooted small parsimony problem
def to_unrooted_small_parsimony(tree, nn_tree):
    formatted_tree = deepcopy(tree)
    # Flush the edges in 'tree'
    for node in formatted_tree:
        formatted_tree[node].left = None
        formatted_tree[node].right = None
        formatted_tree[node].middle = None

    # iterate over the nn_tree format and adjust the (left, right, middle) params
    # in the tree
    for node in nn_tree:
        # if the node is a leaf then skip it, because leafs dont have children lol
        if len(nn_tree[node]) == 1: continue
        for n in nn_tree[node]:
            if formatted_tree[node].left == None:
                formatted_tree[node].left = n
            elif formatted_tree[node].right == None:
                formatted_tree[node].right = n
            elif formatted_tree[node].middle == None:
                formatted_tree[node].middle = n
    return formatted_tree

# Everthing seems fine with the code, i have no idea why its incorrect
def nearest_neighbor_interchange(n, tree, strings, pairs):
    score = float('inf')
    # generate an arbitrary unrooted binary tree Tree with |Strings| leaves - done == tree
    # label the leaves of Tree by arbitrary strings from Strings - done from input

    # solve  the  Small Parsimony in an Unrooted Tree Problem for Tree
    new_score, new_tree = unrooted_small_parsimony(n, tree, strings, pairs)

    while new_score < score:
        score = new_score
        tree = deepcopy(new_tree)
        internal_edges = find_internal_edges(n, tree)
        for edge in internal_edges:
            a_adj = find_adjacent_nodes(tree, edge[0], edge[1])
            b_adj = find_adjacent_nodes(tree, edge[1], edge[0])

            # Reformat the tree from the unrooted small parsimony output to match
            # the tree format for the tree nearest neighbor
            nn_format = to_nearest_neighbor(n, tree)

            neighbor1, neighbor2 = tree_nearest_neighbors(edge, nn_format, a_adj, b_adj)

            # Reformat the tree from the nearest neighbor output to match the tree
            # format for the unrooted small parsimony problem
            neighbor1 = to_unrooted_small_parsimony(tree, neighbor1)
            neighbor2 = to_unrooted_small_parsimony(tree, neighbor2)

            # Solve Small Parsimony for neighbor1
            neighbor1_pairs = find_internal_edges(n, neighbor1)
            neighbor1_score, neighbor1_tree = unrooted_small_parsimony(n, neighbor1, strings, neighbor1_pairs)

            # Solve Small Parsimony for neighbor2
            neighbor2_pairs = find_internal_edges(n, neighbor2)
            neighbor2_score, neighbor2_tree = unrooted_small_parsimony(n, neighbor2, strings, neighbor2_pairs)

            # Take the best score i.e. the minimum
            updated = False
            if neighbor1_score < new_score:
                new_score = neighbor1_score
                new_tree = deepcopy(neighbor1_tree)
                updated = True
            if neighbor2_score < new_score:
                new_score = neighbor2_score
                new_tree = deepcopy(neighbor2_tree)
                updated = True

        print(new_score)
        output = directed_edges_adjaceny_list(new_tree)
        for e in output:
            print(e)
        print()

def start():
    n, tree, strings, pairs = read_input("dataset.txt")
    nearest_neighbor_interchange(n, tree, strings, pairs)

if __name__ == '__main__':
    start()

# This is the extra dataset provided for this problem:
# 8
# GTCCAAGAGTATGTGAAACCTGCAGTGACGAAGGCGAGAT->8
# 8->GTCCAAGAGTATGTGAAACCTGCAGTGACGAAGGCGAGAT
# 8->CCACACGTGGCTGTTATATGATATTAATATATTTAATCTT
# 8->13
# CCACACGTGGCTGTTATATGATATTAATATATTTAATCTT->8
# ATTATGGGGCACTGAGCATACGCAAACGACTATGCTTTCC->9
# 9->ATTATGGGGCACTGAGCATACGCAAACGACTATGCTTTCC
# 9->TGCGGCGGGCGCGCCCAAACAGCGTGACCAAGTCGATGCA
# 9->13
# TGCGGCGGGCGCGCCCAAACAGCGTGACCAAGTCGATGCA->9
# CCGCCGTACACACAGTCTTGAACCATTTACCGCAGTTTCC->10
# 10->CCGCCGTACACACAGTCTTGAACCATTTACCGCAGTTTCC
# 10->CGGTCCTCTAGGAGCTTGTCTTTATCTGCCGCCGACATGC
# 10->12
# CGGTCCTCTAGGAGCTTGTCTTTATCTGCCGCCGACATGC->10
# AGCTCAGCGCCCCGGAGCACCCTCCTGAAGTATGCACATT->11
# 11->AGCTCAGCGCCCCGGAGCACCCTCCTGAAGTATGCACATT
# 11->ACTGAGGTACGGGTTATACCGCGCATCTGCGAGTAAAACA
# 11->12
# ACTGAGGTACGGGTTATACCGCGCATCTGCGAGTAAAACA->11
# 13->8
# 13->9
# 13->12
# 12->11
# 12->10
# 12->13
