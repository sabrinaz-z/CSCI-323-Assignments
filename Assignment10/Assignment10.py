# Analysis of Algorithms (CSCI 323)
# Summer 2024
# Assignment 10 - Substring Search Algorithms
# Sabrina Zheng

# Acknowledgements:
# I worked with class
# I used the following sites


from time import time
import Assignment1 as as1
import Assignment5 as as5
import random


def run_algs(algs, text, patterns, verbose=False):
    dict_algs = {}
    trials = 1
    for alg in algs:
        dict_algs[alg.__name__] = {}
    data = []
    headers = ["Pattern", "Length"] + [alg.__name__ for alg in algs]
    for pattern in patterns:
        size = len(pattern)
        row = [pattern, size]
        for alg in algs:
            dict_algs[alg.__name__][size] = 0
        for trial in range(1, trials + 1):
            for alg in algs:
                start_time = time()
                idx = alg(text, pattern, verbose)
                row.append(idx)
                end_time = time()
                net_time = end_time - start_time
                dict_algs[alg.__name__][size] += 1000 * net_time
            data.append(row)
    return dict_algs, data, headers


# [1] Define functions that implement these sub-string search algorithms:
# Native Search that wraps the built-in string-search capability of your programming language
# Brute Force - see https://www.geeksforgeeks.org/naive-algorithm-for-pattern-searching/
# Rabin-Karp - see https://www.geeksforgeeks.org/rabin-karp-algorithm-for-pattern-searching
# Rabin-Karp Randomized - (use multiple hash functions with random moduli)
# Knuth-Morris-Pratt - see https://www.geeksforgeeks.org/kmp-algorithm-for-pattern-searching
# Boyer-Moore - see https://www.geeksforgeeks.org/boyer-moore-algorithm-for-pattern-searching

def native_search(text, pattern, verbose=False):
    return text.find(pattern)


def brute_force(text, pattern, verbose=False):
    m = len(pattern)
    n = len(text)
    for i in range(n - m + 1):
        j = 0
        while j < m and text[i + j] == pattern[j]:
            if verbose:
                print(m, n, j, i)
            j += 1
        if j == m:
            return i
    return -1


def rabin_karp(text, pattern, verbose=False):
    q = random.randint(1000, 10000)
    d = 256
    M = len(pattern)
    N = len(text)
    i = 0
    j = 0
    p = 0
    t = 0
    h = 1
    for i in range(M - 1):
        h = (h * d) % q
    for i in range(M):
        p = (d * p + ord(pattern[i])) % q
        t = (d * t + ord(text[i])) % q
    for i in range(N - M + 1):
        if p == t:
            for j in range(M):
                if text[i + j] != pattern[j]:
                    break
                else:
                    j += 1
            if j == M:
                return i
        if i < N - M:
            t = (d * (t - ord(text[i]) * h) + ord(text[i + M])) % q
            if t < 0:
                t = t + q
    return -1


def knuth_morris_pratt(text, pattern, verbose=False):
    M = len(pattern)
    N = len(text)
    j = 0
    lps = compute_kmp_lps(pattern)
    i = 0
    while i < N:
        if j < M and text[i] == pattern[j]:
            i += 1
            j += 1
        if j == M:
            return i - j
        elif i < N and (j >= M or pattern[j] != text[i]):
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return -1


def compute_kmp_lps(pattern):
    M = len(pattern)
    leng = 0
    lps = [0] * M
    i = 1
    while i < M:
        if pattern[i] == pattern[leng]:
            leng += 1
            lps[i] = leng
            i += 1
        else:
            if leng != 0:
                leng = lps[leng - 1]
            else:
                lps[i] = 0
                i += 1
    return lps


def bad_char_heuristic(string, size):
    NO_OF_CHARS = 256
    bad_char = [-1] * NO_OF_CHARS
    for i in range(size):
        bad_char[ord(string[i])] = i
    return bad_char


def boyer_moore(text, pattern, verbose=False):
    m = len(pattern)
    n = len(text)
    bad_char = bad_char_heuristic(pattern, m)
    s = 0
    while s <= n - m:
        j = m - 1
        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1
        if j < 0:
            return s
        else:
            s += max(1, j - bad_char[ord(text[s + j])])


# [2] Read in files Assignment07-Text.txt and Assignment07-Patterns.txt as inputs. Convert the content to upper-case
# to avoid case-sensitivity issues
def read_files(file_name):
    with open(file_name, "r") as f:
        return f.read().upper()


def main():
    text = read_files("Text.txt")
    patterns = read_files("Patterns.txt").split("\n")
    patterns = [p for p in patterns if p.strip()]
    if not patterns:
        print("No patterns to process.")
        return
    algs = [native_search, brute_force, rabin_karp, knuth_morris_pratt, boyer_moore]
    trials = 1
    sizes = [len(pattern) for pattern in patterns]
    dict_algs, data, headers = run_algs(algs, text, patterns, False)
    as1.print_times(dict_algs)
    desc = "String Matching"
    as1.plot_times(desc, dict_algs, sizes, trials, algs, file_name="Assignment10-times.png")
    as5.print_text_table(headers, data, ["l", "r", "r", "r", "r", "r", "r"])


if __name__ == '__main__':
    main()