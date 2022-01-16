from genetic_code import genetic_code

def read_input(filename):
    try:
        input_file = open(filename, "r")
        rna = input_file.readline().rstrip('\n')
        input_file.close()
    except:
        print("Exception caught, file probably doesnt exist")
    return rna

def protein_translation(rna):
    n = len(rna)
    k = 3

    protein = ''
    for i in range(0, n, 3):
        codon = rna[i:i+k]
        if genetic_code[codon] == '*':
            return protein
        else:
            protein += genetic_code[codon]
    return protein

def start():
    rna = read_input("dataset.txt")
    result = protein_translation(rna)
    #print(result)

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
