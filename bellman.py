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
            for neighbour, dist in graph[node]:
                # If the distance between the node and the neighbour is lower than the current, store it
                if distance[neighbour] > distance[node] + dist:
                    distance[neighbour], predecessor[neighbour] = distance[node] + dist, node

     # Step 3: Check for negative weight cycles
    for node in graph:
        for neighbour, dist in graph[node]:
            assert distance[neighbour] <= distance[node] + dist, "Negative weight cycle."

    return distance,predecessor

# predecessor which is a dictionary will be the result found in bellman_ford
def shortest_way(predecessor, source, origin):
    way = [origin]
    start = origin
    while predecessor[start] is not source:
        start = predecessor[start]
        way.append(start)
    way.append(source)
    return way


# test example
graph = {
    'a':[['b', 1], ['c', 4]],
    'b':[['c', 3], ['d', 2], ['e', 2]],
    'c':[],
    'd':[['b', 1], ['c', 5]],
    'e':[['d', 3]]
}
distance, predecessor = bellman_ford(graph, source='a')
print distance
# {'a': 0, 'c': 4, 'b': 1, 'e': 3, 'd': 3}, the shortest to 'a' from each node
print "Shortest distance from d to a:", distance['d']
# the shortest distance from 'b' to 'a'
print "Shortest chemin from d to a:", shortest_way(predecessor, 'a', 'd')
#shortest chemin from 'd' to 'a'
