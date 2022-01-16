from amino_acids_int_mass_table import integer_mass_table, inverse_mass_table
import sys
sys.setrecursionlimit(5000)

def read_input(filename):
    try:
        input_file = open(filename, "r")
        spectrum = input_file.read().split(" ")
        spectrum = [int(i) for i in spectrum]
        spectrum.insert(0, 0)
        input_file.close()
    except:
        print("Exception caught, file probably doesnt exist")
    return spectrum

def spectrum_graph(spectrum):
    n = len(spectrum)
    graph = dict()
    for i in range(0, n):
        for j in range(i+1, n):
            possible_edge = spectrum[j] - spectrum[i]
            if possible_edge in inverse_mass_table:
                amino_acid = inverse_mass_table[possible_edge]
                graph.setdefault(spectrum[i], []).append((spectrum[j], amino_acid))
    return graph

def dfs(graph, node, sink, path, paths):

    if node == sink:
        paths.append(path)
        return paths
    copy = path
    for edge in graph[node]:
        if node == 0: # source
            path = ''
        else:
            path = copy
        path += edge[1]
        paths = dfs(graph, edge[0], sink, path, paths)
    return paths

def ideal_spectrum(peptide):
    # Compute each prefix and its mass and add it to the spectrum
    n = len(peptide)
    spectrum = []

    # Masses of all the prefixes, including the full peptide
    for i in range(1, n+1):
        prefix = peptide[:i]
        mass = 0
        for c in prefix:
            mass += integer_mass_table[c]
        spectrum.append(mass)

    # Masses of all the suffixes not including the full peptide
    for i in range(1, n):
        suffix = peptide[i:]
        mass = 0
        for c in suffix:
            mass += integer_mass_table[c]
        spectrum.append(mass)

    spectrum.sort()
    return spectrum



def decode_ideal_spectrum(graph, source, sink, spectrum):
    # Using DFS we will find all paths from source to the sink
    peptides = dfs(graph, source, sink, '', [])

    for peptide in peptides:
        idealspectrum = ideal_spectrum(peptide)
        if idealspectrum == spectrum:
            return peptide


def start():
    spectrum = read_input("dataset.txt")
    source, sink = 0, spectrum[len(spectrum)-1]
    graph = spectrum_graph(spectrum)
    peptide = decode_ideal_spectrum(graph, source, sink, spectrum[1:])
    print(peptide)

if __name__ == '__main__':
    start()
