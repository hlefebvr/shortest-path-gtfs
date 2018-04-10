#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from csvsort import csvsort;
import csv;
import os;
from util.distances import distance_to_center;

BASE_PATH = os.path.dirname(os.path.realpath(__file__)) + '/';

# supposing file2 has FK to file1 (file2 rows may be unreferenced in file1)
def join_csv_on(file1, keys1, file2, keys2, output_file, sort_file1 = True, sort_file2 = True):
    # sorting file1
    csvsort(BASE_PATH + file1, keys1, output_filename=BASE_PATH + './tmp/file1.sorted', has_header=True);
    # sorting file2
    csvsort(BASE_PATH + file2, keys2, output_filename=BASE_PATH + './tmp/file2.sorted', has_header=True);
    # merging
    file1_reader = open(BASE_PATH + './tmp/file1.sorted', 'r');
    file2_reader = open(BASE_PATH + './tmp/file2.sorted', 'r');
    output_writer = open(BASE_PATH + output_file, 'w');
    file1_csv_reader = csv.reader(file1_reader);
    file2_csv_reader = csv.reader(file2_reader);
    output_csv_writer = csv.writer(output_writer);

    header1 = file1_csv_reader.next();
    header2 = file2_csv_reader.next();
    del header2[keys2[0]];
    output_csv_writer.writerow( header1 + header2 );

    line_from_file1 = file1_csv_reader.next();
    line_from_file2 = file2_csv_reader.next();

    while True:
        if line_from_file1[keys1[0]] < line_from_file2[keys2[0]]:
            try:
                line_from_file1 = file1_csv_reader.next();
                continue;
            except:
                break;
        if line_from_file1[keys1[0]] == line_from_file2[keys2[0]]:
            del line_from_file2[keys2[0]];
            output_csv_writer.writerow( line_from_file1 + line_from_file2 );
        try:
            line_from_file2 = file2_csv_reader.next();
        except:
            break;

    file1_reader.close();
    file2_reader.close();
    output_writer.close();

    # removing tepporary files
    os.remove(BASE_PATH + './tmp/file1.sorted');
    os.remove(BASE_PATH + './tmp/file2.sorted');

def reduce_stops(stopsfile, outut_file):
    file_reader = open(BASE_PATH + stopsfile, 'r');
    file_csv_reader = csv.reader(file_reader);

    output_file_writer = open(BASE_PATH + outut_file, 'w');
    output_csv_writer = csv.writer(output_file_writer);

    header = file_csv_reader.next();
    output_csv_writer.writerow(header);

    for row in file_csv_reader:
        stop_lat = row[3];
        stop_lon = row[4];
        dist = distance_to_center( stop_lat, stop_lon );
        if dist <= 5.63:
            output_csv_writer.writerow( row );

    file_reader.close();
    output_file_writer.close();

print "Reducing stops..."
reduce_stops('../../gtfs/stops.txt', './tmp/stops_heart.csv');

print "Merging stops and stoptimes..."
join_csv_on('./tmp/stops_heart.csv', [0], '../../gtfs/stop_times.txt', [3], './tmp/timetable.csv');
os.remove(BASE_PATH + './tmp/stops_heart.csv');

print "Merging result with trips..."
join_csv_on('../../gtfs/trips.txt', [2], './tmp/timetable.csv', [10], './tmp/timetable2.csv');
os.remove(BASE_PATH + './tmp/timetable.csv');

print "Merging result with routes..."
join_csv_on('../../gtfs/routes.txt', [0], './tmp/timetable2.csv', [0], './tmp/timetable.csv');
os.remove(BASE_PATH + './tmp/timetable2.csv');

print "Sorting timetable by trip id and departure time"
csvsort(BASE_PATH + './tmp/timetable.csv', ['trip_id', 'departure_time'], output_filename=BASE_PATH + './output/timetable.csv', has_header=True);
os.remove(BASE_PATH + './tmp/timetable.csv');