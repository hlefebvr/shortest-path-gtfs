import csv

with open('../gtfs/stops.txt', 'r') as f:
    reader = csv.reader(f)
    print(reader.__next__())
