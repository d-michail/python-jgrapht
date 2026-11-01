"""
Metric traveling salesman
=========================

Find a short tour through a set of points on the plane. The distances are Euclidean, so they obey
the triangle inequality, and the 3/2-approximation of Christofides applies.
"""

import math
import random

import matplotlib.pyplot as plt

import jgrapht as jg
from jgrapht import drawing

# %%
# Random points, and the complete graph on them with the distances as edge weights.

rng = random.Random(11)
points = {i: (rng.random(), rng.random()) for i in range(14)}

g = jg.Graph(weighted=True)
for i in points:
    g.add_vertex(i)
for i in points:
    for j in points:
        if i < j:
            g.add_edge(i, j, weight=math.dist(points[i], points[j]))

# %%
# Compare a quick construction heuristic, the 3/2-approximation, and the 2-opt improvement of
# the first.

for algorithm in ["nearest_neighbor", "christofides", "two_opt"]:
    tour = jg.traveling_salesman_tour(g, algorithm)
    print(f"{algorithm:18s} {tour.weight:.3f}")

# %%
# Draw the Christofides tour.

tour = jg.traveling_salesman_tour(g, "christofides")
fig, ax = plt.subplots()
drawing.draw_edges(g, points, ax, edges=tour.edges, edge_color="royalblue", edge_width=2)
drawing.draw_vertices(g, points, ax, vertex_color="white", border_color="black")
drawing.draw_vertex_labels(g, points, ax, font_size=8)
ax.margins(0.1)
ax.set_axis_off()
plt.show()
