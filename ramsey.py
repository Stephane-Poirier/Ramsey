# -*- coding: utf-8 -*-

__author__ = 'Stéphane-Poirier'

import math
from diff_graph import DiffGraph
from ferrer import FerrerIterator, ferrer_size
import time

def comb(n, k):
    c = 1
    for i in range(1, k+1):
        c = int(c * (n+1-i) / i)
    return c


def multinomial(lst):
    res, i = 1, sum(lst)
    i0 = lst.index(max(lst))
    for a in lst[:i0] + lst[i0+1:]:
        for j in range(1,a+1):
            res *= i
            res //= j
            i -= 1
    return res


def evaluate_triangles(r, size_max):
    t = (r-1) // 3

    while 3*t < size_max:
        t += 1
        n = 3*t
        if n <= r:
            continue
        exp_one_color = 0
        for j in range(r // 2 + 1):
            exp_one_color += comb(t, j) * comb(t-j, r - 2*j) * (3**(r-2*j)) * (2**(j-r*(r-1)/2))

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
            exp_one_color += comb(s, j) * (5**j) * comb(s-j, r - 2*j) * (5**(r-2*j)) * (2**(j-r*(r-1)/2))

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


def expected_cliques(orig_graph_size, nb_cliques, nb_copies, size_cliques_expected, isomorphic=True):
    if not isomorphic:
        print("Case isomorphic False is not yet implemented")
        return
    nb_colors = len(nb_cliques)
    max_cliques_orig = len([x for x in nb_cliques[0] if x > 0])-1
    nb_edges_all = (size_cliques_expected * (size_cliques_expected - 1)) // 2
    one_color_expectation = 0.0
    for cliques_cfg in FerrerIterator(max_cliques_orig, nb_copies, size_cliques_expected):
        nb_edges_cfg = sum(c * (k * (k - 1)) // 2 for (k, c) in enumerate(cliques_cfg))
        choices_cfg = multinomial([x for x in cliques_cfg if x > 0])
        nb_cliques_for_one_choice = 1
        for (nc, c) in zip(nb_cliques[0][:max_cliques_orig+1], cliques_cfg):
            nb_cliques_for_one_choice *= nc ** c
        # to limit under flow effects
        while nb_edges_cfg < nb_edges_all and choices_cfg % 2 == 0:
            nb_edges_cfg += 1
            choices_cfg //= 2
        while nb_edges_cfg < nb_edges_all and nb_cliques_for_one_choice % 2 == 0:
            nb_edges_cfg += 1
            nb_cliques_for_one_choice //= 2
        one_color_expectation += (2 ** (nb_edges_cfg - nb_edges_all)) * choices_cfg * nb_cliques_for_one_choice
    all_colors_expectation = nb_colors * one_color_expectation
    print(" {} copies of G{} ({}) gives expectation {} for cliques of size {}".format(nb_copies, orig_graph_size,
                                                                                 nb_copies*orig_graph_size,
                                                                                 all_colors_expectation,
                                                                                 size_cliques_expected))
    return all_colors_expectation

def expected_cliques_range(orig_graph_size, nb_cliques, max_cliques_avoided, isomorphic=True):
    if not isomorphic:
        print("Case isomorphic False is not yet implemented")
        return

    max_cliques_orig = len([x for x in nb_cliques[0] if x > 0]) - 1
    for cur_cliques_expected in range(max_cliques_orig + 1, max_cliques_avoided + 1):
        nb_copies = 1
        while nb_copies < max_cliques_avoided:
            nb_copies += 1
            expected_cliques(orig_graph_size, nb_cliques, cur_cliques_expected, isomorphic)
    return

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

    # d_graph = diff_graph.DiffGraph(({1, 4}, {2, 3, 5}))
    # print("{}".format(d_graph))

    # for lst in FerrerIterator(4, 7, 10):
    #     cur_size = ferrer_size(lst)
    #     print("list {} : size {}".format(lst, cur_size))

    # n = 17
    # qs0 = quadratic_set(n)
    # qs1 = set(range(1, n)) - qs0
    # d_graph = DiffGraph((qs0, qs1))
    # n_cliques = d_graph.count_cliques(isomorphic=True)
    # expected_cliques(n, n_cliques, 2, 5, isomorphic=True)

    Gp = []
    expectations_dict = {}
    for n in range(5, 150, 4):
        if is_prime(n):
            print(n)
            start = time.process_time()
            qs0 = quadratic_set(n)
            qs1 = set(range(1, n)) - qs0
            d_graph = DiffGraph((qs0, qs1))
            n_cliques = d_graph.count_cliques(isomorphic=True)
            print("nb cliques {}".format(n_cliques))
            max_cliques = len([x for x in n_cliques[0] if x > 0])-1
            Gp.append((n, max_cliques))
            min_r = max_cliques+1
            for nb_copies in range(2, 3*n+1):
                for r in range(min_r, (max_cliques*nb_copies)):
                    exp = expected_cliques(n, n_cliques, nb_copies, r, isomorphic=True)
                    if r not in expectations_dict \
                            or n*nb_copies - math.floor(exp) > expectations_dict[r][1]*expectations_dict[r][2] - math.floor(expectations_dict[r][0]):
                        expectations_dict[r] = (exp, n, nb_copies)
                    if exp < 1.0:
                        break
                    if exp > n * nb_copies:
                        min_r = r + 1
            print("time {}".format(time.process_time() - start))

    print(Gp)
    print(expectations_dict)
