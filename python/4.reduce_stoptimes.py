import csv

stops_file = open('./csv/2.stops_sorted.csv', 'r');
stoptimes_file = open('./csv/3.stoptimes_sorted.csv', 'r');
out_file = open('./csv/4.stoptimes_reduced.csv', 'w');

stops_reader = csv.DictReader(stops_file);
stoptimes_reader = csv.DictReader(stoptimes_file);
out_writer = csv.writer(out_file);

out_writer.writerow( ('stop_id', 'stop_name', 'trip_id', 'arrival_time', 'departure_time') )

curr_stop = stops_reader.next();
curr_stoptime = stoptimes_reader.next();

while True:
    if curr_stop['stop_id'] == curr_stoptime['stop_id']:
        out_writer.writerow( (curr_stop['stop_id'], curr_stop['stop_name'], curr_stoptime['trip_id'], curr_stoptime['arrival_time'], curr_stoptime['departure_time']) );
        try:
            # one-one correspondance
            curr_stoptime = stoptimes_reader.next();
            curr_stop = stops_reader.next();
        except:
            break;
    elif curr_stop['stop_id'] > curr_stoptime['stop_id']:
        try:
            curr_stoptime = stoptimes_reader.next();
        except:
            break;
    else:
        try:
            curr_stop = stops_reader.next();
        except:
            break;

stops_file.close();
stoptimes_file.close();
out_file.close();