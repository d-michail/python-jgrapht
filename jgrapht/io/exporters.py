from .. import backend as _backend

from .._internals._wrappers import _JGraphTString
from .._internals._collections import _JGraphTIntegerStringMap
from .._internals._attributes import (
    _JGraphTAttributeStore,
    _JGraphTAttributesRegistry,
)
from .._internals._anyhashableg import _is_anyhashable_graph


def _export_to_file(name, graph, filename, *args):
    alg_method_name = "jgrapht_export_file_" + name
    alg_method = getattr(_backend, alg_method_name)
    alg_method(graph.handle, filename, *args)


def _export_to_string(name, graph, *args):
    alg_method_name = "jgrapht_export_string_" + name
    alg_method = getattr(_backend, alg_method_name)
    handle = alg_method(graph.handle, *args)
    # We wrap around a python string which copies the result and
    # releases the actual object inside the backend
    return str(_JGraphTString(handle))


def _vertex_id_store(graph, check_valid_id=None, export_vertex_id_cb=None):
    """Create a vertex identifier store inside the capi backend.

    :param graph: a graph
    :param check_valid_id: a validator. If None no validation takes place.
    :param export_vertex_id_cb: a function which converts from a graph vertex to
      an identifier to be written to file.
    """
    vertex_id_store = None
    if _is_anyhashable_graph(graph):
        # special case, read identifiers from any-hashable graph
        vertex_id_store = _JGraphTIntegerStringMap()

        if export_vertex_id_cb is not None:
            for k, v in graph._vertex_id_to_hash.items():
                vid = export_vertex_id_cb(v)
                if check_valid_id is not None:
                    check_valid_id(vid)
                vertex_id_store[k] = str(vid)
        else:
            for k, v in graph._vertex_id_to_hash.items():
                if check_valid_id is not None:
                    check_valid_id(v)
                vertex_id_store[k] = str(v)
    else:
        if export_vertex_id_cb is not None:
            vertex_id_store = _JGraphTIntegerStringMap()
            for v in graph.vertices:
                vid = export_vertex_id_cb(v)
                if check_valid_id is not None:
                    check_valid_id(vid)
                vertex_id_store[v] = str(vid)
    return vertex_id_store


def _vertex_attributes_store(graph, attributes_dict):
    """Combine the attributes from an any-hashable graph and a per-vertex attributes
    dictionary and create an equivalent structure in the capi. This can then be
    used in order to export a graph with attributes.
    """
    attribute_store = None
    if _is_anyhashable_graph(graph):
        # any-hashable graph
        attribute_store = _JGraphTAttributeStore()
        for v in graph.vertices:
            for key, value in graph.vertex_attrs[v].items():
                attribute_store.put(graph._vertex_hash_to_id[v], key, str(value))
        if attributes_dict is not None:
            for v, attr_dict in attributes_dict.items():
                for key, value in attr_dict.items():
                    try:
                        attribute_store.put(
                            graph._vertex_hash_to_id[v], key, str(value)
                        )
                    except KeyError:
                        # ignore
                        pass
    else:
        # default graph
        if attributes_dict is not None:
            if attribute_store is None:
                attribute_store = _JGraphTAttributeStore()

            for v, attr_dict in attributes_dict.items():
                for key, value in attr_dict.items():
                    attribute_store.put(v, key, str(value))

    return attribute_store


def _edge_id_store(graph):
    """Create an edge identifier store inside the capi backend. This only 
    works for any-hashable graphs, otherwise it returns None.
    """
    edge_id_store = None
    if _is_anyhashable_graph(graph):
        # special case, read identifiers from an any-hashable graph
        edge_id_store = _JGraphTIntegerStringMap()
        for k, v in graph._edge_id_to_hash.items():
            edge_id_store[k] = str(v)
    return edge_id_store


def _edge_attributes_store(graph, attributes_dict):
    """Combine the attributes from an any-hashable graph and a per-edge attributes
    dictionary and create an equivalent structure in the capi. This can then be
    used in order to export a graph with attributes.
    """
    attribute_store = None
    if _is_anyhashable_graph(graph):
        # any-hashable graph
        attribute_store = _JGraphTAttributeStore()
        for e in graph.edges:
            for key, value in graph.edge_attrs[e].items():
                attribute_store.put(graph._edge_hash_to_id[e], key, str(value))
        if attributes_dict is not None:
            for e, attr_dict in attributes_dict.items():
                for key, value in attr_dict.items():
                    try:
                        attribute_store.put(graph._edge_hash_to_id[e], key, str(value))
                    except KeyError:
                        # just ignore
                        pass
    else:
        # default graph
        if attributes_dict is not None:
            if attribute_store is None:
                attribute_store = _JGraphTAttributeStore()

            for e, attr_dict in attributes_dict.items():
                for key, value in attr_dict.items():
                    attribute_store.put(e, key, str(value))

    return attribute_store


