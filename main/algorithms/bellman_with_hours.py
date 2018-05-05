#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from csv import DictReader


def shortest_path(arcs_file, start, end, departure_time=None):
    class DataStore:
        def __init__(self, default_value):
            self.default_value = default_value
            self.dict = {}

        def get(self, stop_id):
            try:
                return self.dict[stop_id]
            except:
                return self.default_value

        def set(self, stop_id, value):
            if (value != self.default_value):
                self.dict[stop_id] = value

        def get_dict(self):
            return self.dict

    # Init values
    d = DataStore(float('inf'))  # sets all the distances to +inf
    d.set(start, 0)
    p = DataStore(None)  # sets all the predecessors to None

    # compute n
    n = 300

    print("Executing Bellman with ", n, "nodes.")
    for k in range(n - 1):
        src_file = open(arcs_file, 'r')
        arcIterator = DictReader(src_file)
        for row in arcIterator:
            u = row['x']
            v = row['y']
            h = row['departure_time']
            w = int(row['travel_time'])
            if(d.get(v) > d.get(u) + w):
                d.set(v, d.get(u) + w)
                p.set(v, u)
        src_file.close()

    print ("Formatting result...")

    result = [end]
    x = end
    s = 0
    while x != start and s <= 20:
        x = p.get(x)
        result += [x]
        s += 1

    return result, d.get(end)
    # return p.get_dict()
