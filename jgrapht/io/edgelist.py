from .. import backend as _backend

from .._internals._collections import _JGraphTEdgeStrTripleList
from .._internals._ioutils import (
    _create_wrapped_import_string_id_callback,
    _create_wrapped_import_integer_id_callback,
    _create_wrapped_attribute_callback,
    _create_wrapped_strid_attribute_callback,
)


def _import_edgelist_with_string_ids(name, with_attrs, filename_or_string, *args):
    alg_method_name = "jgrapht_import_edgelist_"
    if with_attrs:
        alg_method_name += "attrs_"
    else:
        alg_method_name += "noattrs_"
    alg_method_name += name
    alg_method = getattr(_backend, alg_method_name)

    filename_or_string_as_bytearray = bytearray(filename_or_string, encoding="utf-8")

    res = alg_method(filename_or_string_as_bytearray, *args)
    return _JGraphTEdgeStrTripleList(res)


def read_edgelist_dimacs(filename, vertex_attribute_cb=None, edge_attribute_cb=None):
    """Read a graph as an edgelist from a file in DIMACS format. 

    For a description of the formats see http://dimacs.rutgers.edu/Challenges . Note that
    there a lot of different formats based on each different challenge. The importer supports
    the shortest path challenge format, the coloring format and the maximum-clique challenge
    formats.

    .. note:: In DIMACS formats the vertices are integers numbered from one.
                 The importer automatically translates them to zero-based numbering. 

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

    .. note:: This implementation does not fully implement the DIMACS specifications! Special
              fields specified as 'Optional Descriptors' are ignored.

    .. note:: Attribute callback functions accept three parameters. The first is the vertex
              or edge identifier. The second is the attribute key and the third is the 
              attribute value. For the vertices the identifier is a string read from the input.
              For the edges the identifier is an integer denoting the rank of the particular
              edge in the returned edge list.

    :param filename: filename to read from
    :param vertex_attribute_cb: Callback function for vertex attributes
    :param edge_attribute_cb: Callback function for edge attributes    
    :returns: an edge list. This is an iterable which returns iterators of named
      tuples(source, target, weight)      
    :raises IOError: In case of an import error 
    """
    if vertex_attribute_cb is None and edge_attribute_cb is None:
        with_attrs = False
        args = []
    else:
        with_attrs = True
        (
            vertex_attribute_f_ptr,
            vertex_attribute_f,
        ) = _create_wrapped_strid_attribute_callback(vertex_attribute_cb)
        edge_attribute_f_ptr, edge_attribute_f = _create_wrapped_attribute_callback(
            edge_attribute_cb
        )
        args = [vertex_attribute_f_ptr, edge_attribute_f_ptr]

    return _import_edgelist_with_string_ids("file_dimacs", with_attrs, filename, *args)


def parse_edgelist_dimacs(
    input_string, vertex_attribute_cb=None, edge_attribute_cb=None,
):
    """Read graph in DIMACS format from string. 

    For a description of the formats see http://dimacs.rutgers.edu/Challenges . Note that
    there a lot of different formats based on each different challenge. The importer supports
    the shortest path challenge format, the coloring format and the maximum-clique challenge
    formats.

    .. note:: In DIMACS formats the vertices are integers numbered from one.
                 The importer automatically translates them to zero-based numbering. 

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

    .. note:: This implementation does not fully implement the DIMACS specifications! Special
              fields specified as 'Optional Descriptors' are ignored.

    .. note:: Attribute callback functions accept three parameters. The first is the vertex
              or edge identifier. The second is the attribute key and the third is the 
              attribute value. For the vertices the identifier is a string read from the input.
              For the edges the identifier is an integer denoting the rank of the particular
              edge in the returned edge list.              

    :param input_string: Input string to read from
    :param vertex_attribute_cb: Callback function for vertex attributes
    :param edge_attribute_cb: Callback function for edge attributes
    :returns: an edge list. This is an iterable which returns iterators of named
      tuples(source, target, weight)            
    :raises IOError: In case of an import error 
    """
    if vertex_attribute_cb is None and edge_attribute_cb is None:
        with_attrs = False
        args = []
    else:
        with_attrs = True
        (
            vertex_attribute_f_ptr,
            vertex_attribute_f,
        ) = _create_wrapped_strid_attribute_callback(vertex_attribute_cb)
        edge_attribute_f_ptr, edge_attribute_f = _create_wrapped_attribute_callback(
            edge_attribute_cb
        )
        args = [vertex_attribute_f_ptr, edge_attribute_f_ptr]

    return _import_edgelist_with_string_ids(
        "string_dimacs", with_attrs, input_string, *args
    )


