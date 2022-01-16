
def read_input(filename):
    try:
        input_file = open(filename, "r")
        graph_al = dict()
        for line in input_file:
            graph_al[line.split(' ')[0]] = set(num for num in line.split('->')[1][1:].rstrip('\n').split(','))
        input_file.close()
    except:
        print("Exception caught, file probably doesnt exist")

    # Add the nodes with no incoming edges to the graph with empty lists
    new_keys = []
    for node in graph_al:
        for node2 in graph_al[node]:
            if node2 not in graph_al:
                new_keys.append({node2:[]})

    for key in new_keys:
        graph_al.update(key)

    return graph_al

def topological_sort(graph):
    # Create a dict of indegrees
    indegrees = dict.fromkeys(graph.keys(), 0)
    for node in graph:
        for node2 in graph:
            if node in graph[node2]:
                indegrees[node] += 1
    #print(indegrees)

    order = []
    candidates = set(node for node in indegrees if indegrees[node] == 0)
    #print(candidates)

    while len(candidates) != 0:
        a = next(iter(candidates)) # pick an element
        candidates.remove(a)
        order.append(a)
        while len(graph[a]) != 0:
            b = next(iter(graph[a])) # pick an element
            graph[a].remove(b)
            has_incoming = False
            for node in graph:
                if b in graph[node]:
                    has_incoming = True

            if not has_incoming:
                candidates.add(b)

    has_edges = False
    for node in graph:
        if len(graph[node]) != 0:
            has_edges = True
            break
    if has_edges:
        return "The input graph is not a DAG"
    else:
        return order

def start():
    graph = read_input("dataset.txt")
    result = topological_sort(graph)
    for ordering in result:
        print(int(ordering), end=", ")
    print()

if __name__ == '__main__':
    start()
