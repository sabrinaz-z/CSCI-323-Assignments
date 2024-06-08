# Analysis of Algorithms (CSCI 323)
# Summer 2024
# Assignment 2 - Empirical Analysis of Sorting Algorithms
# Sabrina Zheng

# Acknowledgements:
# I worked with class
# I used the following sites

import Assignment1 as as1
from time import time
from random import randint, shuffle
import copy


def has_inversion(arr):
    for i in range(len(arr) - 1):
        if arr[i] > arr[i + 1]:
            return i
    return -1


def native_sort(arr):
    arr.sort()


def bubble_sort_optimized(arr):
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break


def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]


def selection_sort(arr):
    n = len(arr)
    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            if arr[min_idx] > arr[j]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]


def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key


def binary_search(arr, val, start, end):
    if start == end:
        if arr[start] > val:
            return start
        else:
            return start + 1
    if start > end:
        return start
    mid = (start + end) // 2
    if arr[mid] < val:
        return binary_search(arr, val, mid + 1, end)
    elif arr[mid] > val:
        return binary_search(arr, val, start, mid - 1)
    else:
        return mid


def binary_insertion_sort(arr):
    for i in range(1, len(arr)):
        val = arr[i]
        j = binary_search(arr, val, 0, i - 1)
        for k in range(i, j, -1):
            arr[k] = arr[k - 1]
        arr[j] = val


def cocktail_sort(arr):
    n = len(arr)
    swapped = True
    start = 0
    end = n - 1
    while swapped:
        swapped = False
        for i in range(start, end):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                swapped = True
        if not swapped:
            break
        swapped = False
        end = end - 1
        for i in range(end - 1, start - 1, -1):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                swapped = True
        start = start + 1


def shell_sort(arr):
    n = len(arr)
    gap = n // 2
    while gap > 0:
        j = gap
        while j < n:
            i = j - gap
            while i >= 0:
                if arr[i + gap] > arr[i]:
                    break
                else:
                    arr[i + gap], arr[i] = arr[i], arr[i + gap]
                i = i - gap
            j += 1
        gap = gap // 2


def merge(array, left, mid, right):
    subArrayOne = mid - left + 1
    subArrayTwo = right - mid
    leftArray = [0] * subArrayOne
    rightArray = [0] * subArrayTwo
    for i in range(subArrayOne):
        leftArray[i] = array[left + i]
    for j in range(subArrayTwo):
        rightArray[j] = array[mid + 1 + j]
    indexOfSubArrayOne = 0  # Initial index of first sub-array
    indexOfSubArrayTwo = 0  # Initial index of second sub-array
    indexOfMergedArray = left  # Initial index of merged array
    while indexOfSubArrayOne < subArrayOne and indexOfSubArrayTwo < subArrayTwo:
        if leftArray[indexOfSubArrayOne] <= rightArray[indexOfSubArrayTwo]:
            array[indexOfMergedArray] = leftArray[indexOfSubArrayOne]
            indexOfSubArrayOne += 1
        else:
            array[indexOfMergedArray] = rightArray[indexOfSubArrayTwo]
            indexOfSubArrayTwo += 1
        indexOfMergedArray += 1
    while indexOfSubArrayOne < subArrayOne:
        array[indexOfMergedArray] = leftArray[indexOfSubArrayOne]
        indexOfSubArrayOne += 1
        indexOfMergedArray += 1
    while indexOfSubArrayTwo < subArrayTwo:
        array[indexOfMergedArray] = rightArray[indexOfSubArrayTwo]
        indexOfSubArrayTwo += 1
        indexOfMergedArray += 1


def merge_sort_helper(arr, begin, end):
    if begin >= end:
        return
    mid = begin + (end - begin) // 2
    merge_sort_helper(arr, begin, mid)
    merge_sort_helper(arr, mid + 1, end)
    merge(arr, begin, mid, end)


def merge_sort(arr):
    merge_sort_helper(arr, 0, len(arr) - 1)


def get_pivot_index_high(arr, low, high):
    return high


def get_pivot_index_rnd(arr, low, high):
    return randint(low, high)


def partition(arr, low, high, get_pivot_index):
    pivot_idx = get_pivot_index(arr, low, high)
    pivot = arr[pivot_idx]
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i = i + 1
            (arr[i], arr[j]) = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def quick_sort_helper(arr, low, high, get_pivot_index):
    if low < high:
        pi = partition(arr, low, high, get_pivot_index)
        quick_sort_helper(arr, low, pi - 1, get_pivot_index)
        quick_sort_helper(arr, pi + 1, high, get_pivot_index)


def quick_sort(arr):
    quick_sort_helper(arr, 0, len(arr) - 1, get_pivot_index_high)


def quick_sort_randomized(arr):
    quick_sort_helper(arr, 0, len(arr) - 1, get_pivot_index_rnd)


