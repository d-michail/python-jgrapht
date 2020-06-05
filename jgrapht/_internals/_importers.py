from collections import defaultdict

from .. import backend as _backend

from ._ioutils import _create_wrapped_import_integer_id_callback
from ._ioutils import _create_wrapped_import_string_id_callback
from ._ioutils import _create_wrapped_attribute_callback
from ._ioutils import _create_wrapped_notify_id_callback

from ._pg import is_property_graph


def _create_graph_callbacks(
    import_id_cb,
    vertex_attribute_cb,
    edge_attribute_cb,
    vertex_notify_id_cb,
    edge_notify_id_cb,
):
    import_id_f_ptr, import_id_f = _create_wrapped_import_string_id_callback(
        import_id_cb
    )
    vertex_attribute_f_ptr, vertex_attribute_f = _create_wrapped_attribute_callback(
        vertex_attribute_cb
    )
    edge_attribute_f_ptr, edge_attribute_f = _create_wrapped_attribute_callback(
        edge_attribute_cb
    )
    vertex_notify_f_ptr, vertex_notify_f = _create_wrapped_notify_id_callback(
        vertex_notify_id_cb
    )
    edge_notify_f_ptr, edge_notify_f = _create_wrapped_notify_id_callback(
        edge_notify_id_cb
    )

    return (
        import_id_f_ptr,
        import_id_f,
        vertex_attribute_f_ptr,
        vertex_attribute_f,
        edge_attribute_f_ptr,
        edge_attribute_f,
        vertex_notify_f_ptr,
        vertex_notify_f,
        edge_notify_f_ptr,
        edge_notify_f,
    )


def _create_property_graph_callbacks(
    graph,
    vertex_id_to_hash,
    vertex_id_to_props,
    edge_id_to_hash,
    edge_id_to_props,
    import_id_cb,
):
    next_vertex_id = max(graph._graph.vertices, default=-1) + 1

    def use_import_id_cb(id_from_file):
        # We assume that the user callback accepts the id from file and returns any hashable
        nonlocal next_vertex_id
        new_vertex = next_vertex_id
        next_vertex_id += 1
        vertex_id_to_hash[new_vertex] = import_id_cb(id_from_file)
        return new_vertex

    def use_edge_notify_id_cb(eid):
        edge_id_to_hash[eid] = graph.edge_supplier()

    def use_vertex_attribute_cb(id, key, value):
        vertex_id_to_props[id][key] = value

    def use_edge_attribute_cb(id, key, value):
        edge_id_to_props[id][key] = value

    import_id_f_ptr, import_id_f = _create_wrapped_import_string_id_callback(
        use_import_id_cb
    )
    vertex_attribute_f_ptr, vertex_attribute_f = _create_wrapped_attribute_callback(
        use_vertex_attribute_cb
    )
    edge_attribute_f_ptr, edge_attribute_f = _create_wrapped_attribute_callback(
        use_edge_attribute_cb
    )
    vertex_notify_f_ptr, vertex_notify_f = _create_wrapped_notify_id_callback(None)
    edge_notify_f_ptr, edge_notify_f = _create_wrapped_notify_id_callback(
        use_edge_notify_id_cb
    )

    return (
        import_id_f_ptr,
        import_id_f,
        vertex_attribute_f_ptr,
        vertex_attribute_f,
        edge_attribute_f_ptr,
        edge_attribute_f,
        vertex_notify_f_ptr,
        vertex_notify_f,
        edge_notify_f_ptr,
        edge_notify_f,
    )


def _populate_properties(
    graph, vertex_id_to_hash, vertex_id_to_props, edge_id_to_hash, edge_id_to_props
):
    # After creating, populate the property graph with the new vertices and edges
    for vid, vhash in vertex_id_to_hash.items():
        graph._add_new_vertex(vid, vhash)
        for key, value in vertex_id_to_props[vid].items():
            graph.vertex_props[vhash][key] = value

    for eid, ehash in edge_id_to_hash.items():
        graph._add_new_edge(eid, ehash)
        for key, value in edge_id_to_props[eid].items():
            graph.edge_props[ehash][key] = value


def _parse_graph_json(
    graph,
    input,
    import_id_cb=None,
    vertex_attribute_cb=None,
    edge_attribute_cb=None,
    input_is_filename=False,
):
    if is_property_graph(graph):
        raise ValueError("Property graphs not supported")

    (
        import_id_f_ptr,
        import_id_f,  # pylint: disable=unused-variable
        vertex_attribute_f_ptr,
        vertex_attribute_f,  # pylint: disable=unused-variable
        edge_attribute_f_ptr,
        edge_attribute_f,  # pylint: disable=unused-variable
        vertex_notify_f_ptr,
        vertex_notify_f,  # pylint: disable=unused-variable
        edge_notify_f_ptr,
        edge_notify_f,  # pylint: disable=unused-variable
    ) = _create_graph_callbacks(
        import_id_cb=import_id_cb,
        vertex_attribute_cb=vertex_attribute_cb,
        edge_attribute_cb=edge_attribute_cb,
        vertex_notify_id_cb=None,
        edge_notify_id_cb=None,
    )

    string_as_bytearray = bytearray(input, encoding="utf-8")

    if input_is_filename:
        backend_function = _backend.jgrapht_import_file_json
    else:
        backend_function = _backend.jgrapht_import_string_json

    backend_function(
        graph.handle,
        string_as_bytearray,
        import_id_f_ptr,
        vertex_attribute_f_ptr,
        edge_attribute_f_ptr,
        vertex_notify_f_ptr,
        edge_notify_f_ptr,
    )


def _parse_property_graph_json(graph, input_string, import_id_cb, input_is_filename=False):

    if not is_property_graph(graph):
        raise ValueError("Only property graphs supported")

    idmaps = ({}, defaultdict(lambda: {}), {}, defaultdict(lambda: {}))

    (
        import_id_f_ptr,
        import_id_f,  # pylint: disable=unused-variable
        vertex_attribute_f_ptr,
        vertex_attribute_f,  # pylint: disable=unused-variable
        edge_attribute_f_ptr,
        edge_attribute_f,  # pylint: disable=unused-variable
        vertex_notify_f_ptr,
        vertex_notify_f,  # pylint: disable=unused-variable
        edge_notify_f_ptr,
        edge_notify_f,  # pylint: disable=unused-variable
    ) = _create_property_graph_callbacks(graph, *idmaps, import_id_cb,)

    string_as_bytearray = bytearray(input_string, encoding="utf-8")

    if input_is_filename:
        backend_function = _backend.jgrapht_import_file_json
    else:
        backend_function = _backend.jgrapht_import_string_json

    backend_function(
        graph._graph.handle,
        string_as_bytearray,
        import_id_f_ptr,
        vertex_attribute_f_ptr,
        edge_attribute_f_ptr,
        vertex_notify_f_ptr,
        edge_notify_f_ptr,
    )

    _populate_properties(graph, *idmaps)
