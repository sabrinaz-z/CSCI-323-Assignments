# Analysis of Algorithms (CSCI 323)
# Summer 2024
# Assignment 8 - Shortest Path Algorithms
# Sabrina Zheng

# Acknowledgements:
# I worked with class
# I used the following sites

import Assignment7 as as7
import copy


# [1] Define a function floyd_apsp(graph) that solves APSP for a graph using Floyd's dynamic programming algorithm.
# See https://www.geeksforgeeks.org/floyd-warshall-algorithm-dp-16/
def floyd_apsp(matrix):
    dist = copy.deepcopy(matrix)
    dist = list(map(lambda i: list(map(lambda j: j, i)), graph))
    for k in range(V):
        for i in range(V):
            for j in range(V):
                dist[i][j] = min(dist[i][j],
                                 dist[i][k] + dist[k][j]
                                 )
    printSolution(dist)


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