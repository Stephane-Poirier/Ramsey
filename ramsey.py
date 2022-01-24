# -*- coding: utf-8 -*-

__author__ = 'Stéphane-Poirier'

import math
import graph
import time

def comb(n, k):
    c = 1
    for i in range(1, k+1):
        c = int(c * (n+1-i) / i)
    return c


def evaluate_triangles(r, size_max):
    t = (r-1) // 3

    while 3*t < size_max:
        t += 1
        n = 3*t
        if n <= r:
            continue
        exp_one_color = 0
        for j in range(r // 2 + 1):
            exp_one_color += comb(t, j) * (5**j) * comb(t-j, r - 2*j) * (5**(r-2*j)) * (2**(j-r*(r-1)/2))

        exp = 2* exp_one_color

        print (" size {} : expected value {}".format(n, exp))


def evaluate_stars(r, size_max):
    s = (r-1) // 5

    while 5*s < size_max:
        s += 1
        n = 5*s
        if n <= r:
            continue
        exp_one_color = 0
        for j in range(r // 2 + 1):
            exp_one_color += comb(s, j) * comb(s-2*j, r - 2*j) * (3**(r-2*j)) * (2**(j-r*(r-1)/2))

        exp = 2* exp_one_color

        print (" size {} : expected value {}".format(n, exp))


def evaluate_erdos(r, size_max):
    m = r

    while m < size_max:
        m += 1
        nb = comb(m, r)
        exp = nb * (2 ** (1 - r * (r - 1) / 2))
        print(" size {} : expected value {}".format(m, exp))


def is_prime(n):
    if n <= 1:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False

    sqn = int(math.sqrt(n)+1)
    for p in range(6, sqn+1, 6):
        if n % (p-1) == 0 or n % (p+1) == 0:
            return False
    return True

def quadratic_set(n):
    qs = set()
    for i in range(1, n):
        qs.add((i*i) % n)

    return qs


def test():
    n = 4
    k = 1
    t1 = comb(n, k)
    print("C({},{}) = {}".format(n, k, t1))
    n = 4
    k = 3
    t1 = comb(n, k)
    print("C({},{}) = {}".format(n, k, t1))
    n = 4
    k = 4
    t1 = comb(n, k)
    print("C({},{}) = {}".format(n, k, t1))
    n = 6
    k = 2
    t1 = comb(n, k)
    print("C({},{}) = {}".format(n, k, t1))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='ramsey : evaluate expected value of Kr presence for a range of sizes')

    parser.add_argument("-r", "--Kr", type=int, default=5, help="size of Kr to avoid")
    parser.add_argument("-n", "--size_max", type=int, default=51, help="size max of Kn to measure")
    parser.add_argument("-m", "--method", type=str, default="triangles", help="method used to evaluate expected value")

    options = parser.parse_args()

    if options.method == "test":
        test()
    elif options.method.lower() == "erdos":
        print("Erdös method to evaluate expected value of K{}".format(options.Kr))
        evaluate_erdos(options.Kr, options.size_max)
    elif options.method.lower() == "triangles":
        print("Triangles method to evaluate expected value of K{}".format(options.Kr))
        evaluate_triangles(options.Kr, options.size_max)
    elif options.method.lower() == "stars":
        print("Stars method to evaluate expected value of K{}".format(options.Kr))
        evaluate_stars(options.Kr, options.size_max)
    else:
        print("Method {} is not yet implemented".format(options.method))

    # n_graph = graph.Graph.from_diffs(({1, 4}, {2, 3, 5}))
    # n_graph.set_edge(2, 3, 1)
    # print("{}".format(n_graph))
    # n_cliques = n_graph.count_cliques()
    # print("nb cliques {}".format(n_cliques))

    Gp = []
    for n in range(5, 150, 4):
        if is_prime(n):
            print(n)
            start = time.process_time()
            qs0 = quadratic_set(n)
            qs1 = set(range(1, n)) - qs0
            n_graph = graph.Graph.from_diffs((qs0, qs1))
            n_cliques = n_graph.count_cliques(isomorphic=True)
            print("nb cliques {}".format(n_cliques))
            Gp.append((n, len([x for x in n_cliques[0] if x > 0])-1))
            print("time {}".format(time.process_time() - start))

    print(Gp)