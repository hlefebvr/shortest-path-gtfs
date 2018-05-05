#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import csv
import os
import json
from util.diff_h import diff_h


class Memo:
    def __init__(self, mem_size):
        self._mem_size = mem_size
        self._index = 0
        self._memo = [None] * mem_size
        self._is_ready = False

    def put(self, x):
        self._memo[self._index] = x
        self._index = (self._index + 1) % self._mem_size
        if self._index == 0:
            self._is_ready = True

    def get(self):
        values = []
        for offset in range(0, self._mem_size):
            values.append(self._memo[(self._index + offset) % self._mem_size])
        return values

    def is_ready(self):
        return self._is_ready


BASE_PATH = os.path.dirname(os.path.realpath(__file__)) + '/'

output_writer = open(BASE_PATH + './output/arcs.csv', 'w')
csv_writer = csv.writer(output_writer)

timetable_file_reader = open(BASE_PATH + './output/timetable.csv')
timetable = csv.DictReader(timetable_file_reader)

csv_writer.writerow(('is_transfer', 'u', 'v', 'departure_time', 'travel_time'))

print "Generating arc list..."
memo = Memo(2)
for x in timetable:
    memo.put(x)
    if memo.is_ready():
        stop1, stop2 = memo.get()
        if stop1['trip_id'] == stop2['trip_id']:
            if int(stop1['route_type']) in [1]:
                duree_trajet = diff_h(
                    stop1['departure_time'], stop2['arrival_time'])
                csv_writer.writerow((0, stop1['stop_id'], stop2['stop_id'],
                                     stop1['departure_time'], duree_trajet))

timetable_file_reader.close()
del memo

print "Adding transfers..."
transfer_file_reader = open(BASE_PATH + '../../gtfs/transfers.txt')
transfers = csv.DictReader(transfer_file_reader)
memo = Memo(2)

for tr in transfers:
    csv_writer.writerow(
        (1, tr['from_stop_id'], tr['to_stop_id'], 'NA', tr['min_transfer_time']))

transfer_file_reader.close()
output_writer.close()
