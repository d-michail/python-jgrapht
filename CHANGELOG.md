# Changelog

## [2.0.0rc1] - 2026-10-31
Complete rewrite on top of the Rust crate
[`jgrapht`](https://crates.io/crates/jgrapht) ([source](https://github.com/d-michail/jgrapht-rs)). This is a breaking change from the 1.x
series, which wrapped the GraalVM-built `jgrapht-capi` shared library.

### Added
- Event-driven import: `read_events`, `parse_events`, `event_formats`.
- TSPLIB tours and distances: `read_tsplib_tour`, `parse_tsplib_tour`, `tsplib_geographic_distance`.
- Derived graphs, as independent copies: `copy_graph`, `induced_subgraph`, `edge_subgraph`, `graph_union`, `as_undirected`, `reverse_edges`, `as_weighted`, `as_unweighted`.
- `as_unmodifiable` and `UnmodifiableGraph`: a read-only wrapper that holds a reference to its graph, shows its current state, raises `GraphError` on every modification, and is accepted by the algorithms.
- Drawing with matplotlib (`jgrapht.drawing`: `draw`, `draw_vertices`, `draw_edges`, `draw_vertex_labels`, `draw_edge_labels`) and conversion to and from NetworkX and pydot (`jgrapht.convert`: `to_nx`, `from_nx`, `to_pydot`, `from_pydot`). These packages are optional: install `jgrapht[plot]`, `jgrapht[networkx]` or `jgrapht[pydot]`.
- Graph I/O: `read_graph`, `parse_graph`, `write_graph`, `graph_to_string`, `import_formats`,
  `export_formats` for CSV, DIMACS, DOT, GEXF, GML, graph6, GraphML, JSON and TSPLIB (import), and
  LEMON, matrix and Visio (export), with vertex/edge attributes.
- Generators (`generators` module): `empty_graph`, `path_graph`, `ring_graph`, `star_graph`, `wheel_graph`, `complete_graph`, `complete_bipartite_graph`, `grid_graph`, `hypercube_graph`, `generalized_petersen_graph`, `windmill_graph`, `graph_from_weight_matrix`, `bipartite_graph_from_weight_matrix`, `gnp_random_graph`, `gnm_random_graph`, `barabasi_albert_graph`, `barabasi_albert_forest`, `scale_free_graph`, `directed_scale_free_graph`, `watts_strogatz_graph`, `prufer_tree`, `random_regular_graph`, `planted_partition_graph`, `kleinberg_small_world_graph`, `linearized_chord_diagram_graph`, `gnm_random_bipartite_graph`, `gnp_random_bipartite_graph`, `named_graph_names`, `named_graph`, `maximum_flow_network`, `bipartite_matching_network`, `minimum_cost_flow_network`; all accept `sparse=True`.
- Attributes: `vertex_attrs`, `edge_attrs` and `graph_attrs` of `Graph` and `SparseGraph`, live dicts for the vertices, edges and the graph. Copies and derived graphs copy them, removing a vertex or edge removes them, importers fill them and exporters write them (replacing the `attributes=True` option of `read_graph`), and the NetworkX and pydot conversions carry them.
- `Graph`: mutable graph whose vertices and edges are arbitrary hashable objects.
- `SparseGraph`: immutable graph on integer vertices `0..n` and edges `0..m`.
- `GraphPath`, `GraphError`.
- Shortest paths: `shortest_path`, `single_source_distances` (Dijkstra, Bellman-Ford,
  Floyd-Warshall, Johnson), `all_pairs_distances`, `astar_shortest_path` (with a Python heuristic callback).
- `shortest_path` / `single_source_distances` also accept `bidirectional_dijkstra`,
  `delta_stepping` and `bfs`.
- `k_shortest_paths` (Yen, Eppstein), `k_disjoint_shortest_paths` (Suurballe, Bhandari),
  `all_directed_paths`, `count_dag_paths`.
- Metrics: `diameter`, `radius`, `eccentricities`, `graph_center`, `graph_periphery`,
  `graph_pseudo_periphery`, `girth`.
- Matching: `maximum_matching` (sparse/dense Edmonds, greedy), `weighted_matching` (path growing,
  greedy), `perfect_matching` (Blossom V, minimize or maximize), bipartite
  `bipartite_maximum_matching`, `bipartite_maximum_weight_matching` and
  `bipartite_minimum_weight_perfect_matching`; results are `Matching` objects.
- Cycles: `has_cycle`, `vertices_on_cycles`, `simple_cycles` (Johnson, Tarjan, Tiernan,
  Szwarcfiter-Lauer, Hawick-James), `cycle_basis` (Paton, fundamental), `is_eulerian`,
  `eulerian_cycle`, `chinese_postman`, `minimum_mean_cycle`, `is_chordal`,
  `perfect_elimination_order`, `chordal_hole`.
- Connectivity: `is_connected`, `is_weakly_connected`, `is_strongly_connected`, `is_biconnected`,
  `articulation_points`, `bridges`, `biconnected_components`, `block_cut_tree`, `condensation`,
  `edge_connectivity`, `vertex_connectivity`, `is_k_edge_connected`, `is_k_vertex_connected`.
- Cuts: `minimum_st_cut`, `stoer_wagner_minimum_cut`, `gomory_hu_tree`, `equivalent_flow_tree`,
  `minimum_odd_cut`; results are `MinimumCut` objects.
- `minimum_arborescence_tree`, `maximum_arborescence_tree`, `steiner_tree`,
  `steiner_tree_weight`, `greedy_multiplicative_spanner`.
- Properties: `is_forest`, `is_tree`, `has_self_loops`, `has_multiple_edges`, `is_simple`,
  `is_complete`, `is_triangle_free`, `is_cubic`, `is_split`.
- Tours: `traveling_salesman_tour` (nearest neighbor, insertion heuristics, greedy, 2-approx,
  Christofides, 2-opt, random, Held-Karp), `hamiltonian_cycle`, `hamiltonian_path`.
- Isomorphism (VF2 with optional vertex/edge predicates, AHU for trees): `is_isomorphic`,
  `isomorphisms`, `is_subgraph_isomorphic`, `subgraph_isomorphisms`, `tree_isomorphism`.
- Planarity: `is_planar`, `planar_embedding`, `kuratowski_subdivision`.
- `lowest_common_ancestors`; transformations `complement`, `line_graph`, `transitive_closure`,
  `transitive_reduction`.
- Flow: `minimum_cost_flow` returning `MinimumCostFlow`.
- Clustering: `label_propagation_clustering`, `k_spanning_tree_clustering`,
  `girvan_newman_clustering`, `greedy_modularity_clustering`, `modularity`.
- Similarity: `link_score`, `predict_links`, `simrank`, `tree_edit_distance`.
- Layouts: `circular_layout`, `random_layout`, `fruchterman_reingold_layout`.
- `k_center`, `densest_subgraph`, `is_perfect`, `is_weakly_chordal`, `odd_hole_or_antihole`,
  `weak_chordality_certificate`, `tree_decomposition`, `treewidth`.
- More cliques / covers / colorings: Bron-Kerbosch variants, `is_clique`, `is_independent_set`,
  chordal maximum clique and independent set, chordal minimal separators,
  `clique_minimal_separator_decomposition`, `berge_certificate`, `number_of_triangles`; weighted,
  edge-based and bipartite vertex covers with `is_vertex_cover`; random greedy, exact (Brown),
  chordal and color-refinement colorings with `is_proper_coloring`.
- Decompositions: `heavy_path_decomposition`, `dulmage_mendelsohn_decomposition`.
- Advanced shortest paths: `alt_shortest_path`, `bidirectional_astar_shortest_path`,
  `batch_shortest_paths` (contraction hierarchies, transit node routing),
  `many_to_many_shortest_paths`, `multi_objective_shortest_paths` (Martin, label correcting),
  `closest_first`, `single_source_paths`, `negative_cycle`, `tree_center`; `delta_stepping_parallel`
  and `bounded_pruned_yen` options; `path_validator` callbacks for `k_shortest_paths` and
  `all_directed_paths`.
- Capacitated spanning trees (`capacitated_minimum_spanning_tree`: Esau-Williams, Ahuja-Orlin-Sharma
  local search), `cyclic_exchange_augmentation`, exact `densest_subgraph(algorithm="goldberg")`,
  `gon_k_center`, Boykov-Kolmogorov flow and cuts, LCA algorithms (binary lifting, Euler tour,
  heavy path, Tarjan, naive) with `all_lowest_common_ancestors`, `forest_isomorphism`,
  `color_refinement_isomorphism`, Blossom V `weighted_matching` with tuning options, and
  `exact_betweenness_centrality` (arbitrary precision).
- Traversal orders: `bfs`/`dfs` over all components, `bfs_depths`, `dfs_postorder`,
  `lex_bfs_order`, `maximum_cardinality_order`, `degeneracy_ordering`, `random_walk`;
  `strongly_connected_components` with Kosaraju and Gabow; `connected_component_of`, `path_exists`,
  `block_cutpoint_graph`; `TreeDynamicConnectivity`.
- `improve_tour` (2-opt), `contract_edge`, weighted `line_graph`, `cycle_to_path`, and the
  `layout_2d` framework (circular, random, Fruchterman-Reingold with Barnes-Hut, bipartite) with
  `rescale_layout`.
- Traversal and connectivity: `bfs`, `dfs`, `connected_components`,
  `strongly_connected_components`; `minimum_spanning_tree` (Kruskal, Prim, Borůvka).
- Flow: `maximum_flow` (Dinic, Edmonds-Karp, push-relabel) returning `MaximumFlow`.
- Scoring: degree, closeness, harmonic, betweenness (vertex and edge), PageRank, eigenvector and
  Katz centrality, coreness, clustering coefficients, triangle count.
- `coloring` (greedy, largest-degree-first, smallest-degree-last, saturation degree).
- `maximal_cliques`, `maximum_clique`, `greedy_independent_set`, `maximum_independent_set`,
  `vertex_cover`.
- `is_bipartite`, `bipartite_partition`, `is_dag`, `topological_sort`.

### Removed
- Everything from 1.x that is not listed above; it is being ported incrementally.
