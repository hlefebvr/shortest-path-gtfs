#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import csv;
import os;
import json;

BASE_PATH = os.path.dirname(os.path.realpath(__file__)) + '/';

id2name = {};

timetable_file_reader = open(BASE_PATH + './output/timetable.csv');
timetable_csv_reader = csv.DictReader(timetable_file_reader);
output_writer = open(BASE_PATH + './output/id2name.json', 'w');

def str_route_type(route_type):
    route_type = int(route_type);
    if route_type == 1:
        return 'Metro';
    elif route_type == 2:
        return 'Train';
    elif route_type == 3:
        return 'Bus';
    elif route_type == 0 or route_type == 5:
        return 'Tramway';
    else:
        return 'Mode inconnu';

for stop in timetable_csv_reader:
    id2name[stop['stop_id']] = [stop['stop_name'], str_route_type(stop['route_type']), stop['route_short_name']];

output_writer.write( json.dumps(id2name) );

timetable_file_reader.close();
output_writer.close();