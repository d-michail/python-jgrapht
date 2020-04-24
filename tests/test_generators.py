#!/usr/bin/env python3

import jgrapht.graph as graph
import jgrapht.generators as generators



g = graph.Graph(directed=False, allowing_self_loops=False, allowing_multiple_edges=False, weighted=True)
generators.generate_barabasi_albert(g, 10, 5, 100)
assert len(g.vertices()) == 100

g = graph.Graph(directed=False, allowing_self_loops=False, allowing_multiple_edges=False, weighted=True)
generators.generate_barabasi_albert_forest(g, 10, 100)
assert len(g.vertices()) == 100

g = graph.Graph(directed=False, allowing_self_loops=False, allowing_multiple_edges=False, weighted=True)
generators.generate_complete(g, 10)
assert len(g.vertices()) == 10

g = graph.Graph(directed=False, allowing_self_loops=False, allowing_multiple_edges=False, weighted=True)
generators.generate_complete_bipartite(g, 10, 10)
assert len(g.vertices()) == 20

g = graph.Graph(directed=False, allowing_self_loops=False, allowing_multiple_edges=False, weighted=True)
generators.generate_empty(g, 10)
assert len(g.vertices()) == 10

g = graph.Graph(directed=False, allowing_self_loops=False, allowing_multiple_edges=False, weighted=True)
generators.generate_gnm_random(g, 10, 30)
assert len(g.vertices()) == 10

g = graph.Graph(directed=False, allowing_self_loops=False, allowing_multiple_edges=False, weighted=True)
generators.generate_gnp_random(g, 10, 0.2)
assert len(g.vertices()) == 10

g = graph.Graph(directed=False, allowing_self_loops=False, allowing_multiple_edges=False, weighted=True)
generators.generate_ring(g, 10)
assert len(g.vertices()) == 10

g = graph.Graph(directed=False, allowing_self_loops=False, allowing_multiple_edges=False, weighted=True)
generators.generate_scalefree(g, 10)
assert len(g.vertices()) == 10

g = graph.Graph(directed=False, allowing_self_loops=False, allowing_multiple_edges=False, weighted=True)
generators.generate_watts_strogatz(g, 10, 2, 0.1)
assert len(g.vertices()) == 10

g = graph.Graph(directed=False, allowing_self_loops=False, allowing_multiple_edges=False, weighted=True)
generators.generate_kleinberg_smallworld(g, 10, 2, 2, 1)
assert len(g.vertices()) == 100