DIMACS_FORMATS = dict(
    {
        "shortestpath": _backend.DIMACS_FORMAT_SHORTEST_PATH,
        "maxclique": _backend.DIMACS_FORMAT_MAX_CLIQUE,
        "coloring": _backend.DIMACS_FORMAT_COLORING,
    }
)


def write_dimacs(
    graph,
    filename,
    format="maxclique",
    export_edge_weights=False,
    export_vertex_id_cb=None,
):
    """Export a graph using the DIMACS format.

    For a description of the formats see http://dimacs.rutgers.edu/Challenges . Note that
    there a lot of different formats based on each different challenge. The exports supports
    the shortest path challenge format, the coloring format and the maximum-clique challenge
    formats. By default the maximum-clique is used.

    .. note:: In DIMACS formats the vertices are integers numbered from one. In case of default graphs 
              (with integer vertices) this translation happens automatically. With any-hashable graphs the
              user must either use positive integers as vertices, or must explicitly provide a function 
              which does the conversion to a positive integer (`export_vertex_id_cb`).


    Briefly, one of the most common DIMACS formats is the
    `2nd DIMACS challenge <http://mat.gsia.cmu.edu/COLOR/general/ccformat.ps>`_ and follows the 
    following structure::

      DIMACS G {
        c <comments> ignored during parsing of the graph
        p edge <number of nodes> <number of edges>
        e <edge source 1> <edge target 1>
        e <edge source 2> <edge target 2>
        e <edge source 3> <edge target 3>
        e <edge source 4> <edge target 4>
        ...
      }

    Although not specified directly in the DIMACS format documentation, this implementation also
    allows for the a weighted variant::
 
      e <edge source 1> <edge target 1> <edge_weight>

    :param graph: the graph
    :param filename: the filename
    :param format: a string with the format to use. Valid are `maxclique`, `shortestpath`
                   and `coloring`.
    :param export_edge_weights: whether to also export edge weights
    :param export_vertex_id_cb: function which converts from vertex to positive integer identifiers to be written 
      to the output
    """
    format = DIMACS_FORMATS.get(format, _backend.DIMACS_FORMAT_MAX_CLIQUE)

    def check_valid_id(id):
        if not isinstance(id, int):
            raise TypeError("Identifiers must be integers")
        if id <= 0:
            raise ValueError("Identifiers must be positive")

    vertex_id_store = _vertex_id_store(graph, check_valid_id, export_vertex_id_cb)
    custom = [
        format,
        export_edge_weights,
        vertex_id_store.handle if vertex_id_store is not None else None,
    ]
    return _export_to_file("dimacs", graph, filename, *custom)


def generate_dimacs(
    graph, format="maxclique", export_edge_weights=False, export_vertex_id_cb=None
):
    """Export a graph to a string using the DIMACS format.

    For a description of the formats see http://dimacs.rutgers.edu/Challenges . Note that
    there a lot of different formats based on each different challenge. The exports supports
    the shortest path challenge format, the coloring format and the maximum-clique challenge
    formats. By default the maximum-clique is used.

    .. note:: In DIMACS formats the vertices are integers numbered from one. In case of default graphs 
              (with integer vertices) this translation happens automatically. With any-hashable graphs the
              user must either use positive integers as vertices, or must explicitly provide a function 
              which does the conversion to a positive integer (`export_vertex_id_cb`). 

    Briefly, one of the most common DIMACS formats is the
    `2nd DIMACS challenge <http://mat.gsia.cmu.edu/COLOR/general/ccformat.ps>`_ and follows the 
    following structure::

      DIMACS G {
        c <comments> ignored during parsing of the graph
        p edge <number of nodes> <number of edges>
        e <edge source 1> <edge target 1>
        e <edge source 2> <edge target 2>
        e <edge source 3> <edge target 3>
        e <edge source 4> <edge target 4>
        ...
      }

    Although not specified directly in the DIMACS format documentation, this implementation also
    allows for the a weighted variant::
 
      e <edge source 1> <edge target 1> <edge_weight>

    :param graph: the graph
    :param format: a string with the format to use. Valid are `maxclique`, `shortestpath`
                   and `coloring`.
    :param export_edge_weights: whether to also export edge weights
    :param export_vertex_id_cb: function which converts from vertex to positive integer identifiers to be written 
      to the output    
    :returns: a string containing the exported graph    
    """
    format = DIMACS_FORMATS.get(format, _backend.DIMACS_FORMAT_MAX_CLIQUE)

    def check_valid_id(id):
        if not isinstance(id, int):
            raise TypeError("Identifiers must integers")
        if id <= 0:
            raise ValueError("Identifiers must be positive")

    vertex_id_store = _vertex_id_store(graph, check_valid_id, export_vertex_id_cb)
    custom = [
        format,
        export_edge_weights,
        vertex_id_store.handle if vertex_id_store is not None else None,
    ]
    return _export_to_string("dimacs", graph, *custom)


