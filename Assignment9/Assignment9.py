# Analysis of Algorithms (CSCI 323)
# Summer 2024
# Assignment 9 - Minimum Spanning Tree Algorithms
# Sabrina Zheng

# Acknowledgements:
# I worked with class
# I used the following sites

import Assignment1 as as1
import Assignment7 as as7
import Assignment4 as as4
from time import time
INF = 9999


def prim_mst(matrix):
    n = len(matrix)
    keys = [INF] * n
    parents = [None] * n
    keys[0] = 0
    mst = [False] * n
    mst_edges = []
    parents[0] = -1
    for i in range(n):
        u, min_cost = closest(keys, mst)
        if u == 0:
            w = -1
            for w in range(1, n):
                if matrix[u][w] == min_cost:
                    break
            # mst_edges.append([u, w, matrix[u][w]])
        else:
            mst_edges.append([parents[u], u, matrix[parents[u]][u]])
        mst[u] = True
        for v in range(n):
            if not mst[v] and matrix[u][v] < INF and matrix[u][v] < keys[v]:
                keys[v] = matrix[u][v]
                parents[v] = u
    result = []
    for i in range(1, n):
        result.append([parents[i], matrix[i][parents[i]]])
    cost = sum([result[i][1] for i in range(len(result))])
    return cost, mst_edges


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
    return min_index, min_cost


def find(parents, i):
    while parents[i] != i:
        i = parents[i]
    return i


def union(parents, i, j):
    a = find(parents, i)
    b = find(parents, j)
    parents[a] = b


def make_set(matrix):
    n = len(matrix)
    parents = [i for i in range(n)]
    return parents


def kruskal_mst(matrix):
    min_cost = 0
    mst_edges = []
    n = len(matrix)
    parents = make_set(matrix)
    edge_count = 0
    while edge_count < n - 1:
        min_edge = INF
        a = -1
        b = -1
        for i in range(n):
            for j in range(n):
                if find(parents, i) != find(parents, j) and matrix[i][j] < min_edge:
                    min_edge = matrix[i][j]
                    a = i
                    b = j
        union(parents, a, b)
        mst_edges.append([a, b, min_edge])
        edge_count += 1
        min_cost += min_edge
    return min_cost, mst_edges


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
                cost, mst_edge = alg(matrix)
                end_time = time()
                if size == sizes[0]:
                    print(alg.__name__, "has cost", cost, "with MST", mst_edge)
                    edges = [(mst_edge[0], mst_edge[1]) for mst_edge in mst_edge]
                    as7.draw_graph(edges, False, f"Assignment9{alg.__name__}.png")
                net_time = end_time - start_time
                dict_algs[alg.__name__][size] += 1000 * net_time
    return dict_algs


def main():
    algs = [prim_mst, kruskal_mst]
    sizes = [10, 20, 30, 40]
    trials = 10
    dict_algs = run_algs(algs, sizes, trials)
    as1.print_times(dict_algs)
    as1.plot_times("MST", dict_algs, sizes, trials, algs, "Assignment9.png")






if __name__ == '__main__':
    main()
