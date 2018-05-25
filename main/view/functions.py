#!/usr/bin/python3
# -*- coding: utf-8 -*-

def str0(n): return str(n) if n > 9 else '0%s' % n

def strh(t): return '%s:%s' % ( str0(int(t/60)), str0(t % 60) )
