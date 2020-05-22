from .. import backend

from .._internals._collections import _JGraphTEdgeTripleList
from .._internals._ioutils import _create_wrapped_import_id_callback
from .._internals._ioutils import _create_wrapped_attribute_callback


def _import_edgelist(name, with_attrs, filename_or_string, *args):
    alg_method_name = "jgrapht_import_edgelist_"
    if with_attrs:
        alg_method_name += 'attrs_'
    else:
        alg_method_name += 'noattrs_'
    alg_method_name += name

    try:
        alg_method = getattr(backend, alg_method_name)
    except AttributeError:
        raise NotImplementedError("Algorithm {} not supported.".format(name))

    filename_or_string_as_bytearray = bytearray(filename_or_string, encoding="utf-8")

    res = alg_method(filename_or_string_as_bytearray, *args)
    return _JGraphTEdgeTripleList(res)


def read_edgelist_json(
    filename, import_id_cb, vertex_attribute_cb=None, edge_attribute_cb=None
):
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
              from the input file as a string. It should return a integer with the identifier of the 
              graph vertex.

    .. note:: Attribute callback functions accept three parameters. The first is the vertex
              or edge identifier. The second is the attribute key and the third is the 
              attribute value.

    :param filename: Filename to read from
    :param import_id_cb: Callback to transform identifiers from file to integer vertices.
    :param vertex_attribute_cb: Callback function for vertex attributes
    :param edge_attribute_cb: Callback function for edge attributes
    :returns: an edge list. This is an iterator which returns named tuples(source, target, weight)
    :raises IOError: In case of an import error    
    """
    import_id_f_ptr, _ = _create_wrapped_import_id_callback(import_id_cb)

    if vertex_attribute_cb is None and edge_attribute_cb is None: 
        with_attrs = False
        args = [import_id_f_ptr]
    else:
        with_attrs = True
        vertex_attribute_f_ptr, _ = _create_wrapped_attribute_callback(vertex_attribute_cb)
        edge_attribute_f_ptr, _ = _create_wrapped_attribute_callback(edge_attribute_cb)
        args = [import_id_f_ptr, vertex_attribute_f_ptr, edge_attribute_f_ptr]

    return _import_edgelist('file_json', with_attrs, filename, *args)


def parse_edgelist_json(
    input_string,
    import_id_cb,
    vertex_attribute_cb=None,
    edge_attribute_cb=None,
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
              from the input file as a string. It should return a integer with the identifier of the 
              graph vertex.

    .. note:: Attribute callback functions accept three parameters. The first is the vertex
              or edge identifier. The second is the attribute key and the third is the 
              attribute value.

    :param input_string: The input string to read from
    :param import_id_cb: Callback to transform identifiers from file to integer vertices.  
    :param vertex_attribute_cb: Callback function for vertex attributes
    :param edge_attribute_cb: Callback function for edge attributes
    :returns: an edge list. This is an iterator which returns named tuples(source, target, weight)    
    :raises IOError: In case of an import error    
    """
    import_id_f_ptr, _ = _create_wrapped_import_id_callback(import_id_cb)

    if vertex_attribute_cb is None and edge_attribute_cb is None: 
        with_attrs = False
        args = [import_id_f_ptr]
    else:
        with_attrs = True
        vertex_attribute_f_ptr, _ = _create_wrapped_attribute_callback(vertex_attribute_cb)
        edge_attribute_f_ptr, _ = _create_wrapped_attribute_callback(edge_attribute_cb)
        args = [import_id_f_ptr, vertex_attribute_f_ptr, edge_attribute_f_ptr]

    return _import_edgelist('string_json', with_attrs, input_string, *args)