def read_edgelist_gml(
    filename, vertex_attribute_cb=None, edge_attribute_cb=None,
):
    """Read a graph as an edgelist from a file in GML format (Graph Modelling Language).

    For a description of the format see http://www.infosun.fmi.uni-passau.de/Graphlet/GML/.
    Below is small example of a graph in GML format.::

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

    The importer also supports reading additional string attributes such as label or custom
    user attributes. String attributes are unescaped as if they are Java strings.

    The parser completely ignores elements from the input that are not related to vertices or
    edges of the graph. Moreover, complicated nested structures are simply returned as a whole.
    For example, in the following graph::

        graph [
            node [ 
                id 1
            ]
            node [ 
                id 2
            ]
            edge [
                source 1
                target 2 
                points [ x 1.0 y 2.0 ]
            ]
        ]

    the points attribute of the edge is returned as a string containing "[ x 1.0 y 2.0 ]".

    .. note:: Attribute callback functions accept three parameters. The first is the vertex
              or edge identifier. The second is the attribute key and the third is the 
              attribute value. For the vertices the identifier is a string read from the input.
              For the edges the identifier is an integer denoting the rank of the particular
              edge in the returned edge list.

    :param filename: Filename to read from
    :param vertex_attribute_cb: Callback function for vertex attributes
    :param edge_attribute_cb: Callback function for edge attributes
    :returns: an edge list. This is an iterable which returns iterators of named
      tuples(source, target, weight)    
    :raises IOError: In case of an import error 
    """
    if vertex_attribute_cb is None and edge_attribute_cb is None:
        with_attrs = False
        args = []
    else:
        with_attrs = True
        (
            vertex_attribute_f_ptr,
            vertex_attribute_f,
        ) = _create_wrapped_strid_attribute_callback(vertex_attribute_cb)
        edge_attribute_f_ptr, edge_attribute_f = _create_wrapped_attribute_callback(
            edge_attribute_cb
        )
        args = [vertex_attribute_f_ptr, edge_attribute_f_ptr]

    return _import_edgelist_with_string_ids("file_gml", with_attrs, filename, *args)


def parse_edgelist_gml(
    input_string, vertex_attribute_cb=None, edge_attribute_cb=None,
):
    """Read a graph as an edgelist from a string in GML format (Graph Modelling Language).

    For a description of the format see http://www.infosun.fmi.uni-passau.de/Graphlet/GML/.
    Below is small example of a graph in GML format.::

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

    The importer also supports reading additional string attributes such as label or custom
    user attributes. String attributes are unescaped as if they are Java strings.

    The parser completely ignores elements from the input that are not related to vertices or
    edges of the graph. Moreover, complicated nested structures are simply returned as a whole.
    For example, in the following graph::

        graph [
            node [ 
                id 1
            ]
            node [ 
                id 2
            ]
            edge [
                source 1
                target 2 
                points [ x 1.0 y 2.0 ]
            ]
        ]

    the points attribute of the edge is returned as a string containing "[ x 1.0 y 2.0 ]".

    .. note:: Attribute callback functions accept three parameters. The first is the vertex
              or edge identifier. The second is the attribute key and the third is the 
              attribute value. For the vertices the identifier is a string read from the input.
              For the edges the identifier is an integer denoting the rank of the particular
              edge in the returned edge list.

    :param graph: The graph to read into
    :param input_string: Input string to read from 
    :param vertex_attribute_cb: Callback function for vertex attributes
    :param edge_attribute_cb: Callback function for edge attributes
    :returns: an edge list. This is an iterable which returns iterators of named
      tuples(source, target, weight)    
    :raises IOError: In case of an import error 
    """
    if vertex_attribute_cb is None and edge_attribute_cb is None:
        with_attrs = False
        args = []
    else:
        with_attrs = True
        (
            vertex_attribute_f_ptr,
            vertex_attribute_f,
        ) = _create_wrapped_strid_attribute_callback(vertex_attribute_cb)
        edge_attribute_f_ptr, edge_attribute_f = _create_wrapped_attribute_callback(
            edge_attribute_cb
        )
        args = [vertex_attribute_f_ptr, edge_attribute_f_ptr]

    return _import_edgelist_with_string_ids(
        "string_gml", with_attrs, input_string, *args
    )


