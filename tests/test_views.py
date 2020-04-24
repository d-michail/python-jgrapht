#!/usr/bin/env python3
import jgrapht.graph as graph
import jgrapht.errors as errors

from jgrapht.views import as_undirected, as_edgereversed, as_unmodifiable, as_unweighted


g = graph.Graph(directed=True, allowing_self_loops=True, allowing_multiple_edges=False, weighted=True)

v1 = g.add_vertex()
v2 = g.add_vertex()
v3 = g.add_vertex()
v4 = g.add_vertex()
v5 = g.add_vertex()
e12 = g.add_edge(v1, v2)
e23 = g.add_edge(v2, v3)
e14 = g.add_edge(v1, v4)
e11 = g.add_edge(v1, v1)
e45 = g.add_edge(v4, v5)
e51 = g.add_edge(v5, v1)

g.set_edge_weight(e45, 100.0);

# unweighted
g1 = as_unweighted(g)

assert g.graph_type.directed == g1.graph_type.directed
assert g.graph_type.allowing_self_loops == g1.graph_type.allowing_self_loops
assert g.graph_type.allowing_multiple_edges == g1.graph_type.allowing_multiple_edges
assert g.graph_type.weighted != g1.graph_type.weighted
assert g.get_edge_weight(e45) == 100.0
assert g1.get_edge_weight(e45) == 1.0

# undirected
g2 = as_undirected(g)
assert g2.graph_type.directed is False
assert not g.contains_edge_between(2, 1)
assert g2.contains_edge_between(2, 1)

# unmodifiable
g3 = as_unmodifiable(g)
assert g3.graph_type.modifiable is False
try:
    g3.add_edge(v2, v2)
    assert False
except errors.UnsupportedOperationError:
    pass

# edge reversed
g4 = as_edgereversed(g)
assert g.edge_source(e45) == v4
assert g.edge_target(e45) == v5
assert g4.edge_source(e45) == v5
assert g4.edge_target(e45) == v4

