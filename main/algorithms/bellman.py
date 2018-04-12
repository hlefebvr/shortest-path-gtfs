#!/usr/local/bin/python
# -*- coding: utf-8 -*-

# Graph is a dictionary including a list of predecessor of each node
# graph = {'stop_id1':[[precessor1, distance1],[precessor2, distance2], ...],
#           'stop_id2':[[precessor1, distance1],[precessor2, distance2], ...],
#           ...
#           }
def bellman_ford(graph, source):
    # Step 1: Prepare the distance and predecessor for each node
    distance, predecessor = dict(), dict()
    for node in graph:
        distance[node], predecessor[node] = float('inf'), None
    distance[source] = 0

    # Step 2: Relax the edges
    for _ in range(len(graph) - 1):
        for node in graph:
            for dist, neighbour in graph[node]:
                if neighbour not in distance:
                    distance[neighbour] = float('inf');
                # If the distance between the node and the neighbour is lower than the current, store it
                if distance[neighbour] > distance[node] + dist:
                    distance[neighbour], predecessor[neighbour] = distance[node] + dist, node

     # Step 3: Check for negative weight cycles
    for node in graph:
        for dist, neighbour in graph[node]:
            assert distance[neighbour] <= distance[node] + dist, "Negative weight cycle."

    return distance,predecessor

# predecessor which is a dictionary will be the result found in bellman_ford
id2name = eval( open('../data_generation/output/id2name.json', 'r').read() );
def shortest_way(predecessor, source, origin):
    way = [id2name[origin][0].replace('\u00e9', 'é')]
    start = origin
    while True:
        if predecessor[start] == source:
            break;
        start = predecessor[start]
        way.append(id2name[start][0].replace('\u00e9', 'é'))
    way.append(id2name[source][0].replace('\u00e9', 'é'))
    return way;

graph = eval( open('../data_generation/output/graph_pred.json', 'r').read() );

starting_node = "StopPoint:OIF59587"; # Républiques
end_node = "StopPoint:OIF59659"; # Rivoli louvre

distance, predecessor = bellman_ford(graph, starting_node)
# {'a': 0, 'c': 4, 'b': 1, 'e': 3, 'd': 3}, the shortest to 'a' from each node
print "Shortest distance from d to a:", distance[end_node]
# the shortest distance from 'b' to 'a'
print "Shortest chemin from d to a:", shortest_way(predecessor, starting_node, end_node)
#shortest chemin from 'd' to 'a'
