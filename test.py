#!/usr/bin/env python3
import jgrapht.graph as graph
import jgrapht.algorithms.mst as mst
import jgrapht.algorithms.vertexcover as vc

print('Creating graph')
g = graph.Graph(directed=True, allowing_self_loops=True, allowing_multiple_edges=False, weighted=True)

print('Graph type {}'.format(g.graph_type))
print('directed = {}'.format(g.graph_type.directed))
print('undirected = {}'.format(g.graph_type.undirected))
print('Adding vertex') 
v1 = g.add_vertex()
v2 = g.add_vertex()
v3 = g.add_vertex()
v4 = g.add_vertex()
v5 = g.add_vertex()

vcount = len(g.vertices())
print('Total vertices ' + str(vcount))

for v in g.vertices(): 
    print('Vertex {}'.format(v))

print('Adding edges')
e12 = g.add_edge(v1, v2)
e23 = g.add_edge(v2, v3)
e14 = g.add_edge(v1, v4)
e11 = g.add_edge(v1, v1)
e45 = g.add_edge(v4, v5)
e51 = g.add_edge(v5, v1)
print('Added edge ' + str(e12)) 
print('Added edge ' + str(e23)) 

print('Total edges ' + str(len(g.edges())))

for e in g.edges(): 
    print('Edge {} from {} to {}'.format(e, g.edge_source(e), g.edge_target(e)))

for e in g.outedges_of(v1):
    print('Outgoing edge of {} is {} from {} to {}'.format(v1, e, g.edge_source(e), g.edge_target(e)))

mst_w, mst_edges = mst.mst_kruskal(g)
print('Mst weight {}, mst edges {}'.format(mst_w, mst_edges))

mst_w1, mst_edges1 = mst.mst_prim(g)
print('Mst weight {}, mst edges {}'.format(mst_w1, mst_edges1))
