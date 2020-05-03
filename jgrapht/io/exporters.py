import time
import ctypes

from .. import backend
from ..exceptions import UnsupportedOperationError
from .._errors import raise_status
from .._wrappers import JGraphTLongIterator, JGraphTGraphPath, JGraphTAttributeStore


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


def write_dimacs(graph, filename, format="shortestpath", export_edge_weights=False):
    format = DIMACS_FORMATS.get(format, backend.DIMACS_FORMAT_SHORTEST_PATH)
    custom = [format, export_edge_weights]
    return _export_to_file("dimacs", graph, filename, *custom)


def write_lemon(graph, filename, export_edge_weights=False, escape_strings=False):
    custom = [export_edge_weights, escape_strings]
    return _export_to_file("lemon", graph, filename, *custom)


def write_gml(
    graph,
    filename,
    export_edge_weights=False,
    per_vertex_attrs_dict=None,
    per_edge_attrs_dict=None,
):

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
