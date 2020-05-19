# -*- coding: utf-8 -*-

"""
JSON Export
===========

This is an example on how to export a graph into JSON format. Our JSON format
is very simple and compatible with the `sigmajs <http://sigmajs.org/>`_ library.
"""

# %%
# Start by importing the package.

import jgrapht
from jgrapht.generators import complete_graph
from jgrapht.io.exporters import generate_json

# %%
# Let us create an undirected graph

g = jgrapht.create_graph(directed=False)

# %% 
# and use the complete generator to populate the graph,

complete_graph(g, 5)

print(g)

# %%
# We will export the graph to string in JSON format.

output = generate_json(g)
print(output)

# %%
# Let us also export the graph using some custom attributes.

vertex_attrs = {} 
for v in g.vertices: 
    vertex_attrs[v] = {}
    vertex_attrs[v]['label'] = 'vertex {}'.format(v)

edge_attrs = {} 
for e in g.edges: 
    u, v, _ = g.edge_tuple(e)
    edge_attrs[e] = {}
    edge_attrs[e]['name'] = 'edge {}-{}'.format(u, v)

# %%
# Now call the exporter with the vertex and edge attributes dictionaries
# as extra parameters.

output = generate_json(g, per_vertex_attrs_dict=vertex_attrs, per_edge_attrs_dict=edge_attrs)
print(output)
 
# %%
# For an export to file use function :py:meth:`jgrapht.io.exporters.write_json`.
#
