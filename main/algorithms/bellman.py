#!/usr/local/bin/python
# -*- coding: utf-8 -*-

# Graph is a dictionary including a list of predecessor of each node
# graph = {'stop_id1':[[precessor1, distance1],[precessor2, distance2], ...],
#           'stop_id2':[[precessor1, distance1],[precessor2, distance2], ...],
#           ...
#           }
def shortest_path(graph, source, dest):
    # Step 1: Prepare the distance and predecessor for each node
    distance, predecessor = {}, {}
    distance[source] = 0

    def getDistance(node):
        try:
            return distance[node];
        except:
            return float('inf');

    # Step 2: Relax the edges
    for _ in range(len(graph) - 1):
        for node in graph:
            for dist, neighbour in graph[node]:
                # If the distance between the node and the neighbour is lower than the current, store it
                if getDistance(neighbour) > getDistance(node) + dist:
                    distance[neighbour], predecessor[neighbour] = getDistance(node) + dist, node

    path = [dest];
    curr_node = dest;
    while predecessor[curr_node] != source:
        curr_node = predecessor[curr_node];
        path = path + [curr_node];
    path = path + [source];

    return distance[dest], reversed(path)
