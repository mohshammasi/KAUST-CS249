import numpy as np
from operator import itemgetter
from math import floor

def read_input(filename):
    try:
        input_file = open(filename, "r")
        text = input_file.readline().rstrip('\n')
        patterns = input_file.readline().rstrip('\n').split(' ')
        d = input_file.readline().rstrip('\n')
        input_file.close()
    except IOError as e:
        print(e)
    return text, patterns, int(d)

def string_dict(string, idx_keys=False):
    string_d = dict()
    chars_found = dict()
    for i, c in enumerate(string):
        if c in chars_found:
            key = c + str(chars_found[c] + 1)
            if idx_keys:
                string_d[i] = key
            else:
                string_d[key] = i
            chars_found[c] = chars_found.get(c, 0) + 1 # record the char
        else:
            key = c + '1'
            if idx_keys:
                string_d[i] = key
            else:
                string_d[key] = i
            chars_found[c] = chars_found.get(c, 0) + 1 # record the char
    return string_d

def last_to_first_array(fc, bwt):
    n = len(bwt)
    bwt_dict = string_dict(bwt, idx_keys=True)
    fc_dict = string_dict(fc)

    # Build the last to first array using these 2 dictionaries
    ltfa = dict()
    for idx in bwt_dict:
        char = bwt_dict[idx] # get char at index
        idx2 = fc_dict[char] # get the index corresponding to that char in fc
        ltfa[idx] = idx2 # map index to index
    return ltfa

def suffix_array(text):
    n = len(text)
    suffix_array = []
    for i in range(0, n):
        suffix_array.append((i, text[i:n]))
    suffix_array.sort(key=itemgetter(1)) # sort lexicographically
    suffix_array = [tup[0] for tup in suffix_array] # remove the strings
    return suffix_array

def partial_suffix_array(sa, k):
    partial_suffix_array = dict()
    for i, val in enumerate(sa):
        if val % k == 0:
            partial_suffix_array[i] = val
    return partial_suffix_array

def burrow_wheeler_transform(text):
    n = len(text)
    cyclic_rotations = []
    for i in range(0, n):
        rotation = text[n-i:n] + text[0:n-i]
        cyclic_rotations.append(rotation)
    cyclic_rotations.sort() # order them lexicographically

    bwm = np.zeros((n, n), dtype='object')
    for i, string in enumerate(cyclic_rotations):
        bwm[i] = list(string)

    transposed_bwm = np.array(bwm).T.tolist()
    bwt = ''.join(transposed_bwm[n-1])
    return bwt

def move_forward(bwt, checkpoint_arrays, start, end, map):
    checkpoint = checkpoint_arrays[start][:]
    # constant number of iterations :o
    while start < end:
        idx = map[bwt[start]]
        checkpoint[idx] += 1
        start += 1
    return checkpoint

def move_backward(bwt, checkpoint_arrays, start, end, map):
    checkpoint = checkpoint_arrays[start][:]
    # constant number of iterations :o
    while start > end:
        idx = map[bwt[start-1]]
        checkpoint[idx] -= 1
        start -= 1
    return checkpoint

def switch(mismatches, ltfa):
    new_dict = dict()
    for key in mismatches:
        new_key = ltfa[key]
        new_dict[new_key] = mismatches[key]
    return new_dict

