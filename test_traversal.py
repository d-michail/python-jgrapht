#!/usr/bin/env python3

import jgrapht.graph as graph
import jgrapht.traversal as traversal

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

print('BFS all: {}'.format(list(traversal.bfs_traversal(g))))
print('BFS from 5: {}'.format(list(traversal.bfs_traversal(g, 5))))
print('DFS all: {}'.format(list(traversal.dfs_traversal(g))))
print('DFS from 5: {}'.format(list(traversal.dfs_traversal(g, 5))))
print('lexBFS: {}'.format(list(traversal.lexicographic_bfs_traversal(g))))
print('max-card: {}'.format(list(traversal.max_cardinality_traversal(g))))
print('degeneracy-ordering: {}'.format(list(traversal.degeneracy_ordering_traversal(g))))
print('random_walk_traversal: {}'.format(list(traversal.random_walk_traversal(g, 0, False, 3, 17))))
print('closest first: {}'.format(list(traversal.closest_first_traversal(g, 0))))


# Create a dag to test top

g1 = graph.Graph(directed=True, allowing_self_loops=False, allowing_multiple_edges=False, weighted=True)
g1.add_vertex()
g1.add_vertex()
g1.add_vertex()
g1.add_vertex()

g1.add_edge(0, 1)
g1.add_edge(1, 2)
g1.add_edge(3, 2)

print('topological: {}'.format(list(traversal.topological_order_traversal(g1))))

