# I/O roadmap

Status of `read_graph`, `parse_graph`, `write_graph`, `graph_to_string` (`src/formats.rs`)
against the `jgrapht-io` crate. Each item is a self-contained issue: done means implemented,
tested, documented, merged. Update this file as items are closed.

## Issues

1. ~~**Reject options a format cannot use.**~~ *Done.* The attribute and id options (`vertex_attributes`,
   `edge_attributes`, `graph_attributes`, `graph_id`, `vertex_id`, `edge_id`) are consumed before
   the format is known, so formats without them (CSV, DIMACS, graph6, matrix, ...) silently drop
   them. They must raise `GraphError` like any unknown option. *Bug fix.*
2. ~~**Parity tests.**~~ *Done (`tests/test_io_parity.py`, fixtures in `tests/data`).* Port the documents and expected results of the `jgrapht-io` parity tests
   (`crates/jgrapht-io/tests`, derived from the Java suite; only three fixture files exist, the
   rest are inline) for every format, to catch parser differences that self-generated round trips
   cannot.
3. ~~**Missing option tests.**~~ *Done (`tests/test_formats.py`, `tests/test_io_parity.py`).* `matrix_zero_when_no_edge`, `escape_strings` (LEMON, GML), GEXF
   `edge_labels`/`edge_types`, `default_weight`, GraphML `edge_weight_attribute`,
   `vertex_labels`/`edge_labels`, graph6 `variant`, JSON collection names on import.
4. ~~**Directedness detection.**~~ *Done (`src/formats/sniff.rs`).* The scan for DOT/GML/GraphML/GEXF/DIMACS/digraph6 is textual.
   Make it robust against comments, quoted names and attribute order, and test awkward inputs.
5. ~~**Docs.**~~ *Done (`docs/api/io/`, `docs/tutorials/io.rst`).* A per-format option table, the `weighted=False` default and the `attributes=True`
   result described with examples, plus a tutorial section on I/O.
6. ~~**Explicit attribute registration (GraphML, GEXF).**~~ *Done.* Allow declaring attribute types, defaults
   and categories instead of inferring them from values, and custom label/weight attribute names.
7. ~~**DOT subgraphs/clusters on export.**~~ *Done (`subgraphs=`).*
8. ~~**GML vertex graphics blocks on export.**~~ *Done (`vertex_graphics=`).*
9. ~~**GEXF custom ids.**~~ *Done: jgrapht-io gained `set_vertex_id_provider` / `set_edge_id_provider`.*
10. ~~**TSPLIB tours.**~~ *Done (`read_tsplib_tour`, `parse_tsplib_tour`, `tsplib_geographic_distance`).* Read a separate tour file against a graph read earlier, and expose the
    geographic distance helper.
11. ~~**Importing into an existing graph**~~ *Done (`into=`).* Per-element import callbacks are not
    added: `attributes=True` returns everything the callbacks of the Rust importers receive.
12. ~~**Event-driven importers.**~~ *Done (`read_events`, `parse_events`, `event_formats`; the schema switch is item 13).* Expose the event-driven importers (CSV, DIMACS, GEXF, GraphML,
    graph6, JSON, and the simple GraphML edge-list importer): `read_events` / `parse_events`
    with the events `Start`, `End`, `VertexCount`, `EdgeCount`, `Vertex`, `VertexWithAttributes`,
    `Edge`, `EdgeWithAttributes`, `GraphAttribute`, `VertexAttribute`, `EdgeAttribute`, delivered
    to a Python callback (exceptions propagate and stop the import) or returned as a list. Also
    DIMACS `zero_based_numbering` / `renumber_vertices` and the JSON collection names, which are
    only available there.
13. ~~**Schema-validation switch**~~ *Done; accepted but without effect until upstream validates.* of the GraphML/GEXF importers (`schema_validation=`). The Rust
    parser currently records the flag without validating; expose it so code written against it
    keeps working, and document that it has no effect until upstream implements validation.

## Not possible (upstream)

* Formats the Rust crate implements in one direction only: LEMON, matrix and Visio import;
  TSPLIB export.

## Update: attributes are stored in the graph

`attributes=True` no longer exists. Graphs store their attributes (`vertex_attrs`, `edge_attrs`,
`graph_attrs`), importers fill them (`graph_attrs["vertex_ids"]` keeps the file identifiers when the
vertices are not the identifiers, `graph_attrs["tsplib"]` the TSPLIB data), and exporters write them
unless the `vertex_attributes`, `edge_attributes` or `graph_attributes` option is given.
