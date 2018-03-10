import csv

trips_file = open('./csv/6.trips_sorted.csv', 'r');
routes_file = open('./csv/7.routes_sorted.csv', 'r');
out_file = open('./csv/8.trips_reduced.csv', 'w');

trips_reader = csv.DictReader(trips_file);
routes_reader = csv.DictReader(routes_file);
out_writer = csv.writer(out_file);

out_writer.writerow( ('trip_id', 'route_id') )

curr_trip = trips_reader.next();
curr_route = routes_reader.next();

while True:
    if curr_trip['route_id'] == curr_route['route_id']:
        out_writer.writerow( (curr_trip['trip_id'], curr_route['route_id']) );
        try:
            curr_trip = trips_reader.next();
        except:
            break;
    elif curr_trip['route_id'] > curr_route['route_id']:
        try:
            curr_route = routes_reader.next();
        except:
            break;
    else:
        try:
            curr_trip = trips_reader.next();
        except:
            break;

trips_file.close();
routes_file.close();
out_file.close();