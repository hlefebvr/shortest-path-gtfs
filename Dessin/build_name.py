import csv
import json

file_reader = open('../gui/tmp/14.successors_list.csv','r');
csv_reader = csv.reader(file_reader);

line = csv_reader.next(); # skip header

G = {};

def get_successors_unique():
    return [];

while True:
    try:
        line = csv_reader.next();
    except:
        break;
    successors_unique = [];
    i = 2;
    while True:
        try:
            fields = line[i][1:-1].split('/');
        except:
            break;
        i = i + 1;
        stop_name = fields[1];
        try:
            dist = int(fields[2]);
        except:
            continue;
        if (dist, stop_name) not in successors_unique:
            successors_unique.append((dist, stop_name));
    try:
        G[line[1]] = G[line[1]] + successors_unique;
    except:
        G[line[1]] = successors_unique;

file_reader.close();
import pdb; pdb.set_trace()
with open('dict_name.txt', 'w') as file:
    file.write(json.dumps(G))
