from collections import defaultdict

from .. import backend as _backend
from .. import GraphBackend as _GraphBackend

from ._callbacks_graph import (
    _create_import_id_wrapper,
    _create_attribute_callback_wrapper,
    _create_notify_id_callback_wrapper,
)

from ._ioutils import _create_wrapped_import_integer_id_callback
from ._ioutils import _create_wrapped_import_string_id_callback
from ._ioutils import _create_wrapped_attribute_callback
from ._ioutils import _create_wrapped_notify_id_callback


def _create_import_method(graph, read_from, format):
    if graph._backend_type == _GraphBackend.REF_GRAPH:
        graph_type = "rr"
    elif graph._backend_type == _GraphBackend.LONG_GRAPH:
        graph_type = "ll"
    else:
        graph_type = "ii"
    method_name = "jgrapht_{}_import_{}_{}".format(graph_type, read_from, format)
    return getattr(_backend, method_name)


def _create_callback_wrappers(
    graph,
    import_id_cb,
    vertex_attribute_cb,
    edge_attribute_cb,
    vertex_notify_id_cb,
    edge_notify_id_cb,
    integer_input_ids,
    populate_graph_with_attributes
):
    import_id_wrapper = _create_import_id_wrapper(
        graph, callback=import_id_cb, integer_input_ids=integer_input_ids
    )

    if populate_graph_with_attributes: 
        def use_vertex_attribute_cb(vertex, key, value): 
            graph.vertex_attrs[vertex][key] = value
    else:
        use_vertex_attribute_cb = vertex_attribute_cb

    vertex_attribute_wrapper = _create_attribute_callback_wrapper(
        graph, use_vertex_attribute_cb
    )

    if populate_graph_with_attributes: 
        def use_edge_attribute_cb(edge, key, value):
            if key == "weight":
                try: 
                    graph.edge_attrs[edge][key] = float(value)
                except ValueError:
                    pass
            else:
                graph.edge_attrs[edge][key] = value
    else:
        use_edge_attribute_cb = edge_attribute_cb

    edge_attribute_wrapper = _create_attribute_callback_wrapper(
        graph, use_edge_attribute_cb
    )
    
    vertex_notify_id_wrapper = _create_notify_id_callback_wrapper(
        graph, vertex_notify_id_cb
    )
    edge_notify_id_wrapper = _create_notify_id_callback_wrapper(
        graph, edge_notify_id_cb
    )
    return (
        import_id_wrapper,
        vertex_attribute_wrapper,
        edge_attribute_wrapper,
        vertex_notify_id_wrapper,
        edge_notify_id_wrapper,
    )


def _create_graph_callbacks(
    import_id_cb,
    vertex_attribute_cb,
    edge_attribute_cb,
    vertex_notify_id_cb,
    edge_notify_id_cb,
    integer_ids=False,
):
    if integer_ids:
        import_id_f_ptr, import_id_f = _create_wrapped_import_integer_id_callback(
            import_id_cb
        )
    else:
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


def _parse_graph_dimacs(
    graph,
    input,
    import_id_cb=None,
    input_is_filename=False,
):
    (
        import_id_f_ptr,
        import_id_f,  # pylint: disable=unused-variable
        _,
        _,
        _,
        _,
        vertex_notify_f_ptr,
        vertex_notify_f,  # pylint: disable=unused-variable
        edge_notify_f_ptr,
        edge_notify_f,  # pylint: disable=unused-variable
    ) = _create_graph_callbacks(
        import_id_cb=import_id_cb,
        vertex_attribute_cb=None,
        edge_attribute_cb=None,
        vertex_notify_id_cb=None,
        edge_notify_id_cb=None,
        integer_ids=True,
    )

    string_as_bytearray = bytearray(input, encoding="utf-8")

    if input_is_filename:
        backend_function = _backend.jgrapht_ii_import_file_dimacs
    else:
        backend_function = _backend.jgrapht_ii_import_string_dimacs

    backend_function(
        graph.handle,
        string_as_bytearray,
        import_id_f_ptr,
        vertex_notify_f_ptr,
        edge_notify_f_ptr,
    )


