class IteratorIterator():
    def __init__(self, iterators, _filter = lambda _ : True):
        self.list = iterators
        self.filter = _filter
    
    def __iter__(self):
        n = len(self.list)
        for i in range(n):
            self.list[i] = iter(self.list[i])
        return self
    
    def __next__(self):
        for iterator in self.list:
            for value in iterator:
                if self.filter(value):
                    return value
        raise StopIteration

import lmdb, pickle

env = lmdb.open('../gtfs/stops')
txn = env.begin()
cursor = txn.cursor()

env2 = lmdb.open('../gtfs/stops')
txn2 = env2.begin()
cursor2 = txn2.cursor()

def read_lmdb(item): return pickle.loads(item[0]), pickle.loads(item[1])

queue = IteratorIterator([cursor, cursor2], lambda item: int(read_lmdb(item)[1]['route_type']) in [1, 2] )
for x in queue:
    key, value = read_lmdb(x)
    print(key, value)
