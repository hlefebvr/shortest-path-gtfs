import csv

def get_number_line(path):
    file = open(path, 'r');
    reader = csv.reader(file);
    n = 0;
    for row in reader: n = n + 1;
    file.close();
    return n;

def get_variation(start, end):
    return float(end - start) / float(start) * 100;

nl_src_stops = get_number_line('../gtfs/stops.txt');
nl_first_stops = get_number_line('./csv/1.stops_center.csv');

print('1. Reducing number of stops (keeping ones in the heart of Paris) : ' + format(get_variation(nl_src_stops, nl_first_stops), '.2f') + ' % number of stops');
print('\tNumber of stops : ' + str(nl_first_stops) + '/' + str(nl_src_stops));

print('2. Sorting stops by stop_id');
print('3. Sorting stop_times by stop_id');

nl_src_stoptimes = get_number_line('../gtfs/stop_times.txt');
nl_fourth_stoptimes = get_number_line('./csv/4.stoptimes_reduced.csv');

print('4. Removing stop_times not related to releveant stops : ' + format(get_variation(nl_src_stoptimes, nl_fourth_stoptimes), '.2f') + ' % number of stoptimes');
print('\tNumber of stop_times : ' + str(nl_fourth_stoptimes) + '/' + str(nl_src_stoptimes));

nl_src_routes = get_number_line('../gtfs/routes.txt');
nl_fifth_routes = get_number_line('./csv/5.routes_reduced.csv');

print('5. Reducing number of routes (keeping ones by bus, subway, train) : ' + format(get_variation(nl_src_routes, nl_fifth_routes), '.2f') + ' % number of routes');
print('\tNumber of routes : ' + str(nl_fifth_routes) + '/' + str(nl_src_routes));

print('6. Sorting trips by route_id');
print('7. Sorting routes by route_id');

nl_src_trips = get_number_line('../gtfs/trips.txt');
nl_eighth_trips = get_number_line('./csv/8.trips_reduced.csv');

print('8. Reducing number of trips (keeping ones linked to routes found at step 5) : ' + format(get_variation(nl_src_trips, nl_eighth_trips), '.2f') + ' % number of trips');
print('\tNumber of trips : ' + str(nl_eighth_trips) + '/' + str(nl_src_trips));

print('9. Sorting stoptimes by trip_id');
print('10. Sorting trips by trip_id');

nl_nineth_stoptimes = get_number_line('./csv/11.stoptimes_reduced.csv');

print('11. Reducing number of stoptimes (keeping ones linked to trips found at step 8)' + format(get_variation(nl_fourth_stoptimes, nl_nineth_stoptimes), '.2f') + '% number of stoptimes');
print('\tNumber of stoptimes : '  + str(nl_nineth_stoptimes) + '/' + str(nl_fourth_stoptimes) + '/' + str(nl_src_stoptimes));