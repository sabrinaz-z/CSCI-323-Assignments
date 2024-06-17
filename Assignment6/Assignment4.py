# Analysis of Algorithms (CSCI 323)
# Summer 2024
# Assignment 4 - Computational Geometry
# Sabrina Zheng

# Acknowledgements:
# I worked with class
# I used the following sites

from random import randint
import numpy as np
import matplotlib.pyplot as plt
import math
from functools import cmp_to_key
from math import sqrt


# [1] Define a function generate_points(n, mn, mx) to make a random list of points in 2D,
# with each coordinate being between mn and mx.
def generate_points(n, mn, mx):
    return [(randint(mn, mx), randint(mn, mx)) for i in range(n)]


# [2] Define a function line(points, i, j) that finds the line between two points in a list.
# See: https://www.geeksforgeeks.org/program-find-line-passing-2-points/
def compute_line(points, i, j):
    Q = points[i]
    P = points[j]
    a = Q[1] - P[1]
    b = P[0] - Q[0]
    c = a * (P[0]) + b * (P[1])
    sign = "-" if b < 0 else "+"
    line = f"{a}x {sign} {b}y = {c}"
    return line


# [3] Define a function draw_points(points) to draw the points using a package like matplotlib
# See the first posting at https://stackoverflow.com/questions/35363444/plotting-lines-connecting-points
def draw_points(points, file_name):
    x, y = get_x_y(points)
    style = "go-"
    for i in range(len(x)):
        plt.plot(x[i:i + 2], y[i:i + 2], 'ro-')
    plt.plot([x[0], x[-1]], [y[0], y[-1]], 'ro-')
    plt.savefig(file_name)
    plt.show()


# [5] Define a  function sort_points(points) to sort the points in clockwise (or counterclockwise) order
# See https://www.tutorialspoint.com/program-to-sort-given-set-of-cartesian-points-based-on-polar-angles-in-python
def sort_points(points):
    def key(x):
        atan = math.atan2(x[1], x[0])
        return (atan, x[1] ** 2 + x[0] ** 2) if atan >= 0 else (2 * math.pi + atan, x[0] ** 2 + x[1] ** 2)

    return sorted(points, key=key)


# [6] Define a function to compute the convex hull of a set of points. You may use any algorithm.
# See https://www.geeksforgeeks.org/convex-hull-using-divide-and-conquer-algorithm/
def quad(p):
    if p[0] >= 0 and p[1] >= 0:
        return 1
    if p[0] <= 0 and p[1] >= 0:
        return 2
    if p[0] <= 0 and p[1] <= 0:
        return 3
    return 4


def orientation(a, b, c):
    res = (b[1] - a[1]) * (c[0] - b[0]) - (c[1] - b[1]) * (b[0] - a[0])
    if res == 0:
        return 0
    if res > 0:
        return 1
    return -1


def compare(p1, q1):
    p = [p1[0] - mid[0], p1[1] - mid[1]]
    q = [q1[0] - mid[0], q1[1] - mid[1]]
    one = quad(p)
    two = quad(q)
    if one != two:
        if one < two:
            return -1
        return 1
    if p[1] * q[0] < q[1] * p[0]:
        return -1
    return 1


