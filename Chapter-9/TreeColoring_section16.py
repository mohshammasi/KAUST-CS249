import random
from copy import deepcopy

# Defining a TrieNode type to use to build up the Trie
# This version is slightly modified to construct the Trie for text not multiple patterns
class TrieNode:
    def __init__(self, id, character, position=None):
        self.id = id
        self.char = character # the character stored in this node
        self.pos = position # position of this node in text
        self.length = None

        # This is used only for leaf nodes to assign starting pos of this substring
        self.label = None

        # dictionary to store children (other TrieNodes) connected to this one
        self.children = {}

        # For Tree coloring challenge
        self.color = 'gray'

    def __str__(self):
        return "ID: %s, color: %s" \
               % (self.id, self.color)

class Trie(object):
    def __init__(self):
        # Create a root TrieNode with an empty char and ID 0
        self.root = TrieNode('')




def read_input(filename):
    try:
        input_file = open(filename, "r")

        tree = dict()
        leaf_colors = dict()
        reading_tree = True
        for line in input_file:
            if line == '-\n':
                reading_tree = False
                continue

            if reading_tree:
                edge = line.rstrip('\n').split(' -> ')
                start = int(edge[0])
                node = TrieNode(start, '')
                tree[start] = node
                if edge[1] != '{}':
                    end = edge[1].split(',')
                    end = [int(i) for i in end]
                    for n in end:
                        if n not in tree:
                            node = TrieNode(n, '')
                            tree[n] = node
                            tree[start].children[n] = node
                        else:
                            tree[start].children[n] = tree[n]
            else:
                edge = line.rstrip('\n').split(': ')
                leaf, color = int(edge[0]), edge[1]
                leaf_colors[leaf] = color
        input_file.close()
    except IOError as e:
        print(e)
    return tree, leaf_colors

def leaf_coloring(tree, leaf_colors):
    for leaf in leaf_colors:
        tree[leaf].color = leaf_colors[leaf]
    return tree

def get_ripe_nodes(tree):
    # while there exist ripe nodes in T
    ripe_nodes = []
    for node in tree:
        node_gray = False
        no_gray_children = True
        ripe = False
        if tree[node].color == 'gray': node_gray = True

        for child in tree[node].children:
            if tree[child].color == 'gray':
                no_gray_children = False

        if node_gray and no_gray_children: ripe = True

        if ripe:
            ripe_nodes.append(node) # store node id
    return ripe_nodes

def tree_coloring(leaf_colored_tree):
    ripe_nodes = get_ripe_nodes(leaf_colored_tree)
    while len(ripe_nodes) != 0:
        for ripe_n in ripe_nodes:
            children_colors = []
            for child in leaf_colored_tree[ripe_n].children:
                children_colors.append(leaf_colored_tree[child].color)

            result = len(set(children_colors)) == 1
            if result:
                e = next(iter(children_colors))
                leaf_colored_tree[ripe_n].color = e
            else:
                leaf_colored_tree[ripe_n].color = 'purple'

        ripe_nodes = get_ripe_nodes(leaf_colored_tree) # get the leftover ripe nodes (newly generated)
    return leaf_colored_tree

def start():
    tree, leaf_colors = read_input("dataset.txt")
    leaf_colored_tree = leaf_coloring(tree, leaf_colors)
    colored_tree = tree_coloring(leaf_colored_tree)
    for node in colored_tree:
        print(str(node) + str(': ') + colored_tree[node].color)




if __name__ == '__main__':
    start()
