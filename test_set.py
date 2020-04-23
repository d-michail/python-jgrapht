#!/usr/bin/env python3

import jgrapht.util as util

s = util.JGraphTLongSet()
s.add(100)
s.add(200)
s.add(300)
s.remove(200)
print(len(s))
print(list(s))
print(100 not in s)
print(100 in s)

