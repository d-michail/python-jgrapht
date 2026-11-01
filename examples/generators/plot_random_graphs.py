"""
Random graphs
=============

Generate random graphs and look at their degrees.
"""

# %%
# The Erdos-Renyi model G(n, m) picks ``m`` of the possible edges at random. The ``seed`` makes the
# result reproducible.

import jgrapht as jg

g = jg.gnm_random_graph(30, 60, seed=1)
print(g)

# %%
# The Barabasi-Albert model grows a graph by preferential attachment; a few vertices get a very high
# degree.

ba = jg.barabasi_albert_graph(3, 2, 200, seed=7)
degrees = sorted((ba.degree_of(v) for v in ba.vertices()), reverse=True)
print(degrees[:5], degrees[-3:])

# %%
# The Watts-Strogatz model keeps a ring lattice's clustering while shortening distances.

ws = jg.watts_strogatz_graph(50, 4, 0.1, seed=3)
print(jg.average_clustering_coefficient(ws))
print(jg.diameter(ws))

# %%
# Generators can build the compact :class:`~jgrapht.SparseGraph` directly.

s = jg.gnm_random_graph(1000, 5000, seed=2, sparse=True)
print(s)
print(len(jg.connected_components(s)))
