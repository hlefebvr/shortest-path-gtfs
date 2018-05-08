#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import os
import csv
import time
from math import sin, cos, sqrt, atan2, radians
from csvsort import csvsort

BASE_PATH = os.path.dirname(os.path.realpath(__file__)) + '/'
WORKING_SPACE = './'
SOURCE_SPACE = '../../gtfs/'
EXTENSION = '.txt'
TIMETABLE_HEADERS = ['from', 'to', 'departure',
                     'arrival', 'travel_time', 'route', 'route_type']
STOPS_HEADERS = ['stop_id', 'stop_name']


def get_path_to_location(location):
    if location == 'SOURCE_SPACE':
        return SOURCE_SPACE
    elif location == 'WORKING_SPACE':
        return WORKING_SPACE
    raise ValueError(
        'La localisation du fichier doit être SOURCE_SPACE ou WORKING_SPACE')


def minutes(str):  # hh:mm --> mm
    split = str.split(':')
    return int(split[0]) * 60 + int(split[1])


def distance(lat1, lon1, lat2, lon2):
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


def distance_to_center(lat, lon):
    return distance(lat, lon, 48.8610, 2.3439)


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


def remove_csv(file):
    os.remove(BASE_PATH + WORKING_SPACE + file + EXTENSION)


# supposing file2 has FK to file1 (file2 rows may be unreferenced in file1)
def join_csv_on(file1, keys1, file2, keys2, output_file):
    # sorting file1
    csvsort(BASE_PATH + file1, keys1, output_filename=BASE_PATH + WORKING_SPACE +
            './file1.sorted' + EXTENSION, has_header=True)
    # sorting file2
    csvsort(BASE_PATH + file2, keys2, output_filename=BASE_PATH + WORKING_SPACE +
            './file2.sorted' + EXTENSION, has_header=True)
    # merging
    file1_reader = open(BASE_PATH + WORKING_SPACE +
                        './file1.sorted' + EXTENSION, 'r')
    file2_reader = open(BASE_PATH + WORKING_SPACE +
                        './file2.sorted' + EXTENSION, 'r')
    output_writer = open(BASE_PATH + output_file, 'w')
    file1_csv_reader = csv.reader(file1_reader)
    file2_csv_reader = csv.reader(file2_reader)
    output_csv_writer = csv.writer(output_writer)

    header1 = file1_csv_reader.next()
    header2 = file2_csv_reader.next()
    del header2[keys2[0]]
    output_csv_writer.writerow(header1 + header2)

    line_from_file1 = file1_csv_reader.next()
    line_from_file2 = file2_csv_reader.next()

    while True:
        if line_from_file1[keys1[0]] < line_from_file2[keys2[0]]:
            try:
                line_from_file1 = file1_csv_reader.next()
                continue
            except:
                break
        if line_from_file1[keys1[0]] == line_from_file2[keys2[0]]:
            del line_from_file2[keys2[0]]
            output_csv_writer.writerow(line_from_file1 + line_from_file2)
        try:
            line_from_file2 = file2_csv_reader.next()
        except:
            break

    file1_reader.close()
    file2_reader.close()
    output_writer.close()

    # removing tepporary files
    os.remove(BASE_PATH + WORKING_SPACE + './file1.sorted' + EXTENSION)
    os.remove(BASE_PATH + WORKING_SPACE + './file2.sorted' + EXTENSION)


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


class ExecutionTime:
    def __init__(self):
        self.start = time.time()
        self.last_stop = self.start

    def get(self, total):
        since = self.start if total else self.last_stop
        self.last_stop = time.time()
        return float(time.time() - since) / 60

    def out(self, total=False):
        t = self.get(total)
        s = 's' if t > 1 else ''
        print(str(t) + ' minute' + s)


exec_time = ExecutionTime()

print('Suppressions des stops (stops.txt) qui ne sont pas dans Paris...')
stops = open_csv('stops')
stops_reduced = new_csv('stops', STOPS_HEADERS)
for row in stops:
    if distance_to_center(row['stop_lat'], row['stop_lon']) <= 5.63:
        stops_reduced.writerow({
            'stop_id': row['stop_id'],
            'stop_name': row['stop_name']
        })
stops.close()
stops_reduced.close()
exec_time.out()

print('Jointure des stops résultants avec les heures d\'arrets (stop_times.txt)...')
join_csv_on(
    WORKING_SPACE + 'stops' + EXTENSION, [0],
    SOURCE_SPACE + 'stop_times' + EXTENSION, [3],
    WORKING_SPACE + 'stops-stop_times' + EXTENSION  # output file
)
exec_time.out()

