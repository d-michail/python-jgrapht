from collections import defaultdict

from .. import backend as _backend

from ._ioutils import _create_wrapped_import_integer_id_callback
from ._ioutils import _create_wrapped_import_string_id_callback
from ._ioutils import _create_wrapped_attribute_callback
from ._ioutils import _create_wrapped_notify_id_callback


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


def _create_anyhashable_graph_callbacks(
    graph,
    vertex_id_to_hash,
    vertex_id_to_attrs,
    edge_id_to_hash,
    edge_id_to_attrs,
    import_id_cb,
    integer_ids=False,
    include_weights=False,
):
    next_vertex_id = max(graph._graph.vertices, default=-1) + 1

    if import_id_cb is None:
        use_import_id_cb = None

        def use_vertex_notify_id_cb(vid):
            vertex_id_to_hash[vid] = graph.vertex_supplier()

    else:

        def use_import_id_cb(id_from_file):
            # We assume that the user callback accepts the id from file and returns any hashable
            nonlocal next_vertex_id
            new_vertex = next_vertex_id
            next_vertex_id += 1
            vertex_id_to_hash[new_vertex] = import_id_cb(id_from_file)
            return new_vertex

        use_vertex_notify_id_cb = None

    def use_edge_notify_id_cb(eid):
        edge_id_to_hash[eid] = graph.edge_supplier()

    def use_vertex_attribute_cb(id, key, value):
        vertex_id_to_attrs[id][key] = value

    def use_edge_attribute_cb(id, key, value):
        if key != "weight" or include_weights:
            edge_id_to_attrs[id][key] = value

    if integer_ids:
        import_id_f_ptr, import_id_f = _create_wrapped_import_integer_id_callback(
            use_import_id_cb
        )
    else:
        import_id_f_ptr, import_id_f = _create_wrapped_import_string_id_callback(
            use_import_id_cb
        )

    vertex_attribute_f_ptr, vertex_attribute_f = _create_wrapped_attribute_callback(
        use_vertex_attribute_cb
    )
    edge_attribute_f_ptr, edge_attribute_f = _create_wrapped_attribute_callback(
        use_edge_attribute_cb
    )
    vertex_notify_f_ptr, vertex_notify_f = _create_wrapped_notify_id_callback(
        use_vertex_notify_id_cb
    )
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


def _populate_anyhashable(
    graph, vertex_id_to_hash, vertex_id_to_attrs, edge_id_to_hash, edge_id_to_attrs
):
    # After creating, populate the any-hashable graph with the new vertices and edges
    for vid, vhash in vertex_id_to_hash.items():
        graph._add_new_vertex(vid, vhash)
        for key, value in vertex_id_to_attrs[vid].items():
            graph.vertex_attrs[vhash][key] = value

    for eid, ehash in edge_id_to_hash.items():
        graph._add_new_edge(eid, ehash)
        for key, value in edge_id_to_attrs[eid].items():
            graph.edge_attrs[ehash][key] = value


def _parse_graph_dimacs(
    graph, input, import_id_cb=None, input_is_filename=False,
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
        backend_function = _backend.jgrapht_import_file_dimacs
    else:
        backend_function = _backend.jgrapht_import_string_dimacs

    backend_function(
        graph.handle,
        string_as_bytearray,
        import_id_f_ptr,
        vertex_notify_f_ptr,
        edge_notify_f_ptr,
    )


def _parse_anyhashable_graph_dimacs(
    graph, input_string, import_id_cb, input_is_filename=False
):
    idmaps = ({}, defaultdict(lambda: {}), {}, defaultdict(lambda: {}))

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
    ) = _create_anyhashable_graph_callbacks(
        graph, *idmaps, import_id_cb, integer_ids=True
    )

    string_as_bytearray = bytearray(input_string, encoding="utf-8")

    if input_is_filename:
        backend_function = _backend.jgrapht_import_file_dimacs
    else:
        backend_function = _backend.jgrapht_import_string_dimacs

    backend_function(
        graph._graph.handle,
        string_as_bytearray,
        import_id_f_ptr,
        vertex_notify_f_ptr,
        edge_notify_f_ptr,
    )

    _populate_anyhashable(graph, *idmaps)


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
        backend_function = _backend.jgrapht_import_file_gml
    else:
        backend_function = _backend.jgrapht_import_string_gml

    backend_function(
        graph.handle,
        string_as_bytearray,
        import_id_f_ptr,
        vertex_attribute_f_ptr,
        edge_attribute_f_ptr,
        vertex_notify_f_ptr,
        edge_notify_f_ptr,
    )


