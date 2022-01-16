

# Defining a TrieNode type to use to build up the Trie
# This version is slightly modified to construct the Trie for text not multiple patterns
class TrieNode:
    # id label counter for inserting nodes
    id_count = 0
    def __init__(self, character, position=None):
        self.id = TrieNode.id_count
        self.char = character # the character stored in this node
        self.pos = position # position of this node in text

        # This is used only for leaf nodes to assign starting pos of this substring
        self.label = None

        # dictionary to store children (other TrieNodes) connected to this one
        self.children = {}

        # Increment the label number, the 'id'
        TrieNode.id_count += 1

class Trie(object):
    def __init__(self):
        # Create a root TrieNode with an empty char and ID 0
        self.root = TrieNode('')

    # Construct the full Trie from text
    def construct(self, text):
        n = len(text)
        for i in range(0, n-1):
            current_node = self.root
            for j in range(i, n-1):
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

    def print_trie(self, node):
        # Start recursively printing the edges from the given node to the leafs
        for n in node.children:
            print(str(node.id) + '->' + str(node.children[n].id) + ':'  \
                + node.children[n].char + ' - ' + str(node.pos))
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
        input_file.close()
    except IOError as e:
        print(e)
    return text

def modified_trie_construction(text):
    trie = Trie()
    trie.construct(text)
    return trie


def start():
    text = read_input("dataset.txt")
    print(text)
    trie = modified_trie_construction(text)
    trie.print_trie(trie.root) # formats the trie like the required output
    #trie.write_trie(trie.root) # write the trie to a file
    #print("Output written successfully to the textfile.")


if __name__ == '__main__':
    start()
