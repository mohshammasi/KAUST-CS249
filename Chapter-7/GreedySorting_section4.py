

def read_input(filename):
    try:
        input_file = open(filename, "r")
        permutation = input_file.read().split(" ")
        permutation = [int(i) for i in permutation]
        permutation.insert(0, 0)
        input_file.close()
    except:
        print("Exception caught, file probably doesnt exist")
    return permutation

def reverse_sublist(list, s, e):
    list[s:e] = list[s:e][::-1]
    return list

def greedy_sorting(permutation):
    n = len(permutation)
    approx_reversal_distance = 0

    for i in range(1, n):
        if abs(permutation[i]) != i:
            s = i
            j = i
            while True:
                if abs(permutation[j]) == i:
                    permutation[j] = -(permutation[j])
                    e = j+1
                    break
                else:
                    permutation[j] = -(permutation[j]) # flip sign
                    j += 1
            permutation = reverse_sublist(permutation, s, e)

            # Print required output for code challenge, formatting:
            for w in range (1, n):
                if permutation[w] < 0:
                    if w == n-1:
                        print(str(permutation[w]))
                    else:
                        print(str(permutation[w]), end=" ")
                else:
                    if w == n-1:
                        print('+' + str(permutation[w]))
                    else:
                        print('+' + str(permutation[w]), end=" ")

            approx_reversal_distance += 1

        if permutation[i] == (-i):
            permutation[i] = -(permutation[i])
            # Print required output for code challenge, formatting:
            for w in range (1, n):
                if permutation[w] < 0:
                    if w == n-1:
                        print(str(permutation[w]))
                    else:
                        print(str(permutation[w]), end=" ")
                else:
                    if w == n-1:
                        print('+' + str(permutation[w]))
                    else:
                        print('+' + str(permutation[w]), end=" ")
            approx_reversal_distance += 1
    return approx_reversal_distance


def start():
    permutation = read_input("dataset.txt")
    result = greedy_sorting(permutation)
    print(result)


if __name__ == '__main__':
    start()
