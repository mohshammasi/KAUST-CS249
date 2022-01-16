from operator import itemgetter


def read_input(filename):
    try:
        input_file = open(filename, "r")
        k, genome1, genome2 = input_file.read().splitlines()
        input_file.close()
    except:
        print("Exception caught, file probably doesnt exist")
    return int(k), genome1, genome2

def reverse_complement(string):
    nucleotides = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
    reverse_string = ''
    for i in range(len(string)-1, -1, -1):
        reverse_string += nucleotides[string[i]]
    return reverse_string

def shared_kmers(k, genome1, genome2):
    kmers = dict()
    n1 = len(genome1)
    n2 = len(genome2)

    for i in range(0, n1-k+1):
        kmers[genome1[i:i+k]] = kmers.get(genome1[i:i+k], []) + [i]

    shared_kmers = []
    for i in range(0, n2-k+1):
        kmer = genome2[i:i+k]
        if kmer in kmers:
            for pos in kmers[kmer]:
                shared_kmers.append((pos, i))

        rev_kmer = reverse_complement(kmer)
        if rev_kmer in kmers:
            for pos in kmers[rev_kmer]:
                shared_kmers.append((pos, i))
    shared_kmers = sorted(shared_kmers, key=itemgetter(1))
    return shared_kmers

def start():
    k, genome1, genome2 = read_input("dataset.txt")
    result = shared_kmers(k, genome1, genome2)
    #for kmer in result:
    #    print(kmer)
    #print(len(result))

    try:
        output_file = open("output.txt", "w")
        for kmer in result:
            output_file.write(str(kmer) + '\n')
        output_file.close()
        print("Output written successfully to the textfile.")
    except IOError as e:
        print('File I/O Error...', e)


if __name__ == '__main__':
    start()
