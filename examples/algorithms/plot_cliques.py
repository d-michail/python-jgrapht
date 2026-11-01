"""
Clique enumeration
==================

Find the maximal cliques of a social network and highlight the largest one.
"""

# %%
# Zachary's karate club is one of the famous graphs that can be created by name.

import matplotlib.pyplot as plt

import jgrapht as jg
from jgrapht import drawing

g = jg.named_graph("zachary_karate_club")
print(len(g), "members,", g.edge_count(), "friendships")

# %%
# A clique is a set of vertices that are all connected to each other. A maximal clique cannot be
# extended by another vertex.

cliques = jg.maximal_cliques(g)
print(len(cliques), "maximal cliques")
print("sizes:", sorted({len(c) for c in cliques}))

# %%
# The largest clique has its own function. Draw it in another color.

largest = jg.maximum_clique(g)
print("a largest clique:", sorted(largest))

pos = jg.fruchterman_reingold_layout(g, seed=3)
drawing.draw(
    g,
    pos,
    vertex_color={v: "tomato" if v in largest else "lightsteelblue" for v in g.vertices()},
    vertex_size=250,
    font_size=8,
)
plt.show()
