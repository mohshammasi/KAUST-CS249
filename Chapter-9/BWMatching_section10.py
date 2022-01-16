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

###############################################################

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


def bwmatching(bwt, pattern, ltfa):
    n = len(bwt)
    top = 0
    bottom = n - 1
    while top <= bottom:
        if pattern != '':
            s = pattern[-1:] # get the last character of the pattern
            pattern = pattern[:-1] # update pattern

            # Find first and last occurance of 's' in bwt
            found_first_occurance = False
            top_i = None
            bottom_i = None
            for i in range(top, bottom+1):
                if s == bwt[i]:
                    if not found_first_occurance:
                        top_i = i
                        found_first_occurance = True
                    bottom_i = i # always update bottom

            # Make sure that we found at least 1 occurance of 's'
            if top_i != None and bottom_i != None:
                top = ltfa[top_i]
                bottom = ltfa[bottom_i]
            else:
                return 0
        else:
            return (bottom - top + 1)



def start():
    bwt, patterns = read_input("dataset.txt")
    s = list(bwt)
    s.sort()
    fc = ''.join(s) # first column

    # Create the lastToFirst array
    ltfa = last_to_first_array(fc, bwt)

    # Get the number of matches for each pattern in patterns
    patterns_num_of_matches = []
    for pattern in patterns:
        num_of_matches = bwmatching(bwt, pattern, ltfa)
        patterns_num_of_matches.append(num_of_matches)

    # Output the results
    for num in patterns_num_of_matches:
        print(num, end=" ")
    print()

if __name__ == '__main__':
    start()
