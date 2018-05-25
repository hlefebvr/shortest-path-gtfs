#!/usr/bin/python3
# -*- coding: utf-8 -*-

import lmdb, pickle

class LmdbDataStore:
    def __init__(self, path, default_value = None):
        self.default_value = default_value
        self.path = path
        try: os.remove(self.path)
        except: pass
        self.env = lmdb.open(self.path, map_size=int(1e9))
        self.txn = self.env.begin(write = True)

    def get(self, key):
        try:
            key = pickle.dumps(key)
            value = pickle.loads(self.txn.get(key))
        except: return self.default_value
        return value if value is not None else self.default_value
    
    def set(self, key, value):
        key = pickle.dumps(key)
        value = pickle.dumps(value)
        self.txn.put(key, value)

class Memo:
    def __init__(self, mem_size):
        self._mem_size = mem_size
        self._index = 0
        self._memo = [None] * mem_size
        self._is_ready = False

    def put(self, x):
        self._memo[self._index] = x
        self._index = (self._index + 1) % self._mem_size
        if self._index == 0:
            self._is_ready = True

    def get(self):
        values = []
        for offset in range(0, self._mem_size):
            values.append(self._memo[(self._index + offset) % self._mem_size])
        return values

    def is_ready(self):
        return self._is_ready
