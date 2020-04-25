#!/usr/bin/env python3

import jgrapht.graph as graph
import jgrapht.algorithms.scoring as scoring

print('Creating graph')
g = graph.Graph(directed=False, allowing_self_loops=False, allowing_multiple_edges=False, weighted=True)

print('Graph type {}'.format(g.graph_type))

for i in range(0, 10):
    g.add_vertex()

vcount = len(g.vertices())
print('Total vertices ' + str(vcount))

print('Adding edges')
e01 = g.add_edge(0, 1)
e02 = g.add_edge(0, 2)
e03 = g.add_edge(0, 3)
e04 = g.add_edge(0, 4)
e05 = g.add_edge(0, 5)
e06 = g.add_edge(0, 6)
e07 = g.add_edge(0, 7)
e08 = g.add_edge(0, 8)
e09 = g.add_edge(0, 9)

e12 = g.add_edge(1, 2)
e23 = g.add_edge(2, 3)
e34 = g.add_edge(3, 4)
e45 = g.add_edge(4, 5)
e56 = g.add_edge(5, 6)
e67 = g.add_edge(6, 7)
e78 = g.add_edge(7, 8)
e89 = g.add_edge(8, 9)
e91 = g.add_edge(9, 1)

print('Total edges ' + str(len(g.edges())))

pagerank = scoring.scoring_pagerank(g)
for v in g.vertices():
    print ('Pagerank of vertex {} is {}'.format(v, pagerank[v]))

harmonic_centrality = scoring.scoring_harmonic_centrality(g)
for v in g.vertices():
    print ('Harmonic centrality of vertex {} is {}'.format(v, harmonic_centrality[v]))

closeness_centrality = scoring.scoring_closeness_centrality(g)
for v in g.vertices():
    print ('Closeness centrality of vertex {} is {}'.format(v, closeness_centrality[v]))

betweenness_centrality = scoring.scoring_betweenness_centrality(g)
for v in g.vertices():
    print ('Betweenness centrality of vertex {} is {}'.format(v, betweenness_centrality[v]))

alpha_centrality = scoring.scoring_alpha_centrality(g)
for v in g.vertices():
    print ('Alpha centrality of vertex {} is {}'.format(v, alpha_centrality[v]))