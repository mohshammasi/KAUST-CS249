from genetic_code import genetic_code
from amino_acids_int_mass_table import integer_mass_table

def read_input(filename):
    try:
        input_file = open(filename, "r")
        peptide = input_file.readline().rstrip('\n')
        input_file.close()
    except:
        print("Exception caught, file probably doesnt exist")
    return peptide

def cyclic_spectrum(peptide):
    prefix_mass = [0]
    peptide = ' ' + peptide  # pad first space
    n = len(peptide)
    for i in range(1, n):
        for s in integer_mass_table:
            if s == peptide[i]:
                prefix_mass.append(prefix_mass[i-1] + integer_mass_table[s])
    peptide_mass = prefix_mass[n-1]
    cyclic_spectrum = [0]
    for i in range(0, n-1):
        for j in range(i+1, n):
            cyclic_spectrum.append(prefix_mass[j]-prefix_mass[i])
            if i > 0 and j < (n-1):
                cyclic_spectrum.append(peptide_mass - (prefix_mass[j]-prefix_mass[i]))
    cyclic_spectrum.sort()
    return cyclic_spectrum

def start():
    peptide = read_input("dataset.txt")
    result = cyclic_spectrum(peptide)
    for num in result:
        print(num, end=" ")
    print()



if __name__ == '__main__':
    start()
