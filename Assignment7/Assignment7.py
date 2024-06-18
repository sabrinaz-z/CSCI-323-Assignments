# Analysis of Algorithms (CSCI 323)
# Summer 2024
# Assignment 7 - Graphs and Graph Algorithms
# Sabrina Zheng

# Acknowledgements:
# I worked with class
# I used the following sites

from random import random, randint
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from time import time


def do_graph(des, matrix, directed):
    print(des)
    print_adj_matrix(matrix)
    table = adjacency_table(matrix)
    print_adj_table(table)
    edges = edge_set(matrix, directed)
    print_edge_set(edges)
    map = edge_map(matrix, directed)
    print_edge_map(map)
    bfs_visited = [False] * len(matrix)
    bfs_order = bfs(table, 0, bfs_visited)
    print("The BFS:", bfs_order)
    dfs_order = dfs(table, 0)
    print("The DFS:", bfs_order)
    file_name = "Assignment7_" + des.replace(" ", "_") + ".png"
    draw_graph(edges, directed, file_name)


def print_edge_set(edges):
    print(edges)
    print()


def print_edge_map(map):
    for i in map:
        print(i, ":", map[i])
    print()


def print_adj_matrix(matrix):
    print(np.array(matrix))
    print()


def print_adj_table(table):
    n = len(table)
    for i in range(n):
        print(i, ":", table[i])
    print()


# [1] Define a function read_graph(file_name) that reads a graph from a text file and returns an adjacency/cost matrix.
def read_graph(file_name):
    with open(file_name) as f:
        lines = f.readlines()
        matrix = [[int(cost) for cost in line.strip().split(" ")] for line in lines]
        return matrix


# [2] Define a function adjacency_table(matrix) that accepts a graph as an adjacency/cost matrix and returns an
# adjacency/cost table.
def adjacency_table(matrix):
    n = len(matrix)
    table = [[] for i in range(n)]
    for i in range(n):
        for j in range(n):
            if matrix[i][j] > 0:
                table[i].append(j)
    return table


# [3] Define a function edge_set(matrix) that accepts a graph as an adjacency/cost matrix and returns an edge/cost set.
def edge_set(matrix, directed):
    n = len(matrix)
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            if matrix[i][j] > 0:
                edges.append((i, j))
            if directed and matrix[j][i] > 0:
                edges.append((j, i))
    return edges


# [4] Define a function edge_map(matrix) that accepts a graph as an adjacency/cost matrix and returns an edge/cost set.
def edge_map(matrix, directed=False):
    n = len(matrix)
    graph_map = {}
    for i in range(n):
        for j in range(i + 1, n):
            if matrix[i][j] > 0:
                graph_map[f"{i}-{j}"] = matrix[i][j]
            if directed and matrix[j][i] > 0:
                graph_map[f"{j}-{i}"] = matrix[j][i]
    return graph_map


# [6] Define a function random_graph(size, max_cost, p=1) that generates a graph with size edges, where each edge (
# except loops/self-edges) is assigned a random integer cost between 1 and max_cost. The additional parameter p
# represents the probability that there should be an edge between a given pair of vertices.
def random_graph(size, max_cost, p=1, directed=False):
    matrix = [[0] * size for i in range(size)]
    for i in range(size):
        for j in range(i + 1, size):
            if random() < p:
                matrix[i][j] = randint(1, max_cost)
                if not directed:
                    matrix[j][i] = matrix[i][j]
                elif random() < p:
                    matrix[j][i] = randint(1, max_cost)
    return matrix


# [7] Define functions that traverse the graph in these two standard orderings
# Breadth-First Search (BFS)
def bfs(adjList, startNode, visited):
    bfs_order = []
    q = []
    visited[startNode] = True
    bfs_order.append(startNode)
    q.append(startNode)
    while q:
        node = q.pop()
        for neighbor in adjList[node]:
            if not visited[neighbor]:
                visited[neighbor] = True
                bfs_order.append(neighbor)
                q.append(neighbor)
    return bfs_order


# Depth-First Search (DFS)
def dfs_util(table, v, visited, dfs_order):
    visited.add(v)
    dfs_order.append(v)
    for w in table[v]:
        if w not in visited:
            dfs_util(table, w, visited, dfs_order)


def dfs(table, v):
    visited = set()
    dfs_order = []
    dfs_util(table, v, visited, dfs_order)
    return dfs_order


# [9] Define a function print_graph_tabular(matrix) that prints a graph in tabular form.

# [10] Define a function draw_graph(graph) that draws a graph
# Define a function draw_graph(graph) that draws a graph and saves it as a file.
# https://stackoverflow.com/questions/20133479/how-to-draw-directed-graphs-using-networkx-in-python
# https://stackoverflow.com/questions/74312314/draw-a-directed-graph-in-python
def draw_graph(edges, directed, filename):
    G = nx.DiGraph()
    G.add_edges_from(edges)
    val_map = {'A': 1.0, 'D': 0.5714285714285714, 'H': 0.0}
    values = [val_map.get(node, 0.25) for node in G.nodes()]
    pos = nx.spring_layout(G)
    cmap = plt.get_cmap('jet')
    nx.draw_networkx_nodes(G, pos, cmap=cmap, node_color=values, node_size=500)
    nx.draw_networkx_labels(G, pos, font_size=12, font_color='white')
    if directed:
        nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color='r', arrows=directed, arrowsize=10)
    else:
        nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color='r', arrows=False)

    plt.savefig(filename)
    plt.show()


def main():
    matrix = read_graph("Graph.txt")
    do_graph("Graph from file Graph.txt", matrix, True)

    matrix2 = random_graph(10, max_cost=9, directed=True)
    do_graph("Random Directed Graph of size 10", matrix2, True)

    matrix3 = random_graph(10, max_cost=9, directed=False)
    do_graph("Random Undirected Graph of size 10", matrix3, False)

    matrix4 = random_graph(10, max_cost=9, p=.4, directed=False)
    do_graph("Random Undirected Graph of size 10", matrix4, False)


if __name__ == '__main__':
    main()
