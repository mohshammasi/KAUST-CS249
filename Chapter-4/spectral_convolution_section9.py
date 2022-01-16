from genetic_code import genetic_code
from amino_acids_int_mass_table import integer_mass_table
from operator import itemgetter

def read_input(filename):
    try:
        input_file = open(filename, "r")
        spectrum = input_file.read().split(" ")
        spectrum = [int(i) for i in spectrum]
        input_file.close()
    except:
        print("Exception caught, file probably doesnt exist")
    return spectrum

def spectral_convolution(spectrum):
    n = len(spectrum)
    convolution = []
    for i in range(1, n):
        for j in range(i-1, -1, -1): # to -1 instead of 0 because its not inclusive
            element = abs(spectrum[i] - spectrum[j])
            if element != 0:
                convolution.append(element)
    return convolution

def start():
    spectrum = read_input("dataset.txt")
    result = spectral_convolution(spectrum)
    for num in result:
        print(num, end=" ")
    print()

if __name__ == '__main__':
    start()
