# -*- coding: utf-8 -*-

__author__ = 'Stéphane-Poirier'

import numpy as np


class Graph:
    def __init__(self, nb_vertices):
        self.nb_vertices = nb_vertices
        self.adjacencies = np.full((self.nb_vertices, self.nb_vertices), -1, dtype=np.int8)
        self.nb_colors = 0

    def __str__(self):
        ret_str = "nb vertices : {}\n".format(self.nb_vertices)
        ret_str += "nb colors : {}\n".format(self.nb_colors)
        ret_str += "adjacency :\n"
        ret_str += "{}".format(self.adjacencies)
        return ret_str

    # methods to get some information from graph
    def count_cliques_c(self, color):
        nb_cliques = [0 for x in range(self.nb_vertices+1)]
        nb_cliques[0] = 1
        nb_cliques[1] = self.nb_vertices

        if self.nb_vertices == 1:
            None
        elif self.nb_vertices == 2:
            if self.adjacencies[0, 1] == color:
                nb_cliques[2] = 1
        elif self.nb_vertices == 3:
            if self.adjacencies[0, 1] == color:
                nb_cliques[2] += 1
            if self.adjacencies[0, 2] == color:
                nb_cliques[2] += 1
            if self.adjacencies[1, 2] == color:
                nb_cliques[2] += 1
                if nb_cliques[2] == 3:
                    nb_cliques[3] = 1
        elif len(np.where(self.adjacencies==color)[0]) == 0:
            None
        else: # greater than 3
            for v in range(self.nb_vertices):
                color_list = np.where(self.adjacencies[v, :] == color)[0].tolist()
                nxt_list = [x for x in color_list if x > v]
                if len(nxt_list) > 1:
                    sub_cliques = self.sub_graph(nxt_list).count_cliques_c(color)
                    for s in range(1, len(nxt_list)+1):
                        nb_cliques[s+1] += sub_cliques[s]
                elif len(nxt_list) == 1: # sub_cliques should equals [1, 1]
                    nb_cliques[2] += 1

        return nb_cliques

    def count_cliques(self, isomorphic=False):
        nb_cliques_all_colors = []

        if isomorphic:
            # all colors are isomorphic to first color
            nb_cliques = self.count_cliques_c(0)
            for c in range(self.nb_colors):
                nb_cliques_all_colors.append(nb_cliques)
        else:
            for c in range(self.nb_colors):
                nb_cliques = self.count_cliques_c(c)
                nb_cliques_all_colors.append(nb_cliques)

        return nb_cliques_all_colors

    def get_edge(self, v1, v2):
        return self.adjacencies[v1, v2]

    # methods to modify current graph
    def set_edge(self, v1, v2, color, symmetric=True):
        self.adjacencies[v1, v2] = color
        if symmetric:
            self.adjacencies[v2, v1] = color
        return

    # methods to get new graphs from current
    def sub_graph(self, vertices_list):
        sub_graph = Graph(len(vertices_list))
        for (n_i, o_i) in enumerate(vertices_list):
            for (n_j, o_j) in enumerate(vertices_list):
                sub_graph.adjacencies[n_i, n_j] = self.adjacencies[o_i, o_j]

        return sub_graph

    # class methods to construct graphs
    @classmethod
    def from_diffs(cls, tuple_of_diffs_lists):
        nb_colors = len(tuple_of_diffs_lists)
        all_diffs = []
        for c in tuple_of_diffs_lists:
            all_diffs.extend(c)
        all_diffs.sort()
        diffs_lists_ok = True
        expected_d = 1
        for d in all_diffs:
            if d != expected_d:
                diffs_lists_ok = False
                break
            else:
                expected_d += 1
        if not diffs_lists_ok:
            print("from_diffs Error : tuple_of_diffs_lists should be complete (each value from 1 to n present one time)")
            print(" expected color is {} get {}".format(expected_d, d))
            return None

        # tuple_of_diffs_lists is ok, create Graph
        nb_vertices = len(all_diffs) + 1
        cur_graph = cls(nb_vertices)
        for (c, diff_list) in enumerate(tuple_of_diffs_lists):
            for d in diff_list:
                for v in range(nb_vertices-d):
                    cur_graph.adjacencies[v, v + d] = cur_graph.adjacencies[v + d, v] = c
        cur_graph.nb_colors = nb_colors
        return cur_graph