import ast
from math import ceil

def read_input(filename):
    try:
        input_file = open(filename, "r")
        edges = input_file.readline().rstrip('\n')
        edges = ast.literal_eval(edges)
        edges = [e for e in edges]
        two_break = input_file.readline().rstrip('\n').split(", ")
        two_break = [int(i) for i in two_break]
        input_file.close()
    except:
        print("Exception caught, file probably doesnt exist")
    return edges, two_break

def two_break_on_genome_graph(graph, i1, i2, i3, i4):
    n = len(graph)
    i = 0
    while i < n:
        if (i1 in graph[i]) and (i2 in graph[i]):
            del graph[i]
            graph.insert(i, (i2, i4))
        elif (i3 in graph[i]) and (i4 in graph[i]):
            del graph[i]
            graph.insert(i, (i1, i3))
        else:
            i += 1
    return graph

def start():
    edges, two_break = read_input("dataset.txt")
    result = two_break_on_genome_graph(edges, *two_break)
    for edge in result:
        print(edge, end=", ")
    print()


if __name__ == '__main__':
    start()