def write_lemon(
    graph,
    filename,
    export_edge_weights=False,
    escape_strings=False,
    export_vertex_id_cb=None,
):
    """Exports a graph into Lemon graph format (LGF). This is the custom graph format
    used in the `Lemon <https://lemon.cs.elte.hu/trac/lemon>`_ graph library.

    :param graph: the graph
    :param filename: the filename
    :param export_edge_weights: whether to also export edge weights
    :param escape_strings: whether to escape all strings as Java strings
    :param export_vertex_id_cb: function which converts from vertex to identifier to be written 
      to the output    
    :raises IOError: In case of an export error        
    """
    vertex_id_store = _vertex_id_store(graph, export_vertex_id_cb=export_vertex_id_cb)
    custom = [
        export_edge_weights,
        escape_strings,
        vertex_id_store.handle if vertex_id_store is not None else None,
    ]
    return _export_to_file("lemon", graph, filename, *custom)


def generate_lemon(
    graph, export_edge_weights=False, escape_strings=False, export_vertex_id_cb=None
):
    """Exports a graph to a string using the Lemon graph format (LGF).
    This is the custom graph format used in the 
    `Lemon <https://lemon.cs.elte.hu/trac/lemon>`_ graph library.

    :param graph: the graph
    :param export_edge_weights: whether to also export edge weights
    :param escape_strings: whether to escape all strings as Java strings
    :param export_vertex_id_cb: function which converts from vertex to identifier to be written 
      to the output    
    :returns: a string contains the exported graph    
    :raises IOError: In case of an export error        
    """
    vertex_id_store = _vertex_id_store(graph, export_vertex_id_cb=export_vertex_id_cb)
    custom = [
        export_edge_weights,
        escape_strings,
        vertex_id_store.handle if vertex_id_store is not None else None,
    ]
    return _export_to_string("lemon", graph, *custom)


def write_gml(
    graph,
    filename,
    export_edge_weights=False,
    export_vertex_labels=False,
    export_edge_labels=False,
    per_vertex_attrs_dict=None,
    per_edge_attrs_dict=None,
    export_vertex_id_cb=None,
):
    """Export a graph in GML format (Graph Modelling Language).

    Below is small example of a graph in GML format::

        graph [
            node [ 
                id 1
            ]
            node [
                id 2
                label "Node 2 has an optional label"
            ]
            node [
                id 3
            ]
            edge [
                source 1
                target 2 
                weight 2.0
                label "Edge between 1 and 2"
            ]
            edge [
                source 2
                target 3
                weight 3.0
                label "Edge between 2 and 3"
            ]
        ]

    .. note:: The exporter escapes all strings as Java strings.

    .. note:: Custom attributes are supported with per vertex and per edge dictionaries. These
      custom attributes are merged with the attributes of any-hashable graphs.

    :param graph: the graph
    :param filename: the filename
    :param export_edge_weights: whether to export edge weights
    :param export_vertex_labels: whether to export a vertex attribute called "label". Even if 
      such an attribute is not provided explicitly, it will be autogenerated.
    :param export_edge_labels: whether to export an edge attribute called "label". Even if 
      such an attribute is not provided explicitly, it will be autogenerated      
    :param per_vertex_attrs_dict: per vertex attribute dicts
    :param per_edge_attrs_dict: per edge attribute dicts
    :param export_vertex_id_cb: function which converts from vertex to identifier to be written 
      to the output    
    :raises IOError: In case of an export error 
    """
    vertex_attribute_store = _vertex_attributes_store(graph, per_vertex_attrs_dict)
    edge_attribute_store = _edge_attributes_store(graph, per_edge_attrs_dict)

    def check_valid_id(id):
        if not isinstance(id, int):
            raise TypeError("Identifiers must be integers")
        if id < 0:
            raise ValueError("Identifiers must be non-negative")

    vertex_id_store = _vertex_id_store(
        graph, check_valid_id=check_valid_id, export_vertex_id_cb=export_vertex_id_cb
    )

    custom = [
        export_edge_weights,
        export_vertex_labels,
        export_edge_labels,
        vertex_attribute_store.handle if vertex_attribute_store is not None else None,
        edge_attribute_store.handle if edge_attribute_store is not None else None,
        vertex_id_store.handle if vertex_id_store is not None else None,
    ]

    return _export_to_file("gml", graph, filename, *custom)


