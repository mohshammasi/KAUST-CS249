from amino_acids_int_mass_table import integer_mass_table, inverse_mass_table

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

def directed_edges_adjaceny_list(graph):
    directed_edges = []
    # sorting just to compare with given answers easily, not necessary
    for node in sorted(graph):
        for e in graph[node]:
            # Get node at the end of the edge and the weight
            node2, weight = e[0], e[1]

            # Create directed edge and add it
            directed_edges.append(str(node) + '->' + str(node2) + ':' + str(weight))
    return directed_edges

def start():
    spectrum = read_input("dataset.txt")
    graph = spectrum_graph(spectrum)
    output = directed_edges_adjaceny_list(graph)
    for e in output:
        print(e)

if __name__ == '__main__':
    start()
