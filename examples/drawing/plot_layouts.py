"""
Layouts
=======

Draw the same graph with three different layouts.
"""

import matplotlib.pyplot as plt

import jgrapht as jg
from jgrapht import drawing

g = jg.generalized_petersen_graph(8, 3)

layouts = {
    "circular": jg.circular_layout(g),
    "random": jg.random_layout(g, seed=7),
    "Fruchterman-Reingold": jg.fruchterman_reingold_layout(g, seed=7),
}

fig, axes = plt.subplots(1, 3, figsize=(12, 4))
for ax, (name, pos) in zip(axes, layouts.items()):
    drawing.draw(g, pos, ax, labels=False, vertex_size=120)
    ax.set_title(name)
plt.show()
