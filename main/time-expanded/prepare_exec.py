#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import os
import csv

BASE_PATH = os.path.dirname(os.path.realpath(__file__)) + '/'
WORKING_SPACE = './'
SOURCE_SPACE = '../../gtfs/'
EXTENSION = '.txt'
TIMETABLE_HEADERS = ['from', 'to', 'departure',
                     'arrival', 'travel_time', 'route', 'route_type']
STOPS_HEADERS = ['stop_id', 'stop_name']
META_DATA = ['n', 'm']

START_TIME = 15 * 60
MAX_TRAVEL_TIME = 2 * 60


def get_path_to_location(location):
    if location == 'SOURCE_SPACE':
        return SOURCE_SPACE
    elif location == 'WORKING_SPACE':
        return WORKING_SPACE
    raise ValueError(
        'La localisation du fichier doit être SOURCE_SPACE ou WORKING_SPACE')


def open_csv(file, location='SOURCE_SPACE'):
    space = get_path_to_location(location)
    f = open(BASE_PATH + space + file + EXTENSION, 'r')
    reader = csv.DictReader(f)
    reader.close = f.close
    return reader


def new_csv(file, fields, write_header=True):
    f = open(BASE_PATH + WORKING_SPACE + file + EXTENSION, 'w')
    if write_header:
        f.write(','.join(fields) + '\n')
    reader = csv.DictWriter(f, fields)
    reader.close = f.close
    return reader


class DataStore:
    def __init__(self, default_value):
        self.default_value = default_value
        self.dict = {}

    def get(self, stop_id):
        try:
            return self.dict[stop_id]
        except:
            return self.default_value

    def set(self, stop_id, value):
        if (value != self.default_value):
            self.dict[stop_id] = value

    def get_dict(self):
        return self.dict


time_expanded = open_csv('time_expanded', 'WORKING_SPACE')
sub_time_expanded = new_csv('sub_time_expanded', TIMETABLE_HEADERS)
meta_data = new_csv('meta_data', META_DATA)
error = 0
n = 0
m = 0

meta = DataStore(0)

for arc in time_expanded:
    try:
        if int(arc['route_type']) in [-1, 1] and int(arc['departure']) >= START_TIME and int(arc['departure']) <= START_TIME + MAX_TRAVEL_TIME:
            sub_time_expanded.writerow(arc)
            id = arc['from'] + arc['departure']
            meta.set(id, 1)
            m += 1
    except:
        error += 1

print(str(error) + ' errors')

for i in meta.get_dict():
    n += meta.get_dict()[i]

meta_data.writerow({'n': n, 'm': m})
