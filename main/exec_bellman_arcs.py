#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from csv import DictReader, writer
import os

BASE_PATH = os.path.dirname(os.path.realpath(__file__)) + '/'

# arcs_file = BASE_PATH + './data_generation/output/arcs.csv'
arcs_file = BASE_PATH + './result.csv'
tmp_file = BASE_PATH + './tmp.csv'


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


class Time:
    def __init__(self, value):
        if(type(value) == str):
            split = value.split(':')
            self._set(int(split[0]) * 60 + int(split[1]))
        else:
            self._set(value)

    def _set(self, value):
        self.value = value % (24 * 60)

    def __int__(self):
        return self.value

    def __str__(self):
        def bind_zero(i):
            return str(int(i)) if i > 9 else '0' + str(int(i))
        h = bind_zero(self.value / 60)
        m = bind_zero(self.value % 60)
        return str(h) + ':' + str(m)

    def __add__(self, other):
        return Time(self.value + int(other))

    def __sub__(self, other):
        return Time(self.value - int(other))

    def __lt__(self, other):
        return self.value < int(other)

    def __gt__(self, other):
        return self.value > int(other)

    def __le__(self, other):
        return self.value <= int(other)

    def __ge__(self, other):
        return self.value >= int(other)


start = "StopPoint:OIF59587"  # Républiques
end = "StopPoint:OIF59659"  # Rivoli louvre
start_time = Time('13:00')

# Init values
d = DataStore(float('inf'))  # sets all the distances to +inf
d.set(start, 0)
p = DataStore((None, 'NA', None))  # sets all the predecessors to None

counter = DataStore(None)

print "Removing useless hours..."

src_file = open(arcs_file, 'r')
arcIterator = DictReader(src_file)
tmp = open(tmp_file, 'w')
tmp_writer = writer(tmp)
tmp_writer.writerow(('u', 'v', 'departure_time', 'travel_time'))
two_hours = Time(1 * 60)
for row in arcIterator:
    is_transfer = ((row['is_transfer'] == '1'))
    departure_time = 'NA' if is_transfer else Time(row['departure_time'])
    travel_time = row['travel_time']
    u = row['u']
    v = row['v']
    if is_transfer or (departure_time >= start_time) and (departure_time - start_time <= two_hours):
        tmp_writer.writerow((u, v, departure_time, travel_time))
        counter.set(u, 1)
        counter.set(v, 1)

n = len(counter.get_dict())

del counter

src_file.close()
tmp.close()

print "Executing Bellman with ", n, "nodes."
for k in range(n - 1):
    has_changed = False
    # print str(float(k) / float(n) * 100) + ' %'
    src_file = open(tmp_file, 'r')
    arcIterator = DictReader(src_file)
    for row in arcIterator:
        u = row['u']
        v = row['v']
        w = int(row['travel_time'])
        h = row['departure_time']

        if(d.get(v) > d.get(u)):
            has_changed = True
            d.set(v, d.get(u) + w)
            p.set(v, (u, h, w))
    src_file.close()
    if(has_changed == False):
        print 'No changes were made during last execution... (', k, ')'
        break

print "Formatting result..."

_, end_time, w = p.get(end)
result = [(end, end_time, w)]
x = end
s = 0
while x != start and s <= 20:
    x, h, w = p.get(x)
    result += [(x, h, w)]
    s += 1

id2name = eval(
    open(BASE_PATH + './data_generation/output/id2name.json', 'r').read())

for id, h, w in reversed(result):
    stop_info = id2name[id]
    print str(h), w,
    for info in reversed(stop_info):
        print info.replace('\u00e9', 'é'), '\t',
    print
