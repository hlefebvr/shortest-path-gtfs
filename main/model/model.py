#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sqlite3
import lmdb, pickle
import csv
from math import acos, cos, sin, radians
from heapq import heappop, heappush
from .classes import LmdbDataStore, Memo
from .functions import minutes
from .constants import getFieldType, getKStatement, getCreateTableOrder

BASEPATH = os.path.dirname(os.path.abspath(__file__))

class Model:
    
    class Config:
        def __init__(self):
            self.config = {
                'gtfs': '~',
                'lat': '48.8610',
                'lon': '2.3439',
                'r': '5.63'
            }
            self.path = os.path.dirname(os.path.realpath(__file__)) + '/../../config.txt'
            with open(self.path, 'r') as f:
                for line in f:
                    try: key, value = line.split('=')
                    except: continue
                    self.config[key] = value.replace('\n', '')
        
        def get(self, key): return self.config[key]

        def set(self, key, value):
            self.config[key] = value
            with open(self.path, 'w') as f:
                for key in self.config:
                    f.write(str(key) + '=' + str(self.config[key]) + '\n')

    class Workspace:
        def __init__(self, model, pathToFoler):
            self.path = pathToFoler + '/'
            self.model = model
        def containsFiles(self, files):
            for file in files:
                if not os.path.exists(self.path + file): return False
            return True
        def canBeUsedAsGTFS(self): return self.containsFiles(['routes.txt', 'trips.txt', 'stop_times.txt', 'stops.txt'])
        def isReady(self): return self.containsFiles(['gtfs.db', 'succ'])
        def create(self, lat, lon, r):
            self.model.controller.showLoading("Création de la base de données")

            db = sqlite3.connect(self.path + 'gtfs.db')
            db.execute('PRAGMA foreign_keys = ON') # Enables Foreign keys in SQLite
            
            # Create all used GTFS tables
            for tableName in getCreateTableOrder():
                if tableName == 'transfers' and not self.containsFiles(['transfers.txt']):
                    header = ['from_stop_id','to_stop_id','transfer_type','min_transfer_time']
                else:
                    with open('%s%s.txt' % (self.path, tableName), 'r', encoding = 'utf8') as f:
                        csvReader = csv.reader(f)
                        header = next(csvReader)
                fieldStatements = [ '%s %s' % (field, getFieldType(tableName, field)) for field in header ]
                db.execute('CREATE TABLE %s (%s);' % (tableName, ', '.join(fieldStatements + [getKStatement(tableName)])))
            
            db.commit()

            # Create tables used by the applciation
            db.execute('CREATE TABLE timetable ( \
                from_stop_id VARCHAR(30), \
                to_stop_id VARCHAR(30), \
                departure_time INT, \
                travel_time INT, \
                route_type INT, \
                trip_id VARCHAR(30) \
            );')

            db.execute('CREATE TABLE stops_routes ( \
                stop_id VARCHAR(30) REFERENCES stops(stop_id), \
                route_id VARCHAR(40) REFERENCES routes(route_id), \
                PRIMARY KEY (stop_id, route_id) \
            );')

            db.commit()
            
            # Import CSV files into SQLite
            def insertCSV(tableName, filter = lambda header, row : True):
                self.model.controller.showLoading("Importations des données : %s" % tableName)
                nInserted = 0
                with open('%s%s.txt' % (self.path, tableName), 'r', encoding = 'utf8') as f:
                    csvReader = csv.reader(f)
                    header = next(csvReader)
                    placeholders = '(?%s)' % (', ?' * (len(header) - 1) )
                    for line in csvReader:
                        if filter(header, line):
                            try:
                                db.execute("INSERT INTO %s VALUES %s" % (tableName, placeholders), tuple(line))
                                nInserted += 1
                            except sqlite3.IntegrityError as e: continue
                db.commit()
                print('Inserted : %s' % nInserted)
            
            if lat != None and lon != None and r != None:
                distance = lambda p1_lat,p1_long,p2_lat,p2_long : (6371*acos(cos(radians(p1_lat))*cos(radians(p2_lat))*cos(radians(p2_long)-radians(p1_long))+sin(radians(p1_lat))*sin(radians(p2_lat))))
                insertCSV('stops', lambda header, stop : distance(float(stop[header.index('stop_lat')]), float(stop[header.index('stop_lon')]), float(lat), float(lon)) <= float(r))
            else: insertCSV('stops')
            # FILTER ON ROUTE_TYPE : lambda header, route : int(route[header.index('route_type')]) in [1, 3]
            insertCSV('routes')
            insertCSV('trips')
            insertCSV('stop_times')
            if self.containsFiles(['transfers.txt']): insertCSV('transfers')

            # Create assoc between stops and routes
            self.model.controller.showLoading("Association des stops et des routes")
            cursor = db.cursor()
            cursor.execute("INSERT INTO stops_routes (stop_id, route_id)\
                            SELECT DISTINCT stops.stop_id, routes.route_id \
                            FROM stops, stop_times, trips, routes \
                            WHERE stops.stop_id = stop_times.stop_id \
                            AND trips.trip_id = stop_times.trip_id \
                            AND routes.route_id = trips.route_id \
            ")

            # Create timetable
            self.model.controller.showLoading("Remplissage de la timetable")
            cursor = db.cursor()
            cursor.execute("SELECT trips.trip_id, stop_times.departure_time, stop_times.stop_id, routes.route_type \
                        FROM routes, trips, stop_times, stops \
                        WHERE routes.route_id = trips.route_id \
                        AND trips.trip_id = stop_times.trip_id \
                        AND stops.stop_id = stop_times.stop_id \
                        -- AND stop_times.departure_time BETWEEN '08:00:00' AND '22:00:00' \
                        -- AND routes.route_type = 1 \
                        ORDER BY stop_times.trip_id, stop_times.departure_time \
                ")
            i = 0
            k = 0
            n = 10000
            memo = Memo(2)
            for row in cursor:
                memo.put(row)
                if memo.is_ready():
                    stoptime_1, stoptime_2 = memo.get()
                    # stop_time = trip_id, departure_time, stop_id, route_type
                    if stoptime_1[0] == stoptime_2[0]:
                        trip_id, departure_time, from_stop_id, route_type = stoptime_1
                        _, arrival_time, to_stop_id, _ = stoptime_2

                        departure_time = minutes(departure_time)
                        travel_time = minutes(arrival_time) - departure_time

                        db.execute('INSERT INTO timetable VALUES (?, ?, ?, ?, ?, ?)', (from_stop_id, to_stop_id, departure_time, travel_time, route_type, trip_id))

                        if i >= n:
                            i = 0
                            k += 1
                            print('Treated %s' % (k * n))

                        i += 1
            db.commit()

            # Add transfers
            self.model.controller.showLoading("Ajout des transfers à la timetable")
            db.execute("INSERT INTO timetable (from_stop_id, to_stop_id, departure_time, travel_time, route_type, trip_id) \
                        SELECT transfers.from_stop_id, transfers.to_stop_id, -1, transfers.min_transfer_time / 60, -1, -1 \
                        FROM transfers \
                ")
            db.commit()

            # Create successors' list
            self.model.controller.showLoading("Création de la liste des successeurs")
            cursor = db.cursor()
            cursor.execute("SELECT from_stop_id, to_stop_id, departure_time, travel_time, route_type FROM timetable ORDER BY from_stop_id, to_stop_id, departure_time, travel_time")

            memo = Memo(2)
            localStorage = LmdbDataStore('%s/succ' % self.path, dict())
            successors = {}
            for connection in cursor:
                memo.put(connection)
                if memo.is_ready():
                    connection1, connection2 = memo.get()
                    from_stop_id, to_stop_id, departure_time, travel_time, route_type = connection1
                    from_stop_id_next, _, _, _, _ = connection2
                    
                    if to_stop_id not in successors: successors[to_stop_id] = []
                    successors[to_stop_id].append( (departure_time, travel_time, route_type) )

                    if from_stop_id != from_stop_id_next:
                        localStorage.set(from_stop_id, successors)
                        successors = {}

            localStorage.txn.commit()
        def getPossibleModes(self):
            db = sqlite3.connect(self.path + 'gtfs.db')
            cursor = db.cursor()
            cursor.execute('SELECT DISTINCT route_type FROM timetable WHERE route_type != -1')
            return [ mode for mode, in cursor ]
        def getAllStops(self, modes):
            names, ids, lats, lons, types = [], [], [], [], []
            if modes == []: return names, ids, lats, lons, types
            db = sqlite3.connect(self.path + 'gtfs.db')
            cursor = db.cursor()
            modeCondition = ' OR '.join(map(lambda mode : 'route_type = %s' % mode, modes))
            cursor.execute("SELECT stop_name, stops.stop_id, stop_lat, stop_lon, route_type FROM stops, routes, stops_routes WHERE stops.stop_id = stops_routes.stop_id AND stops_routes.route_id = routes.route_id AND (%s) " % modeCondition)
            for stop_name, stop_id, stop_lat, stop_lon, route_type in cursor:
                names.append(stop_name)
                ids.append(stop_id)
                lats.append(stop_lat)
                lons.append(stop_lon)
                types.append(route_type)
            return names, ids, lats, lons, types
        def getStopsByStopIds(self, ids):
            db = sqlite3.connect(self.path + 'gtfs.db')
            cursor = db.cursor()
            names, lats, lons, types, rnames, rcols = [], [], [], [], [], []
            for stop_id in ids:
                cursor.execute("SELECT stop_name, stop_lat, stop_lon, route_type, route_short_name, route_color FROM stops, stops_routes, routes WHERE stops.stop_id = stops_routes.stop_id AND stops_routes.route_id = routes.route_id AND stops.stop_id = '%s'" % stop_id)
                stop_name, stop_lat, stop_lon, route_type, route_name, route_color = cursor.fetchone()
                names.append(stop_name)
                lats.append(stop_lat)
                lons.append(stop_lon)
                types.append(route_type)
                rnames.append(route_name)
                rcols.append(route_color)
            return names, ids, lats, lons, types, rnames, rcols
        def getFunctionSuccessorsByStopId(self, modes, withTimes = True):
            localStorage = LmdbDataStore('%s/succ' % self.path, dict())
            modes += [-1]
            
            if withTimes:
                def minValueFromStartTime(expanded, arrival_time):
                    arrival_time %= 24 * 60
                    stop_id, valuations = expanded
                    minimum = float('inf')
                    argmin = None
                    for departure_time, travel_time, route_type in valuations:
                        if route_type in modes:
                            if departure_time == -1: # C'est un transfer
                                minimum = arrival_time + travel_time
                            elif departure_time >= arrival_time and departure_time + travel_time < minimum:
                                minimum = departure_time + travel_time
                    return travel_time, stop_id, minimum
            else:
                def minValueFromStartTime(expanded, arrival_time):
                    stop_id, valuations = expanded
                    minimum = float('inf')
                    argmin = None
                    for departure_time, travel_time, route_type in valuations:
                        if route_type in modes:
                            if travel_time < minimum: minimum = travel_time
                    return minimum, stop_id, 0

            def voisins(stop_id, arrival_time):
                expanded = localStorage.get(stop_id).items()
                return sorted(map(lambda succ : minValueFromStartTime(succ, arrival_time), expanded))
            
            return voisins

    def __init__(self, controller):
        self.controller = controller
        self.config = self.Config()
        
        gtfs = self.config.get('gtfs')
        self.changeWorkspace(gtfs, True)

    def changeWorkspace(self, newWorkspace, confirm = False):
        while True:
            self.workspace = self.Workspace(self, newWorkspace)
            if self.workspace.canBeUsedAsGTFS(): break
            newWorkspace = self.controller.askNewWorkspace(newWorkspace, confirm)
            self.config.set('gtfs', newWorkspace)

        # Checks if workspace has already been initiated
        if not self.workspace.isReady() and self.controller.askInitWorkspace():
            lat, lon, r = self.config.get('lat'), self.config.get('lon'), self.config.get('r')
            lat, lon, r = self.controller.askInitWorkspaceParameters(lat, lon, r)
            self.workspace.create(lat, lon, r)

    def dijkstra(self, from_stop_id, departure_time_string, to_stop_id, modes):
        departure_time = 0 if departure_time_string == "" else minutes(departure_time_string)
        voisins = self.workspace.getFunctionSuccessorsByStopId(modes, not not departure_time)

        M = set()
        d = { from_stop_id: 0 }
        t = { from_stop_id: departure_time }
        p = {}
        suivants = [(0, from_stop_id, departure_time)] # tas de couples (d[x],x,tau)

        while suivants != []:

            opt_travel_time, curr_stop, arrival_time = heappop(suivants)
            if curr_stop in M: continue

            M.add(curr_stop)

            for travel_time, next_stop, next_departure_time in voisins(curr_stop, arrival_time):
                if next_stop in M: continue
                if next_departure_time == float('inf'): continue
                dy = opt_travel_time + travel_time
                if next_stop not in d or d[next_stop] > dy:
                    d[next_stop] = dy
                    heappush(suivants, (dy, next_stop, next_departure_time))
                    p[next_stop] = curr_stop
                    t[next_stop] = next_departure_time

        try:
            stop_ids = [to_stop_id]
            stop_times = [t[to_stop_id]]
            x = to_stop_id
            while x != from_stop_id:
                x = p[x]
                stop_ids.insert(0, x)
                stop_times.insert(0, t[x])
        except:
            return self.controller.showError("Les deux noeuds ne sont pas connexe")

        return stop_ids, stop_times
