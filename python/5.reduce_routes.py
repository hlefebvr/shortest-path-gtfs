import csv;

METRO='1'
TRAIN='2'
BUS='3'

routes_read_file = open('../gtfs/routes.txt', 'r');
routes_reader = csv.DictReader(routes_read_file);

routes_write_file = open('./csv/5.routes_reduced.csv', 'w');
routes_writer = csv.writer(routes_write_file);

routes_writer.writerow( ('route_id', 'route_type') )

for route in routes_reader:
    if (route['route_type'] == METRO or route['route_type'] == TRAIN or route['route_type'] == BUS):
        routes_writer.writerow( (route['route_id'], route['route_type']) );

routes_read_file.close();
routes_write_file.close();
