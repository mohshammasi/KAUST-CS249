

# Defining a TrieNode type to use to build up the Trie
class TrieNode:
    # id label counter for inserting nodes
    label_count = 0
    def __init__(self, character):
        self.id = TrieNode.label_count
        self.char = character # the character stored in this node

        # dictionary to store children (other TrieNodes) connected to this one
        self.children = {}

        # Increment the label number, the 'id'
        TrieNode.label_count += 1

class Trie(object):
    def __init__(self):
        # Create a root TrieNode with an empty char and ID 0
        self.root = TrieNode('')

    # Insert new TrieNodes into the Trie
    def insert(self, string):
        current_node = self.root

        for c in string:
            # Check if there is no child containing the character, if so then
            # create a new child for the current node
            if c in current_node.children:
                current_node = current_node.children[c]

            # If the character is not found, create a new node in the trie
            else:
                new_node = TrieNode(c)
                current_node.children[c] = new_node
                current_node = new_node

    def print_trie(self, node):
        # Start recursively printing the edges from the given node to the leafs
        for n in node.children:
            print(str(node.id) + '->' + str(node.children[n].id) + ':'  \
                + node.children[n].char)
            self.print_trie(node.children[n])

    # This is APPENDING to the file, make sure the file is empty so it doesnt mix up
    def write_trie(self, node):
        try:
            output_file = open("output.txt", "a")
            # Start recursively writing the edges from the given node to the leafs
            for n in node.children:
                output_file.write(str(node.id) + '->' + str(node.children[n].id) \
                    + ':' + node.children[n].char + '\n')
                self.write_trie(node.children[n])
            output_file.close()
        except IOError as e:
            print('File I/O Error...', e)

def read_input(filename):
    try:
        input_file = open(filename, "r")
        text = input_file.readline().rstrip('\n')
        patterns = input_file.read().splitlines()
        input_file.close()
    except IOError as e:
        print(e)
    return text, patterns

def trie_construction(patterns):
    trie = Trie()
    for pattern in patterns:
        trie.insert(pattern)
    return trie

def prefix_trie_matching(text, trie):
    n = len(text)
    c = text[0]
    i = 1
    current_node = trie.root
    pattern = ''
    while True:
        if len(current_node.children) == 0: # we hit a leaf
            return pattern
        elif c in current_node.children:
            current_node = current_node.children[c]
            if i < n:
                c = text[i]
                i += 1
        else:
            return "NO MATCHES FOUND"

def trie_matching(text, trie):
    positions = []
    n = len(text)
    for i in range(0, n):
        match = prefix_trie_matching(text[i:], trie)
        if match != 'NO MATCHES FOUND':
            positions.append(i)
    return positions

def start():
    text, patterns = read_input("dataset.txt")
    trie = trie_construction(patterns)
    #trie.print_trie(trie.root) # formats the trie like the required output
    positions = trie_matching(text, trie)
    for pos in positions:
        print(pos, end=" ")
    print()

if __name__ == '__main__':
    start()
