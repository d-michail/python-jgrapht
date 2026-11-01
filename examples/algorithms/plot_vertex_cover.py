"""
Vertex cover
============

A vertex cover is a set of vertices that touches every edge. Find a small one.
"""

import matplotlib.pyplot as plt

import jgrapht as jg
from jgrapht import drawing

g = jg.named_graph("petersen")

# %%
# Each algorithm returns the weight of the cover and its vertices. The greedy algorithm is quick,
# and the two-approximation is guaranteed to be at most twice the optimum.

for algorithm in ["greedy", "two_approximation", "edge_based_two_approximation"]:
    weight, cover = jg.vertex_cover(g, algorithm)
    print(f"{algorithm:30s} {len(cover)} vertices, valid: {jg.is_vertex_cover(g, cover)}")

# %%
# Draw the greedy cover in red.

weight, cover = jg.vertex_cover(g)
pos = jg.circular_layout(g)
drawing.draw(g, pos, vertex_color={v: "crimson" if v in cover else "lightgray" for v in g.vertices()})
plt.show()

# %%
# For a bipartite graph there is an exact algorithm.

b = jg.complete_bipartite_graph(3, 5)
weight, cover = jg.vertex_cover(b, "bipartite")
print(sorted(cover))
