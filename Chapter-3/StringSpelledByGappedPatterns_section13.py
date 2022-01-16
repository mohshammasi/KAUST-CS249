

def read_input(filename):
    try:
        input_file = open(filename, "r")
        k, d = input_file.readline().strip().split(" ")
        kdmers = input_file.read().splitlines()
        input_file.close()
    except:
        print("Exception caught, file probably doesnt exist")
    return int(k), int(d), kdmers

def prefix(pattern):
    return pattern[:-1]

def suffix(pattern):
    return pattern[1:]

def genome_path(patterns):
    # Get n and k, helps with debugging as well
    n = len(patterns)
    k = len(patterns[0])

    # Build the string
    genome = patterns[0]
    for i in range(1, n):
        genome += patterns[i][k-1]
    return genome

def string_spelled_by_gapped_patterns(kdmers, k, d):
    # Split the kdmers in to first_patterns and second_patterns
    first_patterns = []
    second_patterns = []
    for kdmer in kdmers:
        kdmer = kdmer.split('|')
        first_patterns.append(kdmer[0])
        second_patterns.append(kdmer[1])

    prefix_string = genome_path(first_patterns)
    suffix_string = genome_path(second_patterns)

    for i in range(k+d+1, len(prefix_string)):
        if prefix_string[i] != suffix_string[i-k-d]:
            return 'There is no string spelled by the gapped patterns'
    prefix_string += suffix_string[-(k+d):]
    return prefix_string



def start():
    k, d, kdmers = read_input("dataset.txt")
    result = string_spelled_by_gapped_patterns(kdmers, k, d)
    print(result)
    print(len(result))


if __name__ == '__main__':
    start()
