

def read_input(filename):
    try:
        input_file = open(filename, "r")
        text, k = input_file.read().splitlines()
        input_file.close()
    except:
        print("Exception caught, file probably doesnt exist")
    return text, int(k)

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

def max_map(map):
    return max(map.values())

def frequent_words(text, k):
    frequent_patterns = []
    frequency_map = frequency_table(text, k)
    max = max_map(frequency_map)
    for pattern in frequency_map:
        if frequency_map[pattern] == max:
            frequent_patterns.append(pattern)
    return frequent_patterns


def start():
    text, k = read_input("dataset.txt")
    result = frequent_words(text, k)
    for string in result:
        print(string, end=" ")


if __name__ == '__main__':
    start()
