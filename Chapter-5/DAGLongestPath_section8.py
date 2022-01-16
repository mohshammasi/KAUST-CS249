import numpy as np
import random
from topological_sort_section17 import topological_sort

def read_input(filename):
    try:
        input_file = open(filename, "r")
        # Read start and end nodes
        s = input_file.readline().rstrip('\n')
        e = input_file.readline().rstrip('\n')

        # Read the graph edges and weights
        sort_graph = dict() # contains each node and outgoing edge e.g. 1->2 entry is 1 : 2
        predecessors_al = dict() # contains each node and predecessors with weight e.g. for 1->2:5 entry is 2 : (1, 5)
        predecessors_solo = dict() # contains each node and predecessors without weight e.g. 1->2 enty is 2 : 1
        for line in input_file:
            node_and_weight = line.split('->')[1].rstrip('\n').split(':')
            n_a_w = (node_and_weight[0], node_and_weight[1])
            node = line.split('->')[0]
            if node in sort_graph:
                sort_graph[node].add(node_and_weight[0])
            else:
                sort_graph[node] = set([node_and_weight[0]])
                # must wrap first element with a list to avoid sets from breaking
                # set() interprets the argument as an interable

            p_node = node_and_weight[0]
            if p_node in predecessors_al:
                predecessors_solo[p_node].add(node)
                predecessors_al[p_node].add((node, node_and_weight[1]))
            else:
                predecessors_solo[p_node] = set([node])
                predecessors_al[p_node] = set([(node, node_and_weight[1])])
        #print('predecessors with weights:')
        #print(predecessors_al)
        input_file.close()
    except:
        print("Exception caught, file probably doesnt exist")

    # Add the nodes with no incoming edges to the graph with empty lists
    new_keys = []
    for node in sort_graph:
        for node2 in sort_graph[node]:
            if node2 not in sort_graph:
                new_keys.append({node2:[]})
    for key in new_keys:
        sort_graph.update(key)
    return s, e, sort_graph, predecessors_al, predecessors_solo

# This version enforces a specific node to be the last in the ordering
def topological_sort(graph, end):
    # Create a dict of indegrees
    indegrees = dict.fromkeys(graph.keys(), 0)
    for node in graph:
        for node2 in graph:
            if node in graph[node2]:
                indegrees[node] += 1

    order = []
    candidates = set(node for node in indegrees if indegrees[node] == 0)

    while len(candidates) != 0:
        a = random.sample(candidates, 1) # pick an element, returns it as a list hence [0]
        if a[0] == end and len(candidates) > 1:
            continue
        candidates.remove(a[0])
        order.append(a[0])
        while len(graph[a[0]]) != 0:
            b = next(iter(graph[a[0]])) # pick an element
            graph[a[0]].remove(b)
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

def LongestPath(s, e, sort_graph, predecessors_al):
    # Create a dict of indegrees
    indegrees = dict.fromkeys(sort_graph.keys(), 0)
    for node in sort_graph:
        for node2 in sort_graph:
            if node in sort_graph[node2]:
                indegrees[node] += 1

    longest_path = dict()
    for node in sort_graph:
        longest_path[node] = -float('inf')

    sorted_graph = topological_sort(sort_graph, e)
    #print(sorted_graph)

    backtrack = []
    for b in sorted_graph:
        if indegrees[b] == 0:
            longest_path[b] = 0
            continue
        max = -float('inf')
        node = None
        for a in predecessors_al[b]:
            if (int(longest_path[a[0]]) + int(a[1])) > max:
                max = int(longest_path[a[0]]) + int(a[1])
                node = a[0]
        backtrack.append(node)
        longest_path[b] = max

    backtrack = [n for n in backtrack if n != s] # remove start node
    #print(longest_path)
    return longest_path[e], backtrack


def OutputLP(backtrack, s, i, predecessors, path):
    if i == -1:
        path.insert(0, s)
        return path
    if backtrack[i] in predecessors[path[0]]:
        path.insert(0, backtrack[i])
        return OutputLP(backtrack[:-1], s, i-1, predecessors, path)
    else:
        return OutputLP(backtrack[:-1], s, i-1, predecessors, path)

def start():
    s, e, sort_graph, predecessors_al, predecessors_solo = read_input("dataset.txt")
    length, backtrack = LongestPath(s, e, sort_graph, predecessors_al)
    result = OutputLP(backtrack, s, len(backtrack)-1, predecessors_solo, [e])
    print(length)
    print('->'.join(result))

if __name__ == '__main__':
    start()
