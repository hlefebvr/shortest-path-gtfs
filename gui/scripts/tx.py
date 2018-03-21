from csvsort import csvsort;
from math import sin, cos, sqrt, atan2, radians;
import csv;
from datetime import datetime;
import tkMessageBox;
import time;

def distance_to_center(lat, lon):
    R = 6373.0 # approximate radius of earth in km
    ref_lat = radians(48.8610)
    ref_lon = radians(2.3439)
    dlon = lon - ref_lon
    dlat = lat - ref_lat
    a = sin(dlat / 2)**2 + cos(ref_lat) * cos(lat) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c;

def diff_h(h1, h2):
    def to_ms(str_hour):
        hms = str_hour.split(':');
        return int(hms[0]) * 3600 + int(hms[1]) * 60 + int(hms[2]);
    def to_minutes(int_sec):
        return int_sec / 60
    ms1 = to_ms(h1);
    ms2 = to_ms(h2);
    delta = abs(ms1 - ms2);
    return to_minutes(delta);

def start(folder, treeView, start_at):
    start_time = time.time();
    stepItemIds = treeView.get_children();
    def setStepStatus(step_n, status):
        itemId = stepItemIds[step_n - 1];
        treeView.set(itemId, column="status", value=status);
        treeView.update();
    
    # Sorting stop_times by stop_id
    if start_at <= 1:
        setStepStatus(1, '...');
        csvsort(folder+'/stop_times.txt', [3], output_filename='./tmp/1.stoptimes_sorted.csv', has_header=True);
        setStepStatus(1, 'OK');
    else:
        setStepStatus(1, 'OK');
    
    # Sorting stops by stop_id
    if start_at <= 2:
        setStepStatus(2, '...');
        csvsort(folder+'/stops.txt', [0], output_filename='./tmp/2.stops_sorted.csv', has_header=True);
        setStepStatus(2, 'OK');
    else:
        setStepStatus(2, 'OK');
    
    # Sorting trips by route_id
    if start_at <= 3:
        setStepStatus(3, '...');
        csvsort(folder+'/trips.txt', [0], output_filename='./tmp/3.trips_sorted.csv', has_header=True);
        setStepStatus(3, 'OK');
    else:
        setStepStatus(3, 'OK');
    
    # Removing stops which are too far
    if start_at <= 4:
        setStepStatus(4, '...');
        
        stops_src_file = open('./tmp/2.stops_sorted.csv', 'r')
        stops_src_reader = csv.DictReader(stops_src_file)

        stops_center_file = open('./tmp/4.stops_center.csv', 'w')
        stops_center_writer = csv.writer(stops_center_file)

        stops_center_writer.writerow( ('stop_id', 'stop_name') );
        for row in stops_src_reader:
            stop_lat = radians(float(row['stop_lat']))
            stop_lon = radians(float(row['stop_lon']))
            dist = distance_to_center( stop_lat, stop_lon )
            if dist <= 5.63:
                curr_stop_id = row['stop_id']
                stops_center_writer.writerow( (curr_stop_id, row['stop_name']) );

        stops_src_file.close();
        stops_center_file.close();

        setStepStatus(4, 'OK');
    else:
        setStepStatus(4, 'OK');
    
    # Removing stop_times not related to relevant stops
    if start_at <= 5:
        setStepStatus(5, '...');
        
        stops_file = open('./tmp/4.stops_center.csv', 'r');
        stoptimes_file = open('./tmp/1.stoptimes_sorted.csv', 'r');
        out_file = open('./tmp/5.stoptimes_reduced.csv', 'w');

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
                    curr_stoptime = stoptimes_reader.next();
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

        setStepStatus(5, 'OK');
    else:
        setStepStatus(5, 'OK');
    
    # Removing routes regarding to the transport type
    if start_at <= 6:
        setStepStatus(6, '...');

        modes = ['1', '2', '3'] # METRO, TRAIN, BUS

        routes_read_file = open(folder+'/routes.txt', 'r');
        routes_reader = csv.DictReader(routes_read_file);

        routes_write_file = open('./tmp/6.routes_reduced.csv', 'w');
        routes_writer = csv.writer(routes_write_file);

        routes_writer.writerow( ('route_id', 'route_type') )

        for route in routes_reader:
            if (route['route_type'] in modes):
                routes_writer.writerow( (route['route_id'], route['route_type']) );

        routes_read_file.close();
        routes_write_file.close();

        setStepStatus(6, 'OK');
    else:
        setStepStatus(6, 'OK');
    
    # Sort resulted routes by route_id
    if start_at <= 7:
        setStepStatus(7, '...');
        csvsort('./tmp/6.routes_reduced.csv', [0], output_filename='./tmp/7.routes_sorted.csv', has_header=True);
        setStepStatus(7, 'OK');
    else:
        setStepStatus(7, 'OK');

    # Remove trips not linked to resulted routes
    if start_at <= 8:
        setStepStatus(8, '...');
        
        trips_file = open('./tmp/3.trips_sorted.csv', 'r');
        routes_file = open('./tmp/7.routes_sorted.csv', 'r');
        out_file = open('./tmp/8.trips_reduced.csv', 'w');

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

        setStepStatus(8, 'OK');
    else:
        setStepStatus(8, 'OK');
    
    # Sort stoptimes by trip_id
    if start_at <= 9:
        setStepStatus(9, '...');
        csvsort('./tmp/5.stoptimes_reduced.csv', [2,3], output_filename='./tmp/9.stoptimes_sorted.csv', has_header=True);
        setStepStatus(9, 'OK');
    else:
        setStepStatus(9, 'OK');
    
    # Sort trips by trip_id
    if start_at <= 10:
        setStepStatus(10, '...');
        csvsort('./tmp/8.trips_reduced.csv', [0], output_filename='./tmp/10.trips_sorted.csv', has_header=True);
        setStepStatus(10, 'OK');
    else:
        setStepStatus(10, 'OK');
    
    # Remove stoptimes not related to resulted trips
    if start_at <= 11:
        setStepStatus(11, '...');
        
        trips_file = open('./tmp/10.trips_sorted.csv', 'r');
        stoptimes_file = open('./tmp/9.stoptimes_sorted.csv', 'r');
        out_file = open('./tmp/11.stoptimes_reduced.csv', 'w');

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

        setStepStatus(11, 'OK');
    else:
        setStepStatus(11, 'OK');
    
    # Generate immediate successor list
    if start_at <= 12:
        setStepStatus(12, '...');

        stoptimes_src_file = open('./tmp/11.stoptimes_reduced.csv', 'r');
        successors_dest_file = open('./tmp/12.successors_redondant.csv', 'w');

        stoptimes_reader = csv.DictReader(stoptimes_src_file);
        successors_writer = csv.writer(successors_dest_file);

        successors_writer.writerow( ("stop_id", "successor_id", "stop_name", "successor_name", "duration", "departure_time") );

        curr_stoptimes = stoptimes_reader.next();

        while True:
            try:
                second_stoptimes = stoptimes_reader.next();
            except:
                break;
            if curr_stoptimes['trip_id'] == second_stoptimes['trip_id']:
                delta_h = diff_h(curr_stoptimes['departure_time'], second_stoptimes['arrival_time']);
                successors_writer.writerow( (curr_stoptimes['stop_id'], second_stoptimes['stop_id'], curr_stoptimes['stop_name'], second_stoptimes['stop_name'], delta_h, curr_stoptimes['departure_time']) );
            curr_stoptimes = second_stoptimes;

        stoptimes_src_file.close();
        successors_dest_file.close();

        setStepStatus(12, 'OK');
    else:
        setStepStatus(12, 'OK');

    # Sort resulted successor list by stop_id
    if start_at <= 13:
        setStepStatus(13, '...');
        csvsort('./tmp/12.successors_redondant.csv', [0], output_filename='./tmp/13.successors_redondant_sorted.csv', has_header=True);
        setStepStatus(13, 'OK');
    else:
        setStepStatus(13, 'OK');
    
    # aggregate csv by stop_id
    if start_at <= 14:
        setStepStatus(14, '...');
        
        redondant_src_file = open('./tmp/13.successors_redondant_sorted.csv','r');
        aggregated_output = open('./tmp/14.successors_list.csv', 'w');
        redondant_reader = csv.DictReader(redondant_src_file);
        aggregated_writer = csv.writer(aggregated_output);

        aggregated_writer.writerow( ('stop_id', 'stop_name', 'successors') );

        def getCouple(stoptime):
            return "("+curr_stoptimes['successor_id']+"/"+curr_stoptimes['successor_name']+"/"+curr_stoptimes['duration']+"/"+curr_stoptimes['departure_time']+")";
        def initRow(stoptime):
            return ( curr_stoptimes['stop_id'], curr_stoptimes['stop_name'] );

        curr_stoptimes = redondant_reader.next();
        curr_list = initRow(curr_stoptimes);
        n_succ = 0;
        global_n_edge = 0;
        global_n_node = 0;
        while True:
            try:
                second_stoptimes = redondant_reader.next();
            except:
                break;
            if (curr_stoptimes['stop_id'] == second_stoptimes['stop_id']):
                curr_list = curr_list + (getCouple(curr_stoptimes),);
                n_succ = n_succ + 1;
            else:
                aggregated_writer.writerow( curr_list );
                curr_list = initRow(second_stoptimes);
                global_n_edge = global_n_edge + n_succ;
                global_n_node = global_n_node + 1;
                n_succ = 0;
            curr_stoptimes = second_stoptimes;

        print 'Total number of edges : ', global_n_edge
        print 'Total number of nodes : ', global_n_node
        print 'Average number of successors : ', global_n_edge / global_n_node

        redondant_src_file.close();
        aggregated_output.close();

        setStepStatus(14, 'OK');
    else:
        setStepStatus(14, 'OK');
    
    execution_time = time.time() - start_time;
    tkMessageBox.showinfo("Execution finished", "The execution has terminated in "+str(execution_time)+" seconds");