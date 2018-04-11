#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import csv;
import os;
import json;
from util.distances import distance;

BASE_PATH = os.path.dirname(os.path.realpath(__file__)) + '/';

points = [
    ['PI: La tour Effeil', 48.858525, 2.294492],
    ['PI: L\'arc de Triomphe', 48.874003, 2.295017],
    ['PI: Le musée du Louvre', 48.860752, 2.337644],
    ['PI: Basilic du sacré coeur', 48.887562, 2.343307],
    ['PI: Cathédrale Notre-Dame de Paris', 48.853166, 2.349870],
    ['PI: Pont Alexandre III', 48.864111, 2.313559],
    ['PI: Panthéon', 48.846434, 2.346500],
    ['PI: Place Vendôme', 48.867629, 2.329398]
];
human_speed_in_km_per_hour = 5;
arrival_radius_in_km = 0.5;
graph = eval ( open('./output/graph.json', 'r').read() );
id2name = eval ( open('./output/id2name.json', 'r').read() );

def add_link(stop1_id, stop2_id, time):
    to_add = [time, stop2_id];
    if stop1_id in graph:
        graph[stop1_id].append( to_add );
    else:
        graph[stop1_id] = [to_add];

stops_reader = open(BASE_PATH + '../../gtfs/stops.txt', 'r');
stops_csv_reader = csv.DictReader(stops_reader);
output_writer = open(BASE_PATH + './output/graph_pi.json', 'w');
output_id2name_writer = open(BASE_PATH + './output/id2name_pi.json', 'w');

for stop in stops_csv_reader:
    point_index = 1;
    for point in points:
        dist = distance( point[1], point[2], stop['stop_lat'], stop['stop_lon'] );
        if dist <= arrival_radius_in_km:
            point_id = 'PI' + str(point_index);
            time = int( dist / human_speed_in_km_per_hour * 60 );
            add_link(point_id, stop['stop_id'], time);
            add_link(stop['stop_id'], point_id , time);
        point_index = point_index + 1;

output_writer.write( json.dumps(graph) );

index = 1;
for pi in points:
    point_id = 'PI' + str(index);
    id2name[point_id] = [pi[0], 'P.I.', 'NA'];
    index = index + 1;

output_id2name_writer.write( json.dumps(id2name) );

stops_reader.close();
output_writer.close();
output_id2name_writer.close();
