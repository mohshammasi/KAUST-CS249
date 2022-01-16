import random
from copy import deepcopy

# Defining a TrieNode type to use to build up the Trie
# This version is slightly modified to construct the Trie for text not multiple patterns
class TrieNode:
    # id label counter for inserting nodes
    id_count = 0
    def __init__(self, character, position=None):
        self.id = TrieNode.id_count
        self.char = character # the character stored in this node
        self.pos = position # position of this node in text
        self.length = None

        # This is used only for leaf nodes to assign starting pos of this substring
        self.label = None

        # dictionary to store children (other TrieNodes) connected to this one
        self.children = {}

        self.color = 'gray'

        # Increment the label number, the 'id'
        TrieNode.id_count += 1

    def __str__(self):
        return "ID: %s, color: %s" \
               % (self.id, self.color)

class Trie(object):
    def __init__(self):
        # Create a root TrieNode with an empty char and ID 0
        self.root = TrieNode('')

    # Construct the full Trie from text
    def construct(self, text):
        n = len(text)
        for i in range(0, n):
            current_node = self.root
            for j in range(i, n):
                current_symbol = text[j]
                if current_symbol in current_node.children:
                    current_node = current_node.children[current_symbol]

                # If the character is not found, create a new node in the trie
                else:
                    new_node = TrieNode(current_symbol, j)
                    current_node.children[current_symbol] = new_node
                    current_node = new_node

            if len(current_node.children) == 0:
                self.label = i

    def dictionary_tree(self, node, tree):
        for n in node.children:
            tree[node.children[n].id] = node.children[n]
            self.dictionary_tree(node.children[n], tree)
        return tree


###################################################

def read_input(filename):
    try:
        input_file = open(filename, "r")
        text1 = input_file.readline().rstrip('\n')
        text2 = input_file.readline().rstrip('\n')
        text = text1 + '#' + text2 + '$'
        input_file.close()
    except IOError as e:
        print(e)
    return text

def modified_trie_construction(text):
    trie = Trie()
    trie.construct(text)
    return trie

def modified_suffix_tree_construction(node):
    for n in node.children:
        path = []
        current_node = node.children[n]
        path.append(current_node)
        non_branching = True
        while non_branching:
            try:
                if len(current_node.children) == 0:
                    # we hit a leaf, so substitute all nodes along the path by
                    # a single node
                    path_len = len(path)
                    path[0].length = path_len
                    path[0].children.clear()
                    break
                elif len(current_node.children) == 1:
                    next = list(current_node.children.items())[0] # only 1 item
                    current_node = current_node.children[next[0]]
                    path.append(current_node) # add new node to our path
                else:
                    path_len = len(path)
                    path[0].length = path_len
                    modified_suffix_tree_construction(current_node)
                    temp = deepcopy(current_node)
                    # when we clear, python garbage collection delete the nodes
                    # from memory, therefore we make a temp copy of the node
                    path[0].children.clear()
                    for child in temp.children:
                        path[0].children[child] = temp.children[child]
                    break
            except KeyError as e:
                print('Something wrong', e)


###################################################


def fix_children(tree):
    for node in tree:
        # add keys with the ids instead of symbols in the children dicts
        #print(tree[node].children.items())
        for child in list(tree[node].children.keys()):
            tree[node].children[tree[node].children[child].id] = tree[node].children[child]
            del tree[node].children[child]
    return tree

def leaf_coloring(tree, text):
    # find the index of the '#' and '$'
    n = len(text)
    dollar_i = n-1
    hash_i = text.index('#')

    for node in tree:
        # Only color leaves
        if len(tree[node].children) == 0:
            if tree[node].pos <= hash_i:
                tree[node].color = 'blue'
            elif (tree[node].pos > hash_i) and (tree[node].pos <= dollar_i):
                tree[node].color = 'red'
            else:
                print('Something is wrong here...')
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


def longest_shared_substring(node, shared_substrings, ss, text):
    found_purple = False
    copy = ss
    for n in node.children:
        if node.id == 0:
            ss = ''
        if found_purple:
            ss = copy

        if node.children[n].color == 'purple':
            found_purple = True
            start = node.children[n].pos
            end = node.children[n].pos + node.children[n].length
            ss += text[start:end]
            shared_substrings = longest_shared_substring(node.children[n], shared_substrings, ss, text)

    if not found_purple:
        shared_substrings.append(ss)
    return shared_substrings

# only called on blue nodes, if a node is blue then all its children are blue
# but we only want to recurse at most 1 time to find the shortest
def find_shortest_recurs(node, non_shared_ss, ss, text):
    copy = ss
    for n in node.children:
        ss = copy
        start = node.children[n].pos
        end = node.children[n].pos + node.children[n].length
        ss += text[start:end]
        non_shared_ss.append(ss)
        non_shared_ss = find_shortest_recurs(node.children[n], non_shared_ss, ss, text)
    return non_shared_ss


# Since we are iterating in a bfs like manner, the first non shared substring we
# find will be the shortest. The length gets longer as we go deeper
def shortest_non_shared_substring(node, text):
    purple_nodes = [(node, '')]
    non_shared_ss = []
    while len(purple_nodes) != 0:
        tuple = purple_nodes.pop(0)
        node = tuple[0]
        path = tuple[1]
        copy = path
        for n in node.children:
            if node.children[n].color == 'blue':
                start = node.children[n].pos
                end = node.children[n].pos + node.children[n].length
                string = text[start:end]

                if node.id == 0:
                    path = ''
                else:
                    path = copy

                if string[0] != '#':
                    path += string[0]
                    non_shared_ss.append(path)

            elif node.children[n].color == 'purple':
                if node.id == 0:
                    path = ''
                else:
                    path = copy
                start = node.children[n].pos
                end = node.children[n].pos + node.children[n].length
                path += text[start:end]
                # add to recursion list
                purple_nodes.append((node.children[n], path))
    return non_shared_ss


def start():
    text = read_input("dataset.txt")
    trie = modified_trie_construction(text)
    modified_suffix_tree_construction(trie.root) # trie becomes tree

    tree = dict()
    tree[trie.root.id] = trie.root
    tree = trie.dictionary_tree(trie.root, tree)
    tree = fix_children(tree) # the children are stil messed up after converting to dict


    tree = leaf_coloring(tree, text) # color the leafs red or blue
    colored_tree = tree_coloring(tree) # color the entire tree
    result = shortest_non_shared_substring(tree[0], text)
    print(min(result, key=len)) # output the shortest one

if __name__ == '__main__':
    start()
