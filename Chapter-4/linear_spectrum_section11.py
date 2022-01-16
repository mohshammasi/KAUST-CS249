from genetic_code import genetic_code
from amino_acids_int_mass_table import integer_mass_table

def read_input(filename):
    try:
        input_file = open(filename, "r")
        peptide = input_file.readline().rstrip('\n')
        input_file.close()
        print(peptide)
    except:
        print("Exception caught, file probably doesnt exist")
    return peptide

def linear_spectrum(peptide):
    prefix_mass = [0]
    peptide = ' ' + peptide  # pad first space
    n = len(peptide)
    for i in range(1, n):
        prefix_mass.append(prefix_mass[i-1] + integer_mass_table[peptide[i]])

    linear_spectrum = [0]
    for i in range(0, n-1):
        for j in range(i+1, n):
            linear_spectrum.append(prefix_mass[j]-prefix_mass[i])
    linear_spectrum.sort()
    return linear_spectrum

def start():
    peptide = read_input("dataset.txt")
    result = linear_spectrum(peptide)
    for num in result:
        print(num, end=" ")
    print()

    #try:
    #    output_file = open("output.txt", "w")
    #    for string in result:
    #        output_file.write(string + '\n')
    #    output_file.close()
    #    print("Output written successfully to the textfile.")
    #except:
    #    print('File I/O Error...')



if __name__ == '__main__':
    start()
