# -*- coding: utf-8 -*-

"""
Importing a Sparse Graph
========================

In this example we import an input file into a sparse graph and execute a greedy 
coloring algorithm.
"""

# %%
# Start by importing the package

import jgrapht
import jgrapht.io.edgelist as edgelist


# %%
# A sparse graph can be constructed from edge lists. Assume we would like to 
# read the following graph which is in gexf format.

input_graph=r"""<?xml version="1.0" encoding="UTF-8"?><gexf xmlns="http://www.gexf.net/1.2draft" xsi:schemaLocation="http://www.gexf.net/1.2draft http://www.gexf.net/1.2draft/gexf.xsd" version="1.2" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <graph defaultedgetype="directed">
        <nodes>
            <node id="v0" label="0"/>
            <node id="v1" label="1"/>
            <node id="v2" label="2"/>
            <node id="v3" label="3"/>
            <node id="v4" label="3"/>
        </nodes>
        <edges>
            <edge id="e0" source="v0" target="v1"/>
            <edge id="e1" source="v0" target="v2"/>
            <edge id="e2" source="v0" target="v3"/>
            <edge id="e3" source="v2" target="v3"/>
            <edge id="e4" source="v3" target="v4"/>
        </edges>
    </graph>
</gexf>
"""

# %%
# We use the edge list importers to get the graph into an edge list. 
# 

edges = edgelist.parse_edgelist_gexf(input_graph)
print(edges)

# %%
# We need to convert to integer vertices in order to bulk-load a sparse graph. We provide
# a function which does the conversion.
# 

import re

def convert_id(id):
    m = re.match(r'v([0-9]+)', id)
    vid = int(m.group(1))
    return vid

edges = [(convert_id(s), convert_id(t), w) for s, t, w in edges]

print(edges)

# %%
# Now that we have all our edges, we need to figure out the number of vertices. Sparse graphs
# contain all vertices from :math:`[0, n)` where :math:`n` is the number of vertices. 
# Then we call the :py:meth:`jgrapht.create_sparse_graph()` factory.

sparse = jgrapht.create_sparse_graph(edges, num_of_vertices=5, directed=True, weighted=True)

print(sparse)

# %%
# Note that in the above call the graph must be weighted, as our edges also have a weight.
# Let us calculate a graph coloring using the greedy algorithm using saturation degree ordering.

import jgrapht.algorithms.coloring as coloring

num_colors, color_map = coloring.greedy_dsatur(sparse)

print('Total number of colors: {}'.format(num_colors))
print('Color map: {}'.format(color_map))

