

def read_input(filename):
    try:
        input_file = open(filename, "r")
        graph_al = dict()
        for line in input_file:
            graph_al[line.split(' ')[0]] = list(num for num in line[len(line.split(' ')[0])+4:].rstrip('\n').split(','))
        input_file.close()
        i=0
        for edge in graph_al:
            if len(graph_al[edge]) > 1:
                i += len(graph_al[edge])
            else:
                i += 1
        print('total num of edges')
        print(i)
    except:
        print("Exception caught, file probably doesnt exist")
    return graph_al


def maximal_non_branching_paths(graph):
    # Create a dict of degrees
    degrees = dict.fromkeys(graph.keys(), 0)
    for node in graph:
        degrees[node] = len(graph[node])
        for node2 in graph:
            degrees[node] += graph[node2].count(node)
    print(degrees)

    paths = []
    for node in graph:
        if degrees[node] != 2:
            if node in graph:
                for edge in graph[node]:
                    non_branching_path = node + '->' + edge
                    one_in_one_out_node = True
                    while one_in_one_out_node:
                        non_branching_path_nodes = non_branching_path.split('->')
                        idx = len(non_branching_path_nodes)-1
                        last_n_in_path = non_branching_path_nodes[idx]
                        try:
                            edges = graph[last_n_in_path]
                            print(last_n_in_path)
                            print(degrees[last_n_in_path])
                            if len(edges) == 1 and degrees[last_n_in_path] == 2:
                                e = next(iter(edges))
                                non_branching_path += "->" + e
                            else:
                                one_in_one_out_node = False
                        except KeyError as e:
                            break
                    paths.append(non_branching_path)

    # handle isolated cycles
    for node in graph:
        if degrees[node] == 2:
            if node in graph:
                for edge in graph[node]:
                    isolated_cycle = node + '->' + edge
                    one_in_one_out_node = True
                    while one_in_one_out_node:
                        isolated_cycle_nodes = isolated_cycle.split('->')
                        idx = len(isolated_cycle_nodes)-1
                        last_n_in_cycle = isolated_cycle_nodes[idx]
                        try:
                            edges = graph[last_n_in_cycle]
                            if len(edges) == 1 and degrees[last_n_in_cycle] == 2:
                                e = next(iter(edges))
                                isolated_cycle += "->" + e

                                if e == isolated_cycle_nodes[0]:
                                    one_in_one_out_node = False
                            else:
                                one_in_one_out_node = False
                        except KeyError as e:
                            break
                    isolated_cycle_nodes = isolated_cycle.split('->')
                    idx = len(isolated_cycle_nodes)-1
                    last_n_in_cycle = isolated_cycle_nodes[idx]
                    if isolated_cycle_nodes[idx] == isolated_cycle_nodes[0]:
                        paths.append(isolated_cycle)
    return paths

def start():
    graph = read_input("dataset.txt")
    result = maximal_non_branching_paths(graph)
    #for string in result:
    #    print(string)
    try:
        output_file = open("output.txt", "w")
        for string in result:
            output_file.write(string + '\n')
        output_file.close()
        print("Output written successfully to the textfile.")
    except:
        print('File I/O Error...')
    #nodes = result.split('->')
    #num_edges = len(nodes)-1
    #print(num_edges)


if __name__ == '__main__':
    start()