def _parse_graph_gml(
    graph,
    input,
    import_id_cb=None,
    vertex_attribute_cb=None,
    edge_attribute_cb=None,
    input_is_filename=False,
):
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
        integer_ids=True,
    )

    string_as_bytearray = bytearray(input, encoding="utf-8")

    if input_is_filename:
        backend_function = _backend.jgrapht_ii_import_file_gml
    else:
        backend_function = _backend.jgrapht_ii_import_string_gml

    backend_function(
        graph.handle,
        string_as_bytearray,
        import_id_f_ptr,
        vertex_attribute_f_ptr,
        edge_attribute_f_ptr,
        vertex_notify_f_ptr,
        edge_notify_f_ptr,
    )



CSV_FORMATS = dict(
    {
        "adjacencylist": _backend.CSV_FORMAT_ADJACENCY_LIST,
        "edgelist": _backend.CSV_FORMAT_EDGE_LIST,
        "matrix": _backend.CSV_FORMAT_MATRIX,
    }
)


def _parse_graph_csv(
    graph,
    input,
    import_id_cb=None,
    format="adjacencylist",
    import_edge_weights=False,
    matrix_format_node_id=False,
    matrix_format_zero_when_noedge=True,
    input_is_filename=False,
):
    (
        import_id_f_ptr,
        import_id_f,  # pylint: disable=unused-variable
        _,
        _,
        _,
        _,
        vertex_notify_f_ptr,
        vertex_notify_f,  # pylint: disable=unused-variable
        edge_notify_f_ptr,
        edge_notify_f,  # pylint: disable=unused-variable
    ) = _create_graph_callbacks(
        import_id_cb=import_id_cb,
        vertex_attribute_cb=None,
        edge_attribute_cb=None,
        vertex_notify_id_cb=None,
        edge_notify_id_cb=None,
    )

    string_as_bytearray = bytearray(input, encoding="utf-8")

    if input_is_filename:
        backend_function = _backend.jgrapht_ii_import_file_csv
    else:
        backend_function = _backend.jgrapht_ii_import_string_csv

    backend_function(
        graph.handle,
        string_as_bytearray,
        import_id_f_ptr,
        vertex_notify_f_ptr,
        edge_notify_f_ptr,
        CSV_FORMATS.get(format, _backend.CSV_FORMAT_EDGE_LIST),
        import_edge_weights,
        matrix_format_node_id,
        matrix_format_zero_when_noedge,
    )


def _parse_graph(
    graph_format,
    graph,
    input,
    integer_input_ids,
    import_id_cb,
    vertex_attribute_cb,
    edge_attribute_cb,
    populate_graph_with_attributes,
    input_is_filename,
    *args
):
    (
        import_id_wrapper,
        vertex_attribute_wrapper,
        edge_attribute_wrapper,
        vertex_notify_id_wrapper,
        edge_notify_id_wrapper,
    ) = _create_callback_wrappers(
        graph,
        import_id_cb=import_id_cb,
        vertex_attribute_cb=vertex_attribute_cb,
        edge_attribute_cb=edge_attribute_cb,
        vertex_notify_id_cb=None,
        edge_notify_id_cb=None,
        integer_input_ids=integer_input_ids,
        populate_graph_with_attributes=populate_graph_with_attributes,
    )

    backend_method = _create_import_method(
        graph, "file" if input_is_filename else "string", graph_format
    )

    backend_method(
        graph.handle,
        bytearray(input, encoding="utf-8"),
        import_id_wrapper.fptr,
        vertex_attribute_wrapper.fptr,
        edge_attribute_wrapper.fptr,
        vertex_notify_id_wrapper.fptr,
        edge_notify_id_wrapper.fptr,
        *args
    )

    
