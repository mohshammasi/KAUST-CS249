from operator import itemgetter

def read_input(filename):
    try:
        input_file = open(filename, "r")
        text = input_file.readline().rstrip('\n')
        input_file.close()
    except IOError as e:
        print(e)
    return text

def suffix_array(text):
    n = len(text)
    suffix_array = []
    for i in range(0, n):
        suffix_array.append((i, text[i:n]))
    suffix_array.sort(key=itemgetter(1)) # sort lexicographically
    suffix_array = [tup[0] for tup in suffix_array] # remove the strings
    return suffix_array

def start():
    text = read_input("dataset.txt")
    result = suffix_array(text)
    for position in result:
        print(position, end=", ")
    print()


if __name__ == '__main__':
    start()
