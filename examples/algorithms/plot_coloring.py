"""
Graph coloring
==============

Color the vertices of a graph so that no two adjacent vertices share a color, using few colors.
"""

import matplotlib.pyplot as plt

import jgrapht as jg
from jgrapht import drawing

g = jg.named_graph("petersen")

# %%
# The greedy algorithms are fast but may use more colors than needed. The result is the number of
# colors and a dictionary from vertex to color.

for algorithm in ["greedy", "largest_degree_first", "saturation_degree", "brown_backtrack"]:
    k, colors = jg.coloring(g, algorithm)
    print(f"{algorithm:22s} {k} colors")

# %%
# The backtracking algorithm is exact: it finds the chromatic number. Draw its coloring.

k, colors = jg.coloring(g, "brown_backtrack")
palette = ["tomato", "mediumseagreen", "royalblue", "gold", "orchid", "darkorange"]
pos = jg.circular_layout(g)
drawing.draw(g, pos, vertex_color={v: palette[c] for v, c in colors.items()})
plt.show()
print(jg.is_proper_coloring(g, colors))
