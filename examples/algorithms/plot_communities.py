"""
Community detection
===================

Split a social network into communities with label propagation.
"""

import matplotlib.pyplot as plt

import jgrapht as jg
from jgrapht import drawing

g = jg.named_graph("zachary_karate_club")

# %%
# Label propagation is fast and random; a seed makes it repeatable. The result is a list of
# communities, each a list of vertices.

communities = jg.label_propagation_clustering(g, seed=5)
print(len(communities), "communities of sizes", sorted(len(c) for c in communities))

# %%
# Draw the graph with one color per community.

palette = ["tomato", "mediumseagreen", "royalblue", "gold", "orchid", "darkorange"]
color = {v: palette[i % len(palette)] for i, community in enumerate(communities) for v in community}
pos = jg.fruchterman_reingold_layout(g, seed=3)
drawing.draw(g, pos, vertex_color=color, vertex_size=250, font_size=8)
plt.show()

# %%
# Another method, greedy modularity maximization, usually finds communities of a better quality.

print([sorted(c) for c in jg.greedy_modularity_clustering(g)][:2])
