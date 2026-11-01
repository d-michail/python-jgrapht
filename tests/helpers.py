"""Helpers shared by the algorithm tests: every test runs on both graph classes."""

import random

import pytest

import jgrapht as jg

both = pytest.mark.parametrize("sparse", [False, True], ids=["Graph", "SparseGraph"])


def build(n, edges, weights=None, directed=False, sparse=False, multi=True, loops=True):
    """Graph on vertices ``0..n-1`` from index-pair ``edges``; edge ``i`` is ``edges[i]``.

    For ``Graph`` the auto-assigned edge objects are ``0, 1, 2, ...`` in insertion order, the same
    as the edge numbers of ``SparseGraph``, so edge ids can be compared across both classes.
    """
    if sparse:
        return jg.SparseGraph(n, edges, directed=directed, weights=weights)
    g = jg.Graph(
        directed=directed,
        weighted=weights is not None,
        allow_multiple_edges=multi,
        allow_self_loops=loops,
    )
    for v in range(n):
        g.add_vertex(v)
    for i, (u, v) in enumerate(edges):
        e = g.add_edge(u, v, weight=None if weights is None else weights[i])
        assert e == i
    return g


def cycle(n):
    """The edges of the cycle on ``0..n-1``."""
    return [(i, (i + 1) % n) for i in range(n)]


def random_chordal(n, seed, k=3):
    """A random chordal graph: each new vertex attaches to a clique of earlier vertices."""
    rng = random.Random(seed)
    edges, cliques = [], [[0]]
    for v in range(1, n):
        base = rng.choice(cliques)
        attach = rng.sample(base, min(len(base), rng.randint(1, k)))
        edges += [(u, v) for u in attach]
        cliques.append(attach + [v])
    return edges


def random_edges(n, m, seed):
    """``m`` random distinct undirected edges on ``0..n-1`` (fewer if there are repeats)."""
    rng = random.Random(seed)
    return sorted({tuple(sorted(rng.sample(range(n), 2))) for _ in range(m)})


def attrs_of(g):
    """What a graph stores about itself after an import, in the shape ``{"graph": ..., "vertices":
    ..., "edges": ..., "ids": ...}`` (plus ``"tsplib"``), for the I/O tests."""
    extras = ("vertex_ids", "tsplib")
    out = {
        "graph": {k: v for k, v in g.graph_attrs.items() if k not in extras},
        "vertices": dict(g.vertex_attrs.items()),
        "edges": dict(g.edge_attrs.items()),
        "ids": g.graph_attrs.get("vertex_ids", list(g.vertices())),
    }
    if "tsplib" in g.graph_attrs:
        out["tsplib"] = g.graph_attrs["tsplib"]
    return out


def parse_graph(text, fmt, attributes=False, **kw):
    """``jg.parse_graph``, returning ``(graph, attrs_of(graph))`` if ``attributes`` is set."""
    g = jg.parse_graph(text, fmt, **kw)
    return (g, attrs_of(g)) if attributes else g
