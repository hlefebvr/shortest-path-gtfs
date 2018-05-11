#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import csv


def print_path(path):
    f = open('./time-expanded/stops.txt')
    stops = csv.DictReader(f)
    n = len(path)
    times, ids = zip(*path)
    times, ids = list(times), list(ids)
    for stop in stops:
        try:
            index = ids.index(stop['stop_id'])
        except:
            continue
        ids[index] = stop['stop_name']
    f.close()
    for i in range(n):
        print times[i], ids[i]


values = [('15:29', 'StopPoint:OIF59591'),
          ('15:28', 'StopPoint:OIF59226'),
          ('15:27', 'StopPoint:OIF59235'),
          ('15:25', 'StopPoint:OIF59592'),
          ('15:24', 'StopPoint:OIF59232'),
          ('15:20', 'StopPoint:OIF59249'),
          ('15:18', 'StopPoint:OIF59490'),
          ('15:16', 'StopPoint:OIF59494'),
          ('15:14', 'StopPoint:OIF59489'),
          ('15:13', 'StopPoint:OIF59445'),
          ('15:12', 'StopPoint:OIF59620'),
          ('15:11', 'StopPoint:OIF59481'),
          ('15:10', 'StopPoint:OIF59487'),
          ('15:08', 'StopPoint:OIF59497'),
          ('15:07', 'StopPoint:OIF59274'),
          ('15:05', 'StopPoint:OIF59618'),
          ('15:00', 'StopPoint:OIF59634')
          ]

result = print_path(values)
