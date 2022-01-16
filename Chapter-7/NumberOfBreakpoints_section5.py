

def read_input(filename):
    try:
        input_file = open(filename, "r")
        permutation = input_file.read().split(" ")
        permutation = [int(i) for i in permutation]
        n = len(permutation)
        permutation.append(n+1)
        permutation.insert(0, 0)
        input_file.close()
    except:
        print("Exception caught, file probably doesnt exist")
    return permutation

def number_of_breakpoints(permutation):
    n = len(permutation)

    adjacency_count = 0
    for i in range(0, n-1):
        if permutation[i+1] - permutation[i] == 1:
            adjacency_count += 1

    # calculate the number of breakpoints using (adj + breakpoints = n + 1)
    num_of_breakpoints = (n-1) - adjacency_count
    return num_of_breakpoints


def start():
    permutation = read_input("dataset.txt")
    result = number_of_breakpoints(permutation)
    print(result)


if __name__ == '__main__':
    start()
