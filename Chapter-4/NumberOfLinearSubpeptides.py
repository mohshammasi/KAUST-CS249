
def read_input(filename):
    try:
        input_file = open(filename, "r")
        n = input_file.readline().rstrip('\n')
    except:
        print("Exception caught, file probably doesnt exist")
    return int(n)

def number_of_linear_subpeptides(n):
    return (n*(n+1)/2) + 1

def start():
    n = read_input("dataset.txt")
    result = number_of_linear_subpeptides(n)
    print(result)



if __name__ == '__main__':
    start()