def generate_gml(
    graph,
    export_edge_weights=False,
    export_vertex_labels=False,
    export_edge_labels=False,
    per_vertex_attrs_dict=None,
    per_edge_attrs_dict=None,
    export_vertex_id_cb=None,
):
    """Export a graph to a string in GML format (Graph Modelling Language).

    Below is small example of a graph in GML format::

        graph [
            node [ 
                id 1
            ]
            node [
                id 2
                label "Node 2 has an optional label"
            ]
            node [
                id 3
            ]
            edge [
                source 1
                target 2 
                weight 2.0
                label "Edge between 1 and 2"
            ]
            edge [
                source 2
                target 3
                weight 3.0
                label "Edge between 2 and 3"
            ]
        ]

    .. note:: The exporter escapes all strings as Java strings.

    .. note:: Custom attributes are supported with per vertex and per edge dictionaries. These
      custom attributes are merged with the attributes of any-hashable graphs.

    :param graph: the graph
    :param export_edge_weights: whether to export edge weights
    :param export_vertex_labels: whether to export a vertex attribute called "label". Even if 
      such an attribute is not provided explicitly, it will be autogenerated.
    :param export_edge_labels: whether to export an edge attribute called "label". Even if 
      such an attribute is not provided explicitly, it will be autogenerated          
    :param per_vertex_attrs_dict: per vertex attribute dicts
    :param per_edge_attrs_dict: per edge attribute dicts
    :param export_vertex_id_cb: function which converts from vertex to identifier to be written 
      to the output    
    :returns: a string contains the exported graph    
    :raises IOError: In case of an export error 
    """
    vertex_attribute_store = _vertex_attributes_store(graph, per_vertex_attrs_dict)
    edge_attribute_store = _edge_attributes_store(graph, per_edge_attrs_dict)

    def check_valid_id(id):
        if not isinstance(id, int):
            raise TypeError("Identifiers must be integers")
        if id < 0:
            raise ValueError("Identifiers must be non-negative")

    vertex_id_store = _vertex_id_store(
        graph, check_valid_id=check_valid_id, export_vertex_id_cb=export_vertex_id_cb
    )

    custom = [
        export_edge_weights,
        export_vertex_labels,
        export_edge_labels,
        vertex_attribute_store.handle if vertex_attribute_store is not None else None,
        edge_attribute_store.handle if edge_attribute_store is not None else None,
        vertex_id_store.handle if vertex_id_store is not None else None,
    ]

    return _export_to_string("gml", graph, *custom)


def write_json(
    graph,
    filename,
    per_vertex_attrs_dict=None,
    per_edge_attrs_dict=None,
    export_vertex_id_cb=None,
):
    """Exports a graph using `JSON <https://tools.ietf.org/html/rfc8259>`_.

    The output is one object which contains:

      * A member named nodes whose value is an array of nodes.
      * A member named edges whose value is an array of edges.
      * Two members named creator and version for metadata.

    Each node contains an identifier and possibly other attributes. Similarly each edge
    contains the source and target vertices, a possible identifier and possible other
    attributes. 

    .. note:: Custom attributes are supported with per vertex and per edge dictionaries. These
      custom attributes are merged with the attributes of any-hashable graphs.

    :param graph: The graph to export
    :param filename: Filename to write
    :param per_vertex_attrs_dict: per vertex attribute dicts
    :param per_edge_attrs_dict: per edge attribute dicts
    :param export_vertex_id_cb: function which converts from vertex to identifier to be written 
      to the output        
    :raises IOError: In case of an export error 
    """
    vertex_attribute_store = _vertex_attributes_store(graph, per_vertex_attrs_dict)
    edge_attribute_store = _edge_attributes_store(graph, per_edge_attrs_dict)
    vertex_id_store = _vertex_id_store(graph, export_vertex_id_cb=export_vertex_id_cb)

    custom = [
        vertex_attribute_store.handle if vertex_attribute_store is not None else None,
        edge_attribute_store.handle if edge_attribute_store is not None else None,
        vertex_id_store.handle if vertex_id_store is not None else None,
    ]

    return _export_to_file("json", graph, filename, *custom)


def generate_json(
    graph,
    per_vertex_attrs_dict=None,
    per_edge_attrs_dict=None,
    export_vertex_id_cb=None,
):
    """Exports a graph to string using `JSON <https://tools.ietf.org/html/rfc8259>`_.

    The output is one object which contains:

      * A member named nodes whose value is an array of nodes.
      * A member named edges whose value is an array of edges.
      * Two members named creator and version for metadata.

    Each node contains an identifier and possibly other attributes. Similarly each edge
    contains the source and target vertices, a possible identifier and possible other
    attributes. 

    .. note:: Custom attributes are supported with per vertex and per edge dictionaries. These
      custom attributes are merged with the attributes of any-hashable graphs.

    :param graph: The graph to export
    :param per_vertex_attrs_dict: per vertex attribute dicts
    :param per_edge_attrs_dict: per edge attribute dicts
    :param export_vertex_id_cb: function which converts from vertex to identifier to be written 
      to the output        
    :returns: a string contains the exported graph    
    :raises IOError: In case of an export error 
    """
    vertex_attribute_store = _vertex_attributes_store(graph, per_vertex_attrs_dict)
    edge_attribute_store = _edge_attributes_store(graph, per_edge_attrs_dict)
    vertex_id_store = _vertex_id_store(graph, export_vertex_id_cb=export_vertex_id_cb)

    custom = [
        vertex_attribute_store.handle if vertex_attribute_store is not None else None,
        edge_attribute_store.handle if edge_attribute_store is not None else None,
        vertex_id_store.handle if vertex_id_store is not None else None,
    ]

    return _export_to_string("json", graph, *custom)


