#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from csv import DictReader, writer
import os

BASE_PATH = os.path.dirname(os.path.realpath(__file__)) + '/'


def id(stop_id, time):
    return str(stop_id) + '@' + str(time)


def print_id(stop_id):
    def bind_zero(n):
        return str(n) if n > 9 else '0' + str(n)
    node, time = stop_id.split('@')
    time = int(time)
    str_time = bind_zero(int(time / 60)) + ':' + bind_zero(time % 60)
    print(str_time, node)


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

# start = "StopPoint:OIF59657"  # Barbés
# end = "StopPoint:OIF59421"  # Place de Clichy

start_time = 15 * 60  # 15h

start_node = id(start, start_time)


src_file = open(BASE_PATH + './time-expanded/meta_data.txt', 'r')
meta = DictReader(src_file).next()

n = int(meta['n'])

# Init values
d = DataStore(float('inf'))  # sets all the distances to +inf
d.set(id(start, start_time), 0)
p = DataStore(None)  # sets all the predecessors to None

print "Executing Bellman with ", n, "nodes."
for k in range(n - 1):
    print(k)
    has_changed = False
    src_file = open(BASE_PATH + './time-expanded/sub_time_expanded.txt', 'r')
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

print('Searching for minimal path...')
min_time = float('inf')
end_node = None
for node in d.get_dict():
    curr_time = int(d.get_dict()[node])
    curr_id, _ = node.split('@')
    if curr_id == end:
        if curr_time < min_time:
            min_time = curr_time
            end_node = node

print('Temps : ', d.get(end_node))

print('Searching path....')
x = end_node
i = 0
while x != start_node and i <= 20:
    print_id(x)
    x = p.get(x)
    i += 1
print_id(start_node)
