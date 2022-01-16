

def read_input(filename):
    input_file = open(filename, "r")
    genome1, genome2 = input_file.read().splitlines()
    input_file.close()
    return genome1, genome2

def hamming_distance(genome1, genome2):
    mismatch_count = 0
    for i in range(0, len(genome1)):
        if genome1[i] != genome2[i]:
            mismatch_count += 1
    return mismatch_count

def start():
    genome1, genome2 = read_input("dataset.txt")
    result = hamming_distance(genome1, genome2)
    print(result)


if __name__ == '__main__':
    start()