def _parse_anyhashable_graph_gml(
    graph, input_string, import_id_cb, input_is_filename=False,
):
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
    ) = _create_anyhashable_graph_callbacks(
        graph, *idmaps, import_id_cb, integer_ids=True
    )

    string_as_bytearray = bytearray(input_string, encoding="utf-8")

    if input_is_filename:
        backend_function = _backend.jgrapht_import_file_gml
    else:
        backend_function = _backend.jgrapht_import_string_gml

    backend_function(
        graph._graph.handle,
        string_as_bytearray,
        import_id_f_ptr,
        vertex_attribute_f_ptr,
        edge_attribute_f_ptr,
        vertex_notify_f_ptr,
        edge_notify_f_ptr,
    )

    _populate_anyhashable(graph, *idmaps)


def _parse_graph_json(
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


def _parse_anyhashable_graph_json(
    graph, input_string, import_id_cb, input_is_filename=False
):
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
    ) = _create_anyhashable_graph_callbacks(graph, *idmaps, import_id_cb,)

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

    _populate_anyhashable(graph, *idmaps)


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
        backend_function = _backend.jgrapht_import_file_csv
    else:
        backend_function = _backend.jgrapht_import_string_csv

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


def _parse_anyhashable_graph_csv(
    graph,
    input_string,
    import_id_cb,
    format="adjacencylist",
    import_edge_weights=False,
    matrix_format_node_id=False,
    matrix_format_zero_when_noedge=True,
    input_is_filename=False,
):
    idmaps = ({}, defaultdict(lambda: {}), {}, defaultdict(lambda: {}))

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
    ) = _create_anyhashable_graph_callbacks(graph, *idmaps, import_id_cb)

    string_as_bytearray = bytearray(input_string, encoding="utf-8")

    if input_is_filename:
        backend_function = _backend.jgrapht_import_file_csv
    else:
        backend_function = _backend.jgrapht_import_string_csv

    backend_function(
        graph._graph.handle,
        string_as_bytearray,
        import_id_f_ptr,
        vertex_notify_f_ptr,
        edge_notify_f_ptr,
        CSV_FORMATS.get(format, _backend.CSV_FORMAT_EDGE_LIST),
        import_edge_weights,
        matrix_format_node_id,
        matrix_format_zero_when_noedge,
    )

    _populate_anyhashable(graph, *idmaps)


def _parse_graph_gexf(
    graph,
    input,
    import_id_cb=None,
    vertex_attribute_cb=None,
    edge_attribute_cb=None,
    input_is_filename=False,
    validate_schema=True,
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
    )

    string_as_bytearray = bytearray(input, encoding="utf-8")

    if input_is_filename:
        backend_function = _backend.jgrapht_import_file_gexf
    else:
        backend_function = _backend.jgrapht_import_string_gexf

    backend_function(
        graph.handle,
        string_as_bytearray,
        import_id_f_ptr,
        validate_schema,
        vertex_attribute_f_ptr,
        edge_attribute_f_ptr,
        vertex_notify_f_ptr,
        edge_notify_f_ptr,
    )


def _parse_anyhashable_graph_gexf(
    graph, input_string, import_id_cb, input_is_filename=False, validate_schema=True,
):
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
    ) = _create_anyhashable_graph_callbacks(graph, *idmaps, import_id_cb)

    string_as_bytearray = bytearray(input_string, encoding="utf-8")

    if input_is_filename:
        backend_function = _backend.jgrapht_import_file_gexf
    else:
        backend_function = _backend.jgrapht_import_string_gexf

    backend_function(
        graph._graph.handle,
        string_as_bytearray,
        import_id_f_ptr,
        validate_schema,
        vertex_attribute_f_ptr,
        edge_attribute_f_ptr,
        vertex_notify_f_ptr,
        edge_notify_f_ptr,
    )

    _populate_anyhashable(graph, *idmaps)


