import itertools


modes = ['metro', 'train', 'bus']
n = len(modes)

for model in ['time_expanded', 'condensed', 'alpha_beta']:
    for i in range(n + 1):
        parts = list(itertools.combinations(modes, i))
        for p in parts:
            string = '-'.join(p)
            print "'" + model + \
                ('-' if string != '' else '') + string + ".txt',"
