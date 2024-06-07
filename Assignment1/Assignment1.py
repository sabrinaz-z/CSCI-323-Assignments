# Analysis of Algorithms (CSCI 323)
# Summer 2024
# Assignment 1 - Empirical Analysis of Search Algorithms
# Sabrina Zheng

# Acknowledgements:
# I worked with class
# I used the following sites


from random import randint
from time import time
import pandas as pd
import math
import matplotlib.pyplot as plt


# [1] Define a function random_list(size) that  returns a list of size random numbers.
def random_list(size):
    numbers = [0] * size
    numbers[0] = randint(1, 100)
    for i in range(1, size):
        numbers[i] = numbers[i - 1] + randint(1, 100)
    return numbers


# [2] Define a function native_search(list, key) that wraps the built-in index function
def native_search(arr, key):
    return arr.index(key)


def linear_search(arr, key):
    for i in range(len(arr)):
        if arr[i] == key:
            return i
    return -1


def binary_search_rec(arr, key, low, high):
    while low <= high:
        mid = low + (high - low) // 2
        if arr[mid] == key:
            return mid
        elif arr[mid] < key:
            low = mid + 1
        else:
            high = mid - 1
    return -1


def binary_search_recursive(arr, key):
    return binary_search_rec(arr, key, 0, len(arr) - 1)


def binary_search_iterative_better(arr, key):
    l = 0
    r = len(arr) - 1
    while r - l > 1:
        m = l + (r - l) // 2
        if arr[m] <= key:
            l = m
        else:
            r = m
    if arr[l] == key:
        return l
    if arr[r] == key:
        return r
    return -1


def binary_search_iterative(arr, key):
    l, r = 0, len(arr) - 1
    while l <= r:
        m = int((l + r) / 2)
        if arr[m] == key:
            return m
        if arr[m] < key:
            l = m + 1
        else:
            r = m - 1
    return -1


def binary_search_randomized_rec(arr, key, l, r):
    if r >= l:
        mid = randint(l, r)
        if arr[mid] == key:
            return mid
        if arr[mid] > key:
            return binary_search_randomized_rec(arr, key, l, mid - 1)
        return binary_search_randomized_rec(arr, key, mid + 1, r)
    return -1


def binary_search_randomized(arr, key):
    return binary_search_randomized_rec(arr, key, 0, len(arr) - 1)


def exponential_search(arr, key):
    n = len(arr)
    if arr[0] == key:
        return 0
    i = 1
    while i < n and arr[i] <= key:
        i = i * 2
    return binary_search_rec(arr, key, i // 2, min(i, n - 1))


def jump_search(arr, key):
    n = len(arr)
    step = math.sqrt(n)
    prev = 0
    while arr[int(min(step, n) - 1)] < key:
        prev = step
        step += math.sqrt(n)
        if prev >= n:
            return -1
    while arr[int(prev)] < key:
        prev += 1
        if prev == min(step, n):
            return -1
    if arr[int(prev)] == key:
        return int(prev)
    return -1


def interpolation_search_rec(arr, key, lo, hi):
    if arr[lo] == arr[hi]:
        if key == arr[lo]:
            return lo
        else:
            return -1
    if lo <= hi and arr[lo] <= key <= arr[hi]:
        pos = int(lo + ((hi - lo) / float(arr[hi] - arr[lo])) * float((key - arr[lo])))
        if arr[pos] == key:
            return pos
        elif arr[pos] < key:
            return interpolation_search_rec(arr, key, pos + 1, hi)
        else:
            return interpolation_search_rec(arr, key, lo, pos - 1)
    return -1


def interpolation_search(arr, key):
    return interpolation_search_rec(arr, key, 0, len(arr) - 1)


def fibonacci_search(arr, key):
    n = len(arr)
    fibMMm2 = 0
    fibMMm1 = 1
    fibM = fibMMm2 + fibMMm1
    while fibM < n:
        fibMMm2 = fibMMm1
        fibMMm1 = fibM
        fibM = fibMMm2 + fibMMm1
    offset = -1
    while fibM > 1:
        i = min(offset + fibMMm2, n - 1)
        if arr[i] < key:
            fibM = fibMMm1
            fibMMm1 = fibMMm2
            fibMMm2 = fibM - fibMMm1
            offset = i
        elif arr[i] > key:
            fibM = fibMMm2
            fibMMm1 = fibMMm1 - fibMMm2
            fibMMm2 = fibM - fibMMm1
        else:
            return i
    if fibMMm1 and arr[n - 1] == key:
        return n - 1
    return -1


def ternary_search_rec(arr, key, l, r):
    if r >= l:
        mid1 = l + (r - l) // 3
        mid2 = r - (r - l) // 3
        if arr[mid1] == key:
            return mid1
        if arr[mid2] == key:
            return mid2
        if key < arr[mid1]:
            return ternary_search_rec(arr, key, l, mid1 - 1)
        elif key > arr[mid2]:
            return ternary_search_rec(arr, key, mid2 + 1, r)
        else:
            return ternary_search_rec(arr, key, mid1 + 1, mid2 - 1)
    return -1


def ternary_search(arr, key):
    return ternary_search_rec(arr, key, 0, len(arr) - 1)


def run_searches(searches, sizes, trials):
    dict_searches = {}
    for search in searches:
        dict_searches[search.__name__] = {}
    for size in sizes:
        for search in searches:
            dict_searches[search.__name__][size] = 0
        for trial in range(1, trials + 1):
            arr = random_list(size)
            idx = randint(0, size - 1)
            key = arr[idx]
            for search in searches:
                start_time = time()
                idx_found = search(arr, key)
                end_time = time()
                if idx_found != idx:
                    print(search.__name__, "wrong index found", arr, idx, idx_found)
                net_time = end_time - start_time
                dict_searches[search.__name__][size] += 1000 * net_time
    return dict_searches


def print_times(dict_searches):
    pd.set_option("display.max_rows", 500)
    pd.set_option("display.max_columns", 500)
    pd.set_option("display.width", 1000)
    df = pd.DataFrame.from_dict(dict_searches).T
    print(df)


def plot_times(dict_searches, sizes, trials, searches, file_name):
    search_num = 0
    plt.xticks([j for j in range(len(sizes))], [str(size) for size in sizes])
    for search in searches:
        search_num += 1
        d = dict_searches[search.__name__]
        x_axis = [j + 0.05 * search_num for j in range(len(sizes))]
        y_axis = [d[i] for i in sizes]
        plt.bar(x_axis, y_axis, width=0.05, alpha=0.75, label=search.__name__)
    plt.legend()
    plt.title("Runtime of search algorithms")
    plt.xlabel("Number of elements")
    plt.ylabel(f"Time for {trials} trials (ms)")
    plt.savefig(file_name)
    plt.show()


def main():
    searches = [native_search, linear_search, binary_search_recursive, binary_search_iterative,
                binary_search_iterative_better, binary_search_randomized, exponential_search, jump_search,
                interpolation_search, fibonacci_search, ternary_search]
    size = [100, 1000, 10000]
    trials = 1000
    dict_searches = run_searches(searches, size, trials)
    print_times(dict_searches)
    plot_times(dict_searches, size, trials, searches, file_name="Assignment1.png")


if __name__ == '__main__':
    main()
