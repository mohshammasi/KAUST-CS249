import numpy as np

def read_input(filename):
    try:
        input_file = open(filename, "r")
        n = input_file.readline().rstrip('\n')
        graph = dict()
        degrees = dict()
        for line in input_file:
            node_and_weight = line.split('->')[1].rstrip('\n').split(':')
            n_a_w = (node_and_weight[0], node_and_weight[1])
            node = line.split('->')[0]
            graph.setdefault(node, []).append(n_a_w)

            # Record degree of each node
            degrees[node] = degrees.get(node, 0) + 1
            degrees[node_and_weight[0]] = degrees.get(node_and_weight[0], 0) + 1
        input_file.close()
    except:
        print("Exception caught, file probably doesnt exist")
    return int(n), graph, degrees

def print_matrix(n, m, matrix):
    for i in range(n):
        for j in range(m):
            print(matrix[i][j], end=" ")
        print()
    print('\n')
    return

def write_matrix(n, m, matrix):
    try:
        output_file = open("output.txt", "w")
        for i in range(n):
            for j in range(m):
                output_file.write(str(matrix[i][j]) + ' ')
            output_file.write('\n')
        output_file.close()
        print("Output written successfully to the textfile.")
    except:
        print('File I/O Error...')

# BFS to find the paths from a certain node in the tree
def breadth_first_search(graph, root):
    q = [root]
    visited = dict()
    visited[root] = True

    paths_cost = dict()
    paths_cost[root] = 0
    while len(q) != 0:
        v = q.pop(0)
        visited[v] = True
        # Edges are stored as tuples with weights, e[0] is the node, e[1] is the weight
        for edge in graph[v]:
            if edge[0] not in visited:
                q.append(edge[0])
                paths_cost[edge[0]] = paths_cost[v] + int(edge[1])
    return paths_cost

def distance_matrix(n, graph, degrees):
    # Since im representing the graph as an adjacency list with DIRECTED edges
    # for graphs with UNDIRECTED edges. Leaves 'appear' to have a degree of 2 in the AL
    leaves = []
    for node in degrees:
        if degrees[node] == 2:
            leaves.append(node)

    # Create distance matrix initialised with 0's
    d_matrix = np.zeros((n, n), dtype=int)

    for i, leaf in enumerate(leaves):
        paths = breadth_first_search(graph, leaf)
        for j in range(0, n):
            d_matrix[i][j] = paths[leaves[j]]
    return d_matrix

def start():
    n, graph, degrees = read_input("dataset.txt")
    result = distance_matrix(n, graph, degrees)
    #print_matrix(n, n, result)
    write_matrix(n, n, result)

if __name__ == '__main__':
    start()