def read_edgelist_json(filename, vertex_attribute_cb=None, edge_attribute_cb=None):
    """Read a graph as an edgelist from a JSON file. 

    Below is a small example of a graph in `JSON <https://tools.ietf.org/html/rfc8259>`_ format::

        {
            "nodes": [
                { "id": "1" },
                { "id": "2", "label": "Node 2 label" },
                { "id": "3" }
            ],
            "edges": [
                { "source": "1", "target": "2", "weight": 2.0, "label": "Edge between 1 and 2" },
                { "source": "2", "target": "3", "weight": 3.0, "label": "Edge between 2 and 3" }
            ]
        }

    The importer also supports reading additional string attributes such as label or custom user
    attributes. The parser completely ignores elements from the input that are not related
    to vertices or edges of the graph. Moreover, complicated nested structures which are inside
    vertices or edges are simply returned as a whole. For example, in the following graph::

        {
            "nodes": [
                { "id": "1" },
                { "id": "2" }
            ],
            "edges": [
                { "source": "1", "target": "2", "points": { "x": 1.0, "y": 2.0 } }
            ]
        }
 
    the points attribute of the edge is returned as a string containing {"x":1.0,"y":2.0}.
    The same is done for arrays or any other arbitrary nested structure.

    .. note:: Attribute callback functions accept three parameters. The first is the vertex
              or edge identifier. The second is the attribute key and the third is the 
              attribute value. For the vertices the identifier is a string read from the input.
              For the edges the identifier is an integer denoting the rank of the particular
              edge in the returned edge list.

    :param filename: Filename to read from
    :param vertex_attribute_cb: Callback function for vertex attributes
    :param edge_attribute_cb: Callback function for edge attributes
    :returns: an edge list. This is an iterable which returns iterators of named
      tuples(source, target, weight)
    :raises IOError: In case of an import error    
    """
    if vertex_attribute_cb is None and edge_attribute_cb is None:
        with_attrs = False
        args = []
    else:
        with_attrs = True
        (
            vertex_attribute_f_ptr,
            vertex_attribute_f,
        ) = _create_wrapped_strid_attribute_callback(vertex_attribute_cb)
        edge_attribute_f_ptr, edge_attribute_f = _create_wrapped_attribute_callback(
            edge_attribute_cb
        )
        args = [vertex_attribute_f_ptr, edge_attribute_f_ptr]

    return _import_edgelist_with_string_ids("file_json", with_attrs, filename, *args)


def parse_edgelist_json(
    input_string, vertex_attribute_cb=None, edge_attribute_cb=None,
):
    """Import a graph as an edgelist from a JSON string. 

    Below is a small example of a graph in `JSON <https://tools.ietf.org/html/rfc8259>`_ format::

        {
            "nodes": [
                { "id": "1" },
                { "id": "2", "label": "Node 2 label" },
                { "id": "3" }
            ],
            "edges": [
                { "source": "1", "target": "2", "weight": 2.0, "label": "Edge between 1 and 2" },
                { "source": "2", "target": "3", "weight": 3.0, "label": "Edge between 2 and 3" }
            ]
        }

    The importer also supports reading additional string attributes such as label or custom user
    attributes. The parser completely ignores elements from the input that are not related
    to vertices or edges of the graph. Moreover, complicated nested structures which are inside
    vertices or edges are simply returned as a whole. For example, in the following graph::

        {
            "nodes": [
                { "id": "1" },
                { "id": "2" }
            ],
            "edges": [
                { "source": "1", "target": "2", "points": { "x": 1.0, "y": 2.0 } }
            ]
        }
 
    the points attribute of the edge is returned as a string containing {"x":1.0,"y":2.0}.
    The same is done for arrays or any other arbitrary nested structure.

    .. note:: Attribute callback functions accept three parameters. The first is the vertex
              or edge identifier. The second is the attribute key and the third is the 
              attribute value. For the vertices the identifier is a string read from the input.
              For the edges the identifier is an integer denoting the rank of the particular
              edge in the returned edge list.

    :param input_string: The input string to read from
    :param vertex_attribute_cb: Callback function for vertex attributes
    :param edge_attribute_cb: Callback function for edge attributes
    :returns: an edge list. This is an iterable which returns iterators of named
      tuples(source, target, weight)    
    :raises IOError: In case of an import error    
    """
    if vertex_attribute_cb is None and edge_attribute_cb is None:
        with_attrs = False
        args = []
    else:
        with_attrs = True
        (
            vertex_attribute_f_ptr,
            vertex_attribute_f,
        ) = _create_wrapped_strid_attribute_callback(vertex_attribute_cb)
        edge_attribute_f_ptr, edge_attribute_f = _create_wrapped_attribute_callback(
            edge_attribute_cb
        )
        args = [vertex_attribute_f_ptr, edge_attribute_f_ptr]

    return _import_edgelist_with_string_ids(
        "string_json", with_attrs, input_string, *args
    )


