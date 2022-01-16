

def read_input(filename):
    try:
        input_file = open(filename, "r")
        chromosome = input_file.readline().rstrip('\n')
        chromosome = chromosome[:-1]
        chromosome = chromosome[1:]
        chromosome = [int(i) for i in chromosome.split(" ")]
        input_file.close()
    except:
        print("Exception caught, file probably doesnt exist")
    return chromosome

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

def start():
    chromosome = read_input("dataset.txt")
    result = chromosome_to_cycle(chromosome)
    print('(', *result, ')')


if __name__ == '__main__':
    start()
