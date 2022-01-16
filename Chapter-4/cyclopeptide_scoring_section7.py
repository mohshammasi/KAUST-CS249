from genetic_code import genetic_code
from amino_acids_int_mass_table import integer_mass_table

def read_input(filename):
    try:
        input_file = open(filename, "r")
        peptide = input_file.readline().rstrip('\n')
        spectrum = input_file.read().split(" ")
        spectrum = [int(i) for i in spectrum]
        input_file.close()
    except:
        print("Exception caught, file probably doesnt exist")
    return peptide, spectrum

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


def cyclopeptide_scoring(peptide, spectrum):
    peptide_spectrum = cyclic_spectrum(peptide)
    peptide_dict = {p : peptide_spectrum.count(p) for p in peptide_spectrum}
    spectrum_dict = {s : spectrum.count(s) for s in spectrum}

    score = 0
    for p in peptide_dict:
        for i in range (0, peptide_dict[p]):
            if p in spectrum_dict:
                score += 1
                spectrum_dict[p] -= 1

                if spectrum_dict[p] == 0:
                    del spectrum_dict[p]
    return score



def start():
    peptide, spectrum = read_input("dataset.txt")
    result = cyclopeptide_scoring(peptide, spectrum)
    print(result)


if __name__ == '__main__':
    start()
