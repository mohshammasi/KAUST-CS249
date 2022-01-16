from genetic_code import genetic_code
from amino_acids_int_mass_table import integer_mass_table
from operator import itemgetter

def read_input(filename):
    try:
        input_file = open(filename, "r")
        M = input_file.readline().rstrip('\n')
        N = input_file.readline().rstrip('\n')
        spectrum = input_file.read().split(" ")
        spectrum = [int(i) for i in spectrum]
        input_file.close()
    except:
        print("Exception caught, file probably doesnt exist")
    return int(M), int(N), spectrum

def spectral_convolution(spectrum):
    n = len(spectrum)
    convolution = []
    for i in range(1, n):
        for j in range(i-1, -1, -1): # to -1 instead of 0 because its not inclusive
            element = abs(spectrum[i] - spectrum[j])
            if element != 0:
                convolution.append(element)
    return convolution

def most_frequent(M, convolution):
    # Create a dictionary with counts of each value in convolution
    dict = {}
    for mass in convolution:
        dict[mass] = dict.get(mass, 0) + 1

    # Sort in descending order according to the counter
    most_frequent_m = sorted(dict.items(), key=itemgetter(1), reverse=True)

    # Discard the masses that are not between 57 and 200
    most_frequent_m = [(mass, count) for mass, count in most_frequent_m if mass >= 57 and mass <= 200]

    masses, counters = zip(*most_frequent_m)
    for j in range(M, len(masses)):
        if counters[j] < counters[M-1]:
            masses = masses[:j]
            return masses
    return masses

def expand(peptides, amino_acids):
    expanded = []
    # First fetch all peptides of length 1
    if "" in peptides:
        for aa in amino_acids:
            expanded.append([aa])
    else: # just expand
        for peptide in peptides:
            for aa in amino_acids:
                copy = peptide.copy()
                copy.append(aa)
                expanded.append(copy)
    return expanded

def cyclic_spectrum(peptide, amino_acids):
    prefix_mass = [0]
    #peptide = ' ' + peptide  # pad first space
    copy = peptide.copy()
    copy.insert(0, [])
    n = len(copy)
    for i in range(1, n):
        for aa in amino_acids:
            if aa == copy[i]:
                prefix_mass.append(prefix_mass[i-1] + aa)
    peptide_mass = prefix_mass[n-1]
    cyclic_spectrum = [0]
    for i in range(0, n-1):
        for j in range(i+1, n):
            cyclic_spectrum.append(prefix_mass[j]-prefix_mass[i])
            if i > 0 and j < (n-1):
                cyclic_spectrum.append(peptide_mass - (prefix_mass[j]-prefix_mass[i]))
    cyclic_spectrum.sort()
    return cyclic_spectrum


def cyclopeptide_scoring(peptide, spectrum, amino_acids):
    peptide_spectrum = cyclic_spectrum(peptide, amino_acids)
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

def trim(leaderboard, spectrum, N, amino_acids):
    n = len(leaderboard)
    linear_scores = []
    for j in range(0, n):
        #peptide = translator(leaderboard[j])
        #linear_score = linearpeptide_scoring(leaderboard[j], spectrum, amino_acids)
        linear_score = cyclopeptide_scoring(leaderboard[j], spectrum, amino_acids)
        linear_scores.append(linear_score)

    # Create a combined list and sort it based on scores
    combined_lists = [(e1,e2) for (e1,e2) in zip(leaderboard, linear_scores)]
    combined_lists.sort(key=itemgetter(1), reverse=True)

    # Break it back to 2 lists
    leaderboard, linear_scores = zip(*combined_lists)

    for j in range(N, n):
        if linear_scores[j] < linear_scores[N-1]:
            leaderboard = leaderboard[:j]
            return leaderboard
    return leaderboard

def mass(peptide):
    return sum(peptide)

def parent_mass(spectrum):
    return max(spectrum)

def convolution_cyclopeptide_sequencing(N, spectrum, amino_acids):
    leaderboard = ['']
    leader_peptide = []
    while len(leaderboard) != 0:
        leaderboard = expand(leaderboard, amino_acids)
        n = len(leaderboard)
        j = 0
        while j < n:
            if mass(leaderboard[j]) == parent_mass(spectrum):
                if cyclopeptide_scoring(leaderboard[j], spectrum, amino_acids) > cyclopeptide_scoring(leader_peptide, spectrum, amino_acids):
                    leader_peptide = leaderboard[j]
                j += 1
            elif mass(leaderboard[j]) > parent_mass(spectrum):
                leaderboard.pop(j)
            else:
                j += 1
            n = len(leaderboard)
        if n != 0:
            leaderboard = trim(leaderboard, spectrum, N, amino_acids)
    return leader_peptide

def start():
    M, N, spectrum = read_input("dataset.txt")
    convolution = spectral_convolution(spectrum)
    amino_acids = most_frequent(M, convolution)
    result = convolution_cyclopeptide_sequencing(N, spectrum, amino_acids)
    result = [str(num) for num in result]
    string = "-".join(result)
    print(string, end=" ")
    print()

    try:
        output_file = open("output.txt", "w")
        string = "-".join(result)
        output_file.write(string + ' ')
        output_file.close()
        print("Output written successfully to the textfile.")
    except:
        print('File I/O Error...')



if __name__ == '__main__':
    start()
