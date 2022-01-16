from math import ceil

def read_input(filename):
    try:
        input_file = open(filename, "r")
        genome1 = input_file.readline().rstrip('\n')
        genome2 = input_file.readline().rstrip('\n')

        genome1 = genome1[:-1] # shave brackets
        genome1 = genome1[1:]
        genome1 = [int(i) for i in genome1.split(" ")]
        genome1.append(genome1[0])
        genome1 = [genome1]

        genome2 = genome2[:-1] # shave brackets
        genome2 = genome2[1:]
        genome2 = [int(i) for i in genome2.split(" ")]
        genome2.append(genome2[0])
        genome2 = [genome2]
        input_file.close()
    except:
        print("Exception caught, file probably doesnt exist")
    return genome1, genome2

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

def red_blue_cycles(red, blue):
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
                #print(node)
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
    return cycles, len(cycles)

def two_break_distance(p, q):
    # Find the colored edges of each genome
    red = colored_edges(p)
    blue = colored_edges(q)

    # Calculate the number of blocks in the breakpoint graph and find the cycles
    blocks = (len(red) + len(blue))/2
    cycles, num_of_cycles = red_blue_cycles(red, blue)

    # Finally calculate the 2-Break distance
    distance = blocks - num_of_cycles
    return distance


##########################################################

def two_break_on_genome_graph(graph, i1, i2, i3, i4):
    n = len(graph)
    i = 0
    possible_edges = [(i1, i2), (i2, i1), (i3, i4), (i4, i3)]
    graph = [e for e in graph if e not in possible_edges]
    graph.append((i1, i3))
    graph.append((i2, i4))
    return graph

##########################################################

def black_edges(n):
    edges = []
    for i in range(1, n+1):
        edge = (2*i-1, 2*i)
        edges.append(edge)
    return edges

def cycle_to_chromosome(cycle):
    n = ceil(len(cycle)/2)
    chromosome = []
    for j in range(1, n):
        if cycle[2*j-1] < cycle[2*j]:
            chromosome.append(int(cycle[2*j]/2))
        else:
            chromosome.append(int(-cycle[2*j-1]/2))
    return chromosome

def two_break_on_genome(genome, i1, i2, i3, i4):
    n = 0
    for c in genome:
        n += len(c)-1 # -1 because we dont want to count the extra block that we added for circularisation
    b_edges = black_edges(n)
    c_edges = colored_edges(genome)
    c_edges = two_break_on_genome_graph(c_edges, i1, i2, i3, i4)
    cycles, num_of_cycles = red_blue_cycles(b_edges, c_edges)

    p = []
    for cycle in cycles:
        cycle.insert(0, 0) # pad coz indexing starts at 1
        chromosome = cycle_to_chromosome(cycle)
        p.append(chromosome)
    return p

##########################################################

def two_break_sorting(p, q):
    # Fixing genome Q and sorting P to match Q
    blue = colored_edges(q)

    has_non_trivial = True
    sequence = [p]
    while has_non_trivial:
        red = colored_edges(p)
        cycles, num_of_cycles = red_blue_cycles(red, blue)
        for cycle in cycles:
            if len(cycle) >= 4: # non trivial
                p = two_break_on_genome(p, cycle[0], cycle[1], cycle[3], cycle[2]) # take red edges attacking blue
                sequence.append(p)
                break

        # circularise each of the chromosomes in the new broken up genome P.
        for c in p:
            c.append(c[0])

        # Check if we are done sorting based on the distance
        distance = two_break_distance(p, q)
        if distance == 0:
            has_non_trivial = False
    return sequence


def start():
    p, q = read_input("dataset.txt")
    result = two_break_sorting(p, q)
    # Format output
    for i in range(len(result)):
        for j in range(len(result[i])):
            result[i][j] = [str(c) for c in result[i][j]]
            for k in range(len(result[i][j])-1):
                if int(result[i][j][k]) > 0:
                    result[i][j][k] = '+' + result[i][j][k]
            print('(', *result[i][j][:-1], ')', end="")
        print()


if __name__ == '__main__':
    start()
