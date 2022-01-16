

def read_input(filename):
    input_file = open(filename, "r")
    k = input_file.readline().strip()
    dnas = input_file.read().splitlines()
    input_file.close()
    return int(k), dnas

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

def all_strings(k):
    if k == 0:
        print('Cannot generate all strings of 0-mers, Exiting...')
        exit()
    if k == 1:
        return ['A', 'T', 'C', 'G']
    else:
        patterns = []
        more_strings = all_strings(k-1)
        for string in more_strings:
                for n in nucleotides:
                    patterns.append(string+n)
        return patterns

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

def median_string(k, dnas):
    distance = float('inf')
    patterns = all_strings(k)
    n = len(patterns)
    for i in range(0, n):
        pattern = patterns[i]
        distance_between_patterns = distances_between_pattern_and_strings(pattern, dnas)
        if distance > distance_between_patterns:
            distance = distance_between_patterns
            median = pattern
    return median

def start():
    k, dnas = read_input("dataset.txt")
    result = median_string(k, dnas)
    print(result)


if __name__ == '__main__':
    start()