def merger(a, b):
    n1, n2 = len(a), len(b)
    ia, ib = 0, 0
    # ia -> rightmost point of a
    for i in range(1, n1):
        if a[i][0] > a[ia][0]:
            ia = i
    for i in range(1, n2):
        if b[i][0] < b[ib][0]:
            ib = i
    inda, indb = ia, ib
    done = 0
    while not done:
        done = 1
        while orientation(b[indb], a[inda], a[(inda + 1) % n1]) >= 0:
            inda = (inda + 1) % n1
        while orientation(a[inda], b[indb], b[(n2 + indb - 1) % n2]) <= 0:
            indb = (indb - 1) % n2
            done = 0
    uppera, upperb = inda, indb
    inda, indb = ia, ib
    done = 0
    g = 0
    while not done:
        done = 1
        while orientation(a[inda], b[indb], b[(indb + 1) % n2]) >= 0:
            indb = (indb + 1) % n2
        while orientation(b[indb], a[inda], a[(n1 + inda - 1) % n1]) <= 0:
            inda = (inda - 1) % n1
            done = 0
    ret = []
    lowera, lowerb = inda, indb
    ind = uppera
    ret.append(a[uppera])
    while ind != lowera:
        ind = (ind + 1) % n1
        ret.append(a[ind])
    ind = lowerb
    ret.append(b[lowerb])
    while ind != upperb:
        ind = (ind + 1) % n2
        ret.append(b[ind])
    return ret


def bruteHull(a):
    global mid
    s = set()
    for i in range(len(a)):
        for j in range(i + 1, len(a)):
            x1, x2 = a[i][0], a[j][0]
            y1, y2 = a[i][1], a[j][1]
            a1, b1, c1 = y1 - y2, x2 - x1, x1 * y2 - y1 * x2
            pos, neg = 0, 0
            for k in range(len(a)):
                if (k == i) or (k == j) or (a1 * a[k][0] + b1 * a[k][1] + c1 <= 0):
                    neg += 1
                if (k == i) or (k == j) or (a1 * a[k][0] + b1 * a[k][1] + c1 >= 0):
                    pos += 1
            if pos == len(a) or neg == len(a):
                s.add(tuple(a[i]))
                s.add(tuple(a[j]))
    ret = []
    for x in s:
        ret.append(list(x))
    mid = [0, 0]
    n = len(ret)
    for i in range(n):
        mid[0] += ret[i][0]
        mid[1] += ret[i][1]
        ret[i][0] *= n
        ret[i][1] *= n
    ret = sorted(ret, key=cmp_to_key(compare))
    for i in range(n):
        ret[i] = [ret[i][0] / n, ret[i][1] / n]
    return ret


def divide(a):
    if len(a) <= 5:
        return bruteHull(a)
    left, right = [], []
    start = int(len(a) / 2)
    for i in range(start):
        left.append(a[i])
    for i in range(start, len(a)):
        right.append(a[i])
    left_hull = divide(left)
    right_hull = divide(right)
    return merger(left_hull, right_hull)


def convex_hull(points):
    sorted_points = sort_points(points)
    ch = divide(sorted_points)
    print("The Convex Hull for the point:", points, "is", ch)
    return ch


# [7] Define a function compute_area(points) to find the area of the convex hull, not the original set.
# See https://www.geeksforgeeks.org/area-of-a-polygon-with-given-n-ordered-vertices/
def compute_area(points):
    n = len(points)
    area = 0.0
    j = n - 1
    x, y = get_x_y(points)
    for i in range(n):
        area += (x[j] + x[i]) * (y[j] - y[i])
        j = i  # j is previous vertex to i
    return int(abs(area / 2.0))


# [8] Define a function compute_perimeter(points) to find the perimeter of the convex hull, not the original set.
# See https://www.geeksforgeeks.org/equable-shapes/
def compute_perimeter(points):
    n = len(points)
    perimeter = 0.0
    x, y = get_x_y(points)
    j = n - 1
    for i in range(n):
        perimeter += math.sqrt((x[j] - x[i]) * (x[j] - x[i]) + (y[j] - y[i]) * (y[j] - y[i]))
        j = i
    return perimeter


def get_x_y(points):
    return [point[0] for point in points], [point[1] for point in points]


# [9] Define a function is_equable(points) to determine if the shape is equable (area and perimeter are equal)
# See https://www.geeksforgeeks.org/equable-shapes/
def polygonArea(X, Y, n):
    area = 0.0
    j = n - 1
    for i in range(n):
        area += (X[j] + X[i]) * (Y[j] - Y[i])
        j = i
    return abs(area / 2.0)


