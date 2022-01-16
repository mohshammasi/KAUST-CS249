import random
from operator import itemgetter
from copy import deepcopy

# Defining a TrieNode type to use to build up the Trie
# This version is slightly modified to construct the Trie for text not multiple patterns
class TrieNode:
    # id label counter for inserting nodes
    id_count = 0
    def __init__(self, character, depth, position=None):
        self.id = TrieNode.id_count
        self.char = character # the character stored in this node
        self.pos = position # position of this node in text
        self.length = None

        # This is used only for leaf nodes to assign starting pos of this substring
        self.label = None

        # Added for the longest repeat problem
        self.depth = depth

        # dictionary to store children (other TrieNodes) connected to this one
        self.children = {}

        # Increment the label number, the 'id'
        TrieNode.id_count += 1

class Trie(object):
    def __init__(self):
        # Create a root TrieNode with an empty char and ID 0, at level 0
        self.root = TrieNode('', 0)

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
                    # For the longest repeat challenge, add the level information
                    # to each new node added
                    depth = current_node.depth + 1
                    new_node = TrieNode(current_symbol, depth, j)
                    current_node.children[current_symbol] = new_node
                    current_node = new_node

            if len(current_node.children) == 0:
                self.label = i

    def print_tree_nodes(self, node):
        for n in node.children:
            print('Node pos: ' + str(node.children[n].pos) + ' and ' \
                + str(node.children[n].length) + ' depth is ' + str(node.children[n].depth))
            self.print_tree_nodes(node.children[n])

    def print_tree_symbols(self, node):
        for n in node.children:
            print('Node id: ' + str(node.children[n].id) + ' node s: ' + str(node.children[n].char))
            self.print_tree_symbols(node.children[n])

    def print_tree_strings(self, node, text):
        for n in node.children:
            i = node.children[n].pos
            j = node.children[n].pos + node.children[n].length
            print(text[i:j])
            self.print_tree_strings(node.children[n], text)

def read_input(filename):
    try:
        input_file = open(filename, "r")
        text = input_file.readline().rstrip('\n')
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
                        temp.children[child].depth = path[0].depth + 1
                        path[0].children[child] = temp.children[child]
                    break
            except KeyError as e:
                print('Something wrong', e)
###################################################


# THIS CODE FAILS VERY RARELY FOR SOME REASON I CANNOT FIGURE OUT
def longest_repeat(node, text, repeated_patterns, current_pattern):
    copy = current_pattern
    for i, n in enumerate(node.children):
        if node.id == 0:
            current_pattern = ''
        elif len(node.children) > 2:
            current_pattern = copy

        if len(node.children[n].children) == 0:
            repeated_patterns.add(current_pattern)
            continue

        start = node.children[n].pos
        end = node.children[n].pos + node.children[n].length
        current_pattern = current_pattern + text[start:end]
        repeated_patterns = longest_repeat(node.children[n], text, repeated_patterns, current_pattern)
    return repeated_patterns


def start():
    text = read_input("dataset.txt")
    text = text + '$'
    trie = modified_trie_construction(text)
    modified_suffix_tree_construction(trie.root) # convert trie to tree
    #trie.print_tree_nodes(trie.root)
    #trie.print_tree_symbols(trie.root)

    repeated_patterns = set()
    current_pattern = ''
    result = longest_repeat(trie.root, text, repeated_patterns, current_pattern)
    print(max(result, key=len))


if __name__ == '__main__':
    start()
