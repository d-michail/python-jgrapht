#ifndef __BACKEND_H
#define __BACKEND_H

#include <graal_isolate.h>
#include <jgrapht_capi_types.h>

#if defined(__cplusplus)
extern "C" {
#endif

// library init

void jgrapht_init();

void jgrapht_cleanup();

int jgrapht_is_initialized();

// error

void jgrapht_error_clear_errno();

int jgrapht_error_get_errno();

char *jgrapht_error_get_errno_msg();

void jgrapht_error_print_stack_trace();

// vm

void jgrapht_vmLocatorSymbol();

// attribute store 

int jgrapht_xx_attributes_store_create(void**);

int jgrapht_ii_attributes_store_put_boolean_attribute(void *, int, char*, int);

int jgrapht_ll_attributes_store_put_boolean_attribute(void *, long long int, char*, int);

int jgrapht_ii_attributes_store_put_boolean_attribute(void *, int, char*, int);

int jgrapht_ll_attributes_store_put_boolean_attribute(void *, long long int, char*, int);

int jgrapht_ii_attributes_store_put_int_attribute(void *, int, char*, int);

int jgrapht_ll_attributes_store_put_int_attribute(void *, long long int, char*, int);

int jgrapht_ii_attributes_store_put_long_attribute(void *, int, char*, long long int);

int jgrapht_ll_attributes_store_put_long_attribute(void *, long long int, char*, long long int);

int jgrapht_ii_attributes_store_put_double_attribute(void *, int, char*, double);

int jgrapht_ll_attributes_store_put_double_attribute(void *, long long int, char*, double);

int jgrapht_ii_attributes_store_put_string_attribute(void *, int, char*, char*);

int jgrapht_ll_attributes_store_put_string_attribute(void *, long long int, char*, char*);

int jgrapht_ii_attributes_store_remove_attribute(void *, int, char*);

int jgrapht_ll_attributes_store_remove_attribute(void *, long long int, char*);

int jgrapht_attributes_registry_create(void**);

int jgrapht_attributes_registry_register_attribute(void *, char*, char*, char*, char*);

int jgrapht_attributes_registry_unregister_attribute(void *, char*, char*, char*, char*);

// clique

int jgrapht_xx_clique_exec_bron_kerbosch(void *, long long int, void**);

int jgrapht_xx_clique_exec_bron_kerbosch_pivot(void *, long long int, void**);

int jgrapht_xx_clique_exec_bron_kerbosch_pivot_degeneracy_ordering(void *, long long int, void**);

int jgrapht_xx_clique_exec_chordal_max_clique(void *, void**);

// clustering

int jgrapht_xx_clustering_exec_k_spanning_tree(void *, int, void**);

int jgrapht_xx_clustering_exec_label_propagation(void *, int, long long int, void**);

int jgrapht_xx_clustering_exec_girvan_newman(void *, int, void**);

int jgrapht_xx_clustering_get_number_clusters(void *, int*);

int jgrapht_xx_clustering_ith_cluster_vit(void *, int, void**);

// coloring

int jgrapht_xx_coloring_exec_greedy(void *, int*, void**);

int jgrapht_xx_coloring_exec_greedy_smallestdegreelast(void *, int*, void**);

int jgrapht_xx_coloring_exec_backtracking_brown(void *, int*, void**);

int jgrapht_xx_coloring_exec_greedy_largestdegreefirst(void *, int*, void**);

int jgrapht_xx_coloring_exec_greedy_random(void *, int*, void**);

int jgrapht_xx_coloring_exec_greedy_random_with_seed(void *, long long int, int*, void**);

int jgrapht_xx_coloring_exec_greedy_dsatur(void *, int*, void**);

int jgrapht_xx_coloring_exec_color_refinement(void *, int*, void**);

int jgrapht_xx_coloring_exec_chordal_minimum_coloring(void *, int*, void**);

// connectivity

int jgrapht_xx_connectivity_strong_exec_kosaraju(void *, int*, void**);

int jgrapht_xx_connectivity_strong_exec_gabow(void *, int*, void**);

int jgrapht_xx_connectivity_weak_exec_bfs(void *, int*, void**);

// cut

int jgrapht_xx_cut_mincut_exec_stoer_wagner(void *, double*, void**);
int jgrapht_xx_cut_gomoryhu_exec_gusfield(void *, void**);
int jgrapht_ix_cut_gomoryhu_min_st_cut(void *, int, int, double*, void**);
int jgrapht_lx_cut_gomoryhu_min_st_cut(void *, long long int, long long int, double*, void**);
int jgrapht_xx_cut_gomoryhu_min_cut(void *, double*, void**);
int jgrapht_ii_cut_gomoryhu_tree(void *, void**);
int jgrapht_ll_cut_gomoryhu_tree(void *, void**);
int jgrapht_ll_cut_gomoryhu_tree_with_suppliers(void *, void*, void*, void**);
int jgrapht_xx_cut_oddmincutset_exec_padberg_rao(void *, void *, int, double*, void**);

// cycles

int jgrapht_xx_cycles_eulerian_exec_hierholzer(void *, int*, void**);
int jgrapht_xx_cycles_chinese_postman_exec_edmonds_johnson(void *, void**);
int jgrapht_xx_cycles_simple_enumeration_exec_tarjan(void *, void**);
int jgrapht_xx_cycles_simple_enumeration_exec_tiernan(void *, void**);
int jgrapht_xx_cycles_simple_enumeration_exec_szwarcfiter_lauer(void *, void**);
int jgrapht_xx_cycles_simple_enumeration_exec_johnson(void *, void**);
int jgrapht_xx_cycles_simple_enumeration_exec_hawick_james(void *, void**);
int jgrapht_xx_cycles_fundamental_basis_exec_queue_bfs(void *, double*, void**);
int jgrapht_xx_cycles_fundamental_basis_exec_stack_bfs(void *, double*, void**);
int jgrapht_xx_cycles_fundamental_basis_exec_paton(void *, double*, void**);
int jgrapht_xx_cycles_mean_exec_howard(void *, int, double, double*, void**);


// drawing

int jgrapht_xx_drawing_layout_model_2d_create(double, double, double, double, void**);
int jgrapht_xx_drawing_layout_model_2d_get_drawable_area(void *, double*, double*, double*, double*);
int jgrapht_ix_drawing_layout_model_2d_get_vertex(void *, int, double*, double*);
int jgrapht_lx_drawing_layout_model_2d_get_vertex(void *, long long int, double*, double*);
int jgrapht_ix_drawing_layout_model_2d_put_vertex(void *, int, double, double);
int jgrapht_lx_drawing_layout_model_2d_put_vertex(void *, long long int, double, double);
int jgrapht_ix_drawing_layout_model_2d_get_fixed(void *, int, int*);
int jgrapht_lx_drawing_layout_model_2d_get_fixed(void *, long long int, int*);
int jgrapht_ix_drawing_layout_model_2d_set_fixed(void *, int, int);
int jgrapht_lx_drawing_layout_model_2d_set_fixed(void *, long long int, int);
int jgrapht_xx_drawing_exec_random_layout_2d(void *, void *, long long int);
int jgrapht_ix_drawing_exec_circular_layout_2d(void *, void *, double, void *);
int jgrapht_lx_drawing_exec_circular_layout_2d(void *, void *, double, void *);
int jgrapht_xx_drawing_exec_fr_layout_2d(void *, void *, int, double, long long int);
int jgrapht_xx_drawing_exec_indexed_fr_layout_2d(void *, void *, int, double, long long int, double, double);
int jgrapht_xx_drawing_exec_rescale_layout_2d(void *, void *, double);
int jgrapht_ix_drawing_exec_two_layered_bipartite_layout_2d(void *, void *, void *, void *, int);
int jgrapht_lx_drawing_exec_two_layered_bipartite_layout_2d(void *, void *, void *, void *, int);
int jgrapht_ix_drawing_exec_barycenter_greedy_two_layered_bipartite_layout_2d(void *, void *, void *, void *, int);
int jgrapht_lx_drawing_exec_barycenter_greedy_two_layered_bipartite_layout_2d(void *, void *, void *, void *, int);
int jgrapht_ix_drawing_exec_median_greedy_two_layered_bipartite_layout_2d(void *, void *, void *, void *, int);
int jgrapht_lx_drawing_exec_median_greedy_two_layered_bipartite_layout_2d(void *, void *, void *, void *, int);


// exporter

int jgrapht_ix_export_file_dimacs(void *, char*, dimacs_format_t, int, void *);
int jgrapht_lx_export_file_dimacs(void *, char*, dimacs_format_t, int, void *);
int jgrapht_ix_export_string_dimacs(void *, dimacs_format_t, int, void *, void**);
int jgrapht_lx_export_string_dimacs(void *, dimacs_format_t, int, void *, void**);
int jgrapht_xx_export_file_gml(void *, char*, int, int, int, void *, void *, void *);
int jgrapht_xx_export_string_gml(void *, int, int, int, void *, void *, void *, void **);
int jgrapht_xx_export_file_json(void *, char*, void *, void *, void *);
int jgrapht_xx_export_string_json(void *, void *, void *, void *, void **);
int jgrapht_xx_export_file_lemon(void *, char*, int, int, void *);
int jgrapht_xx_export_string_lemon(void *, int, int, void *, void **);
int jgrapht_xx_export_file_csv(void *, char*, csv_format_t, int, int, int, void *);
int jgrapht_xx_export_string_csv(void *, csv_format_t, int, int, int, void *, void **);
int jgrapht_xx_export_file_gexf(void *, char*, void *, void *, void *, void *, void *, int, int, int, int);
int jgrapht_xx_export_string_gexf(void *, void *, void *, void *, void *, void *, int, int, int, int, void **);
int jgrapht_xx_export_file_dot(void *, char*, void *, void *, void *);
int jgrapht_xx_export_string_dot(void *, void *, void *, void *, void **);
int jgrapht_xx_export_file_graph6(void *, char*);
int jgrapht_xx_export_string_graph6(void *, void **);
int jgrapht_xx_export_file_sparse6(void *, char*);
int jgrapht_xx_export_string_sparse6(void *, void**);
int jgrapht_xx_export_file_graphml(void *, char*, void *, void *, void *, void *, int, int, int);
int jgrapht_xx_export_string_graphml(void *, void *, void *, void *, void *, int, int, int, void**);

// flow 

int jgrapht_ix_maxflow_exec_push_relabel(void *, int, int, double*, void**, void**);
int jgrapht_lx_maxflow_exec_push_relabel(void *, long long int, long long int, double*, void**, void**);
int jgrapht_ix_maxflow_exec_dinic(void *, int, int, double*, void**, void**);
int jgrapht_lx_maxflow_exec_dinic(void *, long long int, long long int, double*, void**, void**);
int jgrapht_ix_maxflow_exec_edmonds_karp(void *, int, int, double*, void**, void**);
int jgrapht_lx_maxflow_exec_edmonds_karp(void *, long long int, long long int, double*, void**, void**);
int jgrapht_ix_maxflow_exec_boykov_kolmogorov(void *, int, int, double*, void **, void **);
int jgrapht_lx_maxflow_exec_boykov_kolmogorov(void *, long long int, long long int, double*, void **, void **);
int jgrapht_ii_mincostflow_exec_capacity_scaling(void *, void *, void *, void *, int, double*, void**, void**);
int jgrapht_ll_mincostflow_exec_capacity_scaling(void *, void *, void *, void *, int, double*, void**, void**);
int jgrapht_xx_equivalentflowtree_exec_gusfield(void *, void**);
int jgrapht_ix_equivalentflowtree_max_st_flow(void *, int, int, double*);
int jgrapht_lx_equivalentflowtree_max_st_flow(void *, long long int, long long int, double*);
int jgrapht_ii_equivalentflowtree_tree(void *, void**);
int jgrapht_ll_equivalentflowtree_tree(void *, void**);
int jgrapht_ll_equivalentflowtree_tree_with_suppliers(void *, void*, void*, void**);

// generate

int jgrapht_xx_generate_barabasi_albert(void *, int, int, int, long long int);
int jgrapht_xx_generate_barabasi_albert_forest(void *, int, int, long long int);
int jgrapht_xx_generate_complete(void *, int);
int jgrapht_xx_generate_bipartite_complete(void *, int, int);
int jgrapht_xx_generate_empty(void *, int);
int jgrapht_xx_generate_gnm_random(void *, int, int, int, int, long long int);
int jgrapht_xx_generate_gnp_random(void *, int, double, int, long long int);
int jgrapht_xx_generate_ring(void *, int);
int jgrapht_xx_generate_scalefree(void *, int, long long int);
int jgrapht_xx_generate_watts_strogatz(void *, int, int, double, int, long long int);
int jgrapht_xx_generate_kleinberg_smallworld(void *, int, int, int, int, long long int);
int jgrapht_xx_generate_complement(void *, void *, int);
int jgrapht_xx_generate_generalized_petersen(void *, int, int);
int jgrapht_xx_generate_grid(void *, int, int);
int jgrapht_xx_generate_hypercube(void *, int);
int jgrapht_xx_generate_linear(void *, int);
int jgrapht_xx_generate_random_regular(void *, int, int, long long int);
int jgrapht_xx_generate_star(void *, int);
int jgrapht_xx_generate_wheel(void *, int, int);
int jgrapht_xx_generate_windmill(void *, int, int, int);
int jgrapht_xx_generate_linearized_chord_diagram(void *, int, int, long long int);

// graph - create

int jgrapht_ii_graph_create(int, int, int, int, void*, void*, void**);
int jgrapht_ll_graph_create(int, int, int, int, void*, void*, void**);
int jgrapht_ii_graph_sparse_create(int, int, int, void *, incoming_edges_support_t, void**);
int jgrapht_ii_graph_succinct_create(int, int, void *, incoming_edges_support_t, void**);

// graph

int jgrapht_ix_graph_vertices_count(void *, int*);
int jgrapht_xx_graph_vertices_count(void *, long long*);
int jgrapht_ix_graph_edges_count(void *, int*);
int jgrapht_xx_graph_edges_count(void *, long long*);
int jgrapht_ix_graph_add_vertex(void *, int*);
int jgrapht_lx_graph_add_vertex(void *, long long*);
int jgrapht_ix_graph_add_given_vertex(void *, int, int *);
int jgrapht_lx_graph_add_given_vertex(void *, long long int, int *);
int jgrapht_ix_graph_remove_vertex(void *, int, int*);
int jgrapht_lx_graph_remove_vertex(void *, long long int, int*);
int jgrapht_ix_graph_contains_vertex(void *, int, int*);
int jgrapht_lx_graph_contains_vertex(void *, long long int, int*);
int jgrapht_ii_graph_add_edge(void *, int, int, int*);
int jgrapht_ll_graph_add_edge(void *, long long int, long long int, long long*);
int jgrapht_ii_graph_add_given_edge(void *, int, int, int, int*);
int jgrapht_ll_graph_add_given_edge(void *, long long int, long long int, long long int, int*);
int jgrapht_xi_graph_remove_edge(void *, int, int*);
int jgrapht_xl_graph_remove_edge(void *, long long int, int*);
int jgrapht_xi_graph_contains_edge(void *, int, int*);
int jgrapht_xl_graph_contains_edge(void *, long long int, int*);
int jgrapht_ix_graph_contains_edge_between(void *, int, int, int*);
int jgrapht_lx_graph_contains_edge_between(void *, long long int, long long int, int*);
int jgrapht_ix_graph_degree_of(void *, int, int*);
int jgrapht_lx_graph_degree_of(void *, long long int, long long*);
int jgrapht_ix_graph_indegree_of(void *, int, int*);
int jgrapht_lx_graph_indegree_of(void *, long long int, long long*);
int jgrapht_ix_graph_outdegree_of(void *, int, int*);
int jgrapht_lx_graph_outdegree_of(void *, long long int, long long*);
int jgrapht_ii_graph_edge_source(void *, int, int*);
int jgrapht_ll_graph_edge_source(void *, long long int, long long*);
int jgrapht_ii_graph_edge_target(void *, int, int*);
int jgrapht_ll_graph_edge_target(void *, long long int, long long*);
int jgrapht_xx_graph_is_weighted(void *, int*);
int jgrapht_xx_graph_is_directed(void *, int*);
int jgrapht_xx_graph_is_undirected(void *, int*);
int jgrapht_xx_graph_is_allowing_selfloops(void *, int*);
int jgrapht_xx_graph_is_allowing_multipleedges(void *, int*);
int jgrapht_xx_graph_is_allowing_cycles(void *, int*);
int jgrapht_xx_graph_is_modifiable(void *, int*);
int jgrapht_xi_graph_get_edge_weight(void *, int, double*);
int jgrapht_xl_graph_get_edge_weight(void *, long long int, double*);
int jgrapht_xi_graph_set_edge_weight(void *, int, double);
int jgrapht_xl_graph_set_edge_weight(void *, long long int, double);
int jgrapht_xx_graph_create_all_vit(void *, void**);
int jgrapht_xx_graph_create_all_eit(void *, void**);
int jgrapht_ix_graph_create_between_eit(void *, int, int, void**);
int jgrapht_lx_graph_create_between_eit(void *, long long int, long long int, void**);
int jgrapht_ix_graph_vertex_create_eit(void *, int, void**);
int jgrapht_lx_graph_vertex_create_eit(void *, long long int, void**);
int jgrapht_ix_graph_vertex_create_out_eit(void *, int, void**);
int jgrapht_lx_graph_vertex_create_out_eit(void *, long long int, void**);
int jgrapht_ix_graph_vertex_create_in_eit(void *, int, void**);
int jgrapht_lx_graph_vertex_create_in_eit(void *, long long int, void**);

// graph - wrappers

int jgrapht_xx_graph_as_undirected(void *, void**);
int jgrapht_xx_graph_as_unmodifiable(void *, void**);
int jgrapht_xx_graph_as_unweighted(void *, void**);
int jgrapht_xx_graph_as_edgereversed(void *, void**);
int jgrapht_xi_graph_as_weighted(void *, void *, int, int, void**);
int jgrapht_xl_graph_as_weighted(void *, void *, int, int, void**);
int jgrapht_ii_graph_as_masked_subgraph(void *, void *, void *, void**);
int jgrapht_ll_graph_as_masked_subgraph(void *, void *, void *, void**);
int jgrapht_xx_graph_as_subgraph(void *, void *, void *, void**);
int jgrapht_xx_graph_as_graph_union(void *, void *, void *, void**);

// dag

int jgrapht_ii_graph_dag_create(int, int, void**);
int jgrapht_ll_graph_dag_create(int, int, void**);
int jgrapht_ll_graph_dag_create_with_suppliers(int, int, void*, void*, void **);
int jgrapht_xx_graph_dag_topological_it(void *, void**);
int jgrapht_ix_graph_dag_vertex_descendants(void *, int, void**);
int jgrapht_lx_graph_dag_vertex_descendants(void *, long long int, void**);
int jgrapht_ix_graph_dag_vertex_ancestors(void *, int, void**);
int jgrapht_lx_graph_dag_vertex_ancestors(void *, long long int, void**);

// graph metrics

int jgrapht_xx_graph_metrics_diameter(void *, double*);
int jgrapht_xx_graph_metrics_radius(void *, double*);
int jgrapht_xx_graph_metrics_girth(void *, int*);
int jgrapht_xx_graph_metrics_triangles(void *, long long int*);
int jgrapht_xx_graph_metrics_measure_graph(void *, double*, double*, void**, void**, void**, void**);

// graph test

int jgrapht_xx_graph_test_is_empty(void *, int*);
int jgrapht_xx_graph_test_is_simple(void *, int*);
int jgrapht_xx_graph_test_has_selfloops(void *, int*);
int jgrapht_xx_graph_test_has_multipleedges(void *, int*);
int jgrapht_xx_graph_test_is_complete(void *, int*);
int jgrapht_xx_graph_test_is_weakly_connected(void *, int*);
int jgrapht_xx_graph_test_is_strongly_connected(void *, int*);
int jgrapht_xx_graph_test_is_tree(void *, int*);
int jgrapht_xx_graph_test_is_forest(void *, int*);
int jgrapht_xx_graph_test_is_overfull(void *, int*);
int jgrapht_xx_graph_test_is_split(void *, int*);
int jgrapht_xx_graph_test_is_bipartite(void *, int*);
int jgrapht_xx_graph_test_is_cubic(void *, int*);
int jgrapht_xx_graph_test_is_eulerian(void *, int*);
int jgrapht_xx_graph_test_is_chordal(void *, int*);
int jgrapht_xx_graph_test_is_weakly_chordal(void *, int*);
int jgrapht_xx_graph_test_has_ore(void *, int*);
int jgrapht_xx_graph_test_is_trianglefree(void *, int*);
int jgrapht_xx_graph_test_is_perfect(void *, int*);
int jgrapht_xx_graph_test_is_planar(void *, int*);
int jgrapht_xx_graph_test_is_kuratowski_subdivision(void *, int*);
int jgrapht_xx_graph_test_is_k33_subdivision(void *, int*);
int jgrapht_xx_graph_test_is_k5_subdivision(void *, int*);

// graph attributes

int jgrapht_xx_graph_attrs_get_long(void *, char*, long long*);
int jgrapht_ix_graph_attrs_vertex_get_long(void *, int, char*, long long*);
int jgrapht_lx_graph_attrs_vertex_get_long(void *, long long int, char*, long long*);
int jgrapht_xi_graph_attrs_edge_get_long(void *, int, char*, long long*);
int jgrapht_xl_graph_attrs_edge_get_long(void *, long long int, char*, long long*);
int jgrapht_xx_graph_attrs_put_long(void *, char*, long long int);
int jgrapht_ix_graph_attrs_vertex_put_long(void *, int, char*, long long int);
int jgrapht_lx_graph_attrs_vertex_put_long(void *, long long int, char*, long long int);
int jgrapht_xi_graph_attrs_edge_put_long(void *, int, char*, long long int);
int jgrapht_xl_graph_attrs_edge_put_long(void *, long long int, char*, long long int);
int jgrapht_xx_graph_attrs_remove(void *, char*);
int jgrapht_ix_graph_attrs_vertex_remove(void *, int, char*);
int jgrapht_lx_graph_attrs_vertex_remove(void *, long long int, char*);
int jgrapht_xi_graph_attrs_edge_remove(void *, int, char*);
int jgrapht_xl_graph_attrs_edge_remove(void *, long long int, char*);
int jgrapht_xx_graph_attrs_contains(void *, char*, int*);
int jgrapht_ix_graph_attrs_vertex_contains(void *, int, char*, int*);
int jgrapht_lx_graph_attrs_vertex_contains(void *, long long int, char*, int*);
int jgrapht_xi_graph_attrs_edge_contains(void *, int, char*, int*);
int jgrapht_xl_graph_attrs_edge_contains(void *, long long int, char*, int*);
int jgrapht_xx_graph_attrs_keys_iterator(void *, void**);
int jgrapht_ix_graph_attrs_vertex_keys_iterator(void *, int, void**);
int jgrapht_lx_graph_attrs_vertex_keys_iterator(void *, long long int, void**);
int jgrapht_xi_graph_attrs_edge_keys_iterator(void *, int, void**);
int jgrapht_xl_graph_attrs_edge_keys_iterator(void *, long long int, void**);
int jgrapht_xx_graph_attrs_size(void *, int*);
int jgrapht_ix_graph_attrs_vertex_size(void *, int, int*);
int jgrapht_lx_graph_attrs_vertex_size(void *, long long int, int*);
int jgrapht_xi_graph_attrs_edge_size(void *, int, int*);
int jgrapht_xl_graph_attrs_edge_size(void *, long long int, int*);

// handles

int jgrapht_handles_destroy(void *);
int jgrapht_handles_put_ref(void *, void *, void**);
int jgrapht_handles_put2_ref(void *, void *, void *, void**);
int jgrapht_handles_get_ref(void *, void**, void**, void**);
int jgrapht_handles_get_ccharpointer(void *, char**);
int jgrapht_handles_get_edge_pair(void *, int*, int*);
int jgrapht_handles_get_long_edge_pair(void *, long long*, long long*);
int jgrapht_handles_get_edge_triple(void *, int*, int*, double*);
int jgrapht_handles_get_long_edge_triple(void *, long long*, long long*, double*);
int jgrapht_handles_get_str_edge_triple(void *, char**, char**, double*);
int jgrapht_ix_handles_get_graphpath(void *, double*, int*, int*, void**);
int jgrapht_lx_handles_get_graphpath(void *, double*, long long*, long long*, void**);
int jgrapht_rr_handles_get_graphpath(void *, double*, void**, void**, void**);

// importers

int jgrapht_ii_import_file_dimacs(void *, char*, void *, void *, void*);
int jgrapht_ll_import_file_dimacs(void *, char*, void *, void *, void*);
int jgrapht_ii_import_string_dimacs(void *, char*, void *, void *, void*);
int jgrapht_ll_import_string_dimacs(void *, char*, void *, void *, void*);
int jgrapht_ii_import_file_gml(void *, char*, void *, void *, void *, void *, void*);
int jgrapht_ll_import_file_gml(void *, char*, void *, void *, void *, void *, void*);
int jgrapht_ii_import_string_gml(void *, char*, void *, void *, void *, void *, void*);
int jgrapht_ll_import_string_gml(void *, char*, void *, void *, void *, void *, void*);
int jgrapht_ii_import_file_json(void *, char*, void *, void *, void *, void *, void*);
int jgrapht_ll_import_file_json(void *, char*, void *, void *, void *, void *, void*);
int jgrapht_ii_import_string_json(void *, char*, void *, void *, void *, void *, void*);
int jgrapht_ll_import_string_json(void *, char*, void *, void *, void *, void *, void*);
int jgrapht_ii_import_file_csv(void *, char*, void *, void *, void*, csv_format_t, int, int, int);
int jgrapht_ll_import_file_csv(void *, char*, void *, void *, void*, csv_format_t, int, int, int);
int jgrapht_ii_import_string_csv(void *, char*, void *, void *, void*, csv_format_t, int, int, int);
int jgrapht_ll_import_string_csv(void *, char*, void *, void *, void*, csv_format_t, int, int, int);
int jgrapht_ii_import_file_gexf(void *, char*, void *, int, void *, void *, void *, void*);
int jgrapht_ll_import_file_gexf(void *, char*, void *, int, void *, void *, void *, void*);
int jgrapht_ii_import_string_gexf(void *, char*, void *, int, void *, void *, void *, void*);
int jgrapht_ll_import_string_gexf(void *, char*, void *, int, void *, void *, void *, void*);
int jgrapht_ii_import_file_graphml_simple(void *, char*, void *, int, void *, void *, void *, void*);
int jgrapht_ll_import_file_graphml_simple(void *, char*, void *, int, void *, void *, void *, void*);
int jgrapht_ii_import_string_graphml_simple(void *, char*, void *, int, void *, void *, void *, void*);
int jgrapht_ll_import_string_graphml_simple(void *, char*, void *, int, void *, void *, void *, void*);
int jgrapht_ii_import_file_graphml(void *, char*, void *, int, void *, void *, void *, void*);
int jgrapht_ll_import_file_graphml(void *, char*, void *, int, void *, void *, void *, void*);
int jgrapht_ii_import_string_graphml(void *, char*, void *, int, void *, void *, void *, void*);
int jgrapht_ll_import_string_graphml(void *, char*, void *, int, void *, void *, void *, void*);
int jgrapht_ii_import_file_dot(void *, char*, void *, void *, void *, void *, void*);
int jgrapht_ll_import_file_dot(void *, char*, void *, void *, void *, void *, void*);
int jgrapht_ii_import_string_dot(void *, char*, void *, void *, void *, void *, void*);
int jgrapht_ll_import_string_dot(void *, char*, void *, void *, void *, void *, void*);
int jgrapht_ii_import_file_graph6sparse6(void *, char*, void *, void *, void *, void *, void*);
int jgrapht_ll_import_file_graph6sparse6(void *, char*, void *, void *, void *, void *, void*);
int jgrapht_ii_import_string_graph6sparse6(void *, char*, void *, void *, void *, void *, void*);
int jgrapht_ll_import_string_graph6sparse6(void *, char*, void *, void *, void *, void *, void*);

// edgelist

int jgrapht_xx_import_edgelist_noattrs_file_dimacs(char*, void**);
int jgrapht_xx_import_edgelist_noattrs_string_dimacs(char*, void**);
int jgrapht_ii_import_edgelist_attrs_file_dimacs(char*, void*, void*, void**);
int jgrapht_ll_import_edgelist_attrs_file_dimacs(char* , void *, void *, void**);
int jgrapht_ii_import_edgelist_attrs_string_dimacs(char* , void *, void *, void**);
int jgrapht_ll_import_edgelist_attrs_string_dimacs(char* , void *, void *, void**);
int jgrapht_xx_import_edgelist_noattrs_file_gml(char* , void**);
int jgrapht_xx_import_edgelist_noattrs_string_gml(char* , void**);
int jgrapht_ii_import_edgelist_attrs_file_gml(char* , void *, void *, void**);
int jgrapht_ll_import_edgelist_attrs_file_gml(char* , void *, void *, void**);
int jgrapht_ii_import_edgelist_attrs_string_gml(char* , void *, void *, void**);
int jgrapht_ll_import_edgelist_attrs_string_gml(char* , void *, void *, void**);
int jgrapht_xx_import_edgelist_noattrs_file_json(char* , void**);
int jgrapht_xx_import_edgelist_noattrs_string_json(char* , void**);
int jgrapht_ii_import_edgelist_attrs_file_json(char* , void *, void *, void**);
int jgrapht_ii_import_edgelist_attrs_string_json(char* , void *, void *, void**);
int jgrapht_xx_import_edgelist_noattrs_file_csv(char* , csv_format_t, int, int, int, void**);
int jgrapht_xx_import_edgelist_noattrs_string_csv(char* , csv_format_t, int, int, int, void**);
int jgrapht_ii_import_edgelist_attrs_file_csv(char* , void *, void *, csv_format_t, int, int, int, void**);
int jgrapht_ll_import_edgelist_attrs_file_csv(char* , void *, void *, csv_format_t, int, int, int, void**);
int jgrapht_ii_import_edgelist_attrs_string_csv(char* , void *, void *, csv_format_t, int, int, int, void**);
int jgrapht_ll_import_edgelist_attrs_string_csv(char* , void *, void *, csv_format_t, int, int, int, void**);
int jgrapht_xx_import_edgelist_noattrs_file_gexf(char* , int, void**);
int jgrapht_xx_import_edgelist_noattrs_string_gexf(char* , int, void**);
int jgrapht_ii_import_edgelist_attrs_file_gexf(char* , int, void *, void *, void**);
int jgrapht_ll_import_edgelist_attrs_file_gexf(char* , int, void *, void *, void**);
int jgrapht_ii_import_edgelist_attrs_string_gexf(char* , int, void *, void *, void**);
int jgrapht_ll_import_edgelist_attrs_string_gexf(char* , int, void *, void *, void**);
int jgrapht_xx_import_edgelist_noattrs_file_graphml_simple(char* , int, void**);
int jgrapht_xx_import_edgelist_noattrs_string_graphml_simple(char* , int, void**);
int jgrapht_ii_import_edgelist_attrs_file_graphml_simple(char* , int, void *, void *, void**);
int jgrapht_ll_import_edgelist_attrs_file_graphml_simple(char* , int, void *, void *, void**);
int jgrapht_ii_import_edgelist_attrs_string_graphml_simple(char* , int, void *, void *, void**);
int jgrapht_ll_import_edgelist_attrs_string_graphml_simple(char* , int, void *, void *, void**);
int jgrapht_xx_import_edgelist_noattrs_file_graphml(char* , int, void**);
int jgrapht_xx_import_edgelist_noattrs_string_graphml(char* , int, void**);
int jgrapht_ii_import_edgelist_attrs_file_graphml(char* , int, void *, void *, void**);
int jgrapht_ll_import_edgelist_attrs_file_graphml(char* , int, void *, void *, void**);
int jgrapht_ii_import_edgelist_attrs_string_graphml(char* , int, void *, void *, void**);
int jgrapht_ll_import_edgelist_attrs_string_graphml(char* , int, void *, void *, void**);
int jgrapht_xx_import_edgelist_noattrs_file_dot(char* , void**);
int jgrapht_xx_import_edgelist_noattrs_string_dot(char* , void**);
int jgrapht_ii_import_edgelist_attrs_file_dot(char* , void *, void *, void**);
int jgrapht_ll_import_edgelist_attrs_file_dot(char* , void *, void *, void**);
int jgrapht_ii_import_edgelist_attrs_string_dot(char* , void *, void *, void**);
int jgrapht_ll_import_edgelist_attrs_string_dot(char* , void *, void *, void**);
int jgrapht_xx_import_edgelist_noattrs_file_graph6sparse6(char* , void**);
int jgrapht_xx_import_edgelist_noattrs_string_graph6sparse6(char* , void**);
int jgrapht_ii_import_edgelist_attrs_file_graph6sparse6(char* , void *, void *, void**);
int jgrapht_ll_import_edgelist_attrs_file_graph6sparse6(char* , void *, void *, void**);
int jgrapht_ii_import_edgelist_attrs_string_graph6sparse6(char* , void *, void *, void**);
int jgrapht_ll_import_edgelist_attrs_string_graph6sparse6(char* , void *, void *, void**);

// independent set

int jgrapht_xx_independent_set_exec_chordal_max_independent_set(void *, void**);

// isomorphism

int jgrapht_xx_isomorphism_exec_vf2(void *, void *, int*, void**);
int jgrapht_xx_isomorphism_exec_vf2_subgraph(void *, void *, int*, void**);
int jgrapht_xi_isomorphism_graph_mapping_edge_correspondence(void *, int, int, int*, int*);
int jgrapht_xl_isomorphism_graph_mapping_edge_correspondence(void *, long long int, int, int*, long long*);
int jgrapht_ix_isomorphism_graph_mapping_vertex_correspondence(void *, int, int, int*, int*);
int jgrapht_lx_isomorphism_graph_mapping_vertex_correspondence(void *, long long int, int, int*, long long*);

// iterators

int jgrapht_it_next_int(void *, int*);
int jgrapht_it_next_long(void *, long long*);
int jgrapht_it_next_double(void *, double*);
int jgrapht_it_next_int_edge_triple(void *, int *, int *, double*);
int jgrapht_it_next_long_edge_triple(void *, long long *, long long *, double*);
int jgrapht_it_next_str_edge_triple(void *, char **, char **, double*);
int jgrapht_it_next_ref(void *, int, void**);
int jgrapht_it_next_object(void *, void**);
int jgrapht_it_hasnext(void *, int*);

// link prediction

int jgrapht_ix_link_prediction_exec_adamic_adar_index(void *, int, int, double*);
int jgrapht_lx_link_prediction_exec_adamic_adar_index(void *, long long int, long long int, double*);
int jgrapht_rr_link_prediction_exec_adamic_adar_index(void *, void*, void*, double*);
int jgrapht_ix_link_prediction_exec_common_neighbors(void *, int, int, double*);
int jgrapht_lx_link_prediction_exec_common_neighbors(void *, long long int, long long int, double*);
int jgrapht_rr_link_prediction_exec_common_neighbors(void *, void*, void*, double*);
int jgrapht_ix_link_prediction_exec_hub_depressed_index(void *, int, int, double*);
int jgrapht_lx_link_prediction_exec_hub_depressed_index(void *, long long int, long long int, double*);
int jgrapht_rr_link_prediction_exec_hub_depressed_index(void *, void*, void*, double*);
int jgrapht_ix_link_prediction_exec_hub_promoted_index(void *, int, int, double*);
int jgrapht_lx_link_prediction_exec_hub_promoted_index(void *, long long int, long long int, double*);
int jgrapht_rr_link_prediction_exec_hub_promoted_index(void *, void*, void*, double*);
int jgrapht_ix_link_prediction_exec_jaccard_coefficient(void *, int, int, double*);
int jgrapht_lx_link_prediction_exec_jaccard_coefficient(void *, long long int, long long int, double*);
int jgrapht_rr_link_prediction_exec_jaccard_coefficient(void *, void*, void*, double*);
int jgrapht_ix_link_prediction_exec_leicht_holme_newman_index(void *, int, int, double*);
int jgrapht_lx_link_prediction_exec_leicht_holme_newman_index(void *, long long int, long long int, double*);
int jgrapht_rr_link_prediction_exec_leicht_holme_newman_index(void *, void*, void*, double*);
int jgrapht_ix_link_prediction_exec_preferential_attachment(void *, int, int, double*);
int jgrapht_lx_link_prediction_exec_preferential_attachment(void *, long long int, long long int, double*);
int jgrapht_rr_link_prediction_exec_preferential_attachment(void *, void*, void*, double*);
int jgrapht_ix_link_prediction_exec_resource_allocation_index(void *, int, int, double*);
int jgrapht_lx_link_prediction_exec_resource_allocation_index(void *, long long int, long long int, double*);
int jgrapht_rr_link_prediction_exec_resource_allocation_index(void *, void*, void*, double*);
int jgrapht_ix_link_prediction_exec_salton_index(void *, int, int, double*);
int jgrapht_lx_link_prediction_exec_salton_index(void *, long long int, long long int, double*);
int jgrapht_rr_link_prediction_exec_salton_index(void *, void*, void*, double*);
int jgrapht_ix_link_prediction_exec_sorensen_index(void *, int, int, double*);
int jgrapht_lx_link_prediction_exec_sorensen_index(void *, long long int, long long int, double*);
int jgrapht_rr_link_prediction_exec_sorensen_index(void *, void*, void*, double*);

// list

int jgrapht_list_create(void**);
int jgrapht_list_it_create(void *, void**);
int jgrapht_list_size(void *, int*);
int jgrapht_list_int_add(void *, int, int*);
int jgrapht_list_long_add(void *, long long int, int*);
int jgrapht_list_double_add(void *, double, int*);
int jgrapht_list_ref_add(void *, void *, int*);
int jgrapht_list_ref_add_direct(void *, void *, void *, int*);
int jgrapht_ii_list_edge_pair_add(void *, int, int, int*);
int jgrapht_ll_list_edge_pair_add(void *, long long int, long long int, int*);
int jgrapht_ii_list_edge_triple_add(void *, int, int, double, int*);
int jgrapht_ll_list_edge_triple_add(void *, long long int, long long int, double, int*);
int jgrapht_list_int_remove(void *, int);
int jgrapht_list_long_remove(void *, long long int);
int jgrapht_list_double_remove(void *, double);
int jgrapht_list_ref_remove(void *, void *);
int jgrapht_list_ref_remove_direct(void *, void *, void *);
int jgrapht_list_int_contains(void *, int, int*);
int jgrapht_list_long_contains(void *, long long int, int*);
int jgrapht_list_double_contains(void *, double, int*);
int jgrapht_list_ref_contains(void *, void *, int*);
int jgrapht_list_ref_contains_direct(void *, void *, void*, int*);
int jgrapht_list_clear(void *);

// listenable

int jgrapht_xx_listenable_as_listenable(void *, void**);
int jgrapht_ii_listenable_create_graph_listener(void *, void**);
int jgrapht_ll_listenable_create_graph_listener(void *, void**);
int jgrapht_ii_listenable_add_graph_listener(void *, void *);
int jgrapht_ll_listenable_add_graph_listener(void *, void *);
int jgrapht_ii_listenable_remove_graph_listener(void *, void *);
int jgrapht_ll_listenable_remove_graph_listener(void *, void *);

// map

int jgrapht_map_create(void**);
int jgrapht_map_linked_create(void**);
int jgrapht_map_keys_it_create(void *, void**);
int jgrapht_map_size(void *, int*);
int jgrapht_map_values_it_create(void *, void**);
int jgrapht_map_int_double_put(void *, int, double);
int jgrapht_map_int_int_put(void *, int, int);
int jgrapht_map_int_string_put(void *, int, char*);
int jgrapht_map_long_double_put(void *, long long int, double);
int jgrapht_map_long_int_put(void *, long long int, int);
int jgrapht_map_long_string_put(void *, long long int, char*);
int jgrapht_map_int_double_get(void *, int, double*);
int jgrapht_map_int_int_get(void *, int, int*);
int jgrapht_map_int_string_get(void *, int, void**);
int jgrapht_map_long_double_get(void *, long long int, double*);
int jgrapht_map_long_int_get(void *, long long int, int*);
int jgrapht_map_long_string_get(void *, long long int, void**);
int jgrapht_map_int_contains_key(void *, int, int*);
int jgrapht_map_long_contains_key(void *, long long int, int*);
int jgrapht_map_int_double_remove(void *, int, double*);
int jgrapht_map_int_int_remove(void *, int, int*);
int jgrapht_map_int_string_remove(void *, int, void**);
int jgrapht_map_long_double_remove(void *, long long int, double*);
int jgrapht_map_long_int_remove(void *, long long int, int*);
int jgrapht_map_long_string_remove(void *, long long int, void**);
int jgrapht_map_clear(void *);

// matching

int jgrapht_xx_matching_exec_greedy_general_max_card(void *, double*, void**);
int jgrapht_xx_matching_exec_custom_greedy_general_max_card(void *, int, double*, void**);
int jgrapht_xx_matching_exec_edmonds_general_max_card_dense(void *, double*, void**);
int jgrapht_xx_matching_exec_edmonds_general_max_card_sparse(void *, double*, void**);
int jgrapht_xx_matching_exec_greedy_general_max_weight(void *, double*, void**);
int jgrapht_xx_matching_exec_custom_greedy_general_max_weight(void *, int, double, double*, void**);
int jgrapht_xx_matching_exec_pathgrowing_max_weight(void *, double*, void**);
int jgrapht_xx_matching_exec_blossom5_general_max_weight(void *, double*, void**);
int jgrapht_xx_matching_exec_blossom5_general_min_weight(void *, double*, void**);
int jgrapht_xx_matching_exec_blossom5_general_perfect_max_weight(void *, double*, void**);
int jgrapht_xx_matching_exec_blossom5_general_perfect_min_weight(void *, double*, void**);
int jgrapht_xx_matching_exec_bipartite_max_card(void *, double*, void**);
int jgrapht_xx_matching_exec_bipartite_perfect_min_weight(void *, void *, void *, double*, void**);
int jgrapht_xx_matching_exec_bipartite_max_weight(void *, double*, void**);

// mst

int jgrapht_xx_mst_exec_kruskal(void *, double*, void**);
int jgrapht_xx_mst_exec_prim(void *, double*, void**);
int jgrapht_xx_mst_exec_boruvka(void *, double*, void**);

// partition

int jgrapht_xx_partition_exec_bipartite(void *, int*, void**, void**);

// planarity

int jgrapht_xx_planarity_exec_boyer_myrvold(void *, int*, void**, void**);
int jgrapht_ix_planarity_embedding_edges_around_vertex(void *, int, void**);
int jgrapht_lx_planarity_embedding_edges_around_vertex(void *, long long int, void**);

// ref graphs

int jgrapht_rr_graph_hash_equals_resolver_create(void *, void *, void **);
int jgrapht_rr_graph_create(int, int, int, int, void *, void *, void *, void**);
int jgrapht_rr_graph_add_vertex(void *, void**);
int jgrapht_rr_graph_add_given_vertex(void *, void *, int*);
int jgrapht_rr_graph_remove_vertex(void *, void *, int*);
int jgrapht_rr_graph_contains_vertex(void *, void *, int*);
int jgrapht_rr_graph_add_edge(void *, void *, void *, void**);
int jgrapht_rr_graph_add_given_edge(void *, void *, void *, void *, int*);
int jgrapht_rr_graph_remove_edge(void *, void *, int*);
int jgrapht_rr_graph_contains_edge(void *, void *, int*);
int jgrapht_rr_graph_contains_edge_between(void *, void *, void *, int*);
int jgrapht_rr_graph_degree_of(void *, void *, long long*);
int jgrapht_rr_graph_indegree_of(void *, void *, long long*);
int jgrapht_rr_graph_outdegree_of(void *, void *, long long*);
int jgrapht_rr_graph_edge_source(void *, void *, void**);
int jgrapht_rr_graph_edge_target(void *, void *, void**);
int jgrapht_rr_graph_get_edge_weight(void *, void *, double*);
int jgrapht_rr_graph_set_edge_weight(void *, void *, double);
int jgrapht_rr_graph_create_between_eit(void *, void *, void *, void**);
int jgrapht_rr_graph_vertex_create_eit(void *, void *, void**);
int jgrapht_rr_graph_vertex_create_out_eit(void *, void *, void**);
int jgrapht_rr_graph_vertex_create_in_eit(void *, void *, void**);

// scoring

int jgrapht_xx_scoring_exec_eigenvector_centrality(void *, void**);
int jgrapht_xx_scoring_exec_custom_eigenvector_centrality(void *, int, double, void**);
int jgrapht_xx_scoring_exec_katz_centrality(void *, void**);
int jgrapht_ix_scoring_exec_custom_katz_centrality(void *, double, void *, int, double, void**);
int jgrapht_lx_scoring_exec_custom_katz_centrality(void *, double, void *, int, double, void**);
int jgrapht_xx_scoring_exec_betweenness_centrality(void *, void**);
int jgrapht_xx_scoring_exec_custom_betweenness_centrality(void *, int, void**);
int jgrapht_xx_scoring_exec_edge_betweenness_centrality(void *, void**);
int jgrapht_xx_scoring_exec_closeness_centrality(void *, void**);
int jgrapht_xx_scoring_exec_custom_closeness_centrality(void *, int, int, void**);
int jgrapht_xx_scoring_exec_harmonic_centrality(void *, void**);
int jgrapht_xx_scoring_exec_custom_harmonic_centrality(void *, int, int, void**);
int jgrapht_xx_scoring_exec_pagerank(void *, void**);
int jgrapht_xx_scoring_exec_custom_pagerank(void *, double, int, double, void**);
int jgrapht_xx_scoring_exec_coreness(void *, int*, void**);
int jgrapht_xx_scoring_exec_clustering_coefficient(void *, double*, double*, void**);

// set

int jgrapht_set_create(void**);
int jgrapht_set_linked_create(void**);
int jgrapht_set_it_create(void *, void**);
int jgrapht_set_size(void *, int*);
int jgrapht_set_int_add(void *, int, int*);
int jgrapht_set_long_add(void *, long long int, int*);
int jgrapht_set_double_add(void *, double, int *);
int jgrapht_set_ref_add(void *, void *, int*);
int jgrapht_set_ref_add_direct(void *, void *, void *, int*);
int jgrapht_set_int_remove(void *, int, int*);
int jgrapht_set_long_remove(void *, long long int, int*);
int jgrapht_set_double_remove(void *, double, int*);
int jgrapht_set_ref_remove(void *, void *, int*);
int jgrapht_set_ref_remove_direct(void *, void *, void *, int*);
int jgrapht_set_int_contains(void *, int, int*);
int jgrapht_set_long_contains(void *, long long int, int*);
int jgrapht_set_double_contains(void *, double, int*);
int jgrapht_set_ref_contains(void *, void *, int*);
int jgrapht_set_ref_contains_direct(void *, void *, void*, int*);
int jgrapht_set_clear(void *);

// shortest paths 

int jgrapht_ix_sp_exec_dijkstra_get_path_between_vertices(void *, int, int, void**);
int jgrapht_lx_sp_exec_dijkstra_get_path_between_vertices(void *, long long int, long long int, void**);
int jgrapht_ix_sp_exec_bidirectional_dijkstra_get_path_between_vertices(void *, int, int, void**);
int jgrapht_lx_sp_exec_bidirectional_dijkstra_get_path_between_vertices(void *, long long int, long long int, void**);
int jgrapht_ix_sp_exec_dijkstra_get_singlesource_from_vertex(void *, int, void**);
int jgrapht_lx_sp_exec_dijkstra_get_singlesource_from_vertex(void *, long long int, void**);
int jgrapht_ix_sp_exec_bellmanford_get_singlesource_from_vertex(void *, int, void**);
int jgrapht_lx_sp_exec_bellmanford_get_singlesource_from_vertex(void *, long long int, void**);
int jgrapht_ix_sp_exec_bfs_get_singlesource_from_vertex(void *, int, void**);
int jgrapht_lx_sp_exec_bfs_get_singlesource_from_vertex(void *, long long int, void**);
int jgrapht_xx_sp_exec_johnson_get_allpairs(void *, void**);
int jgrapht_xx_sp_exec_floydwarshall_get_allpairs(void *, void**);
int jgrapht_ix_sp_singlesource_get_path_to_vertex(void *, int, void**);
int jgrapht_lx_sp_singlesource_get_path_to_vertex(void *, long long int, void**);
int jgrapht_ix_sp_allpairs_get_path_between_vertices(void *, int, int, void**);
int jgrapht_lx_sp_allpairs_get_path_between_vertices(void *, long long int, long long int, void**);
int jgrapht_ix_sp_allpairs_get_singlesource_from_vertex(void *, int, void**);
int jgrapht_lx_sp_allpairs_get_singlesource_from_vertex(void *, long long int, void**);
int jgrapht_ix_sp_exec_astar_get_path_between_vertices(void *, int, int, void *, void**);
int jgrapht_lx_sp_exec_astar_get_path_between_vertices(void *, long long int, long long int, void *, void**);
int jgrapht_ix_sp_exec_bidirectional_astar_get_path_between_vertices(void *, int, int, void *, void**);
int jgrapht_lx_sp_exec_bidirectional_astar_get_path_between_vertices(void *, long long int, long long int, void *, void**);
int jgrapht_ix_sp_exec_astar_alt_heuristic_get_path_between_vertices(void *, int, int, void *, void**);
int jgrapht_lx_sp_exec_astar_alt_heuristic_get_path_between_vertices(void *, long long int, long long int, void *, void**);
int jgrapht_ix_sp_exec_bidirectional_astar_alt_heuristic_get_path_between_vertices(void *, int, int, void *, void**);
int jgrapht_lx_sp_exec_bidirectional_astar_alt_heuristic_get_path_between_vertices(void *, long long int, long long int, void *, void**);
int jgrapht_ix_sp_exec_yen_get_k_loopless_paths_between_vertices(void *, int, int, int, void**);
int jgrapht_lx_sp_exec_yen_get_k_loopless_paths_between_vertices(void *, long long int, long long int, int, void**);
int jgrapht_ix_sp_exec_eppstein_get_k_paths_between_vertices(void *, int, int, int, void**);
int jgrapht_lx_sp_exec_eppstein_get_k_paths_between_vertices(void *, long long int, long long int, int, void**);
int jgrapht_ix_sp_exec_delta_stepping_get_path_between_vertices(void *, int, int, double, int, void**);
int jgrapht_lx_sp_exec_delta_stepping_get_path_between_vertices(void *, long long int, long long int, double, int, void**);
int jgrapht_ix_sp_exec_delta_stepping_get_singlesource_from_vertex(void *, int, double, int, void**);
int jgrapht_lx_sp_exec_delta_stepping_get_singlesource_from_vertex(void *, long long int, double, int, void**);

// multi objective shortest paths

int jgrapht_ii_multisp_exec_martin_get_multiobjectivesinglesource_from_vertex(void *, int, void *, int, void**);
int jgrapht_ll_multisp_exec_martin_get_multiobjectivesinglesource_from_vertex(void *, long long int, void *, int, void**);
int jgrapht_ii_multisp_exec_martin_get_paths_between_vertices(void *, int, int, void *, int, void**);
int jgrapht_ll_multisp_exec_martin_get_paths_between_vertices(void *, long long int, long long int, void *, int, void**);
int jgrapht_ix_multisp_multiobjectivesinglesource_get_paths_to_vertex(void *, int, void**);
int jgrapht_lx_multisp_multiobjectivesinglesource_get_paths_to_vertex(void *, long long int, void**);

// contraction hierarchy

int jgrapht_ix_sp_manytomany_get_path_between_vertices(void *, int, int, void**);
int jgrapht_lx_sp_manytomany_get_path_between_vertices(void *, long long int, long long int, void**);
int jgrapht_xx_sp_exec_contraction_hierarchy(void *, int, long long int, void**);
int jgrapht_xx_sp_exec_contraction_hierarchy_get_manytomany(void *, void *, void *, void**);
int jgrapht_ix_sp_exec_contraction_hierarchy_bidirectional_dijkstra_get_path_between_vertices(void *, int, int, double, void**);
int jgrapht_lx_sp_exec_contraction_hierarchy_bidirectional_dijkstra_get_path_between_vertices(void *, long long int, long long int, double, void**);
int jgrapht_xx_sp_exec_transit_node_routing(void *, int, void**);
int jgrapht_ix_sp_exec_transit_node_routing_get_path_between_vertices(void *, int, int, void**);
int jgrapht_lx_sp_exec_transit_node_routing_get_path_between_vertices(void *, long long int, long long int, void**);
int jgrapht_ix_sp_exec_transit_node_routing_get_singlesource_from_vertex(void *, int, void**);
int jgrapht_lx_sp_exec_transit_node_routing_get_singlesource_from_vertex(void *, long long int, void**);

// spanner

int jgrapht_xx_spanner_exec_greedy_multiplicative(void *, int, double*, void**);

// tour

int jgrapht_xx_tour_tsp_random(void *, long long int, void**);
int jgrapht_xx_tour_tsp_greedy_heuristic(void *, void**);
int jgrapht_xx_tour_tsp_nearest_insertion_heuristic(void *, void**);
int jgrapht_xx_tour_tsp_nearest_neighbor_heuristic(void *, long long int, void**);
int jgrapht_xx_tour_metric_tsp_christofides(void *, void**);
int jgrapht_xx_tour_metric_tsp_two_approx(void *, void**);
int jgrapht_xx_tour_tsp_held_karp(void *, void**);
int jgrapht_xx_tour_hamiltonian_palmer(void *, void**);
int jgrapht_xx_tour_tsp_two_opt_heuristic(void *, int, double, long long int, void**);
int jgrapht_xx_tour_tsp_two_opt_heuristic_improve(void *, double, long long int, void**);

// traverse

int jgrapht_xx_traverse_create_bfs_from_all_vertices_vit(void *, void**);
int jgrapht_ix_traverse_create_bfs_from_vertex_vit(void *, int, void**);
int jgrapht_lx_traverse_create_bfs_from_vertex_vit(void *, long long int, void**);
int jgrapht_xx_traverse_create_lex_bfs_vit(void *, void**);
int jgrapht_xx_traverse_create_dfs_from_all_vertices_vit(void *, void**);
int jgrapht_ix_traverse_create_dfs_from_vertex_vit(void *, int, void**);
int jgrapht_lx_traverse_create_dfs_from_vertex_vit(void *, long long int, void**);
int jgrapht_xx_traverse_create_topological_order_vit(void *, void**);
int jgrapht_ix_traverse_create_random_walk_from_vertex_vit(void *, int, void**);
int jgrapht_lx_traverse_create_random_walk_from_vertex_vit(void *, long long int, void**);
int jgrapht_ix_traverse_create_custom_random_walk_from_vertex_vit(void *, int, int, long long int, long long int, void**);
int jgrapht_lx_traverse_create_custom_random_walk_from_vertex_vit(void *, long long int, int, long long int, long long int, void**);
int jgrapht_xx_traverse_create_max_cardinality_vit(void *, void**);
int jgrapht_xx_traverse_create_degeneracy_ordering_vit(void *, void**);
int jgrapht_ix_traverse_create_closest_first_from_vertex_vit(void *, int, void**);
int jgrapht_lx_traverse_create_closest_first_from_vertex_vit(void *, long long int, void**);
int jgrapht_ix_traverse_create_custom_closest_first_from_vertex_vit(void *, int, double, void**);
int jgrapht_lx_traverse_create_custom_closest_first_from_vertex_vit(void *, long long int, double, void**);

// vertex cover

int jgrapht_xx_vertexcover_exec_greedy(void *, double*, void**);
int jgrapht_xx_vertexcover_exec_greedy_weighted(void *, void *, double*, void**);
int jgrapht_xx_vertexcover_exec_clarkson(void *, double*, void**);
int jgrapht_xx_vertexcover_exec_clarkson_weighted(void *, void *, double*, void**);
int jgrapht_xx_vertexcover_exec_edgebased(void *, double*, void**);
int jgrapht_xx_vertexcover_exec_baryehudaeven(void *, double*, void**);
int jgrapht_xx_vertexcover_exec_baryehudaeven_weighted(void *, void *, double*, void**);
int jgrapht_xx_vertexcover_exec_exact(void *, double*, void**);
int jgrapht_xx_vertexcover_exec_exact_weighted(void *, void *, double*, void**);


#if defined(__cplusplus)
}
#endif
#endif
