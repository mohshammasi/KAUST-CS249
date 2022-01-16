import numpy as np

def read_input(filename):
    try:
        input_file = open(filename, "r")
        bwt = input_file.readline().rstrip('\n')
        patterns = input_file.read().rstrip('\n').split(' ')
        input_file.close()
    except IOError as e:
        print(e)
    return bwt, patterns

def better_bwmatching(first_occurance, bwt, pattern, count, map):
    n = len(bwt)
    top = 0
    bottom = n - 1
    while top <= bottom:
        if pattern != '':
            s = pattern[-1:] # get the last character of the pattern
            pattern = pattern[:-1] # update pattern

            # Make sure that we found at least 1 occurance of 's'
            above = count[top][map[s]]
            below = count[bottom+1][map[s]]
            if below - above > 0:
                top = first_occurance[s] + count[top][map[s]]
                bottom = first_occurance[s] + count[bottom+1][map[s]] - 1
            else:
                return 0
        else:
            return (bottom - top + 1)

def create_first_occurance_array(fc):
    first_occurance = dict()
    for i, c in enumerate(fc):
        if c not in first_occurance:
            first_occurance[c] = i
    return first_occurance

def count_matrix(bwt, first_occurance):
    n = len(bwt)
    m = len(first_occurance)

    # character index map
    idx_map = dict()
    i = 0
    for char in sorted(first_occurance):
        idx_map[char] = i
        i += 1

    count = np.zeros((n+1, m), dtype=int)
    row = [0] * m
    i = 0 # index string
    row_num = 1 # index rows
    while row_num <= n:
        idx = idx_map[bwt[i]]
        row[idx] += 1
        count[row_num] = row
        i += 1
        row_num += 1
    return count, idx_map


def start():
    bwt, patterns = read_input("dataset.txt")
    s = list(bwt)
    s.sort()
    fc = ''.join(s) # first column

    # Create the first occurance array and the Count matrix
    first_occurance = create_first_occurance_array(fc)
    count, map = count_matrix(bwt, first_occurance)

    # Get the number of matches for each pattern in patterns
    patterns_num_of_matches = []
    for pattern in patterns:
        num_of_matches = better_bwmatching(first_occurance, bwt, pattern, count, map)
        patterns_num_of_matches.append(num_of_matches)

    # Output the results
    for num in patterns_num_of_matches:
        print(num, end=" ")
    print()

if __name__ == '__main__':
    start()
