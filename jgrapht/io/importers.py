import time
import ctypes

from .. import backend
from .._internals._paths import _JGraphTGraphPath


def _import(name, graph, filename_or_string, *args):
    alg_method_name = "jgrapht_import_" + name

    try:
        alg_method = getattr(backend, alg_method_name)
    except AttributeError:
        raise NotImplementedError("Algorithm {} not supported.".format(name))

    alg_method(graph.handle, filename_or_string, *args)


def _create_wrapped_callback(callback, cfunctype):
    if callback is not None:
        # wrap the python callback with a ctypes function pointer
        f = cfunctype(callback)

        # get the function pointer of the ctypes wrapper by casting it to void* and taking its value
        # we perform the reverse using typemaps on the SWIG layer
        f_ptr = ctypes.cast(f, ctypes.c_void_p).value

        # make sure to also return the callback to avoid garbage collection
        return (f_ptr, f)
    return (0, None)


def read_dimacs(graph, filename, preserve_ids_from_input=True):
    """Read graph in DIMACS format. 

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

    :param graph: the graph to read into
    :param filename: filename to read from
    :param preserve_ids_from_input: whether to preserve the vertex identifiers from the input. If False
           the importer uses new identifiers created from the provided graph.
    :raises IOError: In case of an import error 
    """
    return _import("file_dimacs", graph, filename, preserve_ids_from_input)


