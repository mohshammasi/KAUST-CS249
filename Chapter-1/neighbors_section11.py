

def read_input(filename):
    input_file = open(filename, "r")
    pattern, d = input_file.read().splitlines()
    input_file.close()
    return pattern, int(d)

nucleotides = ['A', 'T', 'C', 'G']

def immediate_neighbors(pattern):
    neighborhood = []
    for i in range(1, len(pattern)):
        symbol = pattern[i]
        for n in [n for n in nucleotides if n != symbol]:
            neighbor = pattern
            neighbor[i] = n
            neighborhood.append(neighbor)
    return neighborhood

def hamming_distance(genome1, genome2):
    mismatch_count = 0
    for i in range(0, len(genome1)):
        if genome1[i] != genome2[i]:
            mismatch_count += 1
    return mismatch_count

def neighbors(pattern, d):
    if d == 0:
        return pattern
    if len(pattern) == 1:
        return ['A', 'T', 'C', 'G']
    else:
        neighborhood = set()
        suffix_neighbors = neighbors(pattern[1:], d)
        for sn in suffix_neighbors:
            if hamming_distance(pattern[1:], sn) < d:
                for n in nucleotides:
                    neighborhood.add(n+sn)
            else:
                neighborhood.add(pattern[0]+sn)
        return neighborhood

def start():
    pattern, d = read_input("dataset.txt")
    result = neighbors(pattern, d)
    for neighbor in result:
        print(neighbor, end=" ")


if __name__ == '__main__':
    start()
