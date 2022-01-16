import numpy as np

def read_input(filename):
    try:
        input_file = open(filename, "r")
        n, m = input_file.readline().rstrip('\n').split(" ")

        # Read the down and right matrices
        down = []
        right = []
        reading_down = True
        for line in input_file:
            if line == '-\n':
                reading_down = False
                continue

            if reading_down:
                down.append(line.rstrip('\n').split(' '))
            else:
                right.append(line.rstrip('\n').split(' '))

        # Convert the lists of lists to numpy arrays
        down = np.array(down, dtype=int)
        right = np.array(right, dtype=int)

        input_file.close()
    except:
        print("Exception caught, file probably doesnt exist")
    return int(n), int(m), down, right

def manhattan_tourist(n, m, down, right):
    longest_path = np.zeros((n+1, m+1), dtype=int)

    for i in range(1, n):
        longest_path[i][0] = longest_path[i-1][0] + down[i-1][0]
    for j in range(1, m):
        longest_path[0][j] = longest_path[0][j-1] + right[0][j-1]
    for i in range(1, n+1):
        for j in range(1, m+1): # compare vertical and horizontal path
            longest_path[i][j] = max(longest_path[i-1][j] + down[i-1][j], longest_path[i][j-1] + right[i][j-1])

    return longest_path[n][m]

def start():
    n, m, down, right = read_input("dataset.txt")
    result = manhattan_tourist(n, m, down, right)
    print(result)

if __name__ == '__main__':
    start()
