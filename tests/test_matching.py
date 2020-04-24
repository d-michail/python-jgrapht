#!/usr/bin/env python3

import jgrapht.graph as graph
import jgrapht.algorithms.matching as matching
import jgrapht.algorithms.partition as partition
import jgrapht.generators as generators

print('Creating graph')
g = graph.Graph(directed=False, allowing_self_loops=False, allowing_multiple_edges=False, weighted=True)

print('Graph type {}'.format(g.graph_type))

for i in range(0, 6):
    g.add_vertex()

g.add_edge(0, 3)
e13 = g.add_edge(1, 3)
g.add_edge(2, 3)
g.add_edge(1, 4)
g.add_edge(2, 5)

g.set_edge_weight(e13, 15.0)

weight, m = matching.bipartite_matching_max_cardinality(g)
assert weight == 3.0
print('Weight {}'.format(weight))
for e in m:
    print("Matching edge {}".format(e))

weight, m = matching.bipartite_matching_max_weight(g)
assert weight == 1.0
print('Weight {}'.format(weight))
for e in m:
    print("Matching edge {}".format(e))    



bg = graph.Graph(directed=False, allowing_self_loops=False, allowing_multiple_edges=False, weighted=True)
generators.generate_complete_bipartite(bg, 10, 10)
_, part1, part2 = partition.partition_bipartite(bg)
weight, m = matching.bipartite_matching_perfect_min_weight(bg, part1, part2)
print('Weight {}'.format(weight))
for e in m:
    print("Matching edge {}".format(e))    
