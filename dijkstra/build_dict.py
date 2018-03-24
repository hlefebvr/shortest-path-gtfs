#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import csv;

file_reader = open('../gui/tmp/14.successors_list.csv','r');
csv_reader = csv.reader(file_reader);

line = csv_reader.next(); # skip header

G = {};

def get_successors_unique():
    return [];

while True:
    try:
        line = csv_reader.next();
    except:
        break;
    successors_unique = [];
    i = 2;
    while True:
        try:
            fields = line[i][1:-1].split('/');
        except:
            break;
        i = i + 1;
        stop_id = fields[0];
        try:
            dist = int(fields[2]);
        except:
            continue;
        if dist != 0 and (dist, stop_id) not in successors_unique:
            successors_unique.append((dist, stop_id));
    G[line[0]] = successors_unique;

file_reader.close();
print G