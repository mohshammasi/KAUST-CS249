

def read_input(filename):
    try:
        input_file = open(filename, "r")
        string = input_file.read()[:-1] # get rid of the newline character
        input_file.close()
    except:
        print("Exception caught, file probably doesnt exist")
    return string

def reverse_complement(string):
    reverse_string = ''
    for i in range(len(string)-1, -1, -1): # 2nd arg not inclusive hence -1
        if string[i] == 'A':
            reverse_string += 'T'
        elif string[i] == 'T':
            reverse_string += 'A'
        elif string[i] == 'C':
            reverse_string += 'G'
        elif string[i] == 'G':
            reverse_string += 'C'
        else:
            print('This string contains a weird thing')
    return reverse_string

## added for exam
def transcribe(dna):
    dna = list(dna)
    for i in range(0, len(dna)):
        if dna[i] == 'T':
            dna[i] = 'U'
    return ''.join(dna)

def start():
    string = read_input("dataset.txt")
    result = reverse_complement(string)
    print(result)
    print('Reverse complement from right to left is: ')
    result = list(result)
    result.reverse()
    result = ''.join(result)
    print(result)

    rna = transcribe(result)
    print('RNA of RC: ')
    print(rna)


if __name__ == '__main__':
    start()
