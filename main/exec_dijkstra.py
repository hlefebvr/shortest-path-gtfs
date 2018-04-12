#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from algorithms.dijkstra import shortest_path;
import os;
import time;

BASE_PATH = os.path.dirname(os.path.realpath(__file__)) + '/';

starting_node = "StopPoint:OIF59587"; # Républiques
end_node = "StopPoint:OIF59659"; # Rivoli louvre

graph = eval ( open(BASE_PATH + './data_generation/output/graph_pi.json', 'r').read() );
id2name = eval ( open(BASE_PATH + './data_generation/output/id2name_pi.json', 'r').read() );

def voisins (s):
    return [] if s not in graph else graph[s];

algo_start_time = time.time();
distance, stop_ids = shortest_path(starting_node, end_node, voisins);
algo_end_time = time.time();

print 'Temps de calcul : ', (algo_end_time - algo_start_time), ' s';
print 'Temps estimé : ', distance, ' minutes';
print '----------------------------'
for id in stop_ids:
    stop_info = id2name[id];
    for info in reversed(stop_info):
        print info.replace('\u00e9', 'é'),'\t',;
    print
