# Analysis of Algorithms (CSCI 323)
# Summer 2024
# Assignment 7 - Graphs and Graph Algorithms
# Sabrina Zheng

# Acknowledgements:
# I worked with class
# I used the following sites

from random import random, randint
import numpy as np


def do_graph(des, matrix, directed):
    print(des)
    print_adj_matrix(matrix)
    table = adjacency_table(matrix)
    print_adj_table(table)
    edges = edge_set(matrix, directed)
    print_edge_set(edges)
    map = edge_map(matrix, directed)
    print_edge_map(map)


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


# [9] Define a function print_graph_tabular(matrix) that prints a graph in tabular form.


def main():
    matrix = read_graph("Graph.txt")
    do_graph("Graph from file Graph.txt", matrix, directed=True)

    matrix2 = random_graph(10, max_cost=9, directed=True)
    do_graph("Random Directed Graph of size 10", matrix2, directed=True)

    matrix3 = random_graph(10, max_cost=9, directed=False)
    do_graph("Random Undirected Graph of size 10", matrix3, directed=False)



if __name__ == '__main__':
    main()
