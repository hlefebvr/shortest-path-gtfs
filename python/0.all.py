print('1. Reducing number of stops (keeping ones in the heart of Paris)');
execfile('1.reduce_stops.py')

print('2. Sorting stops by stop_id')
execfile('2.sort_stops.py')

print('3. Sorting stop_times by stop_id')
execfile('3.sort_stoptimes.py')

print('4. Removing stop_times not related to releveant stops')
execfile('4.reduce_stoptimes.py')

print('5. Reducing number of routes (keeping ones by bus, subway, train)')
execfile('5.reduce_routes.py')

print('6. Sorting trips by route_id')
execfile('6.sort_trips.py')

print('7. Sorting routes by route_id')
execfile('7.sort_routes.py')

print('8. Reducing number of trips (keeping ones linked to routes found at step 5)')
execfile('8.reduce_trips.py')

print('9. Sorting stoptimes by trip_id')
execfile('9.sort_stoptimes.py')

print('10. Sorting trips by trip_id')
execfile('10.sort_trips.py')

print('11. Reducing number of stoptimes (keeping ones linked to trips found at step 8)')
execfile('11.reduce_stoptimes.py')

print('--------------------------')
execfile('n.stats.py')