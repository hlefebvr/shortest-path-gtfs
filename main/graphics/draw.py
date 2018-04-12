#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt;
import matplotlib.image as mpimg
import csv;
from math import cos, sin, radians;

stops_file_reader = open('../data_generation/tmp/stops_heart.csv', 'r');
stops_csv_reader = csv.DictReader(stops_file_reader);

succ_list = eval ( open('../data_generation/output/graph_pi.json', 'r').read() );
id2name = eval ( open('../data_generation/output/id2name_pi.json', 'r').read() );
coord = {};

def isMetro(node):
    try:
        node_type = id2name[node][1];
        return node_type in ['Metro', 'P.I.'];
    except:
        return False;

def getCartesian(lat,lon):
    lat = radians(float(lat));
    lon = radians(float(lon));
    R = 6373.0 # approximate radius of earth in km
    x = R * cos(lat) * cos(lon)
    y = R * cos(lat) * sin(lon)
    return (y,-x); # !!

def getShowParam(x,y):
    transfer_style = {
        'color': '#000000',
        'dashes': [1,1]
    };
    try:
        info_x = id2name[x];
        info_y = id2name[y];
    except:
        return transfer_style;
    if info_x[2] == info_y[2]:
        return {
            'color': '#' + info_x[3],
            'dashes': [],
        };
    else:
        return transfer_style;

def showPI(id, name, lat, lon):
    x,y = getCartesian(lat, lon);
    plt.plot(x,y, 'bd', markersize=10)
    plt.annotate(name, [x, y]);

seine = [(48.830665, 2.258898),(48.860460, 2.292156),(48.863387, 2.300509),(48.863810, 2.318405),(48.850030, 2.359861),(48.823774, 2.393641)];
seine_x = [];
seine_y = [];
seine_w = 20;

for lat, lon in seine:
    x,y = getCartesian(lat, lon);
    seine_x = seine_x + [x];
    seine_y = seine_y + [y];
plt.plot(seine_x, seine_y, color='#dcf8f8', linewidth=seine_w);

for stop in stops_csv_reader:
    if isMetro(stop['stop_id']):
        x,y = getCartesian(stop['stop_lat'], stop['stop_lon']);
        coord[stop['stop_id']] = (x,y);
        plt.plot(x, y, 'ro', markersize = 5);

points = [
    ['La tour Effeil', 48.858525, 2.294492],
    ['L arc de Triomphe', 48.874003, 2.295017],
    ['Le musee du Louvre', 48.860752, 2.337644],
    ['Basilic du sacre coeur', 48.887562, 2.343307],
    ['Cathedrale Notre-Dame de Paris', 48.853166, 2.349870],
    ['Pont Alexandre III', 48.864111, 2.313559],
    ['Pantheon', 48.846434, 2.346500],
    ['Place Vendome', 48.867629, 2.329398]
];

id = 1;
for pi in points:
    pid = 'PI' + str(id);
    x,y = getCartesian( pi[1], pi[2] );
    coord[pid] = (x,y);
    showPI(pid, pi[0], pi[1], pi[2]);
    id = id + 1;

for x in succ_list:
    if isMetro(x):
        for d, y in succ_list[x]:
            if isMetro(y):
                cx = coord[x];
                try:
                    cy = coord[y];
                except:
                    continue;
                param = getShowParam(x,y);
                plt.plot([cx[0], cy[0]], [cx[1], cy[1]], color=param['color'], dashes=param['dashes']);

stops_file_reader.close();

plt.show();