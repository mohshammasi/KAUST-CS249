import ast
from math import ceil

def read_input(filename):
    try:
        input_file = open(filename, "r")
        chromosome = input_file.readline().rstrip('\n')
        chromosome = chromosome[:-1] # shave brackets
        chromosome = chromosome[1:]
        chromosome = [int(i) for i in chromosome.split(" ")]
        chromosome.append(chromosome[0])
        chromosome = [chromosome]
        two_break = input_file.readline().rstrip('\n').split(", ")
        two_break = [int(i) for i in two_break]
        input_file.close()
    except:
        print("Exception caught, file probably doesnt exist")
    return chromosome, two_break

#############################################

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
        #print(nodes)
        nodes.insert(0, 0) # want our nodes to start at 1, just pad
        n = len(chromosome)
        for j in range(1, n):
            edges.append((nodes[2*j], nodes[2*j+1]))
    return edges

#############################################

def two_break_on_genome_graph(graph, i1, i2, i3, i4):
    n = len(graph)
    i = 0
    possible_edges = [(i1, i2), (i2, i1), (i3, i4), (i4, i3)]
    graph = [e for e in graph if e not in possible_edges]
    graph.append((i1, i3))
    graph.append((i2, i4))
    return graph

#############################################

def cycle_to_chromosome(cycle):
    n = ceil(len(cycle)/2)
    chromosome = []
    for j in range(1, n):
        if cycle[2*j-1] < cycle[2*j]:
            chromosome.append(int(cycle[2*j]/2))
        else:
            chromosome.append(int(-cycle[2*j-1]/2))
    return chromosome

#############################################

def black_edges(n):
    edges = []
    for i in range(1, n+1):
        edge = (2*i-1, 2*i)
        edges.append(edge)
    return edges


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
    return cycles

def two_break_on_genome(genome, i1, i2, i3, i4):
    n = len(genome[0])
    b_edges = black_edges(n)
    c_edges = colored_edges(genome)
    c_edges = two_break_on_genome_graph(c_edges, i1, i2, i3, i4)
    cycles = red_blue_cycles(b_edges, c_edges)

    p = []
    for cycle in cycles:
        cycle.insert(0, 0) # pad coz indexing starts at 1
        chromosome = cycle_to_chromosome(cycle)
        p.append(chromosome)
    return p


def start():
    genome, two_break = read_input("dataset.txt")
    result = two_break_on_genome(genome, *two_break)
    for i in range(len(result)):
        result[i] = [str(c) for c in result[i]]
        for j in range(len(result[i])):
            if int(result[i][j]) > 0:
                result[i][j] = '+' + result[i][j]
        print('(', *result[i], ')', end="")
    print()


if __name__ == '__main__':
    start()
