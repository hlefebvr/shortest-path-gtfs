#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from os import listdir;

def add_minute(h, m):
    def bind_zero(n):
        n = int(n);
        return str(n) if n >= 10 else '0' + str(n);
    hh, mm, _ = h.split(':');
    hh = int(hh);
    mm = int(mm)
    r = mm + m
    return bind_zero( hh + r / 60  ) + ':' + bind_zero( r % 60 );

class IteratorWithMemo:
    def __init__(self, iterator):
        self.it = iterator;
        self.memo = None;
    def __iter__(self):
        self.it.__iter__();
        self.memo = None;
        return self;
    def __next__(self):
        self.memo = self.it.__next__();
        return self.memo;
    def current(self):
        return self.memo;

class StopTimeIterator:
    def __init__(self, params):
        self.index = 0;
        self.start_time, self.time, self.space, self.n = params;
    
    def __iter__(self):
        self.index = 0;
        return self;
    
    def __next__(self):
        if self.index == self.n:
            raise StopIteration;
        stoptime = add_minute(self.start_time, self.index * (self.time + self.space));
        self.index += 1;
        return (stoptime, self.time);

class SubGraphArcIterator:
    def __init__(self, graph):
        self.graph = graph;
        self.stoptimes_it = None;
        self.compressed_stoptimes_it = None;
        self.predecessors_it = None;
        self.node_it = IteratorWithMemo(iter(graph));
    
    def __iter__(self):
        return self;
    
    def log(self):
        def pr(str):
            print(str, end='')
        logs = [ self.node_it, self.predecessors_it, self.compressed_stoptimes_it, self.stoptimes_it ]
        pr('>>> ')
        for l in logs:
            pr(' ');
            try:
                pr( l.current() );
            except:
                pr( None );
            pr(' ');
        print('');
    
    def __next__(self):
        # self.log();
        try: # on lit le prochain stoptimes dans les compressed
            
            self.stoptimes_it.__next__();

        except: # fin des stoptimes dans le [compressed]
            
            try:
                self.stoptimes_it = IteratorWithMemo( StopTimeIterator( self.compressed_stoptimes_it.__next__() ) );
                return self.__next__();
                
            except: # fin  des compressed stoptimes
            
                try: # on lit le prochain compressed stoptimes params

                    self.predecessors_it.__next__()
                    compressed_stoptimes = self.graph[ self.node_it.current() ][ self.predecessors_it.current() ];
                    self.compressed_stoptimes_it = IteratorWithMemo( iter( compressed_stoptimes ) );
                    return self.__next__();
                
                except: # on est à la fin des predecesseurs

                    self.predecessors_it = IteratorWithMemo( iter( self.graph[ self.node_it.__next__() ]) );
                    self.__next__();

        departure_time, travel_time = self.stoptimes_it.current();
        return ( self.predecessors_it.current(), self.node_it.current(), departure_time, travel_time );

class SubGraphIterator:
    def __init__(self, folder):
        self.folder = folder;
        self.index = 0;
        self.files = listdir(folder);
        self.max = len(self.files);
    def __iter__(self):
        self.index = 0;
        return self;
    def __next__(self):
        if self.index == self.max:
            raise StopIteration;
        file_reader = open( self.folder + '/' + self.files[self.index] , 'r');
        subgraph = eval( file_reader.read().replace('null', 'None') );
        file_reader.close();
        self.index += 1;
        return subgraph;
    def get_n(self):
        n = 0;
        for f in self.files:
            file_reader = open( self.folder + '/' + f , 'r');
            tmp = eval( file_reader.read().replace('null', 'None') );
            file_reader.close();
            n += len(tmp);
            del tmp;
        return n

class GraphArcIterator:

    def __init__(self, folder):
        self.folder = folder;
        self.subgraph_it = SubGraphIterator(folder);
        self.subgraph_arc_it = None;

    def __iter__(self):
        self.__init__(self.folder);
        return self;

    def __next__(self):
        try:
            return self.subgraph_arc_it.__next__();
        except:
            self.subgraph_arc_it = SubGraphArcIterator( self.subgraph_it.__next__() );
            return self.__next__();
    
    def __len__(self):
        return self.subgraph_it.get_n();
