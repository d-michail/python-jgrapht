#!/usr/bin/env python3
import jgrapht.graph as graph
import jgrapht.algorithms.vertexcover as vc

print('Creating graph')
g = graph.Graph(directed=False, allowing_self_loops=True, allowing_multiple_edges=False, weighted=True)

print('Graph type {}'.format(g.graph_type))

for i in range(0, 10):
    g.add_vertex()

vcount = len(g.vertices())
print('Total vertices ' + str(vcount))

for i in range(1,10):
    g.add_edge(0, i)

print('Total edges ' + str(len(g.edges())))

for e in g.edges(): 
    print('Edge {} from {} to {}'.format(e, g.edge_source(e), g.edge_target(e)))

vertex_weights = dict()
vertex_weights[0] = 1000.0;   
for i in range(1, 10):
    vertex_weights[i] = 1.0;

#vc_weight, vc_vertices = vc.vertexcover_greedy(g)
vc_weight, vc_vertices = vc.vertexcover_clarkson(g, vertex_weights=vertex_weights)
#vc_weight, vc_vertices = vc.vertexcover_edgebased(g, vertex_weights=vertex_weights)
#vc_weight, vc_vertices = vc.vertexcover_edgebased(g)

print("vc weight = {}".format(vc_weight))
print("vc_vertices = {}".format(list(vc_vertices)))

