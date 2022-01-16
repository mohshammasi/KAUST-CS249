from amino_acids_int_mass_table import integer_mass_table, inverse_mass_table, hypothetical_mass_table
import sys
sys.setrecursionlimit(5000)

def read_input(filename):
    try:
        input_file = open(filename, "r")
        peptide = input_file.read().rstrip('\n')
        input_file.close()
    except:
        print("Exception caught, file probably doesnt exist")
    return peptide


def ideal_spectrum(peptide):
    # Compute each prefix and its mass and add it to the spectrum
    n = len(peptide)
    spectrum = []
    prefix_masses = []

    # Masses of all the prefixes, including the full peptide
    for i in range(1, n+1):
        prefix = peptide[:i]
        mass = 0
        for c in prefix:
            mass += integer_mass_table[c]
        spectrum.append(mass)
        prefix_masses.append(mass)

    # Masses of all the suffixes not including the full peptide
    for i in range(1, n):
        suffix = peptide[i:]
        mass = 0
        for c in suffix:
            mass += integer_mass_table[c]
        spectrum.append(mass)

    prefix_masses.sort()
    spectrum.sort()
    return spectrum, prefix_masses

def mass(spectrum):
    return spectrum[len(spectrum)-1]

def to_peptide_vector(peptide):
    # Get the full spectrum and prefix masses of the peptide
    spectrum, prefix_masses = ideal_spectrum(peptide)
    spectrum_mass = mass(spectrum)

    peptide_vector = dict()
    for i in range(1, spectrum_mass+1):
        peptide_vector[i] = 0

    for m in prefix_masses:
        peptide_vector[m] = 1

    peptide_vector = list(peptide_vector.values())
    return peptide_vector


def start():
    peptide = read_input("dataset.txt")
    peptide_vector = to_peptide_vector(peptide)
    for v in peptide_vector:
        print(v, end=" ")
    print()

if __name__ == '__main__':
    start()