from .._internals._importers import CSV_FORMATS


def read_edgelist_csv(
    filename,
    format="adjacencylist",
    import_edge_weights=False,
    matrix_format_node_id=False,
    matrix_format_zero_when_noedge=True,
):
    """Imports a graph as an edgelist from a file in CSV Format.

    The importer supports various different formats which can be adjusted using the format parameter.
    The supported formats are the same CSV formats used by Gephi. The importer respects rfc4180. 

    :param filename: the filename to read from
    :param format: format to use. One of "edgelist", "adjacencylist" and "matrix"    
    :param import_edge_weights: whether to import edge weights
    :param matrix_format_node_id: only for the matrix format, whether to import node identifiers
    :param matrix_format_zero_when_noedge: only for the matrix format, whether the input contains zero
      for missing edges
    :returns: an edge list. This is an iterable which returns iterators of named
      tuples(source, target, weight)    
    :raises IOError: in case of an import error    
    """
    format_to_use = CSV_FORMATS.get(format, _backend.CSV_FORMAT_EDGE_LIST)
    args = [
        format_to_use,
        import_edge_weights,
        matrix_format_node_id,
        matrix_format_zero_when_noedge,
    ]

    return _import_edgelist_with_string_ids("file_csv", False, filename, *args)


def parse_edgelist_csv(
    input_string,
    format="adjacencylist",
    import_edge_weights=False,
    matrix_format_node_id=False,
    matrix_format_zero_when_noedge=True,
):
    """Imports a graph as an edgelist from a string in CSV Format.

    The importer supports various different formats which can be adjusted using the format parameter.
    The supported formats are the same CSV formats used by Gephi. The importer respects rfc4180. 

    :param input_string: the input string to read from
    :param format: format to use. One of "edgelist", "adjacencylist" and "matrix"    
    :param import_edge_weights: whether to import edge weights
    :param matrix_format_node_id: only for the matrix format, whether to import node identifiers
    :param matrix_format_zero_when_noedge: only for the matrix format, whether the input contains
      zero for missing edges
    :returns: an edge list. This is an iterable which returns iterators of named
      tuples(source, target, weight)      
    :raises IOError: in case of an import error    
    """
    format_to_use = CSV_FORMATS.get(format, _backend.CSV_FORMAT_ADJACENCY_LIST)
    args = [
        format_to_use,
        import_edge_weights,
        matrix_format_node_id,
        matrix_format_zero_when_noedge,
    ]

    return _import_edgelist_with_string_ids("string_csv", False, input_string, *args)


def read_edgelist_gexf(
    filename, validate_schema=True, vertex_attribute_cb=None, edge_attribute_cb=None,
):
    """Imports a graph as an edgelist from a GEXF file.

    This is a simple implementation with supports only a limited set of features of the GEXF specification,
    oriented towards parsing speed. Moreover, it notifies lazily and completely out-of-order for any additional
    vertex and edge attributes in the input file. Users can register callbacks for vertex and edge attributes.
    Finally, default attribute values and any nested elements are completely ignored.

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

    The parser completely ignores the global attribute "defaultedgetype" and the edge attribute "type"
    which denotes whether an edge is directed or not. The importer by default validates the input
    using the 1.2draft GEXF Schema. The user can (not recommended) disable the validation by adjusting
    the appropriate parameter. Older schemas are not supported.

    .. note:: Attribute callback functions accept three parameters. The first is the vertex
              or edge identifier. The second is the attribute key and the third is the 
              attribute value. For the vertices the identifier is a string read from the input.
              For the edges the identifier is an integer denoting the rank of the particular
              edge in the returned edge list.

    :param filename: the input file to read from
    :param validate_schema: whether to validate the XML schema    
    :param vertex_attribute_cb: callback function for vertex attributes
    :param edge_attribute_cb: callback function for edge attributes
    :returns: an edge list. This is an iterable which returns iterators of named
      tuples(source, target, weight)        
    :raises IOError: in case of an import error    
    """
    if vertex_attribute_cb is None and edge_attribute_cb is None:
        with_attrs = False
        args = [validate_schema]
    else:
        with_attrs = True
        (
            vertex_attribute_f_ptr,
            vertex_attribute_f,
        ) = _create_wrapped_strid_attribute_callback(vertex_attribute_cb)
        edge_attribute_f_ptr, edge_attribute_f = _create_wrapped_attribute_callback(
            edge_attribute_cb
        )
        args = [
            validate_schema,
            vertex_attribute_f_ptr,
            edge_attribute_f_ptr,
        ]

    return _import_edgelist_with_string_ids("file_gexf", with_attrs, filename, *args)


