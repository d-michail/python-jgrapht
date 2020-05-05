import time
import ctypes

from .. import backend
from ..exceptions import UnsupportedOperationError
from .._errors import raise_status, GraphExportError
from .._wrappers import (
    JGraphTLongIterator, 
    JGraphTGraphPath, 
    JGraphTAttributeStore,
    JGraphTAttributesRegistry,
)


def _export_to_file(name, graph, filename, *args):
    alg_method_name = "jgrapht_export_file_" + name

    try:
        alg_method = getattr(backend, alg_method_name)
    except AttributeError:
        raise UnsupportedOperationError("Algorithm {} not supported.".format(name))

    err = alg_method(graph.handle, filename, *args)
    if err:
        raise_status()


def _attributes_to_store(attributes_dict):
    vertex_attribute_store = None
    if attributes_dict is not None:
        vertex_attribute_store = JGraphTAttributeStore()
        for element, attr_dict in attributes_dict.items():
            for key, value in attr_dict.items():
                vertex_attribute_store.put(element, key, value)

    return vertex_attribute_store


DIMACS_FORMATS = dict(
    {
        "shortestpath": backend.DIMACS_FORMAT_SHORTEST_PATH,
        "maxclique": backend.DIMACS_FORMAT_MAX_CLIQUE,
        "coloring": backend.DIMACS_FORMAT_COLORING,
    }
)


def write_dimacs(graph, filename, format="maxclique", export_edge_weights=False):
    """Export a graph using the DIMACS format.

    For a description of the formats see http://dimacs.rutgers.edu/Challenges . Note that
    there a lot of different formats based on each different challenge. The exports supports
    the shortest path challenge format, the coloring format and the maximum-clique challenge
    formats. By default the maximum-clique is used.

    .. note:: In DIMACS formats the vertices are integers numbered from one.
                 The exporter automatically translates them. 

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
    """
    format = DIMACS_FORMATS.get(format, backend.DIMACS_FORMAT_MAX_CLIQUE)
    custom = [format, export_edge_weights]
    return _export_to_file("dimacs", graph, filename, *custom)


def write_lemon(graph, filename, export_edge_weights=False, escape_strings=False):
    """Exports a graph into Lemon graph format (LGF). This is the custom graph format
    used in the `Lemon <https://lemon.cs.elte.hu/trac/lemon>`_ graph library.

    :param graph: the graph
    :param filename: the filename
    :param export_edge_weights: whether to also export edge weights
    :param escape_strings: whether to escape all strings as Java strings
    :raises GraphExportError: In case of an export error        
    """
    custom = [export_edge_weights, escape_strings]
    return _export_to_file("lemon", graph, filename, *custom)


