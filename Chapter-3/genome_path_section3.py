

def read_input(filename):
    try:
        input_file = open(filename, "r")
        patterns = input_file.read().splitlines()
        input_file.close()
    except:
        print("Exception caught, file probably doesnt exist")
    return patterns

def genome_path(patterns):
    # Get n and k, helps with debugging as well
    n = len(patterns)
    k = len(patterns[0])

    # Build the string
    genome = patterns[0]
    for i in range(1, n):
        genome += patterns[i][k-1]
    return genome

def start():
    patterns = read_input("dataset.txt")
    result = genome_path(patterns)
    print(result)



if __name__ == '__main__':
    start()
