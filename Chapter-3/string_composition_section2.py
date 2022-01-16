

def read_input(filename):
    try:
        input_file = open(filename, "r")
        k, genome = input_file.read().splitlines()
        input_file.close()
    except:
        print("Exception caught, file probably doesnt exist")
    return int(k), genome

def string_composition(k, genome):
    composition = []
    for i in range(0, len(genome)-k+1):
        pattern = genome[i:i+k]
        composition.append(pattern)
    return composition

def start():
    k, genome = read_input("dataset.txt")
    result = string_composition(k, genome)
    for kmer in result:
        print(kmer)
    print(len(result))


if __name__ == '__main__':
    start()