def write_gml(
    graph,
    filename,
    export_edge_weights=False,
    per_vertex_attrs_dict=None,
    per_edge_attrs_dict=None,
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

    .. note:: Custom attributes are supported with per vertex and per edge dictionaries. 

    :param graph: the graph
    :param filename: the filename
    :param export_edge_weights: whether to export edge weights
    :param per_vertex_attrs_dict: per vertex attribute dicts
    :param per_edge_attrs_dict: per edge attribute dicts
    :raises GraphExportError: In case of an export error 
    """
    vertex_attribute_store = _attributes_to_store(per_vertex_attrs_dict)
    edge_attribute_store = _attributes_to_store(per_edge_attrs_dict)

    err = backend.jgrapht_export_file_gml(
        graph.handle,
        filename,
        export_edge_weights,
        vertex_attribute_store.handle if vertex_attribute_store is not None else None,
        edge_attribute_store.handle if edge_attribute_store is not None else None,
    )
    if err:
        raise_status()


def write_json(graph, filename, per_vertex_attrs_dict=None, per_edge_attrs_dict=None):
    """Exports a graph using `JSON <https://tools.ietf.org/html/rfc8259>`_.

    The output is one object which contains:

      * A member named nodes whose value is an array of nodes.
      * A member named edges whose value is an array of edges.
      * Two members named creator and version for metadata.

    Each node contains an identifier and possibly other attributes. Similarly each edge
    contains the source and target vertices, a possible identifier and possible other
    attributes. 

    .. note:: Custom attributes are supported with per vertex and per edge dictionaries. 

    :param graph: The graph to export
    :param filename: Filename to write
    :param per_vertex_attrs_dict: per vertex attribute dicts
    :param per_edge_attrs_dict: per edge attribute dicts
    :raises GraphExportError: In case of an export error 
    """
    vertex_attribute_store = _attributes_to_store(per_vertex_attrs_dict)
    edge_attribute_store = _attributes_to_store(per_edge_attrs_dict)

    err = backend.jgrapht_export_file_json(
        graph.handle,
        filename,
        vertex_attribute_store.handle if vertex_attribute_store is not None else None,
        edge_attribute_store.handle if edge_attribute_store is not None else None,
    )
    if err:
        raise_status()


CSV_FORMATS = dict(
    {
        "adjacencylist": backend.CSV_FORMAT_ADJACENCY_LIST,
        "edgelist": backend.CSV_FORMAT_EDGE_LIST,
        "matrix": backend.CSV_FORMAT_MATRIX,
    }
)


def write_csv(
    graph,
    filename,
    format="adjacencylist",
    export_edge_weights=False,
    matrix_format_nodeid=False,
    matrix_format_zero_when_no_edge=True,
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
    :raises GraphExportError: in case of an export error
    """
    format = CSV_FORMATS.get(format, backend.CSV_FORMAT_ADJACENCY_LIST)
    custom = [
        format,
        export_edge_weights,
        matrix_format_nodeid,
        matrix_format_zero_when_no_edge,
    ]
    return _export_to_file("csv", graph, filename, *custom)


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

    .. note:: Custom attributes are supported with per vertex and per edge dictionaries. 

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
    :raises GraphExportError: In case of an export error         
    """
    attrs_registry = JGraphTAttributesRegistry()
    for name, category, type, default_value in attrs: 
        attrs_registry.put(name, category, type, default_value)

    vertex_attribute_store = _attributes_to_store(per_vertex_attrs_dict)
    edge_attribute_store = _attributes_to_store(per_edge_attrs_dict)

    custom = [ 
        attrs_registry.handle, 
        vertex_attribute_store.handle if vertex_attribute_store is not None else None,
        edge_attribute_store.handle if edge_attribute_store is not None else None,
        export_edge_weights,
        export_edge_labels,
        export_edge_types,
        export_meta
    ]

    return _export_to_file("gexf", graph, filename, *custom)


def write_dot(
    graph,
    filename,
    per_vertex_attrs_dict=None,
    per_edge_attrs_dict=None
):
    """Exports a graph to DOT format.

    For a description of the format see https://en.wikipedia.org/wiki/DOT_language.

    .. note:: Custom attributes are supported with per vertex and per edge dictionaries. 

    :param graph: The graph to export
    :param filename: Filename to write
    :param per_vertex_attrs_dict: per vertex attribute dicts
    :param per_edge_attrs_dict: per edge attribute dicts
    :raises GraphExportError: In case of an export error         
    """
    vertex_attribute_store = _attributes_to_store(per_vertex_attrs_dict)
    edge_attribute_store = _attributes_to_store(per_edge_attrs_dict)

    custom = [ 
        vertex_attribute_store.handle if vertex_attribute_store is not None else None,
        edge_attribute_store.handle if edge_attribute_store is not None else None,
    ]

    return _export_to_file("dot", graph, filename, *custom)


def write_graph6(graph, filename):
    """Exports a graph to graph6 format.

    See https://users.cecs.anu.edu.au/~bdm/data/formats.txt for a description of the format.

    :param graph: The graph to export
    :param filename: Filename to write
    :raises GraphExportError: In case of an export error         
    """

    return _export_to_file("graph6", graph, filename)


def write_sparse6(graph, filename):
    """Exports a graph to sparse6 format.

    See https://users.cecs.anu.edu.au/~bdm/data/formats.txt for a description of the format.

    :param graph: The graph to export
    :param filename: Filename to write
    :raises GraphExportError: In case of an export error         
    """

    return _export_to_file("sparse6", graph, filename)