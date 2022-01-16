

def read_input(filename):
    input_file = open(filename, "r")
    text, pattern = input_file.read().splitlines()
    input_file.close()
    return text, pattern

def pattern_count(text, pattern):
    count = 0
    for i in range(0, len(text)-len(pattern)):
        if text[i:i+len(pattern)] == pattern:
            count += 1
    return count


def start():
    text, pattern = read_input("dataset.txt")
    result = pattern_count(text, pattern)
    print(result)


if __name__ == '__main__':
    start()
