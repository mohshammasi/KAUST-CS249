from genetic_code import genetic_code
from amino_acids_int_mass_table import integer_mass_table
from operator import itemgetter

def read_input(filename):
    try:
        input_file = open(filename, "r")
        leaderboard = input_file.readline().rstrip('\n').split(" ")
        spectrum = input_file.readline().rstrip('\n').split(" ")
        spectrum = [int(i) for i in spectrum]
        N = input_file.readline().rstrip('\n')
        input_file.close()
    except:
        print("Exception caught, file probably doesnt exist")
    return leaderboard, spectrum, int(N)

###################################################

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

####################################################

def trim(leaderboard, spectrum, N):
    n = len(leaderboard)
    linear_scores = []
    for j in range(0, n):
        peptide = leaderboard[j]
        linear_score = linearpeptide_scoring(peptide, spectrum)
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


def start():
    leaderboard, spectrum, N = read_input("dataset.txt")
    result = trim(leaderboard, spectrum, N)

    try:
        output_file = open("output.txt", "w")
        for string in result:
            output_file.write(string + ' ')
        output_file.close()
        print("Output written successfully to the textfile.")
    except:
        print('File I/O Error...')

if __name__ == '__main__':
    start()
