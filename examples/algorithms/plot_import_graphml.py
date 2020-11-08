# -*- coding: utf-8 -*-
"""
GraphML Import
==============

This is an example on how to import a graph from a string in GraphML format.
"""

# %%
# Start by importing the package.

import jgrapht
from jgrapht.io.importers import parse_graphml

# %%
# Let us create a directed graph

g = jgrapht.create_graph(directed=True)

# %%
# Let us assume that we are reading the following graph

graphml_input = r"""<?xml version="1.0" encoding="UTF-8"?><graphml xmlns="http://graphml.graphdrawing.org/xmlns"
             xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns
                                 http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd"
                                 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <key id="edge_weight_key" for="edge" attr.name="weight" attr.type="double">
        <default>1.0</default>
    </key>
    <key id="key0" for="edge" attr.name="cost" attr.type="double"/>
    <key id="key1" for="node" attr.name="name" attr.type="string"/>
    <graph edgedefault="directed">
        <node id="0">
            <data key="key1">node 0</data>
        </node>
        <node id="1">
            <data key="key1">node 1</data>
        </node>
        <node id="2"/>
        <node id="3"/>
        <node id="4"/>
        <edge source="0" target="1">
            <data key="edge_weight_key">100.0</data>
            <data key="key0">20.3</data>
        </edge>
        <edge source="0" target="2"/>
        <edge source="0" target="3"/>
        <edge source="0" target="4"/>
        <edge source="1" target="2"/>
        <edge source="2" target="3"/>
        <edge source="3" target="4">
            <data key="edge_weight_key">33.3</data>
            <data key="key0">48.5</data>
        </edge>
    </graph>
</graphml>"""

# %%
# We would also like to capture the vertex and edge attributes. The
# importer will inform us everytime that it reads a vertex or edge
# attribute. The edge attribute "weight" is considered special and 
# is being read automatically if the provided graph object is weighted.
# Thus, we define the following callback functions.

v_attrs = {}
e_attrs = {}

def vertex_attribute_cb(vertex, attribute_name, attribute_value):
    if vertex not in v_attrs:
        v_attrs[vertex] = {}
    v_attrs[vertex][attribute_name] = attribute_value


def edge_attribute_cb(edge, attribute_name, attribute_value):
    if edge not in e_attrs:
        e_attrs[edge] = {}
    e_attrs[edge][attribute_name] = attribute_value


# %%
# The importer needs a way to translate the vertex identifiers from 
# the input to integer values. By default, if we do not provide a function,
# it will auto assign new integer values. If you want to control the
# actual vertices created, you can also provide a `import_id_cb` function
# like the following. Here we simply convert from a string to integer, since
# the actual input contains integer vertices.

def import_id_cb(vertex):
    return int(vertex)


# %%
# Now we call the importer. 

parse_graphml(
    g,
    graphml_input,
    import_id_cb=import_id_cb,
    vertex_attribute_cb=vertex_attribute_cb,
    edge_attribute_cb=edge_attribute_cb,
)

# %%
# We print the graph for debugging purposes.

print(g)

# %%
# The vertex attributes dictionary should contain all vertex attributes.
# The attribute with key `ID` contains the original identifier from the file.
# In our case it will be the same with the `id`.
print(v_attrs)

# %%
# The edge attributes dictionary should contain all edge attributes.
print(e_attrs)

