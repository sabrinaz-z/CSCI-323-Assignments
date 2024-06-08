# Analysis of Algorithms (CSCI 323)
# Summer 2024
# Assignment 3 - Matrix Multiplication
# Sabrina Zheng

# Acknowledgements:
# I worked with class
# I used the following sites

import Assignment1 as as1
import numpy as np
from random import randint
from time import time


def random_matrix(size):
    return [[randint(1, 10) for _ in range(size)] for _ in range(size)]


# [1] numpy_mult (wrap the function provided by Python's famous NumPy package)
def numpy_mult(m1, m2):
    return np.dot(m1, m2)


# [3] simple_mult (our first approach, typically taught in Discrete Math and Linear Algebra)
def simple_mult(m1, m2):
    n = len(m1)
    return [[sum([m1[i][k] * m2[k][j] for k in range(n)]) for j in range(n)] for i in range(n)]


# [4] divconq_mult (our second approach, basic divide-and-conquer algorithm)
ROW_1 = 4
COL_1 = 4
ROW_2 = 4
COL_2 = 4


def add_matrix(matrix_A, matrix_B, matrix_C, split_index):
    for i in range(split_index):
        for j in range(split_index):
            matrix_C[i][j] = matrix_A[i][j] + matrix_B[i][j]


def initWithZeros(a, r, c):
    for i in range(r):
        for j in range(c):
            a[i][j] = 0


def multiply_matrix(matrix_A, matrix_B):
    col_1 = len(matrix_A[0])
    row_1 = len(matrix_A)
    col_2 = len(matrix_B[0])
    row_2 = len(matrix_B)

    if (col_1 != row_2):
        print("\nError: The number of columns in Matrix A  must be equal to the number of rows in Matrix B\n")
        return 0

    result_matrix_row = [0] * col_2
    result_matrix = [[0 for x in range(col_2)] for y in range(row_1)]

    if (col_1 == 1):
        result_matrix[0][0] = matrix_A[0][0] * matrix_B[0][0]

    else:
        split_index = col_1 // 2

        row_vector = [0] * split_index
        result_matrix_00 = [[0 for x in range(split_index)] for y in range(split_index)]
        result_matrix_01 = [[0 for x in range(split_index)] for y in range(split_index)]
        result_matrix_10 = [[0 for x in range(split_index)] for y in range(split_index)]
        result_matrix_11 = [[0 for x in range(split_index)] for y in range(split_index)]
        a00 = [[0 for x in range(split_index)] for y in range(split_index)]
        a01 = [[0 for x in range(split_index)] for y in range(split_index)]
        a10 = [[0 for x in range(split_index)] for y in range(split_index)]
        a11 = [[0 for x in range(split_index)] for y in range(split_index)]
        b00 = [[0 for x in range(split_index)] for y in range(split_index)]
        b01 = [[0 for x in range(split_index)] for y in range(split_index)]
        b10 = [[0 for x in range(split_index)] for y in range(split_index)]
        b11 = [[0 for x in range(split_index)] for y in range(split_index)]

        for i in range(split_index):
            for j in range(split_index):
                a00[i][j] = matrix_A[i][j]
                a01[i][j] = matrix_A[i][j + split_index]
                a10[i][j] = matrix_A[split_index + i][j]
                a11[i][j] = matrix_A[i + split_index][j + split_index]
                b00[i][j] = matrix_B[i][j]
                b01[i][j] = matrix_B[i][j + split_index]
                b10[i][j] = matrix_B[split_index + i][j]
                b11[i][j] = matrix_B[i + split_index][j + split_index]

        add_matrix(multiply_matrix(a00, b00), multiply_matrix(a01, b10), result_matrix_00, split_index)
        add_matrix(multiply_matrix(a00, b01), multiply_matrix(a01, b11), result_matrix_01, split_index)
        add_matrix(multiply_matrix(a10, b00), multiply_matrix(a11, b10), result_matrix_10, split_index)
        add_matrix(multiply_matrix(a10, b01), multiply_matrix(a11, b11), result_matrix_11, split_index)

        for i in range(split_index):
            for j in range(split_index):
                result_matrix[i][j] = result_matrix_00[i][j]
                result_matrix[i][j + split_index] = result_matrix_01[i][j]
                result_matrix[split_index + i][j] = result_matrix_10[i][j]
                result_matrix[i + split_index][j + split_index] = result_matrix_11[i][j]
    return result_matrix


def divconq_mult(m1, m2):
    return multiply_matrix(m1, m2)


def split(matrix):
    n = len(matrix)
    row, col = n, n
    row2, col2 = int(row // 2), int(col // 2)
    m11 = [matrix[i][:col2] for i in range(0, row2)]
    m12 = [matrix[i][col2:] for i in range(0, row2)]
    m21 = [matrix[i][:col2] for i in range(row2, n)]
    m22 = [matrix[i][col2:] for i in range(row2, n)]
    # return matrix[:row2, :col2], matrix[:row2, col2:], matrix[row2:, :col2], matrix[row2:, col2:]
    return m11, m12, m21, m22


def add_matrix2(m1, m2):
    n = len(m1)
    return [[m1[i][j] + m2[i][i] for j in range(n)] for i in range(n)]


def subtract_matrix2(m1, m2):
    n = len(m1)
    return [[m1[i][j] + m2[i][i] for j in range(n)] for i in range(n)]


def strassen_mult(x, y):
    if len(x) == 1:
        return [[x[0][0] * y[0][0]]]
    a, b, c, d = split(x)
    e, f, g, h = split(y)

    p1 = strassen_mult(a, subtract_matrix2(f, h))
    p2 = strassen_mult(add_matrix2(a, b), h)
    p3 = strassen_mult(add_matrix2(c, d) + d, e)
    p4 = strassen_mult(d, subtract_matrix2(g, e))
    p5 = strassen_mult(add_matrix2(a, d), add_matrix2(e, h))
    p6 = strassen_mult(subtract_matrix2(b, d), add_matrix2(g, h))
    p7 = strassen_mult(subtract_matrix2(a, c), add_matrix2(e, f))

    # Computing the values of the 4 quadrants of the final matrix c
    c11 = subtract_matrix2(add_matrix(p5, p4), add_matrix2(p2, p6))
    c12 = add_matrix2(p1, p2)
    c21 = add_matrix2(p3, p4)
    c22 = subtract_matrix2(add_matrix(p1, p5), add_matrix2(p3, p7))

    # Combining the 4 quadrants into a single matrix by stacking horizontally and vertically.
    c = np.vstack((np.hstack((c11, c12)), np.hstack((c21, c22))))

    return c


def run_algs(algs, sizes, trials):
    dict_algs = {}
    for alg in algs:
        dict_algs[alg.__name__] = {}
    for size in sizes:
        for alg in algs:
            dict_algs[alg.__name__][size] = 0
        for trial in range(1, trials + 1):
            m1 = random_matrix(size)
            m2 = random_matrix(size)
            for alg in algs:
                start_time = time()
                m3 = alg(m1, m2)
                end_time = time()
                net_time = end_time - start_time
                dict_algs[alg.__name__][size] += 1000 * net_time
    return dict_algs


def main():
    algs = [numpy_mult, simple_mult, divconq_mult, strassen_mult]
    size = [10, 50, 100]
    trials = 1
    dict_algs = run_algs(algs, size, trials)
    as1.print_times(dict_algs)
    as1.plot_times("Matrix Multiplication", dict_algs, size, trials, algs, file_name="Assignment3.png")


if __name__ == '__main__':
    main()
