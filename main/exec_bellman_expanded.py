#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from csv import DictReader, writer
import os

BASE_PATH = os.path.dirname(os.path.realpath(__file__)) + '/'


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


start = "StopPoint:OIF59587"  # Républiques
end = "StopPoint:OIF59659"  # Rivoli louvre
start_time = 13 * 60  # 13h


def id(stop_id, time):
    return str(stop_id) + '@' + str(time)


# Init values
d = DataStore(float('inf'))  # sets all the distances to +inf
d.set(id(start, start_time), 0)
p = DataStore((None, 'NA', None))  # sets all the predecessors to None

n = 324  # hard coded for now

print "Executing Bellman with ", n, "nodes."
for k in range(n - 1):
    print(str(int(k / n * 100)) + '%')
    has_changed = False
    src_file = open(BASE_PATH + './time-expanded/time_expanded.txt', 'r')
    arcIterator = DictReader(src_file)
    arcIterator.next()
    for row in arcIterator:
        u = id(row['from'], row['departure'])
        v = id(row['to'], row['arrival'])
        w = int(row['travel_time'])

        if(d.get(v) > d.get(u) + w):
            has_changed = True
            d.set(v, d.get(u) + w)
            p.set(v, u)
    src_file.close()
    if(has_changed == False):
        print 'No changes were made during last execution... (', k, ')'
        break

print p.get_dict()
