

def read_input(filename):
    try:
        input_file = open(filename, "r")
        genome = input_file.readline()[:-1]
        input_file.close()
    except:
        print("Exception caught, file probably doesnt exist")
    return genome

def minimum_skew(genome):
    skew = [0] #init with a 0
    for i in range(0, len(genome)):
        if genome[i] == 'A':
            skew.append(skew[i])
        elif genome[i] == 'T':
            skew.append(skew[i])
        elif genome[i] == 'C':
            skew.append(skew[i]-1)
        elif genome[i] == 'G':
            skew.append(skew[i]+1)
        else:
            print('This string contains a weird thing')

    # get min positions
    minimum_positions = [i for i, m in enumerate(skew) if m==min(skew)]
    return minimum_positions

def start():
    genome = read_input("dataset.txt")
    result = minimum_skew(genome)
    for pos in result:
        print(pos, end=" ")
    


if __name__ == '__main__':
    start()