def polygonPerimeter(X, Y, n):
    perimeter = 0.0
    j = n - 1
    for i in range(n):
        perimeter += math.sqrt((X[j] - X[i]) * (X[j] - X[i]) +
                               (Y[j] - Y[i]) * (Y[j] - Y[i]))
        j = i
    return perimeter


def is_equitable(points):
    n = len(points)
    x, y = get_x_y(points)
    if polygonPerimeter(x, y, n) == polygonArea(x, y, n):
        print("Equable Shape")
    else:
        print("Not Equable Shape")


# [10] Define a function closest_pair(points) to determine the closest pair in a set of points
# Use brute force, or see https://www.geeksforgeeks.org/closest-pair-of-points-using-divide-and-conquer-algorithm/
def compareX(a, b):
    p1 = a
    p2 = b
    return p1.x - p2.x


def compareY(a, b):
    p1 = a
    p2 = b
    return (p1.y - p2.y)


def dist(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)


def bruteForce(points, n):
    min_dist = float("inf")
    for i in range(n):
        for j in range(i + 1, n):
            if dist(points[i], points[j]) < min_dist:
                min_dist = dist(points[i], points[j])
    return min_dist


def min(x, y):
    return x if x < y else y


def stripClosest(strip, size, d):
    min_dist = d
    strip = sorted(strip, key=lambda point: point.y)

    for i in range(size):
        for j in range(i + 1, size):
            if (strip[j].y - strip[i].y) >= min_dist:
                break
            if dist(strip[i], strip[j]) < min_dist:
                min_dist = dist(strip[i], strip[j])
    return min_dist


def closestUtil(points):
    n = len(points)
    if n <= 3:
        return bruteForce(points, n)
    mid = n // 2
    midPoint = points[mid]
    dl = closestUtil(points, mid)
    dr = closestUtil(points[mid:], n - mid)
    d = min(dl, dr)
    strip = []
    for i in range(n):
        if abs(points[i].x - midPoint.x) < d:
            strip.append(points[i])
    return min(d, stripClosest(strip, len(strip), d))


def closest_pair(points):
    min_dist = float('inf')
    closest_points = None
    n = len(points)
    for i in range(n):
        for j in range(i + 1, n):
            distance = dist(points[i], points[j])
            if distance < min_dist:
                min_dist = distance
                closest_points = (points[i], points[j])
    return closest_points, min_dist


# [11] Define a function farthest_pairs(points) to determine the closest pair in a set of points
# Use brute force
def dist2(p1, p2):
    x0 = p1[0] - p2[0]
    y0 = p1[1] - p2[1]
    return x0 * x0 + y0 * y0


def farthest_pairs(points):
    n = len(points)
    maxm = 0
    farthest_pair = None  # To keep track of the pair of points
    for i in range(n):
        for j in range(i + 1, n):
            distance_squared = dist2(points[i], points[j])
            if distance_squared > maxm:
                maxm = distance_squared
                farthest_pair = (points[i], points[j])
    return farthest_pair, math.sqrt(maxm)


def main():
    points = generate_points(10, -10, 10)
    line = compute_line(points, 0, 1)
    print(line, points)
    draw_points(points, "assignment4-unsorted.png")
    sorted_points = sort_points(points)
    draw_points(sorted_points, "assignment4-sorted.png")
    ch = convex_hull(points)
    draw_points(ch, "assignment4-ch.png")
    area = compute_area(ch, )
    print("The area of the convex hull is", area)
    perimeter = compute_perimeter(ch)
    print("The perimeter of the convex hull is", perimeter)
    is_equitable(ch)
    closest_points, closest_distance = closest_pair(points)
    print("Closest Pair:", closest_points, "Distance:", closest_distance)
    farthest_points, farthest_distance = farthest_pairs(points)
    print("Farthest Pair:", farthest_points, "Distance:", farthest_distance)


if __name__ == '__main__':
    main()
