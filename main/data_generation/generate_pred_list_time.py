#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import csv
import os
import json
from util.diff_h import diff_h


class Memo:
    def __init__(self, mem_size):
        self._mem_size = mem_size
        self._index = 0
        self._memo = [None] * mem_size
        self._is_ready = False

    def put(self, x):
        self._memo[self._index] = x
        self._index = (self._index + 1) % self._mem_size
        if self._index == 0:
            self._is_ready = True

    def get(self):
        values = []
        for offset in range(0, self._mem_size):
            values.append(self._memo[(self._index + offset) % self._mem_size])
        return values

    def is_ready(self):
        return self._is_ready


def add_minute(h, m):
    def bind_zero(n):
        n = int(n)
        return str(n) if n >= 10 else '0' + str(n)
    hh, mm, _ = h.split(':')
    hh = int(hh)
    mm = int(mm)
    r = mm + m
    return bind_zero(hh + r / 60) + ':' + bind_zero(r % 60)


class Graph:
    def __init__(self):
        self._graph = {}

    def add_link(self, x, y, heure_depart, duree_trajet):

        heure_arrivee = add_minute(heure_depart, duree_trajet)

        if y not in self._graph:
            self._graph[y] = {}

        if x not in self._graph[y]:
            self._graph[y][x] = [[heure_depart, duree_trajet, None, 1]]

        else:  # le cas ou on rajoute une valuation
            # recupere la derniere valeur
            borne_inf_int, duree_trajet_int, delai_int, nb_trajet_int = self._graph[y][x][-1]

            delai_int_corr = delai_int if delai_int is not None else 0
            borne_sup_int = add_minute(
                borne_inf_int, nb_trajet_int * (delai_int_corr + duree_trajet_int))
            delai = diff_h(heure_depart, borne_sup_int)

            if duree_trajet == duree_trajet_int:  # c'est le meme temps de trajet donc on peut peut-être les mettre ensemble

                if delai_int == None:
                    self._graph[y][x][-1][2] = delai
                    self._graph[y][x][-1][3] += 1

                elif delai_int == delai:
                    self._graph[y][x][-1][3] += 1

                else:
                    self._graph[y][x].append(
                        [heure_depart, duree_trajet, None, 1])

            else:
                self._graph[y][x].append([heure_depart, duree_trajet, None, 1])

    def write(self):
        print self._graph


BASE_PATH = os.path.dirname(os.path.realpath(__file__)) + '/'

graph = Graph()

output_writer = open(BASE_PATH + './output/sub/sub_graph_1.json', 'w')

timetable_file_reader = open(BASE_PATH + './output/timetable.csv')
timetable = csv.DictReader(timetable_file_reader)

memo = Memo(2)
i = 0
n_subgraph = 1
for x in timetable:
    memo.put(x)
    if memo.is_ready():
        stop1, stop2 = memo.get()
        if stop1['trip_id'] == stop2['trip_id']:
            if int(stop1['route_type']) in [1]:
                duree_trajet = diff_h(
                    stop1['departure_time'], stop2['arrival_time'])
                graph.add_link(stop1['stop_id'], stop2['stop_id'],
                               stop1['departure_time'], duree_trajet)
                i += 1
                if i >= 2000:
                    output_writer.write(json.dumps(graph._graph))
                    i = 0
                    n_subgraph += 1
                    del graph
                    graph = Graph()
                    output_writer.close()
                    output_writer = open(
                        BASE_PATH + './output/sub/sub_graph_' + str(n_subgraph) + '.json', 'w')

output_writer.write(json.dumps(graph._graph))

timetable_file_reader.close()
output_writer.close()