def parse_dimacs(graph, input_string, preserve_ids_from_input=True):
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

    :param graph: The graph to read into
    :param input_string: Input string to read from
    :param preserve_ids_from_input: whether to preserve the vertex identifiers from the input. If False
           the importer uses new identifiers created from the provided graph.    
    :raises IOError: In case of an import error 
    """
    return _import("string_dimacs", graph, input_string, preserve_ids_from_input)


def read_gml(
    graph,
    filename,
    preserve_ids_from_input=True,
    vertex_attribute_cb=None,
    edge_attribute_cb=None,
):
    """Read a graph in GML format (Graph Modelling Language).

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

    In case the graph is weighted then the importer also reads edge weights. Otherwise edge
    weights are ignored. The importer also supports reading additional string attributes such
    as label or custom user attributes. String attributes are unescaped as if they are Java
    strings.

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
              attribute value.

    :param graph: The graph to read into
    :param filename: Filename to read from
    :param preserve_ids_from_input: whether to preserve the vertex identifiers from the input. If False
           the importer uses new identifiers created from the provided graph.        
    :param vertex_attribute_cb: Callback function for vertex attributes
    :param edge_attribute_cb: Callback function for edge attributes
    :raises IOError: In case of an import error 
    """
    callback_ctype = ctypes.CFUNCTYPE(
        None, ctypes.c_int, ctypes.c_char_p, ctypes.c_char_p
    )
    vertex_attribute_f_ptr, _ = _create_wrapped_callback(
        vertex_attribute_cb, callback_ctype
    )
    edge_attribute_f_ptr, _ = _create_wrapped_callback(
        edge_attribute_cb, callback_ctype
    )

    args = [preserve_ids_from_input, vertex_attribute_f_ptr, edge_attribute_f_ptr]
    return _import("file_gml", graph, filename, *args)


def parse_gml(
    graph,
    input_string,
    preserve_ids_from_input=True,
    vertex_attribute_cb=None,
    edge_attribute_cb=None,
):
    """Read a graph in GML format (Graph Modelling Language) from a string.

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

    In case the graph is weighted then the importer also reads edge weights. Otherwise edge
    weights are ignored. The importer also supports reading additional string attributes such
    as label or custom user attributes. String attributes are unescaped as if they are Java
    strings.

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
              attribute value.

    :param graph: The graph to read into
    :param input_string: Input string to read from 
    :param preserve_ids_from_input: whether to preserve the vertex identifiers from the input. If False
           the importer uses new identifiers created from the provided graph.        
    :param vertex_attribute_cb: Callback function for vertex attributes
    :param edge_attribute_cb: Callback function for edge attributes
    :raises IOError: In case of an import error 
    """
    callback_ctype = ctypes.CFUNCTYPE(
        None, ctypes.c_int, ctypes.c_char_p, ctypes.c_char_p
    )
    vertex_attribute_f_ptr, _ = _create_wrapped_callback(
        vertex_attribute_cb, callback_ctype
    )
    edge_attribute_f_ptr, _ = _create_wrapped_callback(
        edge_attribute_cb, callback_ctype
    )

    args = [preserve_ids_from_input, vertex_attribute_f_ptr, edge_attribute_f_ptr]
    return _import("string_gml", graph, input_string, *args)


def read_json(
    graph, filename, import_id_cb=None, vertex_attribute_cb=None, edge_attribute_cb=None
):
    """Import a graph from a JSON file. 

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

    In case the graph is weighted then the importer also reads edge weights. Otherwise edge weights
    are ignored. The importer also supports reading additional string attributes such as label or
    custom user attributes. The parser completely ignores elements from the input that are not related
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

    .. note:: The import identifier callback accepts a single parameter which is the identifier read
              from the input file as a string. It should return a long integer with the identifier of the 
              graph vertex.

    .. note:: Attribute callback functions accept three parameters. The first is the vertex
              or edge identifier. The second is the attribute key and the third is the 
              attribute value.

    :param graph: The graph to read into
    :param filename: Filename to read from
    :param import_id_cb: Callback to transform identifiers from file to long integer vertices. Can be 
                         None to allow the graph to assign identifiers to new vertices.
    :param vertex_attribute_cb: Callback function for vertex attributes
    :param edge_attribute_cb: Callback function for edge attributes
    :raises IOError: In case of an import error    
    """
    import_id_cb_ctype = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_char_p)
    import_id_f_ptr, _ = _create_wrapped_callback(import_id_cb, import_id_cb_ctype)

    callback_ctype = ctypes.CFUNCTYPE(
        None, ctypes.c_int, ctypes.c_char_p, ctypes.c_char_p
    )
    vertex_attribute_f_ptr, _ = _create_wrapped_callback(
        vertex_attribute_cb, callback_ctype
    )
    edge_attribute_f_ptr, _ = _create_wrapped_callback(
        edge_attribute_cb, callback_ctype
    )

    args = [import_id_f_ptr, vertex_attribute_f_ptr, edge_attribute_f_ptr]
    return _import("file_json", graph, filename, *args)


def parse_json(
    graph,
    input_string,
    import_id_cb=None,
    vertex_attribute_cb=None,
    edge_attribute_cb=None,
):
    """Import a graph from a JSON string. 

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

    In case the graph is weighted then the importer also reads edge weights. Otherwise edge weights
    are ignored. The importer also supports reading additional string attributes such as label or
    custom user attributes. The parser completely ignores elements from the input that are not related
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

    .. note:: The import identifier callback accepts a single parameter which is the identifier read
              from the input file as a string. It should return a long integer with the identifier of the 
              graph vertex.

    .. note:: Attribute callback functions accept three parameters. The first is the vertex
              or edge identifier. The second is the attribute key and the third is the 
              attribute value.

    :param graph: The graph to read into
    :param input_string: The input string to read from
    :param import_id_cb: Callback to transform identifiers from file to long integer vertices. Can be 
                         None to allow the graph to assign identifiers to new vertices.    
    :param vertex_attribute_cb: Callback function for vertex attributes
    :param edge_attribute_cb: Callback function for edge attributes
    :raises IOError: In case of an import error    
    """
    import_id_cb_ctype = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_char_p)
    import_id_f_ptr, _ = _create_wrapped_callback(import_id_cb, import_id_cb_ctype)

    callback_ctype = ctypes.CFUNCTYPE(
        None, ctypes.c_int, ctypes.c_char_p, ctypes.c_char_p
    )
    vertex_attribute_f_ptr, _ = _create_wrapped_callback(
        vertex_attribute_cb, callback_ctype
    )
    edge_attribute_f_ptr, _ = _create_wrapped_callback(
        edge_attribute_cb, callback_ctype
    )

    args = [import_id_f_ptr, vertex_attribute_f_ptr, edge_attribute_f_ptr]
    return _import("string_json", graph, input_string, *args)


CSV_FORMATS = dict(
    {
        "adjacencylist": backend.CSV_FORMAT_ADJACENCY_LIST,
        "edgelist": backend.CSV_FORMAT_EDGE_LIST,
        "matrix": backend.CSV_FORMAT_MATRIX,
    }
)


def read_csv(
    graph,
    filename,
    import_id_cb=None,
    format="adjacencylist",
    import_edge_weights=False,
    matrix_format_node_id=False,
    matrix_format_zero_when_noedge=True,
):
    """Imports a graph from a file in CSV Format.

    The importer supports various different formats which can be adjusted using the format parameter.
    The supported formats are the same CSV formats used by Gephi. The importer respects rfc4180. 

    .. note:: The import identifier callback accepts a single parameter which is the identifier read
              from the input file as a string. It should return a long integer with the identifier of the 
              graph vertex.

    :param graph: the graph to read into
    :param filename: the filename to read from
    :param import_id_cb: callback to transform identifiers from file to long integer vertices. Can be 
                         None to allow the graph to assign identifiers to new vertices.
    :param format: format to use. One of "edgelist", "adjacencylist" and "matrix"    
    :param import_edge_weights: whether to import edge weights
    :param matrix_format_node_id: only for the matrix format, whether to import node identifiers
    :param matrix_format_zero_when_noedge: only for the matrix format, whether the input contains zero for missing edges
    :raises IOError: in case of an import error    
    """
    import_id_cb_ctype = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_char_p)
    import_id_f_ptr, _ = _create_wrapped_callback(import_id_cb, import_id_cb_ctype)

    format_to_use = CSV_FORMATS.get(format, backend.CSV_FORMAT_EDGE_LIST)
    args = [
        import_id_f_ptr,
        format_to_use,
        import_edge_weights,
        matrix_format_node_id,
        matrix_format_zero_when_noedge,
    ]

    return _import("file_csv", graph, filename, *args)


def parse_csv(
    graph,
    input_string,
    import_id_cb=None,
    format="adjacencylist",
    import_edge_weights=False,
    matrix_format_node_id=False,
    matrix_format_zero_when_noedge=True,
):
    """Imports a graph from a string in CSV Format.

    The importer supports various different formats which can be adjusted using the format parameter.
    The supported formats are the same CSV formats used by Gephi. The importer respects rfc4180. 

    .. note:: The import identifier callback accepts a single parameter which is the identifier read
              from the input file as a string. It should return a long integer with the identifier of the 
              graph vertex.

    :param graph: the graph to read into
    :param input_string: the input string to read from
    :param import_id_cb: callback to transform identifiers from file to long integer vertices. Can be 
                         None to allow the graph to assign identifiers to new vertices.
    :param format: format to use. One of "edgelist", "adjacencylist" and "matrix"    
    :param import_edge_weights: whether to import edge weights
    :param matrix_format_node_id: only for the matrix format, whether to import node identifiers
    :param matrix_format_zero_when_noedge: only for the matrix format, whether the input contains zero for missing edges
    :raises IOError: in case of an import error    
    """

    import_id_cb_ctype = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_char_p)
    import_id_f_ptr, _ = _create_wrapped_callback(import_id_cb, import_id_cb_ctype)

    format_to_use = CSV_FORMATS.get(format, backend.CSV_FORMAT_ADJACENCY_LIST)
    args = [
        import_id_f_ptr,
        format_to_use,
        import_edge_weights,
        matrix_format_node_id,
        matrix_format_zero_when_noedge,
    ]

    return _import("string_csv", graph, input_string, *args)


def read_gexf(
    graph,
    filename,
    import_id_cb=None,
    validate_schema=True,
    vertex_attribute_cb=None,
    edge_attribute_cb=None,
):
    """Imports a graph from a GEXF file.

    This is a simple implementation with supports only a limited set of features of the GEXF specification, oriented towards parsing speed.
    Moreover, it notifies lazily and completely out-of-order for any additional vertex and edge attributes in the input file.
    Users can register callbacks for vertex and edge attributes. Finally, default attribute values and any nested elements are completely ignored.

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

    The importer reads the input into a graph which is provided by the user. In case the graph is weighted and the corresponding edge
    attribute "weight" is defined, the importer also reads edge weights. Otherwise edge weights are ignored. The provided graph object,
    where the imported graph will be stored, must be able to support the features of the graph that is read. For example if the GEXF
    file contains self-loops then the graph provided must also support self-loops. The same for multiple edges. Moreover, the parser
    completely ignores the global attribute "defaultedgetype" and the edge attribute "type" which denotes whether an edge is directed
    or not. Whether edges are directed or not depends on the underlying implementation of the user provided graph object.

    The importer by default validates the input using the 1.2draft GEXF Schema. The user can (not recommended) disable the validation
    by adjusting the appropriate parameter. Older schemas are not supported.

    The graph vertices and edges are build automatically by the graph. The id of the vertices in the input file are reported as a
    vertex attribute named "ID". The user can also bypass vertex creation by providing a import identifier callback. This callback 
    accepts as a parameter the vertex identifier read from file and should return the new vertex.

    .. note:: The import identifier callback accepts a single parameter which is the identifier read
              from the input file as a string. It should return a long integer with the identifier of the 
              graph vertex.

    .. note:: Attribute callback functions accept three parameters. The first is the vertex
              or edge identifier. The second is the attribute key and the third is the 
              attribute value.

    :param graph: the graph to read into
    :param filename: the input file to read from
    :param import_id_cb: callback to transform identifiers from file to long integer vertices. Can be 
                         None to allow the graph to assign identifiers to new vertices.
    :param validate_schema: whether to validate the XML schema    
    :param vertex_attribute_cb: callback function for vertex attributes
    :param edge_attribute_cb: callback function for edge attributes
    :raises IOError: in case of an import error    
    """
    import_id_cb_ctype = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_char_p)
    import_id_f_ptr, _ = _create_wrapped_callback(import_id_cb, import_id_cb_ctype)

    callback_ctype = ctypes.CFUNCTYPE(
        None, ctypes.c_int, ctypes.c_char_p, ctypes.c_char_p
    )
    vertex_attribute_f_ptr, _ = _create_wrapped_callback(
        vertex_attribute_cb, callback_ctype
    )
    edge_attribute_f_ptr, _ = _create_wrapped_callback(
        edge_attribute_cb, callback_ctype
    )

    args = [
        import_id_f_ptr,
        validate_schema,
        vertex_attribute_f_ptr,
        edge_attribute_f_ptr,
    ]

    return _import("file_gexf", graph, filename, *args)


def parse_gexf(
    graph,
    input_string,
    import_id_cb=None,
    validate_schema=True,
    vertex_attribute_cb=None,
    edge_attribute_cb=None,
):
    """Imports a graph from a GEXF input string.

    This is a simple implementation with supports only a limited set of features of the GEXF specification, oriented towards parsing speed.
    Moreover, it notifies lazily and completely out-of-order for any additional vertex and edge attributes in the input file.
    Users can register callbacks for vertex and edge attributes. Finally, default attribute values and any nested elements are completely ignored.

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

    The importer reads the input into a graph which is provided by the user. In case the graph is weighted and the corresponding edge
    attribute "weight" is defined, the importer also reads edge weights. Otherwise edge weights are ignored. The provided graph object,
    where the imported graph will be stored, must be able to support the features of the graph that is read. For example if the GEXF
    file contains self-loops then the graph provided must also support self-loops. The same for multiple edges. Moreover, the parser
    completely ignores the global attribute "defaultedgetype" and the edge attribute "type" which denotes whether an edge is directed
    or not. Whether edges are directed or not depends on the underlying implementation of the user provided graph object.

    The importer by default validates the input using the 1.2draft GEXF Schema. The user can (not recommended) disable the validation
    by adjusting the appropriate parameter. Older schemas are not supported.

    The graph vertices and edges are build automatically by the graph. The id of the vertices in the input file are reported as a
    vertex attribute named "ID". The user can also bypass vertex creation by providing a import identifier callback. This callback 
    accepts as a parameter the vertex identifier read from file and should return the new vertex.

    .. note:: The import identifier callback accepts a single parameter which is the identifier read
              from the input file as a string. It should return a long integer with the identifier of the 
              graph vertex.

    .. note:: Attribute callback functions accept three parameters. The first is the vertex
              or edge identifier. The second is the attribute key and the third is the 
              attribute value.

    :param graph: the graph to read into
    :param input_string: the input string to read from
    :param import_id_cb: callback to transform identifiers from file to long integer vertices. Can be 
                         None to allow the graph to assign identifiers to new vertices.
    :param validate_schema: whether to validate the XML schema    
    :param vertex_attribute_cb: callback function for vertex attributes
    :param edge_attribute_cb: callback function for edge attributes
    :raises IOError: in case of an import error    
    """
    import_id_cb_ctype = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_char_p)
    import_id_f_ptr, _ = _create_wrapped_callback(import_id_cb, import_id_cb_ctype)

    callback_ctype = ctypes.CFUNCTYPE(
        None, ctypes.c_int, ctypes.c_char_p, ctypes.c_char_p
    )
    vertex_attribute_f_ptr, _ = _create_wrapped_callback(
        vertex_attribute_cb, callback_ctype
    )
    edge_attribute_f_ptr, _ = _create_wrapped_callback(
        edge_attribute_cb, callback_ctype
    )

    args = [
        import_id_f_ptr,
        validate_schema,
        vertex_attribute_f_ptr,
        edge_attribute_f_ptr,
    ]

    return _import("string_gexf", graph, input_string, *args)


def read_dot(
    graph,
    filename,
    import_id_cb=None,
    vertex_attribute_cb=None,
    edge_attribute_cb=None,
):
    """Read a graph in DOT format.

    For a description of the format see https://en.wikipedia.org/wiki/DOT_language and 
    http://www.graphviz.org/doc/info/lang.html .

    The provided graph object, where the imported graph will be stored, must be able to support the
    features of the graph that is read. For example if the file contains self-loops then the graph
    provided must also support self-loops. The same for multiple edges. Whether edges are directed or
    not depends on the underlying implementation of the user provided graph object.

    The graph vertices and edges are build automatically by the graph. The id of the vertices in the
    input file are reported as a vertex attribute named "ID". The user can also bypass vertex creation
    by providing a import identifier callback. This callback accepts as a parameter the vertex identifier
    read from file and should return the new vertex.

    .. note:: The import identifier callback accepts a single parameter which is the identifier read
              from the input file as a string. It should return a long integer with the identifier of the 
              graph vertex.

    .. note:: Attribute callback functions accept three parameters. The first is the vertex
              or edge identifier. The second is the attribute key and the third is the 
              attribute value.

    :param graph: The graph to read into
    :param filename: Filename to read from
    :param import_id_cb: callback to transform identifiers from file to long integer vertices. Can be 
                         None to allow the graph to assign identifiers to new vertices.                   
    :param vertex_attribute_cb: Callback function for vertex attributes
    :param edge_attribute_cb: Callback function for edge attributes
    :raises IOError: In case of an import error 
    """
    import_id_cb_ctype = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_char_p)
    import_id_f_ptr, _ = _create_wrapped_callback(import_id_cb, import_id_cb_ctype)

    callback_ctype = ctypes.CFUNCTYPE(
        None, ctypes.c_int, ctypes.c_char_p, ctypes.c_char_p
    )
    vertex_attribute_f_ptr, _ = _create_wrapped_callback(
        vertex_attribute_cb, callback_ctype
    )
    edge_attribute_f_ptr, _ = _create_wrapped_callback(
        edge_attribute_cb, callback_ctype
    )

    args = [ import_id_f_ptr, vertex_attribute_f_ptr, edge_attribute_f_ptr ]
    return _import("file_dot", graph, filename, *args)

def parse_dot(
    graph,
    input_string,
    import_id_cb=None,
    vertex_attribute_cb=None,
    edge_attribute_cb=None,
):
    """Read a graph in DOT format from an input string.

    For a description of the format see https://en.wikipedia.org/wiki/DOT_language and 
    http://www.graphviz.org/doc/info/lang.html .

    The provided graph object, where the imported graph will be stored, must be able to support the
    features of the graph that is read. For example if the file contains self-loops then the graph
    provided must also support self-loops. The same for multiple edges. Whether edges are directed or
    not depends on the underlying implementation of the user provided graph object.

    The graph vertices and edges are build automatically by the graph. The id of the vertices in the
    input file are reported as a vertex attribute named "ID". The user can also bypass vertex creation
    by providing a import identifier callback. This callback accepts as a parameter the vertex identifier
    read from file and should return the new vertex.

    .. note:: The import identifier callback accepts a single parameter which is the identifier read
              from the input file as a string. It should return a long integer with the identifier of the 
              graph vertex.

    .. note:: Attribute callback functions accept three parameters. The first is the vertex
              or edge identifier. The second is the attribute key and the third is the 
              attribute value.

    :param graph: the graph to read into
    :param input_string: the input string to read from
    :param import_id_cb: callback to transform identifiers from file to long integer vertices. Can be 
                         None to allow the graph to assign identifiers to new vertices.                   
    :param vertex_attribute_cb: callback function for vertex attributes
    :param edge_attribute_cb: callback function for edge attributes
    :raises IOError: in case of an import error 
    """
    import_id_cb_ctype = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_char_p)
    import_id_f_ptr, _ = _create_wrapped_callback(import_id_cb, import_id_cb_ctype)

    callback_ctype = ctypes.CFUNCTYPE(
        None, ctypes.c_int, ctypes.c_char_p, ctypes.c_char_p
    )
    vertex_attribute_f_ptr, _ = _create_wrapped_callback(
        vertex_attribute_cb, callback_ctype
    )
    edge_attribute_f_ptr, _ = _create_wrapped_callback(
        edge_attribute_cb, callback_ctype
    )

    args = [ import_id_f_ptr, vertex_attribute_f_ptr, edge_attribute_f_ptr ]
    return _import("string_dot", graph, input_string, *args)


def read_graph6sparse6(
    graph,
    filename,
    import_id_cb=None,
    vertex_attribute_cb=None,
    edge_attribute_cb=None,
):
    """Read a graph in graph6 or sparse6 format.

    See https://users.cecs.anu.edu.au/~bdm/data/formats.txt for a description of the format. Both graph6
    and sparse6 are formats for storing undirected graphs, using a small number of printable ASCII
    characters. Graph6 is suitable for small graphs or large dense graphs while sparse6 is better for 
    large sparse graphs. Moreover, sparse6 supports self-loops and multiple-edges while graph6 does not.

    The provided graph object, where the imported graph will be stored, must be able to support the
    features of the graph that is read. For example if the file contains self-loops then the graph
    provided must also support self-loops. The same for multiple edges. Whether edges are directed or
    not depends on the underlying implementation of the user provided graph object.

    The graph vertices and edges are build automatically by the graph. The id of the vertices in the
    input file are reported as a vertex attribute named "ID". The user can also bypass vertex creation
    by providing a import identifier callback. This callback accepts as a parameter the vertex identifier
    read from file and should return the new vertex.

    .. note:: The import identifier callback accepts a single parameter which is the identifier read
              from the input file as a string. It should return a long integer with the identifier of the 
              graph vertex.

    .. note:: Attribute callback functions accept three parameters. The first is the vertex
              or edge identifier. The second is the attribute key and the third is the 
              attribute value.

    :param graph: the graph to read into
    :param filename: filename to read from
    :param import_id_cb: callback to transform identifiers from file to long integer vertices. Can be 
                         None to allow the graph to assign identifiers to new vertices.                   
    :param vertex_attribute_cb: callback function for vertex attributes
    :param edge_attribute_cb: callback function for edge attributes
    :raises IOError: in case of an import error 
    """
    import_id_cb_ctype = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_char_p)
    import_id_f_ptr, _ = _create_wrapped_callback(import_id_cb, import_id_cb_ctype)

    callback_ctype = ctypes.CFUNCTYPE(
        None, ctypes.c_int, ctypes.c_char_p, ctypes.c_char_p
    )
    vertex_attribute_f_ptr, _ = _create_wrapped_callback(
        vertex_attribute_cb, callback_ctype
    )
    edge_attribute_f_ptr, _ = _create_wrapped_callback(
        edge_attribute_cb, callback_ctype
    )

    args = [ import_id_f_ptr, vertex_attribute_f_ptr, edge_attribute_f_ptr ]
    return _import("file_graph6sparse6", graph, filename, *args)    


def parse_graph6sparse6(
    graph,
    input_string,
    import_id_cb=None,
    vertex_attribute_cb=None,
    edge_attribute_cb=None,
):
    """Read a graph in graph6 or sparse6 format from a string.

    See https://users.cecs.anu.edu.au/~bdm/data/formats.txt for a description of the format. Both
    graph6 and sparse6 are formats for storing undirected graphs, using a small number of printable
    ASCII characters. Graph6 is suitable for small graphs or large dense graphs while sparse6 is
    better for large sparse graphs. Moreover, sparse6 supports self-loops and multiple-edges while
    graph6 does not.

    The provided graph object, where the imported graph will be stored, must be able to support
    the features of the graph that is read. For example if the file contains self-loops then the
    graph provided must also support self-loops. The same for multiple edges. Whether edges are
    directed or not depends on the underlying implementation of the user provided graph object.

    The graph vertices and edges are build automatically by the graph. The id of the vertices in
    the input file are reported as a vertex attribute named "ID". The user can also bypass vertex
    creation by providing a import identifier callback. This callback accepts as a parameter the
    vertex identifier read from file and should return the new vertex.

    .. note:: The import identifier callback accepts a single parameter which is the identifier
              read from the input file as a string. It should return a long integer with the
              identifier of the graph vertex.

    .. note:: Attribute callback functions accept three parameters. The first is the vertex
              or edge identifier. The second is the attribute key and the third is the 
              attribute value.

    :param graph: the graph to read into
    :param input_string: the input string
    :param import_id_cb: callback to transform identifiers from file to long integer vertices.
        Can be None to allow the graph to assign identifiers to new vertices.                   
    :param vertex_attribute_cb: callback function for vertex attributes
    :param edge_attribute_cb: callback function for edge attributes
    :raises IOError: in case of an import error 
    """
    import_id_cb_ctype = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_char_p)
    import_id_f_ptr, _ = _create_wrapped_callback(import_id_cb, import_id_cb_ctype)

    callback_ctype = ctypes.CFUNCTYPE(
        None, ctypes.c_int, ctypes.c_char_p, ctypes.c_char_p
    )
    vertex_attribute_f_ptr, _ = _create_wrapped_callback(
        vertex_attribute_cb, callback_ctype
    )
    edge_attribute_f_ptr, _ = _create_wrapped_callback(
        edge_attribute_cb, callback_ctype
    )

    args = [ import_id_f_ptr, vertex_attribute_f_ptr, edge_attribute_f_ptr ]
    return _import("string_graph6sparse6", graph, input_string, *args)    
