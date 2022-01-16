from amino_acids_int_mass_table import inverse_mass_table, inverse_hypothetical_mass_table

def read_input(filename):
    try:
        input_file = open(filename, "r")
        peptide_vector = input_file.read().split(" ")
        peptide_vector = [int(i) for i in peptide_vector]
        input_file.close()
    except:
        print("Exception caught, file probably doesnt exist")
    return peptide_vector

def to_peptide(peptide_vector):
    n = len(peptide_vector)
    prefix_masses = []
    for i in range(0, n):
        if peptide_vector[i] == 1:
            prefix_masses.append(i+1)

    peptide = ''
    n = len(prefix_masses)
    for i in range(0, n):
        if i == 0:
            c = inverse_mass_table[prefix_masses[i]]
            peptide += c
        else:
            difference = prefix_masses[i] - prefix_masses[i-1]
            c = inverse_mass_table[difference]
            peptide += c
    return peptide

def start():
    peptide_vector = read_input("dataset.txt")
    peptide = to_peptide(peptide_vector)
    print(peptide)

if __name__ == '__main__':
    start()
