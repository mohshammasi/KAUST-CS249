

def read_input(filename):
    input_file = open(filename, "r")
    pattern, genome, d = input_file.read().splitlines()
    input_file.close()
    return pattern, genome, int(d)

def hamming_distance(genome1, genome2):
    mismatch_count = 0
    for i in range(0, len(genome1)):
        if genome1[i] != genome2[i]:
            mismatch_count += 1
    return mismatch_count

def approx_pattern_match(pattern, genome, d):
    positions = []
    for i in range(0, len(genome)-len(pattern)+1):
        hamming_dist = hamming_distance(genome[i:i+len(pattern)], pattern)
        if hamming_dist <= d:
            positions.append(i)
    return positions

def start():
    pattern, genome, d = read_input("dataset.txt")
    result = approx_pattern_match(pattern, genome, d)
    for pos in result:
        print(pos, end=" ")
    print(len(result))


if __name__ == '__main__':
    start()
