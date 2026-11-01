"""
Shortest paths
==============

Build a small weighted road network and compute shortest paths with several algorithms.
"""

# %%
# Start by importing the package and creating a weighted, undirected graph. The vertices are
# city names: any hashable object works.

import jgrapht as jg

g = jg.Graph(weighted=True)
for city in ["Athens", "Patras", "Larissa", "Volos", "Ioannina"]:
    g.add_vertex(city)

roads = [
    ("Athens", "Patras", 215.0),
    ("Athens", "Larissa", 350.0),
    ("Athens", "Volos", 330.0),
    ("Larissa", "Volos", 60.0),
    ("Patras", "Ioannina", 270.0),
    ("Ioannina", "Larissa", 240.0),
]
for u, v, km in roads:
    g.add_edge(u, v, weight=km)

# %%
# A single shortest path comes back as a :class:`~jgrapht.GraphPath` with its vertices, edges and
# weight.

path = jg.shortest_path(g, "Patras", "Volos")
print(path.vertices)
print(path.weight)

# %%
# All distances from one vertex are a dictionary.

print(jg.single_source_distances(g, "Athens"))

# %%
# The next best routes between two cities come from the k shortest paths.

for p in jg.k_shortest_paths(g, "Patras", "Volos", 3):
    print(p.weight, p.vertices)

# %%
# An unreachable vertex has no path, which is ``None``.

g.add_vertex("Rhodes")
print(jg.shortest_path(g, "Athens", "Rhodes"))