CSV_FORMATS = dict(
    {
        "adjacencylist": _backend.CSV_FORMAT_ADJACENCY_LIST,
        "edgelist": _backend.CSV_FORMAT_EDGE_LIST,
        "matrix": _backend.CSV_FORMAT_MATRIX,
    }
)


def write_csv(
    graph,
    filename,
    format="adjacencylist",
    export_edge_weights=False,
    matrix_format_nodeid=False,
    matrix_format_zero_when_no_edge=True,
    export_vertex_id_cb=None,
):
    """Export a graph using the CSV format.

    The exporter supports various different formats which can be adjusted using the format parameter.
    The supported formats are the same CSV formats used by Gephi. The exporter respects rfc4180.

    :param graph: the graph
    :param filename: the filename
    :param format: a string with the format to use. Valid are `maxclique`, `shortestpath`
                   and `coloring`.
    :param export_edge_weights: whether to export edge weights
    :param matrix_format_node_id: only for the matrix format, whether to export node identifiers
    :param matrix_format_zero_when_noedge: only for the matrix format, whether the output should contain
           zero for missing edges
    :param export_vertex_id_cb: function which converts from vertex to identifier to be written 
      to the output               
    :raises IOError: in case of an export error
    """
    format = CSV_FORMATS.get(format, _backend.CSV_FORMAT_ADJACENCY_LIST)
    vertex_id_store = _vertex_id_store(graph, export_vertex_id_cb=export_vertex_id_cb)
    custom = [
        format,
        export_edge_weights,
        matrix_format_nodeid,
        matrix_format_zero_when_no_edge,
        vertex_id_store.handle if vertex_id_store is not None else None,
    ]
    return _export_to_file("csv", graph, filename, *custom)


def generate_csv(
    graph,
    format="adjacencylist",
    export_edge_weights=False,
    matrix_format_nodeid=False,
    matrix_format_zero_when_no_edge=True,
    export_vertex_id_cb=None,
):
    """Export a graph to string using the CSV format.

    The exporter supports various different formats which can be adjusted using the format parameter.
    The supported formats are the same CSV formats used by Gephi. The exporter respects rfc4180.

    :param graph: the graph
    :param format: a string with the format to use. Valid are `maxclique`, `shortestpath`
                   and `coloring`.
    :param export_edge_weights: whether to export edge weights
    :param matrix_format_node_id: only for the matrix format, whether to export node identifiers
    :param matrix_format_zero_when_noedge: only for the matrix format, whether the output should contain
           zero for missing edges
    :param export_vertex_id_cb: function which converts from vertex to identifier to be written 
      to the output               
    :returns: a string contains the exported graph           
    :raises IOError: in case of an export error
    """
    format = CSV_FORMATS.get(format, _backend.CSV_FORMAT_ADJACENCY_LIST)
    vertex_id_store = _vertex_id_store(graph, export_vertex_id_cb=export_vertex_id_cb)
    custom = [
        format,
        export_edge_weights,
        matrix_format_nodeid,
        matrix_format_zero_when_no_edge,
        vertex_id_store.handle if vertex_id_store is not None else None,
    ]
    return _export_to_string("csv", graph, *custom)


