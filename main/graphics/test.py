import matplotlib.pyplot as plt;
import csv;
from math import cos, sin, radians;

stops_file_reader = open('../data_generation/tmp/stops_heart.csv', 'r');
stops_csv_reader = csv.DictReader(stops_file_reader);

succ_list = eval ( open('../data_generation/output/graph.json', 'r').read() );
id2name = eval ( open('../data_generation/output/id2name.json', 'r').read() );
coord = {};

def isMetro(node):
    try:
        node_type = id2name[node][1];
        return node_type == 'Metro';
    except:
        return False;

for stop in stops_csv_reader:
    if isMetro(stop['stop_id']):
        R = 6373.0 # approximate radius of earth in km
        lat = radians(float(stop['stop_lat']))
        lon = radians(float(stop['stop_lon']))
        x = R * cos(lat) * cos(lon)
        y = R * cos(lat) * sin(lon)
        coord[stop['stop_id']] = (x,y);
        plt.plot(x, y, 'ro', markersize = 5);

def getShowParam(x,y):
    transfer_style = {
        'color': '#000000',
        'dashes': [1,1]
    };
    try:
        info_x = id2name[x];
        info_y = id2name[y];
    except:
        return transfer_style;
    if info_x[2] == info_y[2]:
        return {
            'color': '#' + info_x[3],
            'dashes': [],
        };
    else:
        return transfer_style;

for x in succ_list:
    if isMetro(x):
        for d, y in succ_list[x]:
            if isMetro(y):
                cx = coord[x];
                try:
                    cy = coord[y];
                except:
                    continue;
                param = getShowParam(x,y);
                plt.plot([cx[0], cy[0]], [cx[1], cy[1]], color=param['color'], dashes=param['dashes']);

stops_file_reader.close();

plt.show();