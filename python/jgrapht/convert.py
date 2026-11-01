"""Conversion between jgrapht graphs and other graph packages: NetworkX and pydot.

The structure, the edge weights and the attributes are converted. The attributes of a graph are the
dicts ``vertex_attrs``, ``edge_attrs`` and ``graph_attrs``; they correspond to the attributes of the
nodes, of the edges and of the graph in NetworkX, and to the attributes of the nodes, edges and graph
statement in pydot. An edge weight is not an attribute of the jgrapht graph, so the attribute
called ``weight`` (or the name given by the ``weight`` parameter) is the edge weight on the other
side. The attribute dicts are copied (their values are shared), never shared with the other graph.

NetworkX and pydot are not dependencies of the package. Install them with ``pip install networkx``
or ``pip install pydot`` (or ``pip install jgrapht[networkx]`` and ``jgrapht[pydot]``); using these
functions without them raises :class:`ImportError`.
"""

from ._jgrapht_rs import Graph, SparseGraph

__all__ = ["to_nx", "from_nx", "to_pydot", "from_pydot"]


def _networkx():
    try:
        import networkx
    except ImportError as exc:
        raise ImportError(
            "jgrapht.convert needs networkx; install it with 'pip install networkx'"
        ) from exc
    return networkx


def to_nx(graph, weight="weight"):
    """Converts ``graph`` to a NetworkX graph.

    The result is a ``DiGraph`` or ``Graph``, or a ``MultiDiGraph`` or ``MultiGraph`` if the graph
    has parallel edges (for a :class:`~jgrapht.Graph`: if it allows them). The vertices become the
    nodes, so the same objects are used, and isolated vertices are kept. The attributes of the
    vertices, of the edges and of the graph become the attributes of the nodes, of the edges and of
    the NetworkX graph. The weight of every edge of a weighted graph is stored in the edge attribute
    ``weight``, replacing an attribute of that name.

    :param graph: a :class:`~jgrapht.Graph`, a :class:`~jgrapht.SparseGraph`, or a read-only
        wrapper of one.
    :param weight: the name of the edge attribute that receives the weight.
    :returns: a new NetworkX graph.

    >>> import jgrapht as jg
    >>> from jgrapht.convert import to_nx
    >>> g = jg.path_graph(3, directed=True)
    >>> g.vertex_attrs[0]["color"] = "red"
    >>> n = to_nx(g)
    >>> sorted(n.edges()), n.nodes[0]
    ([(0, 1), (1, 2)], {'color': 'red'})
    """
    nx = _networkx()
    edges = [(graph.edge_source(e), graph.edge_target(e), e) for e in graph.edges()]
    multi = getattr(graph, "allow_multiple_edges", None)
    if multi is None:  # a SparseGraph has no flag: it is a multigraph if it has parallel edges
        seen = set()
        for u, v, _ in edges:
            key = (u, v) if graph.directed else frozenset((u, v))
            if key in seen:
                multi = True
                break
            seen.add(key)
        else:
            multi = False
    if graph.directed:
        result = nx.MultiDiGraph() if multi else nx.DiGraph()
    else:
        result = nx.MultiGraph() if multi else nx.Graph()
    result.graph.update(graph.graph_attrs)
    result.add_nodes_from(graph.vertices())
    for v, attrs in graph.vertex_attrs.items():
        result.nodes[v].update(attrs)
    for u, v, e in edges:
        key = result.add_edge(u, v)
        data = result.edges[u, v, key] if multi else result.edges[u, v]
        data.update(graph.edge_attrs.get(e, {}))
        if graph.weighted:
            data[weight] = graph.edge_weight(e)
    return result


