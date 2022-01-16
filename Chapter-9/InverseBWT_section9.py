import numpy as np

def read_input(filename):
    try:
        input_file = open(filename, "r")
        bwt = input_file.readline().rstrip('\n')
        input_file.close()
    except IOError as e:
        print(e)
    return bwt

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

def inverse_bwt(bwt, first_c):
    bwt_dict = string_dict(bwt)
    first_c_dict = string_dict(first_c, True)

    n = len(bwt)
    text = ''

    bwt_dollar_i = bwt_dict['$1']
    char = first_c_dict[bwt_dollar_i]
    text += char[0] # only take the char, leave the number label
    for i in range(0, n-1):
        idx = bwt_dict[char]
        char = first_c_dict[idx]
        text += char[0]
    return text

def start():
    bwt = read_input("dataset.txt")
    s = list(bwt)
    s.sort()
    first_column = ''.join(s)
    text = inverse_bwt(bwt, first_column)
    print(text)


if __name__ == '__main__':
    start()
