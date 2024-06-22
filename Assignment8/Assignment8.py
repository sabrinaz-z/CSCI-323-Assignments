# Analysis of Algorithms (CSCI 323)
# Summer 2024
# Assignment 8 - Shortest Path Algorithms
# Sabrina Zheng

# Acknowledgements:
# I worked with class
# I used the following sites

import Assignment7 as as7
import Assignment1 as as1
from time import time
import copy


inf = 9999


# [1] Define a function floyd_apsp(graph) that solves APSP for a graph using Floyd's dynamic programming algorithm.
# See https://www.geeksforgeeks.org/floyd-warshall-algorithm-dp-16/
def floyd_apsp(matrix):
    n = len(matrix)
    pred = [[i if matrix[i][j] < inf else -1 for j in range(n)] for i in range(n)]
    dist = copy.deepcopy(matrix)
    for i in range(n):
        dist[i][i] = 0

    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    pred[i][j] = pred[k][j]
    return dist, pred


def zero_to_inf(matrix):
    n = len(matrix)
    return [[inf if matrix[i][j] == 0 else matrix[i][j] for j in range(n)] for i in range(n)]


# [4] Define a function dijkstra_sssp_matrix(graph, src) that takes a graph and a starting point, and solves SSSP
# using Dijsktra's greedy SSSP algorithm, assuming an adjacency matrix and minimization over an array. See
# https://www.geeksforgeeks.org/dijkstras-shortest-path-algorithm-greedy-algo-7/
def min_dist(dist, s):
    best_i = -1
    best_dist = inf
    n = len(dist)
    for i in range(n):
        if i not in s and dist[i] < best_dist:
            best_dist = dist[i]
            best_i = i
    return best_i


def dijkstra_sssp(matrix, src):
    n = len(matrix)
    dist = [inf] * n
    pred = [-1] * n
    dist[src] = 0
    s = []
    for i in range(n):
        x = min_dist(dist, s)
        s.append(x)
        for y in range(n):
            if y not in s and dist[x] + matrix[x][y] < dist[y]:
                dist[y] = dist[x] + matrix[x][y]
                pred[y] = x
    return dist, pred


# [7] Define a wrapper function dijkstra_apsp that calls dijsktra_sssp for each of the n possible sources.
def dijkstra_apsp(matrix):
    dist = []
    pred = []
    n = len(matrix)
    for src in range(n):
        d, p = dijkstra_sssp(matrix, src)
        dist.append(d)
        pred.append(p)
    return dist, pred


# [2] Define a function bellman_ford_sssp(es, n, src) that takes an edge-set of the graph, the size of the graph,
# and a starting point, and solves SSSP using the Bellman Ford dynamic programming algorithm. See
# https://www.geeksforgeeks.org/bellman-ford-algorithm-dp-23/
def bellman_ford_sssp(matrix, src):
    n = len(matrix)
    pred = [-1] * n
    dist = [inf] * n
    dist[src] = 0
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if matrix[i][j] < inf and dist[i] + matrix[i][j] < dist[j]:
                    dist[j] = dist[i] + matrix[i][j]
                    pred[j] = i
    for i in range(n):
        for j in range(n):
            if matrix[i][j] < inf and dist[i] + matrix[i][j] < dist[j]:
                print("Negative weight cycle detected")

    return dist, pred


def bellman_ford_apsp(matrix):
    dist = []
    pred = []
    n = len(matrix)
    for src in range(n):
        d, p = bellman_ford_sssp(matrix, src)
        dist.append(d)
        pred.append(p)
    return dist, pred


def run_algs(algs, sizes, trials):
    dict_algs = {}
    for alg in algs:
        dict_algs[alg.__name__] = {}
    for size in sizes:
        for alg in algs:
            dict_algs[alg.__name__][size] = 0
        for trial in range(1, trials + 1):
            matrix = as7.random_graph(size, max_cost=99, p=.5, directed=True)
            matrix = zero_to_inf(matrix)
            if size == sizes[0]:
                print("Matrix")
                as7.print_adj_matrix(matrix)
            for alg in algs:
                start_time = time()
                dist, pred = alg(matrix)
                end_time = time()
                net_time = end_time - start_time
                dict_algs[alg.__name__][size] += 1000 * net_time
                if size == sizes[0]:
                    print("\n", alg.__name__)
                    print("Dist")
                    as7.print_adj_matrix(dist)
                    print("Pred")
                    as7.print_adj_matrix(pred)
    return dict_algs


def main():
    # matrix = as7.random_graph(10, max_cost=99, p=.5, directed=True)
    # matrix = zero_to_inf(matrix)
    # as7.print_adj_matrix(matrix)
    # dist, pred = floyd_apsp(matrix)
    # as7.print_adj_matrix(dist)
    # as7.print_adj_matrix(pred)
    # dist, pred = dijkstra_apsp(matrix)
    # as7.print_adj_matrix(dist)
    # as7.print_adj_matrix(pred)
    # dist, pred = bellman_ford_apsp(matrix)
    # as7.print_adj_matrix(dist)
    # as7.print_adj_matrix(pred)

    algs = [dijkstra_apsp, bellman_ford_apsp, floyd_apsp]
    sizes = [10, 20, 30, 40, 50, 60, 70, 80]
    trials = 1
    dict_algs = run_algs(algs, sizes, trials)
    as1.print_times(dict_algs)
    desc = "Graph APSP"
    as1.plot_times(desc, dict_algs, sizes, trials, algs, file_name="Assignment8-times.png")


if __name__ == '__main__':
    main()
