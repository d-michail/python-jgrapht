import time
import ctypes

from .. import backend
from ..exceptions import UnsupportedOperationError
from .._errors import raise_status
from .._wrappers import JGraphTLongIterator, JGraphTGraphPath, JGraphTAttributeStore


def _import(name, graph, filename_or_string, *args):
    alg_method_name = "jgrapht_import_" + name

    try:
        alg_method = getattr(backend, alg_method_name)
    except AttributeError:
        raise UnsupportedOperationError("Algorithm {} not supported.".format(name))

    err = alg_method(graph.handle, filename_or_string, *args)
    if err:
        raise_status()


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
    :raises GraphImportError: In case of an import error 
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
    :raises GraphImportError: In case of an import error 
    """
    return _import("string_dimacs", graph, input_string, preserve_ids_from_input)


def read_gml(graph, filename, preserve_ids_from_input=True, vertex_attribute_cb=None, edge_attribute_cb=None):
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
    :raises GraphImportError: In case of an import error 
    """
    callback_ctype = ctypes.CFUNCTYPE(None, ctypes.c_longlong, ctypes.c_char_p, ctypes.c_char_p)
    vertex_attribute_f_ptr, _ = _create_wrapped_callback(vertex_attribute_cb, callback_ctype)
    edge_attribute_f_ptr, _ = _create_wrapped_callback(edge_attribute_cb, callback_ctype)

    args = [ preserve_ids_from_input, vertex_attribute_f_ptr, edge_attribute_f_ptr ]
    return _import("file_gml", graph, filename, *args)


def parse_gml(graph, input_string, preserve_ids_from_input=True, vertex_attribute_cb=None, edge_attribute_cb=None):
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
    :raises GraphImportError: In case of an import error 
    """
    callback_ctype = ctypes.CFUNCTYPE(None, ctypes.c_longlong, ctypes.c_char_p, ctypes.c_char_p)
    vertex_attribute_f_ptr, _ = _create_wrapped_callback(vertex_attribute_cb, callback_ctype)
    edge_attribute_f_ptr, _ = _create_wrapped_callback(edge_attribute_cb, callback_ctype)

    args = [ preserve_ids_from_input, vertex_attribute_f_ptr, edge_attribute_f_ptr ]
    return _import("string_gml", graph, input_string, *args)


def read_json(graph, filename, import_id_cb=None, vertex_attribute_cb=None, edge_attribute_cb=None):
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
    :raises GraphImportError: In case of an import error    
    """
    import_id_cb_ctype = ctypes.CFUNCTYPE(ctypes.c_longlong, ctypes.c_char_p)
    import_id_f_ptr, _ = _create_wrapped_callback(import_id_cb, import_id_cb_ctype)

    callback_ctype = ctypes.CFUNCTYPE(None, ctypes.c_longlong, ctypes.c_char_p, ctypes.c_char_p)
    vertex_attribute_f_ptr, _ = _create_wrapped_callback(vertex_attribute_cb, callback_ctype)
    edge_attribute_f_ptr, _ = _create_wrapped_callback(edge_attribute_cb, callback_ctype)

    args = [ import_id_f_ptr, vertex_attribute_f_ptr, edge_attribute_f_ptr ]
    return _import("file_json", graph, filename, *args)


