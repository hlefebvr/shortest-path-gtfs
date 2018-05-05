#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from structures.arc_iterator import GraphArcIterator
from algorithms.bellman_with_hours import shortest_path

arcIterator = GraphArcIterator('./data_generation/output/sub')

starting_node = "StopPoint:OIF59587"  # Républiques
end_node = "StopPoint:OIF59659"  # Rivoli louvre

print(shortest_path(arcIterator, starting_node, end_node))
