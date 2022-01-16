import numpy as np
from math import ceil

def read_input(filename):
    try:
        input_file = open(filename, "r")
        graph_al = dict()
        for line in input_file:
            graph_al[line.split(' ')[0]] = set(num for num in line[len(line.split(' ')[0])+4:].rstrip('\n').split(','))
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

def create_path(graph):
    # Create a dict of degrees
    degrees = dict.fromkeys(graph.keys(), 0)
    for node in graph:
        degrees[node] = len(graph[node])
        for node2 in graph:
            if node in graph[node2]:
                degrees[node] += 1

    # Pick the node with odd degree as starting node since its unbalanced
    for node in degrees:
        if (degrees[node] % 2) != 0:
            first_node = node
            break

    # pick first node/edge in graph dictionary
    e = next(iter(graph[first_node]))
    path = first_node + "->" + e
    graph[first_node].remove(e)

    # If there are no more outgoing edges in that node delete the node from dict
    if len(graph[first_node]) == 0:
        del graph[first_node]

    # Add nodes to the path until we find an edge from the final node in the path to the first
    while True:
        path_nodes = path.split('->')
        idx = len(path_nodes)-1
        last_n_in_path = path_nodes[idx]
        try:
            edges = graph[last_n_in_path] # get edges from the final node in the path
            e = next(iter(edges))
            path += "->" + e
            graph[last_n_in_path].remove(e)
            if len(graph[last_n_in_path]) == 0:
                del graph[last_n_in_path]
        except KeyError as e:
            #print('we are probably back at the start so stop here')
            break
    return path, graph


def select_new_node(path, graph):
    try:
        # Create a dict of degrees
        degrees = dict.fromkeys(graph.keys(), 0)
        for node in graph:
            degrees[node] = len(graph[node])
            for node2 in graph:
                if node in graph[node2]:
                    degrees[node] += 1

        # Pick the node with odd degree as starting node since its unbalanced
        i=0
        for node in degrees:
            if (degrees[node] % 2) != 0:
                i+=1
                print('returning ', node)
                return node

        # if the code reaches this point that means that no odds were found
        # grab anything that has an edge to the first thing in our path
        path_nodes = path.split('->')
        first_node = path_nodes[0]
        for node in graph:
            if first_node in graph[node]:
                return node

    except TypeError as e:
        print('no odds found', e)
        print(i)


def expand_back_path(first_node, path, graph):
    # pick first node/edge in graph dictionary
    e = next(iter(graph[first_node]))
    path = first_node + "->" + e
    graph[first_node].remove(e)

    # If there are no more outgoing edges in that node delete the node from dict
    if len(graph[first_node]) == 0:
        del graph[first_node]
    return path, graph

def expand(path, graph):
    # Add nodes to the path until we find an edge from the final node in the path to the first
    while True:
        path_nodes = path.split('->')
        idx = len(path_nodes)-1
        last_n_in_path = path_nodes[idx]
        try:
            edges = graph[last_n_in_path] # get edges from the final node in the path
            e = next(iter(edges))
            path += "->" + e
            graph[last_n_in_path].remove(e)
            if len(graph[last_n_in_path]) == 0:
                del graph[last_n_in_path]
        except KeyError as e:
            #print('we are probably back at the start so change start')
            break
    return path, graph

def brute_expand(path, graph):
    path_nodes = path.split('->')
    length = 0
    for i in range(0, len(path_nodes)):
        if path_nodes[i] in graph:
            e = next(iter(graph[path_nodes[i]]))
            sub_path = path_nodes[i] + "->" + e
            graph[path_nodes[i]].remove(e)
            if len(graph[path_nodes[i]]) == 0:
                del graph[path_nodes[i]]
            expanded_sub_path, graph = expand(sub_path, graph)

            # insert it where it belongs in the path
            path = path[:((2*i)+length)] + expanded_sub_path + path[((2*i)+length)+len(path_nodes[i]):]
            break
        length += len(path_nodes[i])
    return path, graph

def eulerian_path(graph):
    path, graph = create_path(graph)
    while len(graph) != 0:
        path, graph = brute_expand(path, graph)
        new_start = select_new_node(path, graph)
        if new_start is not None:
            expanded_path, graph = expand_back_path(new_start, path, graph)
            expanded_nodes = expanded_path.split('->')
            idx = len(expanded_nodes)-1
            l = len(expanded_nodes[idx])
            path = expanded_path[:-(l)] + path
    return path


def start():
    graph = read_input("dataset.txt")
    result = eulerian_path(graph)
    try:
        output_file = open("output.txt", "w")
        for string in result:
            output_file.write(string)
        output_file.close()
        print("Output written successfully to the textfile.")
    except:
        print('File I/O Error...')
    nodes = result.split('->')
    num_edges = len(nodes)-1
    print(num_edges)


if __name__ == '__main__':
    start()
