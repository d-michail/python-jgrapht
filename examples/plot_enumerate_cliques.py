# -*- coding: utf-8 -*-

"""
Clique Enumeration
==================

In this example we execute the Bron-Kerbosch algorithm for enumeration 
of maximal cliques. This particular implementations uses pivoting and 
the degeneracy ordering. 

"""

# %%
# Start by importing the package

import jgrapht
import jgrapht.algorithms.cliques as cliques

# %%
# We first create a graph an undirected graph.

g = jgrapht.create_graph(directed=False)

for i in range(0, 6):
    g.add_vertex(i)

g.add_edge(0, 1)
g.add_edge(0, 2)
g.add_edge(1, 2)
g.add_edge(3, 4)
g.add_edge(3, 5)
g.add_edge(4, 5)
g.add_edge(2, 3)

print(g)

# %%
# We execute the clique enumeration algorithm which returns an iterator
# over all maximal cliques in the graph.

clique_it = cliques.bron_kerbosch_with_degeneracy_ordering(g)

# %%
# Finally we iterate over all cliques

for clique in clique_it: 
    print(clique)

