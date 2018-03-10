import csv

trips_file = open('./csv/10.trips_sorted.csv', 'r');
stoptimes_file = open('./csv/9.stoptimes_sorted.csv', 'r');
out_file = open('./csv/11.stoptimes_reduced.csv', 'w');

trips_reader = csv.DictReader(trips_file);
stoptimes_reader = csv.DictReader(stoptimes_file);
out_writer = csv.writer(out_file);

out_writer.writerow( ('stop_id', 'stop_name', 'trip_id', 'route_id', 'arrival_time', 'departure_time') )

curr_trip = trips_reader.next();
curr_stoptimes = stoptimes_reader.next();

while True:
    if curr_trip['trip_id'] == curr_stoptimes['trip_id']:
        out_writer.writerow( ( curr_stoptimes['stop_id'], curr_stoptimes['stop_name'], curr_stoptimes['trip_id'], curr_trip['route_id'], curr_stoptimes['arrival_time'], curr_stoptimes['departure_time'] ) );
        try:
            curr_stoptimes = stoptimes_reader.next();
        except:
            break;
    elif curr_trip['trip_id'] > curr_stoptimes['trip_id']:
        try:
            curr_stoptimes = stoptimes_reader.next();
        except:
            break;
    else:
        try:
            curr_trip = trips_reader.next();
        except:
            break;

trips_file.close();
stoptimes_file.close();
out_file.close();