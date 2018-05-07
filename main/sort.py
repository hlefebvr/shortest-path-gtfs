import csv

file = open('./data_generation/output/arcs.csv')
# file = open('./test.csv')

line = file.readline()

for line in file:
    print line,

file.close()
