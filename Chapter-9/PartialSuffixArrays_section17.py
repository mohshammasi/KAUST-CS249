from operator import itemgetter

def read_input(filename):
    try:
        input_file = open(filename, "r")
        text = input_file.readline().rstrip('\n')
        k = input_file.readline().rstrip('\n')
        input_file.close()
    except IOError as e:
        print(e)
    return text, int(k)

def suffix_array(text):
    n = len(text)
    suffix_array = []
    for i in range(0, n):
        suffix_array.append((i, text[i:n]))
    suffix_array.sort(key=itemgetter(1)) # sort lexicographically
    suffix_array = [tup[0] for tup in suffix_array] # remove the strings
    return suffix_array

def partial_suffix_array(sa, k):
    partial_suffix_array = []
    for i, val in enumerate(sa):
        if val % k == 0:
            partial_suffix_array.append((i, val))
    return partial_suffix_array

def start():
    text, k = read_input("dataset.txt")
    sa = suffix_array(text)
    psa = partial_suffix_array(sa, k)

    try:
        output_file = open("output.txt", "w")
        for tup in psa:
            output_file.write(str(tup[0]) + ',' + str(tup[1]) + '\n')
        output_file.close()
        print("Output written successfully to the textfile.")
    except:
        print('File I/O Error...')


if __name__ == '__main__':
    start()