def parse_json(graph, input_string, import_id_cb=None, vertex_attribute_cb=None, edge_attribute_cb=None):
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
    :raises GraphImportError: In case of an import error    
    """
    import_id_cb_ctype = ctypes.CFUNCTYPE(ctypes.c_longlong, ctypes.c_char_p)
    import_id_f_ptr, _ = _create_wrapped_callback(import_id_cb, import_id_cb_ctype)

    callback_ctype = ctypes.CFUNCTYPE(None, ctypes.c_longlong, ctypes.c_char_p, ctypes.c_char_p)
    vertex_attribute_f_ptr, _ = _create_wrapped_callback(vertex_attribute_cb, callback_ctype)
    edge_attribute_f_ptr, _ = _create_wrapped_callback(edge_attribute_cb, callback_ctype)

    args = [ import_id_f_ptr, vertex_attribute_f_ptr, edge_attribute_f_ptr]
    return _import("string_json", graph, input_string, *args)


CSV_FORMATS = dict(
    {
        "adjacencylist": backend.CSV_FORMAT_ADJACENCY_LIST,
        "edgelist": backend.CSV_FORMAT_EDGE_LIST,
        "matrix": backend.CSV_FORMAT_MATRIX,
    }
)


def read_csv(graph, filename, import_id_cb=None, format="edgelist", import_edge_weights=False, matrix_format_node_id=False, matrix_format_zero_when_noedge=True):

    import_id_cb_ctype = ctypes.CFUNCTYPE(ctypes.c_longlong, ctypes.c_char_p)
    import_id_f_ptr, _ = _create_wrapped_callback(import_id_cb, import_id_cb_ctype)

    format_to_use = CSV_FORMATS.get(format, backend.CSV_FORMAT_EDGE_LIST)
    args = [ import_id_f_ptr, format_to_use, import_edge_weights, matrix_format_node_id, matrix_format_zero_when_noedge ]

    return _import('file_csv', graph, filename, *args)


def parse_csv(graph, input_string, import_id_cb=None, format="edgelist", import_edge_weights=False, matrix_format_node_id=False, matrix_format_zero_when_noedge=True):

    import_id_cb_ctype = ctypes.CFUNCTYPE(ctypes.c_longlong, ctypes.c_char_p)
    import_id_f_ptr, _ = _create_wrapped_callback(import_id_cb, import_id_cb_ctype)

    format_to_use = CSV_FORMATS.get(format, backend.CSV_FORMAT_EDGE_LIST)
    args = [ import_id_f_ptr, format_to_use, import_edge_weights, matrix_format_node_id, matrix_format_zero_when_noedge ]

    return _import('string_csv', graph, input_string, *args)


def read_gexf(graph, filename, import_id_cb=None, validate_schema=True, vertex_attribute_cb=None, edge_attribute_cb=None):

    import_id_cb_ctype = ctypes.CFUNCTYPE(ctypes.c_longlong, ctypes.c_char_p)
    import_id_f_ptr, _ = _create_wrapped_callback(import_id_cb, import_id_cb_ctype)

    callback_ctype = ctypes.CFUNCTYPE(None, ctypes.c_longlong, ctypes.c_char_p, ctypes.c_char_p)
    vertex_attribute_f_ptr, _ = _create_wrapped_callback(vertex_attribute_cb, callback_ctype)
    edge_attribute_f_ptr, _ = _create_wrapped_callback(edge_attribute_cb, callback_ctype)

    args = [ import_id_f_ptr, validate_schema, vertex_attribute_f_ptr, edge_attribute_f_ptr ]

    return _import('file_gexf', graph, filename, *args)


def parse_gexf(graph, input_string, import_id_cb=None, validate_schema=True, vertex_attribute_cb=None, edge_attribute_cb=None):

    import_id_cb_ctype = ctypes.CFUNCTYPE(ctypes.c_longlong, ctypes.c_char_p)
    import_id_f_ptr, _ = _create_wrapped_callback(import_id_cb, import_id_cb_ctype)

    callback_ctype = ctypes.CFUNCTYPE(None, ctypes.c_longlong, ctypes.c_char_p, ctypes.c_char_p)
    vertex_attribute_f_ptr, _ = _create_wrapped_callback(vertex_attribute_cb, callback_ctype)
    edge_attribute_f_ptr, _ = _create_wrapped_callback(edge_attribute_cb, callback_ctype)

    args = [ import_id_f_ptr, validate_schema, vertex_attribute_f_ptr, edge_attribute_f_ptr ]

    return _import('string_gexf', graph, input_string, *args)
