import csv, operator, sys

trips_src_file = open('../gtfs/stop_times.txt', 'r')
trips_src_reader = csv.DictReader(trips_src_file)

sortedlist = sorted(trips_src_reader, key = lambda x: (x['trip_id'], x['departure_time']))

trip_sort_file = open('./result/Trips.csv', 'w')
trip_sort_writer = csv.writer(trip_sort_file)

trip_dict = {}
for row in sortedlist:
    trip_id = row['trip_id']
    if trip_id not in trip_dict.keys():
        trip_sort_writer.writerow(trip_dict.keys())
        trip_sort_writer.writerow(trip_dict.values())
        trip_dict = {}
        trip_dict[trip_id] = [row['stop_id']]
    else:
        trip_dict[trip_id].append(row['stop_id'])

trip_sort_writer.writerows(trip_dict)
trip_sort_file.close()
trips_src_file.close()
