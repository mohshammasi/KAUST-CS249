
def read_input(filename):
    try:
        input_file = open(filename, "r")
        genome = input_file.readline().rstrip('\n')
        genome = genome.split(")(")
        p = []
        for i in range(0, len(genome)):
            genome[i] = genome[i].replace("(", "")
            genome[i] = genome[i].replace(")", "")
            chromosome = genome[i].split(" ")
            chromosome.append(chromosome[0]) # circular chromosome
            chromosome = [int(i) for i in chromosome]
            p.append(chromosome)
        input_file.close()
    except:
        print("Exception caught, file probably doesnt exist")
    return p

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
        print(nodes)
        nodes.insert(0, 0) # want our nodes to start at 1, just pad
        n = len(chromosome)
        for j in range(1, n):
            edges.append((nodes[2*j], nodes[2*j+1]))
    return edges

def start():
    p = read_input("dataset.txt")
    result = colored_edges(p)
    for edge in result:
        print(edge, end=", ")
    print()


if __name__ == '__main__':
    start()
