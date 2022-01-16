from genetic_code import genetic_code

def read_input(filename):
    try:
        input_file = open(filename, "r")
        n = input_file.readline().rstrip('\n')
    except:
        print("Exception caught, file probably doesnt exist")
    return int(n)

def number_of_subpeptides(n):
    return n * (n-1)

def start():
    n = read_input("dataset.txt")
    result = number_of_subpeptides(n)
    print(result)

    try:
        output_file = open("output.txt", "w")
        for string in result:
            output_file.write(string)
        output_file.close()
        print("Output written successfully to the textfile.")
    except:
        print('File I/O Error...')



if __name__ == '__main__':
    start()
