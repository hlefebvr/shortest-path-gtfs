#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os, csv, pickle, lmdb, itertools
from math import cos, sin, radians, atan2, sqrt
from csvsort import csvsort

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


def minutes(str):  # hh:mm --> mm
    if str == 'None':
        return ''
    split = str.split(':')
    return int(split[0]) * 60 + int(split[1])


def getCartesian(lat, lon):
    lat = radians(float(lat))
    lon = radians(float(lon))
    R = 6373.0  # approximate radius of earth in km
    x = R * cos(lat) * cos(lon)
    y = R * cos(lat) * sin(lon)
    return (y, -x)


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
        self.STOPS_HEADERS = ['stop_id', 'stop_name', 'stop_lat', 'stop_lon']
        self.TIMETABLE_HEADERS = ['from', 'to', 'departure',
                                  'arrival', 'travel_time', 'route', 'route_type']
        self.STOPSMAP_HEADERS = ['id', 'name', 'lat', 'lon', 'route_type']
        self.MODES = {1: 'metro', 2: 'train', 3: 'bus'}

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
        all = ['alpha_beta.txt',
               'alpha_beta-metro.txt',
               'alpha_beta-train.txt',
               'alpha_beta-bus.txt',
               'alpha_beta-metro-train.txt',
               'alpha_beta-metro-bus.txt',
               'alpha_beta-train-bus.txt',
               'alpha_beta-metro-train-bus.txt']
        return self.files_exists(['time_expanded-metro.db',
                                  'time_expanded-train.db',
                                  'time_expanded-bus.db',
                                  'time_expanded-metro-train.db',
                                  'time_expanded-metro-bus.db',
                                  'time_expanded-train-bus.db',
                                  'time_expanded-metro-train-bus.db',
                                  'condensed-metro.db',
                                  'condensed-train.db',
                                  'condensed-bus.db',
                                  'condensed-metro-train.db',
                                  'condensed-metro-bus.db',
                                  'condensed-train-bus.db',
                                  'condensed-metro-train-bus.db',
                                  'time_expanded-metro.txt',
                                  'time_expanded-train.txt',
                                  'time_expanded-bus.txt',
                                  'time_expanded-metro-train.txt',
                                  'time_expanded-metro-bus.txt',
                                  'time_expanded-train-bus.txt',
                                  'time_expanded-metro-train-bus.txt',
                                  'stops-metro.txt',
                                  'stops-train.txt',
                                  'stops-bus.txt',
                                  'stops-metro-train.txt',
                                  'stops-metro-bus.txt',
                                  'stops-train-bus.txt',
                                  'stops-metro-train-bus.txt',
                                  'condensed-metro.txt',
                                  'condensed-train.txt',
                                  'condensed-bus.txt',
                                  'condensed-metro-train.txt',
                                  'condensed-metro-bus.txt',
                                  'condensed-train-bus.txt',
                                  'condensed-metro-train-bus.txt', ])

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
        writer = csv.DictWriter(f, fields)
        writer.close = f.close
        return writer

    def remove_csv(self, filename):
        path = self.get_conf('WORKSPACE') + '/' + \
            filename + self.get_conf('EXTENSION')
        try:
            os.remove(path)
        except:
            print('File does not exist')

    def join_csv_on(self, file1, keys1, file2, keys2, output_file):
        workspace_path = self.get_conf('WORKSPACE') + '/'
        extension = self.get_conf('EXTENSION')
        # sorting file1
        csvsort(workspace_path + file1 + extension, keys1, output_filename=workspace_path +
                '/file1.sorted' + extension, has_header=True)
        # sorting file2
        csvsort(workspace_path + file2 + extension, keys2, output_filename=workspace_path +
                '/file2.sorted' + extension, has_header=True)
        # merging
        file1_reader = open(workspace_path + '/file1.sorted' + extension, 'r')
        file2_reader = open(workspace_path + '/file2.sorted' + extension, 'r')
        output_writer = open(workspace_path + output_file + extension, 'w')
        file1_csv_reader = csv.reader(file1_reader)
        file2_csv_reader = csv.reader(file2_reader)
        output_csv_writer = csv.writer(output_writer)

        header1 = file1_csv_reader.__next__()
        header2 = file2_csv_reader.__next__()
        del header2[keys2[0]]
        output_csv_writer.writerow(header1 + header2)

        line_from_file1 = file1_csv_reader.__next__()
        line_from_file2 = file2_csv_reader.__next__()

        while True:
            if line_from_file1[keys1[0]] < line_from_file2[keys2[0]]:
                try:
                    line_from_file1 = file1_csv_reader.__next__()
                    continue
                except:
                    break
            if line_from_file1[keys1[0]] == line_from_file2[keys2[0]]:
                del line_from_file2[keys2[0]]
                output_csv_writer.writerow(line_from_file1 + line_from_file2)
            try:
                line_from_file2 = file2_csv_reader.__next__()
            except:
                break

        file1_reader.close()
        file2_reader.close()
        output_writer.close()

        # removing tepporary files
        self.remove_csv('file1.sorted')
        self.remove_csv('file2.sorted')

    def get_stops_xy(self, filename='stops-metro-train-bus', stop_ids=None):
        stops = self.open_csv(filename)
        x, y = [], []
        for stop in stops:
            if (stop_ids == None) or (stop['id'] in stop_ids):
                _x, _y = getCartesian(stop['lat'], stop['lon'])
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
                    'stop_name': row['stop_name'],
                    'stop_lat': row['stop_lat'],
                    'stop_lon': row['stop_lon']
                })
        stops.close()
        stops_reduced.close()

    def build_time_expanded_model(self):
        workspace_path = self.get_conf('WORKSPACE') + '/'
        extension = self.get_conf('EXTENSION')
        print('Building time expanded model...')

        print('Jointure des stops résultants avec les heures d\'arrets (stop_times.txt)...')
        self.join_csv_on('stops-reduced', [0],
                         'stop_times', [3], 'stops-stop_times')

        print('Jointure des heures d\'arrêts résultants avec les voyages (trips.txt)')
        self.join_csv_on('trips', [2], 'stops-stop_times',
                         [4], 'stops-stop_times-trips')

        print('Jointure des heures d\'arrêts résultants avec les routes (routes.txt)')
        self.join_csv_on('routes', [0], 'stops-stop_times-trips',
                         [0], 'stops-stop_times-trips-routes')

        print('Tri des heures d\'arrêts par voyage (trip_id) et heure de départs (departure_time)...')
        csvsort(workspace_path + 'stops-stop_times-trips-routes' + extension,
                ['trip_id', 'departure_time'], output_filename=workspace_path + 'jointure' + extension)

        print('Génération des arcs de transports...')
        arcs_transport = self.new_csv('arcs_transport', self.TIMETABLE_HEADERS)
        stoptimes = self.open_csv('jointure')
        last_two = Memo(2)
        all_stops = {}

        for row in stoptimes:
            last_two.put(row)
            if last_two.is_ready():
                stop1, stop2 = last_two.get()
                if stop1['trip_id'] == stop2['trip_id']:
                    arc = {
                        'from': stop1['stop_id'],
                        'to': stop2['stop_id'],
                        'departure': minutes(stop1['departure_time']),
                        'arrival': minutes(stop2['departure_time']),
                        'travel_time': minutes(stop2['departure_time']) - minutes(stop1['departure_time']),
                        'route_type': stop1['route_type'],
                        'route': stop1['route_short_name']
                    }
                    all_stops[stop1['stop_id']] = True
                    arcs_transport.writerow(dict(arc))
        print('Tri des transfers (transfers) par stops de départ (from_stop_id)...')
        csvsort(workspace_path + 'transfers' + extension, [0],
                output_filename=workspace_path + 'transfers' + extension)

        print('Tri des arcs par stop (stop_id)')
        csvsort(workspace_path + 'arcs_transport' + extension, [0],
                output_filename=workspace_path + 'arcs_transport' + extension)

        print('Génération des arcs de transfers...')
        transfers = self.open_csv('transfers')
        arcs_transport = self.open_csv('arcs_transport')
        arcs_transfers = self.new_csv('arcs_transfers', self.TIMETABLE_HEADERS)
        stop = False
        arc = arcs_transport.__next__()

        for tr in transfers:
            if tr['from_stop_id'] in all_stops:
                while tr['from_stop_id'] > arc['from']:
                    try:
                        arc = arcs_transport.__next__()
                    except:
                        stop = True
                        break
                if stop:
                    break
                while tr['from_stop_id'] == arc['from']:
                    try:
                        travel_time = int(int(tr['min_transfer_time']) / 60)
                        arc = {
                            'from': tr['from_stop_id'],
                            'to': tr['to_stop_id'],
                            'departure': int(arc['arrival']),
                            'arrival': int(arc['arrival']) + travel_time,
                            'travel_time': travel_time,
                            'route_type': '-1',  # signifiant "transfer"
                            'route': '-1'
                        }
                        arcs_transfers.writerow(dict(arc))
                    except:
                        print('There was one error...')
                    try:
                        arc = arcs_transport.__next__()
                    except:
                        stop = True
                        break
            if stop:
                break
        transfers.close()
        arcs_transport.close()
        arcs_transfers.close()

        print('Concaténation des arcs...')
        filename = 'time_expanded'
        for mode in self.MODES:
            filename += '-' + self.MODES[mode]
        time_expanded = self.new_csv(filename, self.TIMETABLE_HEADERS)
        arcs_transport = self.open_csv('arcs_transport')
        arcs_transfers = self.open_csv('arcs_transfers')
        error = 0
        for arc in arcs_transport:
            try:
                time_expanded.writerow(dict(arc))
            except:
                # on a trouvé le cas où deux lignes étaient sur une...
                error += 1
        for arc in arcs_transfers:
            try:
                time_expanded.writerow(dict(arc))
            except:
                # on a trouvé le cas où deux lignes étaient sur une...
                error += 1
        arcs_transport.close()
        arcs_transfers.close()
        time_expanded.close()
        if error > 0:
            print('Nombre de ligne non traitée : ' + str(error))

        print('Nettoyage en cours....')
        del all_stops
        self.remove_csv('arcs_transfers')
        self.remove_csv('arcs_transport')
        self.remove_csv('transfers-sorted')
        self.remove_csv('stops-stop_times')
        self.remove_csv('stops-stop_times-trips')
        self.remove_csv('stops-stop_times-trips-routes')

    def build_condensed_model_from_time_expanded_model(self):
        print('Building condensed model')
        workspace_path = self.get_conf('WORKSPACE') + '/'
        extension = self.get_conf('EXTENSION')
        csvsort(workspace_path + 'time_expanded-metro-train-bus' + extension,
                ['from', 'to'], output_filename=workspace_path + 'beta-metro-train-bus' + extension, has_header=True)
        arcs = self.open_csv('beta-metro-train-bus')
        condensed = self.new_csv(
            'condensed-metro-train-bus', self.TIMETABLE_HEADERS)
        min = None
        memo = Memo(2)
        for arc in arcs:
            memo.put(arc)
            if memo.is_ready():
                _arc, arc = memo.get()
                if _arc['from'] != arc['from'] or _arc['to'] != arc['to']:
                    condensed.writerow({
                        'from': _arc['from'],
                        'to': _arc['to'],
                        'travel_time': min,
                        'route': _arc['route'],
                        'route_type': _arc['route_type']
                    })
                    min = arc['travel_time']
                elif _arc['travel_time'] > arc['travel_time']:
                    min = arc['travel_time']
        arcs.close()
        print('Condensed model done')
        print('Condensed sorted')

    def build_cuboid_from_model(self, model_type):
        print('Building cuboid')
        workspace_path = self.get_conf('WORKSPACE') + '/'
        extension = self.get_conf('EXTENSION')
        filename = model_type
        for mode in self.MODES:
            filename += '-' + self.MODES[mode]
        path = workspace_path + filename + extension
        modes = list(self.MODES)
        n_modes = len(modes)
        cuboid = []
        for i in range(1, n_modes):
            cuboid += list(itertools.combinations(modes, i))
        filename = model_type
        for mode in self.MODES:
            filename += '-' + self.MODES[mode]
        arcs = self.open_csv(filename)
        outputs = {}
        for combi in cuboid:
            filename = model_type
            for mode_index in combi:
                filename += '-' + self.MODES[mode_index]
            outputs[combi] = self.new_csv(filename, self.TIMETABLE_HEADERS)
        error_count = 0
        for arc in arcs:
            for combi in cuboid:
                try:
                    route_type = int(arc['route_type'])
                except:
                    error_count += 1
                    continue
                if route_type in combi or route_type == -1:  # -1 is for transfers
                    outputs[combi].writerow(dict(arc))
        arcs.close()
        for combi in cuboid:
            outputs[combi].close()
        print(str(len(cuboid)) + ' ' + model_type +
              ' models have been generated')
        print(str(error_count) + ' errors occured')

    def build_alpha_beta_from_condensed_model(self):
        print('Building alpha-beta')

    def build_stops(self):
        print("Building stops...")
        modes = list(self.MODES)
        n_modes = len(modes)
        cuboid = []
        for i in range(1, n_modes + 1):
            cuboid += list(itertools.combinations(modes, i))
        path = self.get_conf('WORKSPACE') + '/jointure' + \
            self.get_conf('EXTENSION')
        csvsort(path, ['stop_id'], output_filename=path, has_header=True)
        memo = Memo(2)
        jointure = self.open_csv('jointure')
        outputs = {}
        for combi in cuboid:
            filename = 'stops'
            for mode_index in combi:
                filename += '-' + self.MODES[mode_index]
            outputs[combi] = self.new_csv(filename, self.STOPSMAP_HEADERS)
        for line in jointure:
            memo.put(line)
            if memo.is_ready():
                line1, line2 = memo.get()
                if (line1['stop_id'] != line2['stop_id']):
                    for combi in cuboid:
                        if int(line1['route_type']) in combi:
                            outputs[combi].writerow({
                                'id': line1['stop_id'],
                                'name': line1['stop_name'],
                                'lat': line1['stop_lat'],
                                'lon': line1['stop_lon'],
                                'route_type': line1['route_type']
                            })

        jointure.close()
        for combi in cuboid:
            outputs[combi].close()
        print('Stops have been generated')

    def prepare_bellman(self, source, start_node, start_time):
        start_time = int(start_time)
        time_expanded = self.open_csv(source)
        output = self.new_csv('bellman_prepared', self.TIMETABLE_HEADERS)
        for i in range(1, 21):
            output.writerow({
                'from': start_node,
                'to': start_node,
                'departure': str(start_time),
                'arrival': str(start_time + i),
                'travel_time': str(i)
            })
        for arc in time_expanded:
            try:
                departure = int(arc['departure'])
                arrival = int(arc['arrival'])
            except:
                print('An error occured')
                continue
            if (departure >= start_time and arrival <= start_time + 120):
                output.writerow(dict(arc))
        time_expanded.close()

    def bellman(self, mode_prefix, start_node, end_node, start_time):
        def id(stop_id, time): return str(stop_id) + '@' + str(time)
        self.controller.report_exec('state', 'preparation...')
        start_id = id(start_node, minutes(start_time))
        if start_time == 'None':
            filename = 'condensed' + mode_prefix
        else:
            filename = 'time_expanded' + mode_prefix
            self.prepare_bellman(filename, start_node, minutes(start_time))
            filename = 'bellman_prepared'

        n = 300  # hard coded for now

        # Init values
        d = DataStore(float('inf'))  # sets all the distances to +inf
        d.set(start_id, 0)
        p = DataStore(None)  # sets all the predecessors to None

        self.controller.report_exec('state', 'en cours...')
        for k in range(n - 1):
            self.controller.report_exec('k', k)
            has_changed = False
            arcIterator = self.open_csv(filename)
            m = 0
            for row in arcIterator:
                try:
                    u = id(row['from'], row['departure'])
                    v = id(row['to'], row['arrival'])
                    w = int(row['travel_time'])
                    m += 1
                except:
                    print('There was an error on ' + row['from'])
                    continue

                if(d.get(v) > d.get(u) + w):
                    has_changed = True
                    d.set(v, d.get(u) + w)
                    p.set(v, u)
            arcIterator.close()
            self.controller.report_exec('m', m)
            if(has_changed == False):
                print('No changes were made during last execution... (' + str(k) + ')')
                break

        end_id = id(end_node, minutes(start_time))
        if start_time != 'None':
            print('Searching for minimal path...')
            min_time = float('inf')
            end_id = None
            for node in d.get_dict():
                curr_time = int(d.get_dict()[node])
                curr_id, _ = node.split('@')
                if curr_id == end_node:
                    if curr_time < min_time:
                        min_time = curr_time
                        end_id = node

        x = end_id
        i = 0
        path = []
        while x != start_id and i <= 30:
            i += 1
            path.append(x)
            x = p.get(x)
        path.append(start_id)
        stops = self.open_csv('stops-metro-train-bus')  # + mode_prefix)
        for stop in stops:
            for i in range(len(path)):
                try:
                    node_id, time = path[i].split("@")
                except:
                    continue
                if stop['id'] == node_id:
                    x, y = getCartesian(stop['lat'], stop['lon'])
                    path[i] = (time, stop['name'], '',
                               stop['route_type'], x, y)
        stops.close()
        self.controller.report_exec('state', 'termine')
        self.controller.show_result(path)

    def build_successors_list(self):
        workspace_path = self.get_conf('WORKSPACE') + '/'
        extension = self.get_conf('EXTENSION')
        print('Building successors list...')
        for source in ['time_expanded-metro',
                       'time_expanded-train',
                       'time_expanded-bus',
                       'time_expanded-metro-train',
                       'time_expanded-metro-bus',
                       'time_expanded-train-bus',
                       'time_expanded-metro-train-bus',
                       'condensed-metro',
                       'condensed-train',
                       'condensed-bus',
                       'condensed-metro-train',
                       'condensed-metro-bus',
                       'condensed-train-bus',
                       'condensed-metro-train-bus']:
            print(workspace_path+source+'.db')
            csvsort(workspace_path + source + extension,
                ['from', 'departure'], output_filename=workspace_path + source + 'sort' + extension)
            print(source + 'have sorted')
            env = lmdb.open(workspace_path + source + '.db', map_size=int(1e13))
            with env.begin(write=True) as txn:
                csviterator = self.open_csv(source+'sort')
                row = csviterator.next()
                suc = []
                stop = row['from']
                for row in csviterator:
                    if row['from'] == stop:
                        suc.append((row['travel_time'],row['departure'],row['arrival'],row['to']))
                    else:
                        stop = row['from']
                        txn.put(stop.encode(), str(suc).encode())
                        suc = [(row['travel_time'],row['departure'],row['arrival'],row['to'])]
            print('list sucessors of' + source +'have generated')
    
    def dijkstra(self, mode_prefix, start_node, end_node):
        print('Dijkstra')

    def get_stops_iterator(self, filename):
        return self.open_csv(filename)
