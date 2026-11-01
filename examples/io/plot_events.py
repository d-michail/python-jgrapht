"""
Streaming a file as events
==========================

Process a large file without building a graph in memory.
"""

# %%
# The event importers report vertices, edges and attributes as the document is read. This DIMACS
# file declares its size first.

import jgrapht as jg

document = "p edge 4 3\ne 1 2\ne 2 3\ne 3 4\n"

# %%
# Without a callback the events are returned as a list of tuples.

for event in jg.parse_events(document, "dimacs"):
    print(event)

# %%
# With a callback each event is handled as it is read. Here we count the degrees.

degree = {}

def count(event):
    if event[0] == "edge":
        for v in event[1][:2]:
            degree[v] = degree.get(v, 0) + 1

jg.parse_events(document, "dimacs", callback=count)
print(degree)
