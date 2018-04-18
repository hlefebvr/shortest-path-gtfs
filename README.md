# Graph algorithms applied to GTFS data

## Data generation

- Joining GTFS data **OK**
- Building successors/predecessors list **OK**
- Adding transfers to successors/predecessors list **OK**
- Adding interest points near stops (valuations = times by walk) **OK**
- Building stop_id stop_name correspondance **OK**
- Building compressed storage of stoptimes _TODO_

## Algorithms

- Dijkstra **OK**
- Bellman **OK**
- Bellman with stop times _TODO_
- Yen _TODO_

## Graph vizualisation

- Using pyplot to draw graph **OK** (for subway points only, doable but too long for bus stops)
- Drawing optimal solution to shortest path problem _TODO_