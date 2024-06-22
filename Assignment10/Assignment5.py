# Analysis of Algorithms (CSCI 323)
# Summer 2024
# Assignment 5 - Estimate, Evaluate and  Rank Recurrences
# Sabrina Zheng

# Acknowledgements:
# I worked with class
# I used the following sites

import inspect
import math
import texttable


# [1] Use this function to obtain the content of a function, i.e. the part after the return statement.
def func_body(f):
    body = inspect.getsource(f)  # gets the code
    idx = body.index("return")  # get the part after the word return
    return '"' + body[7 + idx:].strip() + '"'


# [2] Create an empty dictionary to store intermediate results and a helper function ff to
# efficiently run a function f for input n:
dict_funcs = {}


def ff(f, n):
    func_name = f.__name__
    if func_name not in dict_funcs:
        dict_funcs[func_name] = {}
    dict_func = dict_funcs[func_name]
    if n not in dict_func:
        dict_func[n] = f(f, n)
    return dict_func[n]


# [3] Define a sample function f1, like the one for MergeSort. Try to use the one-line if/else
# (aka "ternary expression") as it will make it easier to capture the function content in Task 1.
# Make sure that all quotients are converted to int.
def f1(f, n):
    # merge sort
    return 0 if n == 1 else 2 * ff(f, int(n / 2)) + n


def f2(f, n):
    # quick sort
    return 0 if n == 1 else 1 * ff(f, int(n / 2)) + n


def f3(f, n):
    # stooge sort
    return 1 if n == 1 else 3 * ff(f, int(n / 1.5)) + 1


def f4(f, n):
    # bubble sort
    return 0 if n == 1 else n + ff(f, n - 1)


def f5(f, n):
    # cocktail sort
    return 0 if n == 1 else 2 * n + ff(f, n - 1)


def f6(f, n):
    # selection sort
    return 0 if n == 1 else n + ff(f, n - 1)


def f7(f, n):
    # binary search
    return 1 if n <= 1 else ff(f, n // 2) + 1


def f8(f, n):
    # shell sort
    return 1 if n == 1 else 2 * ff(f, n // 2) + n


def f9(f, n):
    # radix sort
    return 0 if n <= 1 else 10 * ff(f, n // 10) + n


def f10(f, n):
    # heap sort
    return 0 if n == 1 else 2 * ff(f, n // 2) + n * math.log(n, 2)


def call_and_print(data, func, n, context, desc, a, b, c):
    result = ff(func, n)
    mt_result = master_theorem(a, b, c)
    # print(func.__name__, desc, "for n =", n, "is", result, mt_result)
    data.append([func.__name__, context, desc, n, result, a, b, c, mt_result])


def exp(e):
    return "" if e == 0 else ("n" if e == 1 else f"n^{e}")


# [7] Define a function master_theorem(a, b, c) that determines the order of magnitude of the
# solution to a recurrence of the form T(n) = aT(n/b) + O(nc). See See
# https://www.geeksforgeeks.org/how-to-analyse-complexity-of-recurrence-relation/
def master_theorem(a, b, c):
    lba = math.log(a, b)
    rlba = round(lba, 2)
    if lba > c:
        return f"Θ({exp(rlba)})"
    elif lba == c:
        return f"Θ({exp(c)} log n)"
    elif lba < c:
        return f"Θ({exp(c)}) "


def print_text_table(headers, data, alignments):
    tt = texttable.Texttable(0)
    tt.set_cols_align(alignments)
    tt.add_rows([headers] + data)
    print(tt.draw())
    print()


def main():
    n = 256
    alignments = ["l", "l", "l", "r", "r", "r", "r", "r", "c"]
    headers = ["Function Name", "Context", "Description", "n", "f(n)", "a", "b", "c", "Master Theorem"]
    data = []
    call_and_print(data, f1, n, "Merge Sort", "f(n) = 2f(n/2) + n", 2, 2, 1)
    call_and_print(data, f2, n, "Quick Select", "f(n) = f(n/2) + n", 1, 2, 1)
    call_and_print(data, f3, n, "Stooge Sort", "f(n) = 3f(n/1.5) + 1", 3, 1.5, 0)
    call_and_print(data, f4, n, "Bubble Sort", "f(n) = f(n/n-1) + n", 1, n - 1, 1)
    call_and_print(data, f5, n, "Cocktail Sort", "f(n) = 2f(n/n-1) + n", 2, n - 1, 1)
    call_and_print(data, f6, n, "Selection Sort", "f(n) = f(n/n-1) + n", 1, n - 1, 1)
    call_and_print(data, f7, n, "Binary Search", "f(n) = f(n/2) + 1", 1, 2, 0)
    call_and_print(data, f8, n, "Shell Sort", "f(n) = 2f(n/2) + n", 2, 2, 1)
    call_and_print(data, f9, n, "Radix Sort", "f(n) = 10f(n/10) + n", 10, 10, 1)
    call_and_print(data, f10, n, "Heap Sort", "f(n) = 2f(n/2) + n", 2, 2, 1)

    print_text_table(headers, data, alignments)
    sorted_data = sorted(data, key=lambda l: l[4])
    print_text_table(headers, sorted_data, alignments)


if __name__ == '__main__':
    main()