def parse_edgelist_gexf(
    input_string,
    import_id_cb=None,
    validate_schema=True,
    vertex_attribute_cb=None,
    edge_attribute_cb=None,
):
    """Imports a graph as an edgelist from a GEXF input string.

    This is a simple implementation with supports only a limited set of features of the GEXF specification,
    oriented towards parsing speed. Moreover, it notifies lazily and completely out-of-order for any
    additional vertex and edge attributes in the input file. Users can register callbacks for vertex and
    edge attributes. Finally, default attribute values and any nested elements are completely ignored.

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

    The parser completely ignores the global attribute "defaultedgetype" and the edge attribute "type" which
    denotes whether an edge is directed or not. The importer by default validates the input using the 1.2draft
    GEXF Schema. The user can (not recommended) disable the validation by adjusting the appropriate parameter.
    Older schemas are not supported.

    .. note:: Attribute callback functions accept three parameters. The first is the vertex
            or edge identifier. The second is the attribute key and the third is the 
            attribute value. For the vertices the identifier is a string read from the input.
            For the edges the identifier is an integer denoting the rank of the particular
            edge in the returned edge list.

    :param input_string: the input string to read from
    :param validate_schema: whether to validate the XML schema    
    :param vertex_attribute_cb: callback function for vertex attributes
    :param edge_attribute_cb: callback function for edge attributes
    :returns: an edge list. This is an iterable which returns iterators of named
      tuples(source, target, weight)        
    :raises IOError: in case of an import error    
    """
    if vertex_attribute_cb is None and edge_attribute_cb is None:
        with_attrs = False
        args = [validate_schema]
    else:
        with_attrs = True
        (
            vertex_attribute_f_ptr,
            vertex_attribute_f,
        ) = _create_wrapped_strid_attribute_callback(vertex_attribute_cb)
        edge_attribute_f_ptr, edge_attribute_f = _create_wrapped_attribute_callback(
            edge_attribute_cb
        )
        args = [
            validate_schema,
            vertex_attribute_f_ptr,
            edge_attribute_f_ptr,
        ]

    return _import_edgelist_with_string_ids(
        "string_gexf", with_attrs, input_string, *args
    )


def read_edgelist_dot(
    filename, vertex_attribute_cb=None, edge_attribute_cb=None,
):
    """Read a graph as an edgelist from a file in DOT format.

    For a description of the format see https://en.wikipedia.org/wiki/DOT_language and 
    http://www.graphviz.org/doc/info/lang.html .

    .. note:: Attribute callback functions accept three parameters. The first is the vertex
              or edge identifier. The second is the attribute key and the third is the 
              attribute value. For the vertices the identifier is a string read from the input.
              For the edges the identifier is an integer denoting the rank of the particular
              edge in the returned edge list.

    :param filename: Filename to read from
    :param vertex_attribute_cb: Callback function for vertex attributes
    :param edge_attribute_cb: Callback function for edge attributes
    :returns: an edge list. This is an iterable which returns iterators of named
      tuples(source, target, weight)    
    :raises IOError: In case of an import error 
    """
    if vertex_attribute_cb is None and edge_attribute_cb is None:
        with_attrs = False
        args = []
    else:
        with_attrs = True
        (
            vertex_attribute_f_ptr,
            vertex_attribute_f,
        ) = _create_wrapped_strid_attribute_callback(vertex_attribute_cb)
        edge_attribute_f_ptr, edge_attribute_f = _create_wrapped_attribute_callback(
            edge_attribute_cb
        )
        args = [
            vertex_attribute_f_ptr,
            edge_attribute_f_ptr,
        ]
    return _import_edgelist_with_string_ids("file_dot", with_attrs, filename, *args)


