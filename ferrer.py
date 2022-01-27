# -*- coding: utf-8 -*-

__author__ = 'Stéphane-Poirier'


class FerrerIterator():
    def __init__(self, length_max, nb_max, size=-1):
        self.length_max = length_max
        self.nb_max = nb_max
        self.size = size
        self.current = None
        self.nb_iter = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.size == -1:
            return self.next()
        else:
            if self.current and self.current[1] == self.size:
                print("nb iter {}".format(self.nb_iter))
                raise StopIteration
            nxt = self.next()
            sz = sum([x * y for (x, y) in enumerate(nxt)])
            while sz != self.size:
                if sz > self.size:
                    self.push_last_to_end()
                nxt = self.next()
                sz = sum([x * y for (x, y) in enumerate(nxt)])
            return nxt

    def push_last_to_end(self):
        if self.current[-1] == 0:
            for lg in range(self.length_max - 1, -1, -1):
                if self.current[lg] > 0:
                    self.current[-1] = self.current[lg]
                    self.current[lg] = 0
                    break
        return

    def next(self):
        self.nb_iter += 1
        if not self.current:
            self.current = [0 for x in range(self.length_max + 1)]
            self.current[0] = self.nb_max
        elif self.current[self.length_max] == self.nb_max:
            print("nb iter {}".format(self.nb_iter))
            raise StopIteration
        else:
            last_not_nul = -1
            for lg in range(self.length_max-1, -1, -1):
                if self.current[lg] > 0:
                    last_not_nul = lg
                    break
            if last_not_nul == -1:
                print("nb iter {}".format(self.nb_iter))
                raise StopIteration
            last_val = self.current[self.length_max]
            self.current[self.length_max] = 0 # may be changed after
            self.current[last_not_nul] -= 1
            self.current[last_not_nul+1] = last_val + 1

        return self.current


def ferrer_size(lst):
    return sum([x*y for (x, y) in enumerate(lst)])