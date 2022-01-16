

def read_input(filename):
    input_file = open(filename, "r")
    pattern, genome = input_file.read().splitlines()
    input_file.close()
    return pattern, genome

def pattern_match(pattern, genome):
    positions = []
    for i in range(0, len(genome)):
        if genome[i:i+len(pattern)] == pattern:
            positions.append(i)
    return positions

def start():
    pattern, genome = read_input("dataset.txt")
    result = pattern_match(pattern, genome)
    for pos in result:
        print(pos, end=" ")


if __name__ == '__main__':
    start()