print('Jointure des heures d\'arrêts résultants avec les voyages (trips.txt)')
join_csv_on(
    SOURCE_SPACE + 'trips' + EXTENSION, [2],
    WORKING_SPACE + 'stops-stop_times' + EXTENSION, [2],
    WORKING_SPACE + 'stops-stop_times-trips' + EXTENSION
)
exec_time.out()

print('Jointure des heures d\'arrêts résultants avec les routes (routes.txt)')
join_csv_on(
    SOURCE_SPACE + 'routes' + EXTENSION, [0],
    WORKING_SPACE + 'stops-stop_times-trips' + EXTENSION, [0],
    WORKING_SPACE + 'stops-stop_times-trips-routes' + EXTENSION
)
exec_time.out()

print('Tri des heures d\'arrêts par voyage (trip_id) et heure de départs (departure_time)...')
csvsort(BASE_PATH + WORKING_SPACE + 'stops-stop_times-trips-routes' + EXTENSION,
        ['trip_id', 'departure_time'],
        output_filename=BASE_PATH + WORKING_SPACE + 'jointure' + EXTENSION
        )
exec_time.out()

print('Génération des arcs de transports...')
arcs_transport = new_csv('arcs_transport', TIMETABLE_HEADERS)
stoptimes = open_csv('jointure', 'WORKING_SPACE')
last_two = Memo(2)

for row in stoptimes:
    last_two.put(row)
    if last_two.is_ready():
        stop1, stop2 = last_two.get()
        if stop1['trip_id'] == stop2['trip_id']:
            arc = {
                'from': stop1['stop_id'],
                'to': stop2['stop_id'],
                'departure': minutes(stop1['departure_time']),
                'arrival': minutes(stop2['arrival_time']),
                'travel_time': minutes(stop2['arrival_time']) - minutes(stop1['departure_time']),
                'route_type': stop1['route_type'],
                'route': stop1['route_short_name']
            }
            arcs_transport.writerow(arc)
exec_time.out()

print('Tri des transfers (transfers) par stops de départ (from_stop_id)...')
csvsort(BASE_PATH + SOURCE_SPACE + 'transfers' + EXTENSION, [0],
        output_filename=BASE_PATH + WORKING_SPACE + 'transfers' + EXTENSION)
exec_time.out()

print('Tri des arcs par stop (stop_id)')
csvsort(BASE_PATH + WORKING_SPACE + 'arcs_transport' + EXTENSION, [0],
        output_filename=BASE_PATH + WORKING_SPACE + 'arcs_transport' + EXTENSION)
exec_time.out()

print('Génération des arcs de transfers...')
transfers = open_csv('transfers', 'WORKING_SPACE')
arcs_transport = open_csv('arcs_transport', 'WORKING_SPACE')
arcs_transfers = new_csv('arcs_transfers', TIMETABLE_HEADERS)
stop = False
arc = arcs_transport.next()

for tr in transfers:
    while tr['from_stop_id'] > arc['from']:
        try:
            arc = arcs_transport.next()
        except:
            stop = True
            break
    if stop:
        break
    while tr['from_stop_id'] == arc['from']:
        travel_time = int(int(tr['min_transfer_time']) / 60)
        arc = {
            'from': arc['from'],
            'to': tr['to_stop_id'],
            'departure': int(arc['departure']),
            'arrival': int(arc['departure']) + travel_time,
            'travel_time': travel_time,
            'route_type': '-1',  # signifiant "transfer"
            'route': '-1'
        }
        arcs_transfers.writerow(arc)
        try:
            arc = arcs_transport.next()
        except:
            stop = True
            break
    if stop:
        break
transfers.close()
arcs_transfers.close()
arcs_transport.close()
exec_time.out()

print('Concaténation des arcs...')
time_expanded = new_csv('time_expanded', TIMETABLE_HEADERS)
arcs_transport = open_csv('arcs_transport', 'WORKING_SPACE')
arcs_transfers = open_csv('arcs_transfers', 'WORKING_SPACE')
error = 0
for arc in arcs_transport:
    try:
        time_expanded.writerow(arc)
    except:
        error += 1  # on a trouvé le cas où deux lignes étaient sur une...
for arc in arcs_transfers:
    try:
        time_expanded.writerow(arc)
    except:
        error += 1  # on a trouvé le cas où deux lignes étaient sur une...
arcs_transport.close()
arcs_transfers.close()
time_expanded.close()
exec_time.out()
if error > 0:
    print('Nombre de ligne non traitée : ' + str(error))

print('Nettoyage en cours....')
remove_csv('arcs_transfers')
remove_csv('arcs_transport')
remove_csv('transfers')
remove_csv('stops-stop_times')
remove_csv('stops-stop_times-trips')
remove_csv('stops-stop_times-trips-routes')
remove_csv('jointure')
exec_time.out()

print "\nTime-expanded model générée en ",
exec_time.out(total=True)