def write_gexf(
    graph,
    filename,
    attrs=list(),
    per_vertex_attrs_dict=None,
    per_edge_attrs_dict=None,
    export_edge_weights=False,
    export_edge_labels=False,
    export_edge_types=False,
    export_meta=False,
    export_vertex_id_cb=None,
):
    """Exports a graph to a GEXF file.

    For a description of the format see https://gephi.org/gexf/format/index.html or the 
    `GEXF Primer <https://gephi.org/gexf/format/primer.html>`_.

    Below is small example of a graph in GEXF format::

        <?xml version="1.0" encoding="UTF-8"?>
        <gexf xmlns="http://www.gexf.net/1.2draft"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xsi:schemaLocation="http://www.gexf.net/1.2draft http://www.gexf.net/1.2draft/gexf.xsd"
            version="1.2">
            <graph defaultedgetype="undirected">
                <nodes>
                <node id="n0" label="node 0"/>
                <node id="n1" label="node 1"/>
                <node id="n2" label="node 2"/>
                <node id="n3" label="node 3"/>
                <node id="n4" label="node 4"/>
                <node id="n5" label="node 5"/>
                </nodes>
                <edges>
                <edge id="e0" source="n0" target="n2" weight="1.0"/>
                <edge id="e1" source="n0" target="n1" weight="1.0"/>
                <edge id="e2" source="n1" target="n3" weight="2.0"/>
                <edge id="e3" source="n3" target="n2"/>
                <edge id="e4" source="n2" target="n4"/>
                <edge id="e5" source="n3" target="n5"/>
                <edge id="e6" source="n5" target="n4" weight="1.1"/>
                </edges>
            </graph>
        </gexf>

    .. note:: Custom attributes are supported with per vertex and per edge dictionaries. These
      custom attributes are merged with the attributes of any-hashable graphs.

    .. note:: Custom attributes need to be registered in the `attrs` parameter which accepts a list
              of tuple(name, category, type, default_value). Type and default value may None. Category 
              must be either `node` or `edge`.

    :param graph: The graph to export
    :param filename: Filename to write
    :param attrs: a list of tuples (name, category, type, default_value)
    :param per_vertex_attrs_dict: per vertex attribute dicts
    :param per_edge_attrs_dict: per edge attribute dicts
    :param export_edge_weights: whether to export edge weights
    :param export_edge_labels: whether to export edge labels
    :param export_edge_types: whether to export edge types
    :param export_meta: whether to export meta tag
    :param export_vertex_id_cb: function which converts from vertex to identifier to be written 
      to the output        
    :raises IOError: In case of an export error         
    """
    attrs_registry = _JGraphTAttributesRegistry()
    for name, category, attr_type, default_value in attrs:
        attrs_registry.put(name, category, attr_type, default_value)

    vertex_attribute_store = _vertex_attributes_store(graph, per_vertex_attrs_dict)
    edge_attribute_store = _edge_attributes_store(graph, per_edge_attrs_dict)
    vertex_id_store = _vertex_id_store(graph, export_vertex_id_cb=export_vertex_id_cb)
    edge_id_store = _edge_id_store(graph)

    custom = [
        attrs_registry.handle,
        vertex_attribute_store.handle if vertex_attribute_store is not None else None,
        edge_attribute_store.handle if edge_attribute_store is not None else None,
        vertex_id_store.handle if vertex_id_store is not None else None,
        edge_id_store.handle if edge_id_store is not None else None,
        export_edge_weights,
        export_edge_labels,
        export_edge_types,
        export_meta,
    ]

    return _export_to_file("gexf", graph, filename, *custom)


def generate_gexf(
    graph,
    attrs=list(),
    per_vertex_attrs_dict=None,
    per_edge_attrs_dict=None,
    export_edge_weights=False,
    export_edge_labels=False,
    export_edge_types=False,
    export_meta=False,
    export_vertex_id_cb=None,
):
    """Exports a graph to string using GEXF.

    For a description of the format see https://gephi.org/gexf/format/index.html or the 
    `GEXF Primer <https://gephi.org/gexf/format/primer.html>`_.

    Below is small example of a graph in GEXF format::

        <?xml version="1.0" encoding="UTF-8"?>
        <gexf xmlns="http://www.gexf.net/1.2draft"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xsi:schemaLocation="http://www.gexf.net/1.2draft http://www.gexf.net/1.2draft/gexf.xsd"
            version="1.2">
            <graph defaultedgetype="undirected">
                <nodes>
                <node id="n0" label="node 0"/>
                <node id="n1" label="node 1"/>
                <node id="n2" label="node 2"/>
                <node id="n3" label="node 3"/>
                <node id="n4" label="node 4"/>
                <node id="n5" label="node 5"/>
                </nodes>
                <edges>
                <edge id="e0" source="n0" target="n2" weight="1.0"/>
                <edge id="e1" source="n0" target="n1" weight="1.0"/>
                <edge id="e2" source="n1" target="n3" weight="2.0"/>
                <edge id="e3" source="n3" target="n2"/>
                <edge id="e4" source="n2" target="n4"/>
                <edge id="e5" source="n3" target="n5"/>
                <edge id="e6" source="n5" target="n4" weight="1.1"/>
                </edges>
            </graph>
        </gexf>

    .. note:: Custom attributes are supported with per vertex and per edge dictionaries. These
      custom attributes are merged with the attributes of any-hashable graphs.

    .. note:: Custom attributes need to be registered in the `attrs` parameter which accepts a list
              of tuple(name, category, type, default_value). Type and default value may None. Category 
              must be either `node` or `edge`.

    :param graph: The graph to export
    :param attrs: a list of tuples (name, category, type, default_value)
    :param per_vertex_attrs_dict: per vertex attribute dicts
    :param per_edge_attrs_dict: per edge attribute dicts
    :param export_edge_weights: whether to export edge weights
    :param export_edge_labels: whether to export edge labels
    :param export_edge_types: whether to export edge types
    :param export_meta: whether to export meta tag
    :param export_vertex_id_cb: function which converts from vertex to identifier to be written 
      to the output        
    :returns: a string contains the exported graph    
    :raises IOError: In case of an export error         
    """
    attrs_registry = _JGraphTAttributesRegistry()
    for name, category, attr_type, default_value in attrs:
        attrs_registry.put(name, category, attr_type, default_value)

    vertex_attribute_store = _vertex_attributes_store(graph, per_vertex_attrs_dict)
    edge_attribute_store = _edge_attributes_store(graph, per_edge_attrs_dict)
    vertex_id_store = _vertex_id_store(graph, export_vertex_id_cb=export_vertex_id_cb)
    edge_id_store = _edge_id_store(graph)

    custom = [
        attrs_registry.handle,
        vertex_attribute_store.handle if vertex_attribute_store is not None else None,
        edge_attribute_store.handle if edge_attribute_store is not None else None,
        vertex_id_store.handle if vertex_id_store is not None else None,
        edge_id_store.handle if edge_id_store is not None else None,
        export_edge_weights,
        export_edge_labels,
        export_edge_types,
        export_meta,
    ]

    return _export_to_string("gexf", graph, *custom)


