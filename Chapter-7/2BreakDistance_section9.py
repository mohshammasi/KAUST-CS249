

def read_input(filename):
    try:
        input_file = open(filename, "r")
        genome1 = input_file.readline().rstrip('\n')
        genome2 = input_file.readline().rstrip('\n')
        genome1 = genome1.split(")(")
        genome2 = genome2.split(")(")

        p = []
        q = []
        n = 0
        for i in range(0, len(genome1)):
            genome1[i] = genome1[i].replace("(", "")
            genome1[i] = genome1[i].replace(")", "")
            chromosome = genome1[i].split(" ")
            chromosome.append(chromosome[0])
            chromosome = [int(i) for i in chromosome]
            p.append(chromosome)
        for i in range(0, len(genome2)):
            genome2[i] = genome2[i].replace("(", "")
            genome2[i] = genome2[i].replace(")", "")
            chromosome = genome2[i].split(" ")
            chromosome.append(chromosome[0])
            chromosome = [int(i) for i in chromosome]
            q.append(chromosome)

        input_file.close()
    except:
        print("Exception caught, file probably doesnt exist")
    return p, q

##########################################################
def chromosome_to_cycle(chromosome):
    n = len(chromosome)
    nodes = []
    for j in range(0, n):
        i = chromosome[j]
        if i > 0:
            nodes.append(2*i-1)
            nodes.append(2*i)
        else:
            nodes.append(-2*i)
            nodes.append(-2*i-1)
    return nodes

def colored_edges(p):
    edges = []
    for chromosome in p:
        nodes = chromosome_to_cycle(chromosome)
        nodes.insert(0, 0) # want our nodes to start at 1, just pad
        n = len(chromosome)
        #print(n)
        for j in range(1, n):
            edges.append((nodes[2*j], nodes[2*j+1]))
    return edges
##########################################################

def count_red_blue_cycles(red, blue):
    cycles = []
    blocks = len(red) + len(blue)

    # Build an adjacency list for each node using red edges and blue edges
    red_al = dict()
    for edge in red:
        red_al[edge[0]] = edge[1]
        red_al[edge[1]] = edge[0]

    blue_al = dict()
    for edge in blue:
        blue_al[edge[0]] = edge[1]
        blue_al[edge[1]] = edge[0]

    visited = dict()
    for node in range(1, blocks):
        if node not in visited:
            visited[node] = 'V'
            cycle = [node]
            color = 'R'
            while True:
                if color == 'R':
                    node = red_al[node]
                    color = 'B' # switch
                elif color == 'B':
                    node = blue_al[node]
                    color = 'R'

                if node == cycle[0]:
                    cycles.append(cycle)
                    break
                cycle.append(node)
                visited[node] = 'V'
    return len(cycles)

##########################################################


def two_break_distance(p, q):
    # Find the colored edges of each genome
    red = colored_edges(p)
    blue = colored_edges(q)

    # Calculate the number of blocks in the breakpoint graph and find the cycles
    blocks = (len(red) + len(blue))/2
    num_of_cycles = count_red_blue_cycles(red, blue)

    # Finally calculate the 2-Break distance
    distance = blocks - num_of_cycles
    return distance


def start():
    p, q = read_input("dataset.txt")
    result = two_break_distance(p, q)
    print(result)


if __name__ == '__main__':
    start()