def from_nx(graph, weight="weight", sparse=False):
    """Creates a jgrapht graph from a NetworkX graph.

    The result is directed if ``graph`` is, allows self-loops, and allows parallel edges if
    ``graph`` is a multigraph. It is weighted if any edge has the attribute ``weight``, and an edge
    without it then gets the weight 1.0, as NetworkX does; that attribute is the edge weight and is
    not kept as an attribute. The other attributes of the nodes, of the edges and of the graph become
    the ``vertex_attrs``, ``edge_attrs`` and ``graph_attrs`` of the result. The nodes become the
    vertices, so the same objects are used; edges are numbered ``0, 1, ...`` in the iteration order
    of ``graph``.

    With ``sparse=True`` the result is an immutable :class:`~jgrapht.SparseGraph`. Its vertex ``i``
    is the ``i``-th node of ``list(graph.nodes)``, and its edge ``i`` is the ``i``-th edge of
    ``list(graph.edges)``; the attributes are keyed by these numbers.

    :param graph: a NetworkX ``Graph``, ``DiGraph``, ``MultiGraph`` or ``MultiDiGraph``.
    :param weight: the name of the edge attribute that holds the weight.
    :param sparse: whether to return a :class:`~jgrapht.SparseGraph` instead of a
        :class:`~jgrapht.Graph`.
    :returns: a new graph.

    >>> import networkx as nx
    >>> from jgrapht.convert import from_nx
    >>> n = nx.path_graph(["a", "b", "c"])
    >>> n.nodes["a"]["color"] = "red"
    >>> g = from_nx(n)
    >>> g.vertices(), g.edge_count(), g.vertex_attrs["a"]
    (['a', 'b', 'c'], 2, {'color': 'red'})
    """
    nx = _networkx()
    directed = graph.is_directed()
    multi = graph.is_multigraph()
    edges = [(u, v, dict(data)) for u, v, data in graph.edges(data=True)]
    weighted = any(weight in data for _, _, data in edges)
    weights = [float(data.pop(weight, 1.0)) for _, _, data in edges]
    if sparse:
        index = {v: i for i, v in enumerate(graph.nodes)}
        result = SparseGraph(
            len(index),
            [(index[u], index[v]) for u, v, _ in edges],
            directed=directed,
            weights=weights if weighted else None,
        )
        vertex_key = index.__getitem__
        edge_keys = range(len(edges))
    else:
        result = Graph(
            directed=directed,
            allow_self_loops=True,
            allow_multiple_edges=multi,
            weighted=weighted,
        )
        for v in graph.nodes:
            result.add_vertex(v)
        edge_keys = []
        for (u, v, _), w in zip(edges, weights):
            edge_keys.append(result.add_edge(u, v, weight=w if weighted else None))
        vertex_key = lambda v: v  # noqa: E731
    result.graph_attrs.update(graph.graph)
    for v, data in graph.nodes(data=True):
        if data:
            result.vertex_attrs[vertex_key(v)].update(data)
    for key, (_, _, data) in zip(edge_keys, edges):
        if data and key is not None:
            result.edge_attrs[key].update(data)
    return result


def _pydot():
    try:
        import pydot
    except ImportError as exc:
        raise ImportError(
            "jgrapht.convert needs pydot; install it with 'pip install pydot'"
        ) from exc
    return pydot


def _unquote(name):
    name = str(name)
    if len(name) >= 2 and name[0] == '"' and name[-1] == '"':
        return name[1:-1]
    return name


def _endpoints(end):
    """The node names of one end of a pydot edge, which can be a node or a subgraph of nodes."""
    if isinstance(end, str):
        return [_unquote(end)]
    return [_unquote(n) for n in end["nodes"]]


def to_pydot(graph, weight="weight", name=None):
    """Converts ``graph`` to a pydot graph.

    The vertices become DOT nodes named ``str(vertex)``, so vertices that print the same are
    merged. The result is a ``digraph`` if ``graph`` is directed, and is not ``strict`` if the graph
    allows parallel edges. The attributes of the vertices and of the edges become DOT attributes,
    and so do the attributes of the graph, except ``name``; DOT attributes are strings, so values
    are converted with ``str``. The weight of every edge of a weighted graph is written as the edge
    attribute ``weight``. Use ``pydot_graph.to_string()`` for the DOT text, or ``write_png`` and
    related methods to render it with Graphviz.

    :param graph: a :class:`~jgrapht.Graph`, a :class:`~jgrapht.SparseGraph`, or a read-only
        wrapper of one.
    :param weight: the name of the edge attribute that receives the weight.
    :param name: the name of the DOT graph, by default the graph attribute ``name`` or ``"G"``.
    :returns: a new ``pydot.Dot``.

    >>> import jgrapht as jg
    >>> from jgrapht.convert import to_pydot
    >>> print(to_pydot(jg.path_graph(3)).to_string())
    graph G {
    0;
    1;
    2;
    0 -- 1;
    1 -- 2;
    }
    <BLANKLINE>
    """
    pydot = _pydot()
    multi = getattr(graph, "allow_multiple_edges", True)
    graph_attrs = dict(graph.graph_attrs)
    if name is None:
        name = str(graph_attrs.get("name", "G"))
    graph_attrs.pop("name", None)
    dot = pydot.Dot(
        graph_name=name, graph_type="digraph" if graph.directed else "graph", strict=not multi
    )
    for key, value in graph_attrs.items():
        dot.set(str(key), str(value))
    for v in graph.vertices():
        attrs = {str(k): str(x) for k, x in graph.vertex_attrs.get(v, {}).items()}
        dot.add_node(pydot.Node(str(v), **attrs))
    for e in graph.edges():
        attrs = {str(k): str(x) for k, x in graph.edge_attrs.get(e, {}).items()}
        if graph.weighted:
            attrs[weight] = str(graph.edge_weight(e))
        dot.add_edge(pydot.Edge(str(graph.edge_source(e)), str(graph.edge_target(e)), **attrs))
    return dot


