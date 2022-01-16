

def read_input(filename):
    input_file = open(filename, "r")
    genome = input_file.readline().strip()
    k = input_file.readline().strip()
    profile_matrix = [[float(num) for num in row.split(' ')] for row in input_file]
    input_file.close()
    return genome, int(k), profile_matrix

def profile_most_probable_kmer(genome, k, profile_matrix):
    n = len(genome)
    most_probable_pattern = ''
    most_probable_probability = 0
    for i in range(0, n-k+1):
        pattern = genome[i:i+k]
        probability = 1
        for offset, n in enumerate(pattern):
            if n == 'A':
                probability *= profile_matrix[0][offset]
            elif n == 'C':
                probability *= profile_matrix[1][offset]
            elif n == 'G':
                probability *= profile_matrix[2][offset]
            elif n == 'T':
                probability *= profile_matrix[3][offset]
            else:
                print('Weird string, Exiting...')
                exit()

        if probability > most_probable_probability:
            most_probable_pattern = pattern
            most_probable_probability = probability
    return most_probable_pattern

def start():
    genome, k, profile_matrix = read_input("dataset.txt")
    result = profile_most_probable_kmer(genome, k, profile_matrix)
    print(result)


if __name__ == '__main__':
    start()
