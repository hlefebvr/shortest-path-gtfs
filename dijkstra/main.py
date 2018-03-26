#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import sys;
from heapq import heappush, heappop;

starting_node = "StopPoint:OIF59421"; # place de clichy
end_node = "StopPoint:OIF59657"; # Barbès

#G = {
#    "A": [ (3, "B"), (1, "C"), (10, "D") ],
#    "B": [ (0, "C"), (2, "D") ],
#    "C": [ (10, "D"), (1, "B") ],
#    "D": [],
#};

G = eval ( open('./dict.txt', 'r').read() );

def get_successors_list(node):
    try:
        succ_list = G[node];
    except:
        succ_list = [];
    return succ_list;

def get_stop_names(ids):
    names = ids;
    
    stops_file = open('../../gui/tmp/2.stops_sorted.csv', 'r');
    stops_reader = csv.DictReader(stops_file);

    for stop in stops_reader:
        for id in names:
            index = names.index(id);
            if stop['stop_id'] == id:
                names[index] = stop['stop_name'];
    stops_file.close();
    return names;

next_nodes = [ (0, starting_node) ];
dist = {};
dist[starting_node] = 0;
visited_nodes = [];
paths = {};

while next_nodes != []:
    min_d, curr_node = heappop(next_nodes);
    if curr_node not in visited_nodes: # we have already visited the node, skip it
        visited_nodes.append(curr_node);
        successors = get_successors_list(curr_node);
        for distance, succ in successors:
            if succ not in visited_nodes:
                could_be_better_dist = dist[curr_node] + distance;
                if succ not in visited_nodes or dist[curr_node] > could_be_better_dist:
                    dist[succ] = could_be_better_dist;
                    heappush(next_nodes, (could_be_better_dist, succ) );
                    paths[succ] = curr_node;

result = [end_node];

x = paths[end_node];
while x != starting_node:
    result.append(x);
    x = paths[x];

result.append(starting_node);
result.reverse();

print(result);
print(get_stop_names(result));