def _parse_graph_dot(
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
    )

    string_as_bytearray = bytearray(input, encoding="utf-8")

    if input_is_filename:
        backend_function = _backend.jgrapht_import_file_dot
    else:
        backend_function = _backend.jgrapht_import_string_dot

    backend_function(
        graph.handle,
        string_as_bytearray,
        import_id_f_ptr,
        vertex_attribute_f_ptr,
        edge_attribute_f_ptr,
        vertex_notify_f_ptr,
        edge_notify_f_ptr,
    )


def _parse_anyhashable_graph_dot(
    graph, input_string, import_id_cb, input_is_filename=False,
):
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
    ) = _create_anyhashable_graph_callbacks(graph, *idmaps, import_id_cb)

    string_as_bytearray = bytearray(input_string, encoding="utf-8")

    if input_is_filename:
        backend_function = _backend.jgrapht_import_file_dot
    else:
        backend_function = _backend.jgrapht_import_string_dot

    backend_function(
        graph._graph.handle,
        string_as_bytearray,
        import_id_f_ptr,
        vertex_attribute_f_ptr,
        edge_attribute_f_ptr,
        vertex_notify_f_ptr,
        edge_notify_f_ptr,
    )

    _populate_anyhashable(graph, *idmaps)


def _parse_graph_graph6sparse6(
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
    )

    string_as_bytearray = bytearray(input, encoding="utf-8")

    if input_is_filename:
        backend_function = _backend.jgrapht_import_file_graph6sparse6
    else:
        backend_function = _backend.jgrapht_import_string_graph6sparse6

    backend_function(
        graph.handle,
        string_as_bytearray,
        import_id_f_ptr,
        vertex_attribute_f_ptr,
        edge_attribute_f_ptr,
        vertex_notify_f_ptr,
        edge_notify_f_ptr,
    )


def _parse_anyhashable_graph_graph6sparse6(
    graph, input_string, import_id_cb, input_is_filename=False,
):
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
    ) = _create_anyhashable_graph_callbacks(graph, *idmaps, import_id_cb)

    string_as_bytearray = bytearray(input_string, encoding="utf-8")

    if input_is_filename:
        backend_function = _backend.jgrapht_import_file_graph6sparse6
    else:
        backend_function = _backend.jgrapht_import_string_graph6sparse6

    backend_function(
        graph._graph.handle,
        string_as_bytearray,
        import_id_f_ptr,
        vertex_attribute_f_ptr,
        edge_attribute_f_ptr,
        vertex_notify_f_ptr,
        edge_notify_f_ptr,
    )

    _populate_anyhashable(graph, *idmaps)


def _parse_graph_graphml(
    graph,
    input,
    import_id_cb=None,
    vertex_attribute_cb=None,
    edge_attribute_cb=None,
    input_is_filename=False,
    validate_schema=True,
    simple=True,
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
    )

    string_as_bytearray = bytearray(input, encoding="utf-8")

    if input_is_filename:
        if simple:
            backend_function = _backend.jgrapht_import_file_graphml_simple
        else:
            backend_function = _backend.jgrapht_import_file_graphml
    else:
        if simple:
            backend_function = _backend.jgrapht_import_string_graphml_simple
        else:
            backend_function = _backend.jgrapht_import_string_graphml

    backend_function(
        graph.handle,
        string_as_bytearray,
        import_id_f_ptr,
        validate_schema,
        vertex_attribute_f_ptr,
        edge_attribute_f_ptr,
        vertex_notify_f_ptr,
        edge_notify_f_ptr,
    )


def _parse_anyhashable_graph_graphml(
    graph,
    input_string,
    import_id_cb,
    input_is_filename=False,
    validate_schema=True,
    simple=True,
):
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
    ) = _create_anyhashable_graph_callbacks(graph, *idmaps, import_id_cb)

    string_as_bytearray = bytearray(input_string, encoding="utf-8")

    if input_is_filename:
        if simple:
            backend_function = _backend.jgrapht_import_file_graphml_simple
        else:
            backend_function = _backend.jgrapht_import_file_graphml
    else:
        if simple:
            backend_function = _backend.jgrapht_import_string_graphml_simple
        else:
            backend_function = _backend.jgrapht_import_string_graphml

    backend_function(
        graph._graph.handle,
        string_as_bytearray,
        import_id_f_ptr,
        validate_schema,
        vertex_attribute_f_ptr,
        edge_attribute_f_ptr,
        vertex_notify_f_ptr,
        edge_notify_f_ptr,
    )

    _populate_anyhashable(graph, *idmaps)