def from_pydot(dot, weight="weight", sparse=False):
    """Creates a jgrapht graph from a pydot graph.

    The graph is directed if ``dot`` is a ``digraph``. It allows self-loops, and parallel edges
    unless ``dot`` is ``strict``. The vertices are the node names, as strings without their quotes,
    the nodes declared by a statement first, then those that only appear in edges. An edge between
    two groups of nodes, as in ``{a b} -> {c d}``, becomes an edge for every pair. The graph is
    weighted if any edge has the attribute ``weight`` with a numeric value; an edge without one then
    gets the weight 1.0, and that attribute is not kept as an attribute. The other attributes of the
    nodes and of the edges, and the attributes of the graph (with the graph name as ``name``), are
    stored as ``vertex_attrs``, ``edge_attrs`` and ``graph_attrs``; their values are strings, as in
    DOT. Default attributes set by ``node [...]`` and ``edge [...]`` statements, and nested
    subgraphs, are not read.

    With ``sparse=True`` the result is an immutable :class:`~jgrapht.SparseGraph`, whose vertex
    ``i`` is the ``i``-th node in that order; the attributes are keyed by these numbers.

    :param dot: a ``pydot.Dot`` graph, for example from ``pydot.graph_from_dot_data``.
    :param weight: the name of the edge attribute that holds the weight.
    :param sparse: whether to return a :class:`~jgrapht.SparseGraph` instead of a
        :class:`~jgrapht.Graph`.
    :returns: a new graph.

    >>> import pydot
    >>> from jgrapht.convert import from_pydot
    >>> dot = pydot.graph_from_dot_data("digraph { a [color=red]; a -> b; b -> c [weight=2.5]; }")[0]
    >>> g = from_pydot(dot)
    >>> g.vertices(), g.directed, g.weighted, g.vertex_attrs["a"]
    (['a', 'b', 'c'], True, True, {'color': 'red'})
    """
    _pydot()
    directed = dot.get_type() == "digraph"
    strict = bool(dot.get_strict())
    node_attrs = {}
    for node in dot.get_node_list():
        n = _unquote(node.get_name())
        if n in ("graph", "node", "edge", ""):  # DOT statements that set defaults
            continue
        node_attrs.setdefault(n, {}).update(
            {k: _unquote(v) for k, v in node.get_attributes().items()}
        )
    names = dict.fromkeys(node_attrs)
    edges = []
    for edge in dot.get_edge_list():
        attrs = {k: _unquote(v) for k, v in edge.get_attributes().items()}
        raw = attrs.pop(weight, None)
        try:
            w = float(raw) if raw is not None else None
        except ValueError:
            w = None
            attrs[weight] = raw  # not a number: it stays an attribute
        for u in _endpoints(edge.get_source()):
            for v in _endpoints(edge.get_destination()):
                names.setdefault(u, None)
                names.setdefault(v, None)
                edges.append((u, v, w, attrs))
    weighted = any(w is not None for _, _, w, _ in edges)
    weights = [1.0 if w is None else w for _, _, w, _ in edges]
    if sparse:
        index = {n: i for i, n in enumerate(names)}
        result = SparseGraph(
            len(index),
            [(index[u], index[v]) for u, v, _, _ in edges],
            directed=directed,
            weights=weights if weighted else None,
        )
        vertex_key = index.__getitem__
        edge_keys = range(len(edges))
    else:
        result = Graph(
            directed=directed,
            allow_self_loops=True,
            allow_multiple_edges=not strict,
            weighted=weighted,
        )
        for n in names:
            result.add_vertex(n)
        edge_keys = [
            result.add_edge(u, v, weight=w if weighted else None)
            for (u, v, _, _), w in zip(edges, weights)
        ]
        vertex_key = lambda n: n  # noqa: E731
    result.graph_attrs.update({k: _unquote(v) for k, v in dot.get_attributes().items()})
    graph_name = _unquote(dot.get_name())
    if graph_name:
        result.graph_attrs["name"] = graph_name
    for n, attrs in node_attrs.items():
        if attrs:
            result.vertex_attrs[vertex_key(n)].update(attrs)
    for key, (_, _, _, attrs) in zip(edge_keys, edges):
        if attrs and key is not None:
            result.edge_attrs[key].update(attrs)
    return result
