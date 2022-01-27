# -*- coding: utf-8 -*-

__author__ = 'Stéphane-Poirier'

from graph import Graph
import numpy as np

class DiffGraph(Graph):
    def __init__(self, tuple_of_diffs_lists):
        self.nb_colors = len(tuple_of_diffs_lists)
        all_diffs = []
        diffs_as_list = []
        for c in tuple_of_diffs_lists:
            all_diffs.extend(c)
            diffs_as_list.append(tuple(sorted(c)))
        self.diffs_tuple = tuple(diffs_as_list)
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
            raise ValueError

        # tuple_of_diffs_lists is ok, create Graph
        self.nb_vertices = len(all_diffs) + 1
        self.adjacencies = np.full((self.nb_vertices, self.nb_vertices), -1, dtype=np.int8)
        for (c, diff_list) in enumerate(tuple_of_diffs_lists):
            for d in diff_list:
                for v in range(self.nb_vertices-d):
                    self.adjacencies[v, v + d] = self.adjacencies[v + d, v] = c
        return
