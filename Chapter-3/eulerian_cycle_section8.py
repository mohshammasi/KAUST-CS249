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

def create_cycle(graph):
    # pick first node/edge in graph dictionary
    first_key = next(iter(graph))
    e = next(iter(graph[first_key])) # get first element in set - "conceptually" sets dont have first elements
    cycle = first_key + "->" + e
    graph[first_key].remove(e)

    # If there are no more outgoing edges in that node delete the node from dict
    if len(graph[first_key]) == 0:
        del graph[first_key]

    # Add nodes to the cycle until we find an edge from the final node in the cycle to the first
    while True:
        cycle_nodes = cycle.split('->')
        idx = len(cycle_nodes)-1
        last_n_in_cycle = cycle_nodes[idx]
        try:
            edges = graph[last_n_in_cycle] # get edges from the final node in the cycle
            e = next(iter(edges))
            cycle += "->" + e
            graph[last_n_in_cycle].remove(e)
            if len(graph[last_n_in_cycle]) == 0:
                del graph[last_n_in_cycle]
        except KeyError as e:
            #print('we are probably back at the start so stop here')
            break
    return cycle, graph


def select_new_node(cycle, unexplored_graph):
    try:
        nodes = cycle.split('->')
        length = 0
        for i in range(0, len(nodes)):
            if nodes[i] in unexplored_graph:
                return nodes[i], ((2*i)+length)
            length += len(nodes[i])
    except TypeError as e:
        print(e)


def expand_cycle(new_start, idx, cycle, unexplored_graph):
    # Rearrange the cycle to use the new start index
    nodes = cycle.split('->')
    length = 0
    for i in range(1, len(nodes)):
        if nodes[i] == new_start:
            break
        length += len(nodes[i])

    cycle = cycle[idx:] + "->" + cycle[idx-((2*(i-1))+length):idx] + new_start

    # Add nodes to the cycle until we find an edge from the final node in the cycle to the first
    while True:
        cycle_nodes = cycle.split('->')
        idx = len(cycle_nodes)-1
        last_n_in_cycle = cycle_nodes[idx]
        try:
            edges = unexplored_graph[last_n_in_cycle] # get edges from the final node in the cycle
            e = next(iter(edges))
            cycle += "->" + e
            unexplored_graph[last_n_in_cycle].remove(e)
            if len(unexplored_graph[last_n_in_cycle]) == 0:
                del unexplored_graph[last_n_in_cycle]
        except KeyError as e:
            #print('we are probably back at the start so change start')
            break
    return cycle, unexplored_graph


def eulerian_cycle(graph):
    cycle, unexplored_graph = create_cycle(graph)
    while len(unexplored_graph) != 0:
        new_start, idx = select_new_node(cycle, unexplored_graph)
        cycle, unexplored_graph = expand_cycle(new_start, idx, cycle, unexplored_graph)
    return cycle


def start():
    graph = read_input("dataset.txt")
    result = eulerian_cycle(graph)
    try:
        output_file = open("output.txt", "w")
        for string in result:
            output_file.write(string + '\n')
        output_file.close()
        print("Output written successfully to the textfile.")
    except:
        print('File I/O Error...')
    nodes = result.split('->')
    num_edges = len(nodes)-1
    print(num_edges)


if __name__ == '__main__':
    start()