def parse_edgelist_dot(
    input_string, vertex_attribute_cb=None, edge_attribute_cb=None,
):
    """Read a graph as an edgelist from a string in DOT format.

    For a description of the format see https://en.wikipedia.org/wiki/DOT_language and 
    http://www.graphviz.org/doc/info/lang.html .

    .. note:: Attribute callback functions accept three parameters. The first is the vertex
              or edge identifier. The second is the attribute key and the third is the 
              attribute value. For the vertices the identifier is a string read from the input.
              For the edges the identifier is an integer denoting the rank of the particular
              edge in the returned edge list.

    :param input_string: the input string to read from
    :param vertex_attribute_cb: callback function for vertex attributes
    :param edge_attribute_cb: callback function for edge attributes
    :returns: an edge list. This is an iterable which returns iterators of named
      tuples(source, target, weight)    
    :raises IOError: in case of an import error 
    """
    if vertex_attribute_cb is None and edge_attribute_cb is None:
        with_attrs = False
        args = []
    else:
        with_attrs = True
        vertex_attribute_f_ptr, vertex_attribute_f = _create_wrapped_strid_attribute_callback(
            vertex_attribute_cb
        )
        edge_attribute_f_ptr, edge_attribute_f = _create_wrapped_attribute_callback(
            edge_attribute_cb
        )
        args = [
            vertex_attribute_f_ptr,
            edge_attribute_f_ptr,
        ]
    return _import_edgelist_with_string_ids(
        "string_dot", with_attrs, input_string, *args
    )


def read_edgelist_graph6sparse6(
    filename, vertex_attribute_cb=None, edge_attribute_cb=None,
):
    """Read a graph as an edgelist from a file in graph6 or sparse6 format.

    See https://users.cecs.anu.edu.au/~bdm/data/formats.txt for a description of the format. Both graph6
    and sparse6 are formats for storing undirected graphs, using a small number of printable ASCII
    characters. Graph6 is suitable for small graphs or large dense graphs while sparse6 is better for 
    large sparse graphs. Moreover, sparse6 supports self-loops and multiple-edges while graph6 does not.

    .. note:: Attribute callback functions accept three parameters. The first is the vertex
              or edge identifier. The second is the attribute key and the third is the 
              attribute value. For the vertices the identifier is a string read from the input.
              For the edges the identifier is an integer denoting the rank of the particular
              edge in the returned edge list.

    :param filename: filename to read from
    :param vertex_attribute_cb: callback function for vertex attributes
    :param edge_attribute_cb: callback function for edge attributes
    :returns: an edge list. This is an iterable which returns iterators of named
      tuples(source, target, weight)    
    :raises IOError: in case of an import error 
    """
    if vertex_attribute_cb is None and edge_attribute_cb is None:
        with_attrs = False
        args = []
    else:
        with_attrs = True
        (
            vertex_attribute_f_ptr,
            vertex_attribute_f,
        ) = _create_wrapped_strid_attribute_callback(vertex_attribute_cb)
        edge_attribute_f_ptr, edge_attribute_f = _create_wrapped_attribute_callback(
            edge_attribute_cb
        )
        args = [
            vertex_attribute_f_ptr,
            edge_attribute_f_ptr,
        ]
    return _import_edgelist_with_string_ids(
        "file_graph6sparse6", with_attrs, filename, *args
    )


def parse_edgelist_graph6sparse6(
    input_string, vertex_attribute_cb=None, edge_attribute_cb=None,
):
    """Read a graph as an edgelist from a string in graph6 or sparse6 format.

    See https://users.cecs.anu.edu.au/~bdm/data/formats.txt for a description of the format. Both
    graph6 and sparse6 are formats for storing undirected graphs, using a small number of printable
    ASCII characters. Graph6 is suitable for small graphs or large dense graphs while sparse6 is
    better for large sparse graphs. Moreover, sparse6 supports self-loops and multiple-edges while
    graph6 does not.

    .. note:: Attribute callback functions accept three parameters. The first is the vertex
              or edge identifier. The second is the attribute key and the third is the 
              attribute value. For the vertices the identifier is a string read from the input.
              For the edges the identifier is an integer denoting the rank of the particular
              edge in the returned edge list.

    :param input_string: the input string
    :param vertex_attribute_cb: callback function for vertex attributes
    :param edge_attribute_cb: callback function for edge attributes
    :returns: an edge list. This is an iterable which returns iterators of named
      tuples(source, target, weight)    
    :raises IOError: in case of an import error 
    """
    if vertex_attribute_cb is None and edge_attribute_cb is None:
        with_attrs = False
        args = []
    else:
        with_attrs = True
        (
            vertex_attribute_f_ptr,
            vertex_attribute_f,
        ) = _create_wrapped_strid_attribute_callback(vertex_attribute_cb)
        edge_attribute_f_ptr, edge_attribute_f = _create_wrapped_attribute_callback(
            edge_attribute_cb
        )
        args = [
            vertex_attribute_f_ptr,
            edge_attribute_f_ptr,
        ]
    return _import_edgelist_with_string_ids(
        "string_graph6sparse6", with_attrs, input_string, *args
    )


