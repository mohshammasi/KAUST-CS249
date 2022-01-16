from math import ceil

def read_input(filename):
    try:
        input_file = open(filename, "r")
        cycle = input_file.readline().rstrip('\n')
        cycle = cycle[:-1]
        cycle = cycle[1:]
        cycle = [int(i) for i in cycle.split(" ")]
        cycle.insert(0, 0)
        input_file.close()
    except:
        print("Exception caught, file probably doesnt exist")
    return cycle

def cycle_to_chromosome(cycle):
    n = ceil(len(cycle)/2)
    chromosome = []
    for j in range(1, n):
        if cycle[2*j-1] < cycle[2*j]:
            chromosome.append(int(cycle[2*j]/2))
        else:
            chromosome.append(int(-cycle[2*j-1]/2))
    return chromosome

def start():
    cycle = read_input("dataset.txt")
    result = cycle_to_chromosome(cycle)
    result = [str(i) for i in result]
    for i in range(len(result)):
        if int(result[i]) > 0:
            result[i] = '+' + result[i]
    print('(', *result, ')')


if __name__ == '__main__':
    start()
