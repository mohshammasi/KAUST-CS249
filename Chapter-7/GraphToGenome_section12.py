import ast
from math import ceil

def read_input(filename):
    try:
        input_file = open(filename, "r")
        edges = input_file.readline().rstrip('\n')
        edges = ast.literal_eval(edges)
        input_file.close()
    except:
        print("Exception caught, file probably doesnt exist")
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

def graph_to_genome(edges):
    # First get the cycles from the colored edges
    cycles = []
    cycle = []
    for edge in edges:
        if edge[0] < edge[1]:
            cycle.append(edge[0])
            cycle.append(edge[1])
        else:
            cycle.append(edge[0])
            cycle.insert(0, edge[1])
            cycles.append(cycle)
            cycle = []

    p = []
    for cycle in cycles:
        cycle.insert(0, 0) # pad coz indexing starts at 1
        chromosome = cycle_to_chromosome(cycle)
        p.append(chromosome)
    return p

def start():
    edges = read_input("dataset.txt")
    result = graph_to_genome(edges)
    for i in range(len(result)):
        result[i] = [str(c) for c in result[i]]
        for j in range(len(result[i])):
            if int(result[i][j]) > 0:
                result[i][j] = '+' + result[i][j]
        print('(', *result[i], ')', end="")
    print()


if __name__ == '__main__':
    start()