def read_edgelist_graphml(
    filename,
    validate_schema=True,
    vertex_attribute_cb=None,
    edge_attribute_cb=None,
    simple=True,
):
    """Imports a graph as an edge list from a GraphML file.

    For a description of the format see http://en.wikipedia.org/wiki/GraphML or the
    `GraphML Primer <http://graphml.graphdrawing.org/primer/graphml-primer.html>`_. 
    
    Below is a small example in GraphML::

        <?xml version="1.0" encoding="UTF-8"?>
        <graphml xmlns="http://graphml.graphdrawing.org/xmlns"  
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns 
            http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd">
            <key id="d0" for="node" attr.name="color" attr.type="string" />
            <key id="d1" for="edge" attr.name="weight" attr.type="double"/>
            <graph id="G" edgedefault="undirected">
                <node id="n0">
                    <data key="d0">green</data>
                </node>
                <node id="n1">
                    <data key="d0">black</data>
                </node>     
                <node id="n2">
                    <data key="d0">blue</data>
                </node>
                <node id="n3">
                    <data key="d0">red</data>
                </node>
                <node id="n4">
                    <data key="d0">white</data>
                </node>
                <node id="n5">
                    <data key="d0">turquoise</data>
                </node>
                <edge id="e0" source="n0" target="n2">
                    <data key="d1">1.0</data>
                </edge>
                <edge id="e1" source="n0" target="n1">
                    <data key="d1">1.0</data>
                </edge>
                <edge id="e2" source="n1" target="n3">
                    <data key="d1">2.0</data>
                </edge>
                <edge id="e3" source="n3" target="n2"/>
                <edge id="e4" source="n2" target="n4"/>
                <edge id="e5" source="n3" target="n5"/>
                <edge id="e6" source="n5" target="n4">
                    <data key="d1">1.1</data>
                </edge>
            </graph>
        </graphml>

    The importer reads the input into a graph which is provided by the user. In case the graph
    is weighted and the corresponding edge attribute "weight" is defined, the importer also
    reads edge weights. Otherwise edge weights are ignored. Moreover, the parser completely ignores
    the global attribute "edgedefault" which denotes whether an edge is directed or not.

    The importer by default validates the input using 1.0 
    `GraphML Schema <http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd>`_.
    The user can (not recommended) disable the validation
    by adjusting the appropriate parameter.

    .. note:: Attribute callback functions accept three parameters. The first is the vertex
              or edge identifier. The second is the attribute key and the third is the 
              attribute value. For the vertices the identifier is a string read from the input.
              For the edges the identifier is an integer denoting the rank of the particular
              edge in the returned edge list.

    .. note:: The parameter simple affect the capabilities of the importer. It trades functionality
              for parsing speed. 

    :param filename: the input file to read from
    :param validate_schema: whether to validate the XML schema    
    :param vertex_attribute_cb: callback function for vertex attributes
    :param edge_attribute_cb: callback function for edge attributes
    :param simple: whether to use a simpler parser with more speed but less functionality
    :returns: an edge list. This is an iterable which returns iterators of named
      tuples(source, target, weight)    
    :raises IOError: in case of an import error    
    """
    if vertex_attribute_cb is None and edge_attribute_cb is None:
        with_attrs = False
        args = [validate_schema]
    else:
        with_attrs = True
        (
            vertex_attribute_f_ptr,
            vertex_attribute_f,
        ) = _create_wrapped_strid_attribute_callback(vertex_attribute_cb)
        edge_attribute_f_ptr, edge_attribute_f = _create_wrapped_attribute_callback(
            edge_attribute_cb
        )
        args = [
            validate_schema,
            vertex_attribute_f_ptr,
            edge_attribute_f_ptr,
        ]

    if simple:
        return _import_edgelist_with_string_ids(
            "file_graphml_simple", with_attrs, filename, *args
        )
    else:
        return _import_edgelist_with_string_ids(
            "file_graphml", with_attrs, filename, *args
        )


