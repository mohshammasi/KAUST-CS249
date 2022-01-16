from genetic_code import genetic_code
from amino_acids_int_mass_table import integer_mass_table

def read_input(filename):
    try:
        input_file = open(filename, "r")
        spectrum = input_file.read().split(" ")
        input_file.close()
    except:
        print("Exception caught, file probably doesnt exist")
    return spectrum

def expand(peptides):
    expanded = []
    # First fetch all peptides of length 1
    if "" in peptides:
        for p in integer_mass_table:
            if p == 'L' or p == 'Q':
                continue
            expanded.append([integer_mass_table[p]])
    else: # just expand
        for peptide in peptides:
            for p in integer_mass_table:
                copy = peptide.copy()
                if p == 'L' or p == 'Q':
                    continue
                copy.append(integer_mass_table[p])
                expanded.append(copy)
    return expanded

##########################################

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

############################################

def mass(peptide):
    return sum(peptide)

def parent_mass(spectrum):
    return max(spectrum)

def translator(peptide):
    peptide_string = ''
    n = len(peptide)
    for p in peptide:
        translated = False
        for m in integer_mass_table:
            if p == integer_mass_table[m]:
                peptide_string += m
                translated = True

            if translated:
                break
    #print('peptide translated is ', peptide_string)
    return peptide_string

def check_consistency(peptide, spectrum):
    # Turn both the peptide and spectrum to dictionaries
    peptide_dict = {p : peptide.count(p) for p in peptide}
    spectrum_dict = {s : spectrum.count(s) for s in spectrum}

    # Assume they are consistent to begin with
    consistent = True
    try:
        for p in peptide_dict:
            if peptide_dict[p] > spectrum_dict[p]:
                consistent = False
                break
    except:
        #print('A key error probably happend because p not in spectrum_dict')
        consistent = False
        return consistent
    return consistent

def cyclopeptide_sequencing(spectrum):
    candidate_peptides = ['']
    final_peptides = []
    while len(candidate_peptides) != 0:
        candidate_peptides = expand(candidate_peptides)
        n = len(candidate_peptides)
        j = 0
        while j < n:
            if mass(candidate_peptides[j]) == parent_mass(spectrum):
                # Translate the peptide representation from numbers to letters
                string = translator(candidate_peptides[j])
                peptide_spectrum = cyclic_spectrum(string)
                equal = True
                l = len(peptide_spectrum)
                try:
                    for i in range(0, l):
                        if peptide_spectrum[i] != spectrum[i]:
                            equal = False
                except:
                    equal = False
                if equal and candidate_peptides[j] not in final_peptides:
                    final_peptides.append(candidate_peptides[j])
                # deal with the removing later
                candidate_peptides.pop(j)
            elif not check_consistency(candidate_peptides[j], spectrum):
                candidate_peptides.pop(j)
            else:
                j += 1
            n = len(candidate_peptides)
    return final_peptides




def start():
    spectrum = read_input("dataset.txt")
    spectrum = [int(i) for i in spectrum]
    result = cyclopeptide_sequencing(spectrum)
    #for l in result:
    #    l = [str(i) for i in l]
    #    string = "-".join(l)
    #    print(string, end=" ")
    #print()

    try:
        output_file = open("output.txt", "w")
        for l in result:
            l = [str(i) for i in l]
            string = "-".join(l)
            output_file.write(string + ' ')
        output_file.close()
        print("Output written successfully to the textfile.")
    except:
        print('File I/O Error...')



if __name__ == '__main__':
    start()
