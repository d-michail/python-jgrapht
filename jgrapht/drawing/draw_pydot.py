
from .. import create_graph as _create_graph
from .._internals._anyhashableg import _is_anyhashable_graph

def _strip(elem):
    if isinstance(elem, str):
        return elem.strip('"')
    return elem

def _get_name(elem):
    return _strip(elem.get_name())

def _to_vertex_list(pydot_vertex):
    result = [] 
    if isinstance(pydot_vertex, str): 
        result.append(_strip(pydot_vertex))
    else:
        for u in pydot_vertex['nodes']:
            result.append(_strip(u))
    return result


def from_pydot(graph):
    """Create a graph from a pydot graph.

    :param graph: the graph in pydot format
    :returns: the graph 
    """

    allows_parallel_edges = not graph.get_strict(None)
    allows_self_loops = not graph.get_strict(None)
    is_directed = graph.get_type() == 'digraph'

    g = _create_graph(directed=is_directed, allowing_self_loops=allows_self_loops, weighted=True, any_hashable=True)

    name = _get_name(graph)
    if name != '':
        g.graph_attrs['name'] = name 

    dotg_attrs = graph.get_attributes()
    if dotg_attrs:
        for k, v in dotg_attrs.items():
            g.graph_attrs[k] = _strip(v)
    
    try:
        dotg_node_attrs = graph.get_node_defaults()[0]
        g_node_attrs = {}
        g.graph_attrs['vertex'] = g_node_attrs
        if dotg_node_attrs:
            for k, v in dotg_node_attrs.items():
                g_node_attrs[k] = _strip(v)
    except (IndexError, TypeError):
        pass

    try:
        dotg_edge_attrs = graph.get_edge_defaults()[0]
        g_edge_attrs = {}
        g.graph_attrs['edge'] = g_edge_attrs
        if dotg_edge_attrs:
            for k, v in dotg_edge_attrs.items():
                g_edge_attrs[k] = _strip(v)
    except (IndexError, TypeError):
        pass

    for dotv in graph.get_node_list():
        dotv_name = _get_name(dotv)
        if dotv_name in ('graph', 'node', 'edge'): 
            # skip nodes setting defaults
            continue
        g.add_vertex(dotv_name)
        for k, v in dotv.get_attributes().items():
            g.vertex_attrs[dotv_name][k] = _strip(v)

    for dote in graph.get_edge_list():
        ulist = _to_vertex_list(dote.get_source())
        vlist = _to_vertex_list(dote.get_destination())
        attrs = dote.get_attributes()

        for dotu in ulist:
            for dotv in vlist:
                if not g.contains_vertex(dotu):
                    g.add_vertex(dotu)
                if not g.contains_vertex(dotv):                    
                    g.add_vertex(dotv)

                e = g.add_edge(dotu, dotv)
                g.edge_attrs[e].update(**attrs)

    return g


def to_pydot(graph):
    """Convert a graph to a pydot graph.

    :param graph: the graph
    :returns: the graph in pydot format
    """
    try:
        import pydot
    except ImportError:
        raise ImportError("pydot required")

    graph_type = 'digraph' if graph.type.directed else 'graph'
    strict = graph.type.allowing_self_loops and graph.type.allowing_multiple_edges

    graph_name = 'G'
    if _is_anyhashable_graph(graph):
        graph_name = graph.graph_attrs.get('name', graph_name)

    dotg = pydot.Dot(graph_name=graph_name, graph_type=graph_type, strict=strict)

    if _is_anyhashable_graph(graph):
        try:
            vertex_attrs = graph.graph_attrs['vertex']
            dotg.set_node_defaults(**vertex_attrs)
        except KeyError:
            pass

        try:
            edge_attrs = graph.graph_attrs['edge']
            dotg.set_edge_defaults(**edge_attrs)
        except KeyError:
            pass

    for v in graph.vertices:
        vattrs = {}
        if _is_anyhashable_graph(graph):
            vattrs.update({ k: str(v) for k, v in graph.vertex_attrs[v].items()})
        dotv = pydot.Node(str(v), **vattrs)
        dotg.add_node(dotv)

    for e in graph.edges:
        u, v, weight = graph.edge_tuple(e)
        eattrs = {}
        if _is_anyhashable_graph(graph):
            eattrs.update({ k: str(v) for k, v in graph.edge_attrs[e].items()})
        elif graph.type.weighted:
            eattrs['weight'] = str(weight)
        dote = pydot.Edge(str(u), str(v), **eattrs)
        dotg.add_edge(dote)

    return dotg