def write_dot(
    graph,
    filename,
    per_vertex_attrs_dict=None,
    per_edge_attrs_dict=None,
    export_vertex_id_cb=None,
):
    """Exports a graph to DOT format.

    For a description of the format see https://en.wikipedia.org/wiki/DOT_language.

    .. note:: Custom attributes are supported with per vertex and per edge dictionaries. These
      custom attributes are merged with the attributes of any-hashable graphs.

    :param graph: The graph to export
    :param filename: Filename to write
    :param per_vertex_attrs_dict: per vertex attribute dicts
    :param per_edge_attrs_dict: per edge attribute dicts
    :param export_vertex_id_cb: function which converts from vertex to identifier to be written 
      to the output        
    :raises IOError: In case of an export error         
    """
    vertex_attribute_store = _vertex_attributes_store(graph, per_vertex_attrs_dict)
    edge_attribute_store = _edge_attributes_store(graph, per_edge_attrs_dict)
    vertex_id_store = _vertex_id_store(graph, export_vertex_id_cb=export_vertex_id_cb)

    custom = [
        vertex_attribute_store.handle if vertex_attribute_store is not None else None,
        edge_attribute_store.handle if edge_attribute_store is not None else None,
        vertex_id_store.handle if vertex_id_store is not None else None,
    ]

    return _export_to_file("dot", graph, filename, *custom)


def generate_dot(
    graph,
    per_vertex_attrs_dict=None,
    per_edge_attrs_dict=None,
    export_vertex_id_cb=None,
):
    """Exports a graph to string using DOT format.

    For a description of the format see https://en.wikipedia.org/wiki/DOT_language.

    .. note:: Custom attributes are supported with per vertex and per edge dictionaries. These
      custom attributes are merged with the attributes of any-hashable graphs.

    :param graph: The graph to export
    :param per_vertex_attrs_dict: per vertex attribute dicts
    :param per_edge_attrs_dict: per edge attribute dicts
    :param export_vertex_id_cb: function which converts from vertex to identifier to be written 
      to the output        
    :returns: a string contains the exported graph    
    :raises IOError: In case of an export error         
    """
    vertex_attribute_store = _vertex_attributes_store(graph, per_vertex_attrs_dict)
    edge_attribute_store = _edge_attributes_store(graph, per_edge_attrs_dict)
    vertex_id_store = _vertex_id_store(graph, export_vertex_id_cb=export_vertex_id_cb)

    custom = [
        vertex_attribute_store.handle if vertex_attribute_store is not None else None,
        edge_attribute_store.handle if edge_attribute_store is not None else None,
        vertex_id_store.handle if vertex_id_store is not None else None,
    ]

    return _export_to_string("dot", graph, *custom)


def write_graph6(graph, filename):
    """Exports a graph to graph6 format.

    See https://users.cecs.anu.edu.au/~bdm/data/formats.txt for a description of the format.

    :param graph: The graph to export
    :param filename: Filename to write
    :raises IOError: In case of an export error         
    """
    return _export_to_file("graph6", graph, filename)


def generate_graph6(graph):
    """Exports a graph to string using graph6 format.

    See https://users.cecs.anu.edu.au/~bdm/data/formats.txt for a description of the format.

    :param graph: The graph to export
    :returns: a string contains the exported graph    
    :raises IOError: In case of an export error         
    """
    return _export_to_string("graph6", graph)


