#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import csv;
import os;
import json;
from util.diff_h import diff_h;

BASE_PATH = os.path.dirname(os.path.realpath(__file__)) + '/';

graph = {};

timetable_file_reader = open(BASE_PATH + './output/timetable.csv');
timetable_csv_reader = csv.DictReader(timetable_file_reader);
transfers_file_reader = open(BASE_PATH + '../../gtfs/transfers.txt');
transfers_csv_reader = csv.DictReader(transfers_file_reader);
output_writer = open(BASE_PATH + './output/graph_pred.json', 'w');

print "Building successors' list..."
curr_stop = timetable_csv_reader.next();
for next_stop in timetable_csv_reader:
    curr_trip_id = curr_stop['trip_id'];
    next_trip_id = next_stop['trip_id'];
    if curr_trip_id == next_trip_id:
        distance = diff_h( curr_stop['departure_time'], next_stop['arrival_time'] );
        predecessor = [int(distance), curr_stop['stop_id']]
        if int(next_stop['route_type']) in [1, 2, 3, 0]: # 3: bus
            if next_stop['stop_id'] in graph:
                if predecessor not in graph[next_stop['stop_id']]:
                    graph[next_stop['stop_id']].append( predecessor );
            else:
                graph[next_stop['stop_id']] = [predecessor];
    curr_stop = next_stop;

print "Adding transfers..."
for transfer in transfers_csv_reader:
    if transfer['to_stop_id'] in graph:
        tuple_to_add = [int(transfer['min_transfer_time']) / 60, transfer['from_stop_id']];
        graph[transfer['to_stop_id']].append( tuple_to_add );

output_writer.write( json.dumps(graph) );

timetable_file_reader.close();
transfers_file_reader.close();
output_writer.close();