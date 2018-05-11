#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import csv
from math import cos, sin, radians, atan2, sqrt


class Model:
    def __init__(self,
                 controller
                 ):
        self.controller = controller
        base_path = os.path.dirname(os.path.realpath(__file__)) + '/'
        self.conf_path = base_path + '/config.txt'
        self.default_workspace_path = base_path + './default_workspace'
        self.conf = {}
        self.load_conf()
        self.STOPS_HEADERS = ['stop_id', 'stop_name']

    def load_conf(self):
        conf_file = open(self.conf_path, 'r')
        for line in conf_file:
            key, value = line.split('=')
            self.set_conf(key, value.replace('\n', ''))
        conf_file.close()

    def save_conf(self):
        conf_file = open(self.conf_path, 'w')
        for key in self.conf:
            conf_file.write(str(key) + '=' + str(self.conf[key]) + '\n')
        conf_file.close()

    def set_conf(self, key, value):
        self.conf[key] = value
        self.save_conf()

    def get_conf(self, key):
        if (key in self.conf):
            return self.conf[key]
        if (key == 'WORKSPACE'):
            return self.default_workspace_path
        if (key == 'EXTENSION'):
            return '.txt'
        if (key == 'CENTER_LAT'):
            return '48.8610'
        if (key == 'CENTER_LON'):
            return '2.3439'
        if (key == 'RADIUS'):
            return '5.63'

    def files_exists(self, filesToCheck):
        try:
            files = os.listdir(self.get_conf('WORKSPACE'))
        except:
            return False
        for f in filesToCheck:
            if f not in files:
                return False
        return True

    def check_workspace(self):
        return self.files_exists(['stops.txt', 'stop_times.txt',
                                  'transfers.txt', 'routes.txt', 'trips.txt'])

    def check_workspace_ready(self):
        return self.files_exists(['time_expanded.txt', '''
                                  'time_expanded-metro.txt',
                                  'time_expanded-train.txt',
                                  'time_expanded-bus.txt',
                                  'time_expanded-metro-train.txt',
                                  'time_expanded-metro-bus.txt',
                                  'time_expanded-train-bus.txt',
                                  'time_expanded-metro-train-bus.txt',
                                  'condensed.txt',
                                  'condensed-metro.txt',
                                  'condensed-train.txt',
                                  'condensed-bus.txt',
                                  'condensed-metro-train.txt',
                                  'condensed-metro-bus.txt',
                                  'condensed-train-bus.txt',
                                  'condensed-metro-train-bus.txt',
                                  'alpha_beta.txt',
                                  'alpha_beta-metro.txt',
                                  'alpha_beta-train.txt',
                                  'alpha_beta-bus.txt',
                                  'alpha_beta-metro-train.txt',
                                  'alpha_beta-metro-bus.txt',
                                  'alpha_beta-train-bus.txt',
                                  'alpha_beta-metro-train-bus.txt' '''
                                  ])

    def open_csv(self, filename):
        f = open(self.get_conf('WORKSPACE') + '/' +
                 filename + self.get_conf('EXTENSION'))
        reader = csv.DictReader(f)
        reader.close = f.close
        return reader

    def new_csv(self, filename, fields, write_header=True):
        path = self.get_conf('WORKSPACE') + '/' + \
            filename + self.get_conf('EXTENSION')
        f = open(path, 'w')
        if write_header:
            f.write(','.join(fields) + '\n')
        reader = csv.DictWriter(f, fields)
        reader.close = f.close
        return reader

    def remove_csv(self, filename):
        path = self.get_conf('WORKSPACE') + '/' + \
            filename + self.get_conf('EXTENSION')
        try:
            os.remove(path)
        except:
            print('File does not exist')

    def get_stops_xy(self):
        def getCartesian(lat, lon):
            lat = radians(float(lat))
            lon = radians(float(lon))
            R = 6373.0  # approximate radius of earth in km
            x = R * cos(lat) * cos(lon)
            y = R * cos(lat) * sin(lon)
            return (y, -x)
        stops = self.open_csv('stops')
        x, y = [], []
        for stop in stops:
            _x, _y = getCartesian(stop['stop_lat'], stop['stop_lon'])
            x += [_x]
            y += [_y]
        stops.close()
        return x, y

    def distance(self, lat1, lon1, lat2, lon2):
        lat1 = radians(float(lat1))
        lat2 = radians(float(lat2))
        lon1 = radians(float(lon1))
        lon2 = radians(float(lon2))
        R = 6373.0  # approximate radius of earth in km
        dlon = lon1 - lon2
        dlat = lat1 - lat2
        a = sin(dlat / 2)**2 + cos(lat2) * cos(lat1) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        return R * c

    def reduce_stops(self):
        def distance_to_center(lat1, lon1):
            lat2 = self.get_conf('CENTER_LAT')
            lon2 = self.get_conf('CENTER_LON')
            return self.distance(lat1, lon1, lat2, lon2)
        radius = float(self.get_conf('RADIUS'))
        print('Reducing stops')
        stops = self.open_csv('stops')
        stops_reduced = self.new_csv('stops-reduced', self.STOPS_HEADERS)
        for row in stops:
            if distance_to_center(row['stop_lat'], row['stop_lon']) <= radius:
                stops_reduced.writerow({
                    'stop_id': row['stop_id'],
                    'stop_name': row['stop_name']
                })
        stops.close()
        stops_reduced.close()

    def build_time_expanded_model(self):
        print('Building time expanded model...')

    def build_condensed_model_from_time_expanded_model(self):
        print('Building condensed model')

    def build_cuboid_from_model(self, model_type):
        print('Building cuboid')

    def build_alpha_beta_from_condensed_model(self):
        print('Building alpha-beta')