def heapify(arr, n, i):
    largest = i
    l = 2 * i + 1
    r = 2 * i + 2
    if l < n and arr[largest] < arr[l]:
        largest = l
    if r < n and arr[largest] < arr[r]:
        largest = r
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)


def heap_sort(arr):
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0)


def counting_sort(arr):
    n = len(arr)
    mx = max(arr) + 1
    output = [0 for _ in range(n)]
    count = [0 for _ in range(mx)]
    for a in arr:
        # print(a)
        count[a] += 1
    for i in range(n):
        arr[i] = output[i]


def insertion_sort(bucket):
    for i in range(1, len(bucket)):
        key = bucket[i]
        j = i - 1
        while j >= 0 and bucket[j] > key:
            bucket[j + 1] = bucket[j]
            j -= 1
        bucket[j + 1] = key


def bucket_sort(arr):
    n = len(arr)
    buckets = [[] for _ in range(n)]
    max_value = max(arr)
    for num in arr:
        bi = num * n // (max_value + 1)
        buckets[bi].append(num)
    for bucket in buckets:
        insertion_sort(bucket)
    index = 0
    sorted_arr = []
    for bucket in buckets:
        sorted_arr.extend(bucket)
    for i in range(n):
        arr[i] = sorted_arr[i]


def countingSort(arr, exp1):
    n = len(arr)
    output = [0] * n
    count = [0] * 10
    for i in range(0, n):
        index = arr[i] // exp1
        count[index % 10] += 1
    for i in range(1, 10):
        count[i] += count[i - 1]
    i = n - 1
    while i >= 0:
        index = arr[i] // exp1
        output[count[index % 10] - 1] = arr[i]
        count[index % 10] -= 1
        i -= 1
    i = 0
    for i in range(0, len(arr)):
        arr[i] = output[i]


def radix_sort(arr):
    max1 = max(arr)
    exp = 1
    while max1 / exp >= 1:
        counting_sort(arr)
        exp *= 10


def calcMinRun(n):
    r = 0
    while n >= 32:
        r |= n & 1
        n >>= 1
    return n + r


def insertion_sort_tim(arr, left, right):
    for i in range(left + 1, right + 1):
        j = i
        while j > left and arr[j] < arr[j - 1]:
            arr[j], arr[j - 1] = arr[j - 1], arr[j]
            j -= 1


def merge(arr, l, m, r):
    len1, len2 = m - l + 1, r - m
    left, right = [], []
    for i in range(0, len1):
        left.append(arr[l + i])
    for i in range(0, len2):
        right.append(arr[m + 1 + i])
    i, j, k = 0, 0, l
    while i < len1 and j < len2:
        if left[i] <= right[j]:
            arr[k] = left[i]
            i += 1
        else:
            arr[k] = right[j]
            j += 1
        k += 1
    while i < len1:
        arr[k] = left[i]
        k += 1
        i += 1
    while j < len2:
        arr[k] = right[j]
        k += 1
        j += 1


def tim_sort(arr):
    n = len(arr)
    minRun = calcMinRun(n)
    for start in range(0, n, minRun):
        end = min(start + minRun - 1, n - 1)
        insertion_sort_tim(arr, start, end)
    size = minRun
    while size < n:
        for left in range(0, n, 2 * size):
            mid = min(n - 1, left + size - 1)
            right = min((left + 2 * size - 1), (n - 1))
            if mid < right:
                merge(arr, left, mid, right)
        size = 2 * size


def run_algs(algs, sizes, trials):
    dict_algs = {}
    for alg in algs:
        dict_algs[alg.__name__] = {}
    for size in sizes:
        for alg in algs:
            dict_algs[alg.__name__][size] = 0
        for trial in range(1, trials + 1):
            arr_orig = as1.random_list(size)
            shuffle(arr_orig)
            for alg in algs:
                arr = copy.copy(arr_orig)
                start_time = time()
                alg(arr)
                end_time = time()
                inversion = has_inversion(arr)
                if inversion >= 0:
                    print(alg.__name__, "has inversion at", inversion, arr)
                net_time = end_time - start_time
                dict_algs[alg.__name__][size] += 1000 * net_time
    return dict_algs


def main():
    sorts = [native_sort, bubble_sort, bubble_sort_optimized, selection_sort, insertion_sort,
             binary_insertion_sort, cocktail_sort, shell_sort, merge_sort, quick_sort,
             heap_sort, bucket_sort, counting_sort, radix_sort, tim_sort]
    size = [100, 500, 1000]
    trials = 10
    dict_algs = run_algs(sorts, size, trials)
    as1.print_times(dict_algs)
    as1.plot_times("sorting", dict_algs, size, trials, sorts, file_name="Assignment2.png")


if __name__ == '__main__':
    main()
