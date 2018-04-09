#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import csv;
import os;
import json;

BASE_PATH = os.path.dirname(os.path.realpath(__file__)) + '/';

def diff_h(h1, h2):
    def to_ms(str_hour):
        hms = str_hour.split(':');
        return int(hms[0]) * 3600 + int(hms[1]) * 60 + int(hms[2]);
    def to_minutes(int_sec):
        return int_sec / 60
    ms1 = to_ms(h1);
    ms2 = to_ms(h2);
    delta = abs(ms1 - ms2);
    return to_minutes(delta);

graph = {};

timetable_file_reader = open(BASE_PATH + './output/timetable.csv');
timetable_csv_reader = csv.DictReader(timetable_file_reader);
transfers_file_reader = open(BASE_PATH + '../../gtfs/transfers.txt');
transfers_csv_reader = csv.DictReader(transfers_file_reader);
output_writer = open(BASE_PATH + './output/graph.json', 'w');

print "Building successors' list..."
curr_stop = timetable_csv_reader.next();
for next_stop in timetable_csv_reader:
    curr_trip_id = curr_stop['trip_id'];
    next_trip_id = next_stop['trip_id'];
    if curr_trip_id == next_trip_id:
        distance = diff_h( curr_stop['departure_time'], next_stop['arrival_time'] );
        successor = [int(distance), next_stop['stop_id']]
        if int(curr_stop['route_type']) in [1, 2, 3, 0]: # 3: bus
            if curr_stop['stop_id'] in graph:
                if successor not in graph[curr_stop['stop_id']]:
                    graph[curr_stop['stop_id']].append( successor );
            else:
                graph[curr_stop['stop_id']] = [successor];
    curr_stop = next_stop;

print "Adding transfers..."
for transfer in transfers_csv_reader:
    if transfer['from_stop_id'] in graph:
        tuple_to_add = [int(transfer['min_transfer_time']) / 60, transfer['to_stop_id']];
        graph[transfer['from_stop_id']].append( tuple_to_add );

output_writer.write( json.dumps(graph) );

timetable_file_reader.close();
transfers_file_reader.close();
output_writer.close();