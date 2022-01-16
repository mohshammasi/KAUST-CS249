from genetic_code import genetic_code
from amino_acids_int_mass_table import integer_mass_table
from operator import itemgetter

def read_input(filename):
    try:
        input_file = open(filename, "r")
        N = input_file.readline().rstrip('\n')
        spectrum = input_file.read().split(" ")
        spectrum = [int(i) for i in spectrum]
        input_file.close()
    except:
        print("Exception caught, file probably doesnt exist")
    return int(N), spectrum

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

def linear_spectrum(peptide):
    prefix_mass = [0]
    peptide = ' ' + peptide  # pad first space
    n = len(peptide)
    for i in range(1, n):
        for s in integer_mass_table:
            if s == peptide[i]:
                prefix_mass.append(prefix_mass[i-1] + integer_mass_table[s])
    linear_spectrum = [0]
    for i in range(0, n-1):
        for j in range(i+1, n):
            linear_spectrum.append(prefix_mass[j]-prefix_mass[i])
    linear_spectrum.sort()
    return linear_spectrum


def linearpeptide_scoring(peptide, spectrum):
    peptide_spectrum = linear_spectrum(peptide)
    #peptide_dict = {p : peptide_spectrum.count(p) for p in peptide_spectrum}
    spectrum_dict = {s : spectrum.count(s) for s in spectrum}

    score = 0
    for num in peptide_spectrum:
        if num in spectrum_dict:
            score += 1
            spectrum_dict[num] -= 1
            if spectrum_dict[num] == 0:
                del spectrum_dict[num]
    return score

def trim(leaderboard, spectrum, N):
    n = len(leaderboard)
    linear_scores = []
    for j in range(0, n):
        peptide = translator(leaderboard[j])
        linear_score = linearpeptide_scoring(peptide, spectrum)
        linear_scores.append(linear_score)

    # Create a combined list and sort it based on scores
    combined_lists = [(e1,e2) for (e1,e2) in zip(leaderboard, linear_scores)]
    combined_lists.sort(key=itemgetter(1), reverse=True)

    # Break it back to 2 lists
    #print(combined_lists)
    leaderboard, linear_scores = zip(*combined_lists)

    for j in range(N, n):
        if linear_scores[j] < linear_scores[N-1]:
            leaderboard = leaderboard[:j]
            return leaderboard
    return leaderboard

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

def leaderboard_cyclopeptide_sequencing(N, spectrum):
    leaderboard = ['']
    leader_peptide = ''
    while len(leaderboard) != 0:
        leaderboard = expand(leaderboard)
        n = len(leaderboard)
        j = 0
        while j < n:
            if mass(leaderboard[j]) == parent_mass(spectrum):
                # Translate the peptide representation from numbers to letters
                peptide = translator(leaderboard[j])
                if linearpeptide_scoring(peptide, spectrum) > linearpeptide_scoring(leader_peptide, spectrum):
                    leader_peptide = peptide
                j += 1
            elif mass(leaderboard[j]) > parent_mass(spectrum):
                leaderboard.pop(j)
            else:
                j += 1
            n = len(leaderboard)
        if n != 0:
            leaderboard = trim(leaderboard, spectrum, N)

    # Translate leader peptide to its masses
    leader_peptide_m = []
    for c in leader_peptide:
        leader_peptide_m.append(integer_mass_table[c])
    return leader_peptide_m

def start():
    N, spectrum = read_input("dataset.txt")
    result = leaderboard_cyclopeptide_sequencing(N, spectrum)
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
