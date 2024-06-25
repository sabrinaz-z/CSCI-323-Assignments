# Analysis of Algorithms (CSCI 323)
# Summer 2024
# Assignment 9 - Minimum Spanning Tree Algorithms
# Sabrina Zheng

# Acknowledgements:
# I worked with class
# I used the following sites

import Assignment1 as as1
import Assignment7 as as7
from time import time
INF = 9999


def prim_mst(matrix):
    n = len(matrix)
    keys = [INF] * n
    parents = [None] * n
    keys[0] = 0
    mst = [False] * n
    cost = 0
    parents[0] = -1
    for i in range(n):
        u = closest(keys, mst)
        mst[u] = True
        for v in range(n):
            if not mst[v] and matrix[u][v] < INF and matrix[u][v] < keys[v]:
                keys[v] = matrix[u][v]
                parents[v] = u
    result = []
    for i in range(1, n):
        result.append([parents[i], matrix[i][parents[i]]])
    cost = sum([result[i][1] for i in range(len(result))])
    return cost, result


def zero_to_inf(matrix):
    n = len(matrix)
    return [[INF if matrix[i][j] == 0 else matrix[i][j] for j in range(n)] for i in range(n)]


def closest(keys, mst):
    min_cost = INF
    min_index = -1
    n = len(keys)
    for v in range(n):
        if not mst[v] and keys[v] < min_cost:
            min_cost = keys[v]
            min_index = v
    return min_index


def kruskal_mst(matrix):
    pass


def run_algs(algs, sizes, trials):
    dict_algs = {}
    for alg in algs:
        dict_algs[alg.__name__] = {}
    for size in sizes:
        for alg in algs:
            dict_algs[alg.__name__][size] = 0
        for trial in range(1, trials + 1):
            matrix = as7.random_graph(size, 99, 0.5, False)
            matrix = zero_to_inf(matrix)
            for alg in algs:
                start_time = time()
                cost, result = alg(matrix)
                end_time = time()
                if size == sizes[0]:
                    print(alg.__name__, "has cost", cost, "with MST", result)
                net_time = end_time - start_time
                dict_algs[alg.__name__][size] += 1000 * net_time
    return dict_algs


def main():
    algs = [prim_mst]
    sizes = [10, 20, 30, 40]
    trials = 10
    dict_algs = run_algs(algs, sizes, trials)
    as1.print_times(dict_algs)
    as1.plot_times(dict_algs, sizes, trials, algs, "Assignment9.png")


if __name__ == '__main__':
    main()