def parse_edgelist_graphml(
    input_string,
    validate_schema=True,
    vertex_attribute_cb=None,
    edge_attribute_cb=None,
    simple=True,
):
    """Imports a graph as an edgelist from a GraphML input string.

    For a description of the format see http://en.wikipedia.org/wiki/GraphML or the
    `GraphML Primer <http://graphml.graphdrawing.org/primer/graphml-primer.html>`_. 
    
    Below is a small example in GraphML::

        <?xml version="1.0" encoding="UTF-8"?>
        <graphml xmlns="http://graphml.graphdrawing.org/xmlns"  
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns 
            http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd">
            <key id="d0" for="node" attr.name="color" attr.type="string" />
            <key id="d1" for="edge" attr.name="weight" attr.type="double"/>
            <graph id="G" edgedefault="undirected">
                <node id="n0">
                    <data key="d0">green</data>
                </node>
                <node id="n1">
                    <data key="d0">black</data>
                </node>     
                <node id="n2">
                    <data key="d0">blue</data>
                </node>
                <node id="n3">
                    <data key="d0">red</data>
                </node>
                <node id="n4">
                    <data key="d0">white</data>
                </node>
                <node id="n5">
                    <data key="d0">turquoise</data>
                </node>
                <edge id="e0" source="n0" target="n2">
                    <data key="d1">1.0</data>
                </edge>
                <edge id="e1" source="n0" target="n1">
                    <data key="d1">1.0</data>
                </edge>
                <edge id="e2" source="n1" target="n3">
                    <data key="d1">2.0</data>
                </edge>
                <edge id="e3" source="n3" target="n2"/>
                <edge id="e4" source="n2" target="n4"/>
                <edge id="e5" source="n3" target="n5"/>
                <edge id="e6" source="n5" target="n4">
                    <data key="d1">1.1</data>
                </edge>
            </graph>
        </graphml>

    In case the graph is weighted and the corresponding edge attribute "weight" is defined, the
    importer also reads edge weights. Otherwise edge weights are ignored. Moreover, the parser
    completely ignores the global attribute "edgedefault" which denotes whether an edge is
    directed or not. Whether edges are directed or not depends on the underlying implementation
    of the user provided graph object.

    The importer by default validates the input using 1.0 
    `GraphML Schema <http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd>`_.
    The user can (not recommended) disable the validation
    by adjusting the appropriate parameter.

    .. note:: Attribute callback functions accept three parameters. The first is the vertex
            or edge identifier. The second is the attribute key and the third is the 
            attribute value. For the vertices the identifier is a string read from the input.
            For the edges the identifier is an integer denoting the rank of the particular
            edge in the returned edge list.

    .. note:: The parameter simple affect the capabilities of the importer. It trades functionality
              for parsing speed. 

    :param input_string: the input string to read from
    :param validate_schema: whether to validate the XML schema    
    :param vertex_attribute_cb: callback function for vertex attributes
    :param edge_attribute_cb: callback function for edge attributes
    :param simple: whether to use a simpler parser with more speed but less functionality
    :returns: an edge list. This is an iterable which returns iterators of named
      tuples(source, target, weight)    
    :raises IOError: in case of an import error    
    """
    if vertex_attribute_cb is None and edge_attribute_cb is None:
        with_attrs = False
        args = [validate_schema]
    else:
        with_attrs = True
        (
            vertex_attribute_f_ptr,
            vertex_attribute_f,
        ) = _create_wrapped_strid_attribute_callback(vertex_attribute_cb)
        edge_attribute_f_ptr, edge_attribute_f = _create_wrapped_attribute_callback(
            edge_attribute_cb
        )
        args = [
            validate_schema,
            vertex_attribute_f_ptr,
            edge_attribute_f_ptr,
        ]

    if simple:
        return _import_edgelist_with_string_ids(
            "string_graphml_simple", with_attrs, input_string, *args
        )
    else:
        return _import_edgelist_with_string_ids(
            "string_graphml", with_attrs, input_string, *args
        )

