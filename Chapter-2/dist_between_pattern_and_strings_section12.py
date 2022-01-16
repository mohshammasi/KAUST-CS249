

def read_input(filename):
    input_file = open(filename, "r")
    pattern = input_file.readline().strip()
    dnas = input_file.read().split(" ")
    input_file.close()
    return pattern, dnas

nucleotides = ['A', 'T', 'C', 'G']

def hamming_distance(genome1, genome2):
    mismatch_count = 0
    for i in range(0, len(genome1)):
        if genome1[i] != genome2[i]:
            mismatch_count += 1
    return mismatch_count

def distances_between_pattern_and_strings(pattern, dnas):
    k = len(pattern)
    distance = 0
    for dna in dnas:
        hamming_dist = k+1
        n = len(dna)
        for i in range(0, n-k+1):
            pattern_ = dna[i:i+k]
            hamming_dist_pattern_ = hamming_distance(pattern, pattern_)
            if hamming_dist > hamming_dist_pattern_:
                hamming_dist = hamming_dist_pattern_
        distance += hamming_dist
    return distance

def start():
    pattern, dnas = read_input("dataset.txt")
    result = distances_between_pattern_and_strings(pattern, dnas)
    print(result)


if __name__ == '__main__':
    start()
