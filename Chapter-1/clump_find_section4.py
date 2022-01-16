

def read_input(filename):
    try:
        input_file = open(filename, "r")
        genome = input_file.readline()[:-1]
        k, l, t = input_file.readline().split(" ")
        input_file.close()
    except:
        print("Exception caught, file probably doesnt exist")
    return genome, int(k), int(l), int(t)

def frequency_table(text, k):
    frequency_dict = dict()
    n = len(text)
    for i in range(0, n-k):
        pattern = text[i:i+k]
        if pattern in frequency_dict:
            frequency_dict[pattern] += 1
        else:
            frequency_dict[pattern] = 1
    return frequency_dict

def find_clumps(genome, k, l, t):
    patterns = set()
    n = len(genome)
    for i in range(0, n-l):
        window = genome[i:i+l]
        frequency_map = frequency_table(window, k)
        for pattern in frequency_map:
            if frequency_map[pattern] >= t:
                patterns.add(pattern)
    return patterns


def start():
    genome, k, l, t = read_input("dataset.txt")
    result = find_clumps(genome, k, l, t)
    for string in result:
        print(string, end=" ")


if __name__ == '__main__':
    start()
