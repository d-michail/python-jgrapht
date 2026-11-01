"""
Importing a sparse graph
========================

Read a graph in the DIMACS format directly into a compact, immutable :class:`~jgrapht.SparseGraph`.
"""

import jgrapht as jg

# %%
# A DIMACS graph file: ``p`` gives the sizes, and each ``e`` line is an edge.

dimacs = """\
c a small example, the cycle on five vertices
p edge 5 5
e 1 2
e 2 3
e 3 4
e 4 5
e 5 1
"""

# %%
# With ``sparse=True`` the vertices are the numbers ``0..n-1`` in order of appearance, and the
# edges ``0..m-1`` in file order.

g = jg.parse_graph(dimacs, "dimacs", sparse=True)
print(g)
print([(g.edge_source(e), g.edge_target(e)) for e in g.edges()])

# %%
# A sparse graph works with all the algorithms.

print(jg.girth(g), jg.diameter(g))
