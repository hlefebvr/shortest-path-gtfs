#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from heapq import *

def shortest_path (s, t, voisins):
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
