# Assignment 2 Dijkstra's Algorithm

# Author: Dr. Neha Karanjkar

'''
	Team Members:
1. Aniket Akshay Chaudhri (2003104)
2. Adarsh Anand (2003101)

Date - 29 September 2022
'''

import random
import math
import os
import numpy as np
from math import inf as INF  # positive infinity


def generate_a_random_undirected_graph(num_nodes):
    """
    A function that randomly generates a graph
given the number of nodes, and returns
    the Adjacency matrix with edge costs.
    The edge cost is INF (infinity) if there is
    no direct edge between two nodes
    """

    G = [[] for i in range(num_nodes)]
    for i in range(num_nodes):
        for j in range(num_nodes):
            if (i == j):
                edge_cost = 0
            elif (j < i):
                edge_cost = G[j][i]
            else:
                if (random.random() < 0.5):
                    edge_cost = INF
                else:
                    edge_cost = random.randint(1, 10)
            G[i].append(edge_cost)
    return G


def visualize_graph(G, show_edge_labels=False, node_labels=None):
    """
    Given the graph connectivity matrix G,
    this function generates a visualization of the
    graph as a ".dot" file.

    NOTE: the ".dot" file can be viewed in a browser (http://www.webgraphviz.com/)
    OR converted into a pdf file using graphviz by running the command
            dot -Tpdf dot_file.dot -o plot.pdf
    """
    if node_labels == None:
        node_labels = [str(i) for i in range(len(G))]
    with open("dot_file.dot", "w") as f:
        print("graph  {", file=f)
        for i in range(len(G)):
            print(node_labels[i]+";", file=f)
        for i in range(len(G)):
            for j in range(len(G)):
                if (G[i][j] != INF and j > i):
                    if show_edge_labels:
                        print(
                            f"{node_labels[i]} -- {node_labels[j]}  [weight={G[i][j]}, label=\"{G[i][j]}\"];", file=f)
                    else:
                        print(
                            f"{node_labels[i]} -- {node_labels[j]}  [weight={G[i][j]}];", file=f)
        print("}", file=f)
    # ---- optional-----
    os.system("dot -Tpdf dot_file.dot -o plot.pdf")
    # -------------------


def label(node):
    if node_labels and (node != None):
        return node_labels[node]
    else:
        return str(node)


def find_shortest_paths(source_node, graph, node_labels=None):
    # Find Shortest paths from source_node to
    # all other nodes using Dijkstra's algorithm.
    #
    #
    # Returns lists D and p for every node v
    #
    # where D(v): shortest distance from source to v
    #   and p(v): previous node to v on the shortest path
    # If v is not reachable from source, D(v)=INF and p(v)=None

    # function to return the label of a node(number)

    D, p, done_nodes, nodes_to_process = Initialize(source_node, graph, label)

    # initialize the step counter
    step = 0

    while len(nodes_to_process) > 0:
        # print the current step
        if step:
            print(f"{step}\t", end="")

        min_node = FindMinNode(D, nodes_to_process, done_nodes)

        RelaxNode(graph, D, p, nodes_to_process, min_node)

        PrintTable(source_node, graph, label, D, p, done_nodes, step, min_node)

        step += 1


def PrintTable(source_node, graph, label, D, p, done_nodes, step, min_node):
    # print the distance and previous node lists
    if step:
        for i in range(len(graph)):
            # if current node is the minimum node, print * before the distance
            if i == min_node:
                print(f"*{D[i]},{label(p[i])}\t\t", end="")
            else:
                # if source node, print 0, source node
                if i == source_node:
                    print(f"0,{label(source_node)}\t\t", end="")
                else:
                    if (D[i] == INF):
                        print(f"0,{label(source_node)}\t", end="")
                    else:
                        print(f"{D[i]},{label(p[i])}\t\t", end="")
        print(done_nodes)


def RelaxNode(graph, D, p, nodes_to_process, min_node):
    # update the distance and previous node lists
    for node in nodes_to_process:
        if graph[min_node][node] != INF:
            if D[node] > D[min_node] + graph[min_node][node]:
                D[node] = D[min_node] + graph[min_node][node]
                p[node] = min_node


def FindMinNode(D, nodes_to_process, done_nodes):
    # find the node with the minimum distance
    min_node = nodes_to_process[0]
    for node in nodes_to_process:
        if D[node] < D[min_node]:
            min_node = node

    # add the node with the minimum distance to the list of done nodes
    done_nodes.append(label(min_node))

    # remove the node with the minimum distance from the list of nodes to be processed
    nodes_to_process.remove(min_node)

    return min_node


def Initialize(source_node, graph, label):
    print("---------------------")
    print("Source node:", label(source_node))

    # print a table of D and p for each node and a list of done nodes
    # Print table in this format: Step D(u),p(u)   D(v),p(v)   D(w),p(w)   D(x),p(x)   D(y),p(y)   D(z),p(z)   Done Nodes
    # where u,v,w,x,y,z are the nodes and D(u),p(u) is the distance and previous node of u (for example, D(u),p(u) = 0, None)
    # and Done Nodes is the list of nodes that have been processed so far

    print("Step\t", end="")
    for i in range(len(graph)):
        print(f"D({label(i)}),p({label(i)})\t", end="")
    print("Done Nodes")

    # initialize the distance and previous node lists
    D = [INF for i in range(len(graph))]
    p = [None for i in range(len(graph))]

    # initialize the distance of the source node to 0
    D[source_node] = 0

    # initialize the list of done nodes
    done_nodes = []

    # initialize the list of nodes to be processed
    nodes_to_process = [i for i in range(len(graph))]
    return D, p, done_nodes, nodes_to_process


#     u   v   w   x   y   z
G = [[0,  2,  5,  1,  INF, INF],  # u
     [2,  0,  3,  2,  INF, INF],  # v
     [5,  3,  0,  3,  1,  5],  # w
     [1,  2,  3,  0,  1,  INF],  # x
     [INF, INF, 1,  1,  0,  2],  # y
     [INF, INF, 5,  INF, 2,  0]]  # z

# G = generate_a_random_undirected_graph(5)

print(np.matrix(G))
node_labels = ['u', 'v', 'w', 'x', 'y', 'z']
visualize_graph(G, show_edge_labels=True, node_labels=node_labels)
for s in range(len(G)):
    find_shortest_paths(source_node=s, graph=G, node_labels=node_labels)
exit()
