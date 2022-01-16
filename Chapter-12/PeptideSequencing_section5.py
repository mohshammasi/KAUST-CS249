from amino_acids_int_mass_table import integer_mass_table, inverse_mass_table, inverse_hypothetical_mass_table

def read_input(filename):
    try:
        input_file = open(filename, "r")
        spectra = input_file.read().split(" ")
        spectra = [int(i) for i in spectra]
        spectra.insert(0, 0)
        input_file.close()
    except:
        print("Exception caught, file probably doesnt exist")
    return spectra

def spectra_graph(spectra):
    n = len(spectra)
    graph = dict()

    for i in range(0, n):
        for j in range(i+1, n):
            possible_edge = j - i
            if possible_edge in inverse_mass_table:
                amino_acid = inverse_mass_table[possible_edge]
                graph.setdefault((i, spectra[i]), []).append((j, amino_acid))
    return graph

def dfs(graph, node, sink, path, weight, paths, spectra):

    if node == sink:
        paths.append((path, weight))
        return paths
    pcopy = path
    wcopy = weight
    if node in graph:
        for edge in graph[node]:
            if node == 0: # source
                path = ''
                weight = 0
            else:
                path = pcopy
                weight = wcopy
            path += edge[1]
            weight += node[1] # the weight of the node
            paths = dfs(graph, (edge[0], spectra[edge[0]]), sink, path, weight, paths, spectra)
    return paths

def peptide_sequencing(graph, source, sink, spectra):
    # Using DFS we will find all paths from source to the sink
    spectra[len(spectra)-1] = 0
    peptides = dfs(graph, source, sink, '', 0, [], spectra)

    best_peptide = (0, 0)
    for peptide in peptides:
        if peptide[1] > best_peptide[1]:
            best_peptide = peptide
    return best_peptide[0]

def start():
    spectra = read_input("dataset.txt")
    graph = spectra_graph(spectra)
    source, sink = (0, 0), (len(spectra)-1, 0)
    peptide = peptide_sequencing(graph, source, sink, spectra)
    print(peptide)

if __name__ == '__main__':
    start()