# This is A LOT more memory efficient BUT a tiny bit slower... Still incredibly fast
def even_better_bwmatching(first_occurance, bwt, pattern, checkpoint_arrays, map, d, ltfa):
    n = len(bwt)
    top = 0
    bottom = n - 1
    checkpoints = checkpoint_arrays.keys()

    mismatches = dict()
    for i in range(1, n):
        mismatches[i] = 0

    while pattern != '':
        s = pattern[-1:] # get the last character of the pattern
        pattern = pattern[:-1] # update pattern

        # Make sure that we found at least 1 occurance of 's'
        closest_to_top = min(checkpoints, key=lambda x:abs(x-top)) # find closest checkpoint
        closest_to_bottom = min(checkpoints, key=lambda x:abs(x-bottom+1))

        if closest_to_top < top:
            top_count = move_forward(bwt, checkpoint_arrays, closest_to_top, top, map)
        else:
            top_count = move_backward(bwt, checkpoint_arrays, closest_to_top, top, map)

        if closest_to_bottom < bottom+1:
            bottom_count = move_forward(bwt, checkpoint_arrays, closest_to_bottom, bottom+1, map)
        else:
            bottom_count = move_backward(bwt, checkpoint_arrays, closest_to_bottom, bottom+1, map)

        above = top_count[map[s]]
        below = bottom_count[map[s]]
        top = first_occurance[s] + above
        bottom = first_occurance[s] + below - 1

        for row in mismatches:
            if (row < top) or (row > bottom):
                mismatches[row] += 1

        mismatches = {k:v for k,v in mismatches.items() if v <= d}

        if pattern != '':
            mismatches = switch(mismatches, ltfa)

        top, bottom = 0, n - 1
    walkingback_positions = list(mismatches.keys())
    return walkingback_positions

def create_first_occurance_array(fc):
    first_occurance = dict()
    for i, c in enumerate(fc):
        if c not in first_occurance:
            first_occurance[c] = i

        # Assuming we are working with DNA strings, we only need to find the
        # first occurance of each nucleotide and the dollar sign, so we can stop
        #if len(first_occurance) == 5:
        #    break
    return first_occurance

def create_checkpoint_arrays(bwt, first_occurance, c):
    n = len(bwt)
    m = len(first_occurance)

    # character index map
    idx_map = dict()
    i = 0
    for char in sorted(first_occurance): # 5 iterations for DNA strings
        idx_map[char] = i
        i += 1

    # Changing the count matrix implementation to a dictionary because it makes
    # more sense when we dont have the full matrix
    checkpoint_arrays = dict()
    array = [0] * m
    checkpoint_arrays[0] = array[:] # a COPY
    i = 0 # index string
    array_num = 1 # index rows
    while array_num <= n:
        idx = idx_map[bwt[i]]
        array[idx] += 1
        # ONLY store checkpoint arrays - MEMORY EFFICINCY IS OVER 9000
        if array_num % c == 0:
            checkpoint_arrays[array_num] = array[:]
        i += 1
        array_num += 1
    return checkpoint_arrays, idx_map

def walkback(pos, ltfa, psa):
    n = len(ltfa)
    counter = 0
    for i in range(0, n-1):
        if pos in psa:
            starting_pos = psa[pos] + counter
            return starting_pos
        pos = ltfa[pos]
        counter += 1


def start():
    text, patterns, d = read_input("dataset.txt")
    text = text + '$'

    # Construct the full suffix array then the partial suffix array
    c = 100 # my memory controller and SPEED lol
    sa = suffix_array(text)
    psa = partial_suffix_array(sa, c)

    # Get the last column and first column
    bwt = burrow_wheeler_transform(text)
    s = list(bwt)
    s.sort()
    fc = ''.join(s) # first column

    # Create the lastToFirst array to backtrack
    ltfa = last_to_first_array(fc, bwt)

    # Create the first occurance array and the Count matrix
    first_occurance = create_first_occurance_array(fc)
    checkpoint_arrays, map = create_checkpoint_arrays(bwt, first_occurance, c)

    # Check if the pattern matches a substring of text with at most d mismatches
    # If it does, then we walkback using the psa to find its starting position in text
    starting_positions = []
    for pattern in patterns:
        # Find the positions where we will start backtracking from
        backtracking_positions = even_better_bwmatching(first_occurance, bwt, pattern, checkpoint_arrays, map, d, ltfa)

        # Find the starting positions in text where this appears as a substring
        for position in backtracking_positions:
            starting_pos = walkback(position, ltfa, psa)
            starting_positions.append(starting_pos)

    # Output the results
    for pos in starting_positions:
        print(pos, end=" ")
    print()



if __name__ == '__main__':
    start()
