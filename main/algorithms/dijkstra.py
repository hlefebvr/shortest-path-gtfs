#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from heapq import *

def dijkstra (s, t, voisins):
    M = set()
    d = {s: 0}
    p = {}
    suivants = [[0, s]] # tas de couples [d(x), x]

    while suivants != []:
        dx, x = heappop(suivants)
        if x in M:
            continue
        M.add(x)
        for w, y in voisins(x):
            if y in M:
                continue
            dy = dx + w
            if y not in d or d[y] > dy:
                d[y] = dy
                heappush(suivants, (dy, y))
                p[y] = x
    path = [t]
    x = t
    while x != s:
        x = p[x]
        path.insert(0, x)
    return d[t], path

starting_node = "StopPoint:OIF59587"; # Républiques
end_node = "StopPoint:OIF59659"; # Rivoli louvre

starting_node = "PI1";
end_node = "PI6";

graph = eval ( open('../data_generation/output/graph_pi.json', 'r').read() );

def voisins (s):
    return [] if s not in graph else graph[s];

time, stop_ids = dijkstra(starting_node, end_node, voisins);
del graph;
id2name = eval ( open('../data_generation/output/id2name_pi.json', 'r').read() );

print 'Temps estimé : ', time, ' minutes';
print '----------------------------'

for id in stop_ids:
    stop_info = id2name[id];
    for info in reversed(stop_info):
        print info.replace('\u00e9', 'é'),'\t',;
    print
