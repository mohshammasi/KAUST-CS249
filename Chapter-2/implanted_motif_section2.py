

def read_input(filename):
    input_file = open(filename, "r")
    k, d = input_file.readline().strip().split(" ")
    dnas = [dna.strip() for dna in input_file]
    input_file.close()
    return int(k), int(d), dnas

nucleotides = ['A', 'T', 'C', 'G']

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
        neighborhood = []
        suffix_neighbors = neighbors(pattern[1:], d)
        for sn in suffix_neighbors:
            if hamming_distance(pattern[1:], sn) <= d:
                for n in nucleotides:
                    neighborhood.append(n+sn)
            else:
                neighborhood.append(pattern[0]+sn)
        return neighborhood

def pattern_count(text, pattern):
    count = 0
    for i in range(0, len(text)-len(pattern)):
        if text[i:i+len(pattern)] == pattern:
            count += 1
    return count

def approx_pattern_count(pattern, genome, d):
    count = 0
    for i in range(0, len(genome)-len(pattern)+1):
        hamming_dist = hamming_distance(genome[i:i+len(pattern)], pattern)
        if hamming_dist <= d:
            count += 1
    return count

def implanted_motif(k, d, dnas):
    patterns = set()
    n = len(dnas[0])
    for i in range(0, n-k):
        pattern = dnas[0][i:i+k]
        neighborhood = neighbors(pattern, d)
        for j in range(0, len(neighborhood)):
            neighbor = neighborhood[j]
            found_in_all = True
            for w in range(1, len(dnas)):
                count = approx_pattern_count(neighbor, dnas[w], d)
                if count == 0:
                    found_in_all = False
            if found_in_all:
                patterns.add(neighbor)
    return patterns

def start():
    k, d, dnas = read_input("dataset.txt")
    result = implanted_motif(k, d, dnas)
    for pattern in result:
        print(pattern, end=" ")


if __name__ == '__main__':
    start()