def write_sparse6(graph, filename):
    """Exports a graph to sparse6 format.

    See https://users.cecs.anu.edu.au/~bdm/data/formats.txt for a description of the format.

    :param graph: The graph to export
    :param filename: Filename to write
    :raises IOError: In case of an export error         
    """

    return _export_to_file("sparse6", graph, filename)


def generate_sparse6(graph):
    """Exports a graph to string using sparse6 format.

    See https://users.cecs.anu.edu.au/~bdm/data/formats.txt for a description of the format.

    :param graph: The graph to export
    :returns: a string contains the exported graph         
    :raises IOError: In case of an export error
    """
    return _export_to_string("sparse6", graph)


def write_graphml(
    graph,
    filename,
    attrs=list(),
    per_vertex_attrs_dict=None,
    per_edge_attrs_dict=None,
    export_edge_weights=False,
    export_vertex_labels=False,
    export_edge_labels=False,
    export_vertex_id_cb=None,
):
    """Exports a graph to a GraphML file.

    .. note:: Custom attributes are supported with per vertex and per edge dictionaries. These
      custom attributes are merged with the attributes of any-hashable graphs.

    .. note:: Custom attributes need to be registered in the `attrs` parameter which accepts a list
              of tuple(name, category, type, default_value). Type and default value may None. Category 
              must be either `graph`, `node` or `edge`.

    :param graph: The graph to export
    :param filename: Filename to write
    :param attrs: a list of tuples (name, category, type, default_value)
    :param per_vertex_attrs_dict: per vertex attribute dicts
    :param per_edge_attrs_dict: per edge attribute dicts
    :param export_edge_weights: whether to export edge weights
    :param export_vertex_labels: whether to export vertex labels    
    :param export_edge_labels: whether to export edge labels
    :param export_vertex_id_cb: function which converts from vertex to identifier to be written 
      to the output        
    :raises IOError: In case of an export error         
    """
    attrs_registry = _JGraphTAttributesRegistry()
    for name, category, attr_type, default_value in attrs:
        attrs_registry.put(name, category, attr_type, default_value)

    vertex_attribute_store = _vertex_attributes_store(graph, per_vertex_attrs_dict)
    edge_attribute_store = _edge_attributes_store(graph, per_edge_attrs_dict)
    vertex_id_store = _vertex_id_store(graph, export_vertex_id_cb=export_vertex_id_cb)

    custom = [
        attrs_registry.handle,
        vertex_attribute_store.handle if vertex_attribute_store is not None else None,
        edge_attribute_store.handle if edge_attribute_store is not None else None,
        vertex_id_store.handle if vertex_id_store is not None else None,
        export_edge_weights,
        export_vertex_labels,
        export_edge_labels,
    ]

    return _export_to_file("graphml", graph, filename, *custom)


def generate_graphml(
    graph,
    attrs=list(),
    per_vertex_attrs_dict=None,
    per_edge_attrs_dict=None,
    export_edge_weights=False,
    export_vertex_labels=False,
    export_edge_labels=False,
    export_vertex_id_cb=None,
):
    """Exports a graph to string using GraphML.

    .. note:: Custom attributes are supported with per vertex and per edge dictionaries. These
      custom attributes are merged with the attributes of any-hashable graphs.

    .. note:: Custom attributes need to be registered in the `attrs` parameter which accepts a list
              of tuple(name, category, type, default_value). Type and default value may None. Category 
              must be either `node` or `edge`.

    :param graph: The graph to export
    :param attrs: a list of tuples (name, category, type, default_value)
    :param per_vertex_attrs_dict: per vertex attribute dicts
    :param per_edge_attrs_dict: per edge attribute dicts
    :param export_edge_weights: whether to export edge weights
    :param export_vertex_labels: whether to export vertex labels    
    :param export_edge_labels: whether to export edge labels
    :param export_vertex_id_cb: function which converts from vertex to identifier to be written 
      to the output        
    :returns: a string contains the exported graph    
    :raises IOError: In case of an export error         
    """
    attrs_registry = _JGraphTAttributesRegistry()
    for name, category, type, default_value in attrs:
        attrs_registry.put(name, category, type, default_value)

    vertex_attribute_store = _vertex_attributes_store(graph, per_vertex_attrs_dict)
    edge_attribute_store = _edge_attributes_store(graph, per_edge_attrs_dict)
    vertex_id_store = _vertex_id_store(graph, export_vertex_id_cb=export_vertex_id_cb)

    custom = [
        attrs_registry.handle,
        vertex_attribute_store.handle if vertex_attribute_store is not None else None,
        edge_attribute_store.handle if edge_attribute_store is not None else None,
        vertex_id_store.handle if vertex_id_store is not None else None,
        export_edge_weights,
        export_vertex_labels,
        export_edge_labels,
    ]

    return _export_to_string("graphml", graph, *custom)
