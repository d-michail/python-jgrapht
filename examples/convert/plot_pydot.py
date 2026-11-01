"""
Graphviz DOT with pydot
=======================

Convert a graph to and from pydot, the Python interface to Graphviz DOT. pydot is an optional
dependency.
"""

import pydot

import jgrapht as jg
from jgrapht.convert import from_pydot, to_pydot

# %%
# Parse a DOT description with pydot, and convert it. The nodes become the vertices, and a
# numeric ``weight`` attribute becomes the edge weight.

text = """
digraph build {
    compile -> test [weight=3];
    compile -> package [weight=1];
    test -> package [weight=2];
    package -> deploy [weight=4];
}
"""
g = from_pydot(pydot.graph_from_dot_data(text)[0])
print(g.vertices(), g.directed, g.weighted)

# %%
# Use an algorithm of this package on it.

path = jg.shortest_path(g, "compile", "deploy")
print(path.vertices, path.weight)

# %%
# Convert it back to get DOT text, for example to render it with Graphviz.

print(to_pydot(g, name="build").to_string())
