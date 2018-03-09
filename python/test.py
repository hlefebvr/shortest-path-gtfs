from distance_to_center import distance_to_center
from math import radians
import csv

stops_file = open('../gtfs/stops.txt', 'r')
stops_reader = csv.DictReader(stops_file)

for row in stops_reader:
    stop_lat = radians(float(row['stop_lat']))
    stop_lon = radians(float(row['stop_lon']))
    dist = distance_to_center( stop_lat, stop_lon )
    if dist <= 5.63:
        print row

stops_file.close();