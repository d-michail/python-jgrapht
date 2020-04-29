#ifndef __BACKEND_H
#define __BACKEND_H

#include <jgrapht_capi_types.h>

#if defined(__cplusplus)
extern "C" {
#endif

// library init

void jgrapht_thread_create();

void jgrapht_thread_destroy();

int jgrapht_is_thread_attached();

// clique

status_t jgrapht_clique_exec_bron_kerbosch(void *, long long int, void**);

status_t jgrapht_clique_exec_bron_kerbosch_pivot(void *, long long int, void**);

status_t jgrapht_clique_exec_bron_kerbosch_pivot_degeneracy_ordering(void *, long long int, void**);

// clustering

status_t jgrapht_clustering_exec_k_spanning_tree(void *, int, void**);

status_t jgrapht_clustering_get_number_clusters(void *, long long*);

status_t jgrapht_clustering_ith_cluster_vit(void *, int, void**);

// coloring

status_t jgrapht_coloring_exec_greedy(void *, long long*, void**);

status_t jgrapht_coloring_exec_greedy_smallestdegreelast(void *, long long*, void**);

status_t jgrapht_coloring_exec_backtracking_brown(void *, long long*, void**);

status_t jgrapht_coloring_exec_greedy_largestdegreefirst(void *, long long*, void**);

status_t jgrapht_coloring_exec_greedy_random(void *, long long*, void**);

status_t jgrapht_coloring_exec_greedy_random_with_seed(void *, long long int, long long*, void**);

status_t jgrapht_coloring_exec_greedy_dsatur(void *, long long*, void**);

status_t jgrapht_coloring_exec_color_refinement(void *, long long*, void**);

// error

void jgrapht_clear_errno();

status_t jgrapht_get_errno();

char *jgrapht_get_errno_msg();

// exporter

status_t jgrapht_export_file_dimacs(void *, char*, dimacs_format_t);

// generate

status_t jgrapht_generate_barabasi_albert(void *, int, int, int, long long int);

status_t jgrapht_generate_barabasi_albert_forest(void *, int, int, long long int);

status_t jgrapht_generate_complete(void *, int);

status_t jgrapht_generate_bipartite_complete(void *, int, int);

status_t jgrapht_generate_empty(void *, int);

status_t jgrapht_generate_gnm_random(void *, int, int, int, int, long long int);

status_t jgrapht_generate_gnp_random(void *, int, double, int, long long int);

status_t jgrapht_generate_ring(void *, int);

status_t jgrapht_generate_scalefree(void *, int, long long int);

status_t jgrapht_generate_watts_strogatz(void *, int, int, double, int, long long int);

status_t jgrapht_generate_kleinberg_smallworld(void *, int, int, int, int, long long int);

// graph

status_t jgrapht_graph_create(int, int, int, int, void**);

status_t jgrapht_graph_vertices_count(void *, long long*);

status_t jgrapht_graph_edges_count(void *, long long*);

status_t jgrapht_graph_add_vertex(void *, long long*);

status_t jgrapht_graph_remove_vertex(void *, long long int, int*);

status_t jgrapht_graph_contains_vertex(void *, long long int, int*);

status_t jgrapht_graph_add_edge(void *, long long int, long long int, long long*);

status_t jgrapht_graph_remove_edge(void *, long long int, int*);

status_t jgrapht_graph_contains_edge(void *, long long int, int*);

status_t jgrapht_graph_contains_edge_between(void *, long long int, long long int, int*);

status_t jgrapht_graph_degree_of(void *, long long int, long long*);

status_t jgrapht_graph_indegree_of(void *, long long int, long long*);

status_t jgrapht_graph_outdegree_of(void *, long long int, long long*);

status_t jgrapht_graph_edge_source(void *, long long int, long long*);

status_t jgrapht_graph_edge_target(void *, long long int, long long*);

status_t jgrapht_graph_is_weighted(void *, int*);

status_t jgrapht_graph_is_directed(void *, int*);

status_t jgrapht_graph_is_undirected(void *, int*);

status_t jgrapht_graph_is_allowing_selfloops(void *, int*);

status_t jgrapht_graph_is_allowing_multipleedges(void *, int*);

status_t jgrapht_graph_get_edge_weight(void *, long long int, double*);

status_t jgrapht_graph_set_edge_weight(void *, long long int, double);

status_t jgrapht_graph_create_all_vit(void *, void**);

status_t jgrapht_graph_create_all_eit(void *, void**);

status_t jgrapht_graph_create_between_eit(void *, long long int, long long int, void**);

status_t jgrapht_graph_vertex_create_eit(void *, long long int, void**);

status_t jgrapht_graph_vertex_create_out_eit(void *, long long int, void**);

status_t jgrapht_graph_vertex_create_in_eit(void *, long long int, void**);

status_t jgrapht_graph_as_undirected(void *, void**);

status_t jgrapht_graph_as_unmodifiable(void *, void**);

status_t jgrapht_graph_as_unweighted(void *, void**);

status_t jgrapht_graph_as_edgereversed(void *, void**);

// graph metrics

status_t jgrapht_graph_metrics_diameter(void *, double*);

status_t jgrapht_graph_metrics_radius(void *, double*);

status_t jgrapht_graph_metrics_girth(void *, long long*);

status_t jgrapht_graph_metrics_triangles(void *, long long*);

// graph path 

status_t jgrapht_graphpath_get_fields(void *, double*, long long*, long long*, void**);

// graph test

status_t jgrapht_graph_test_is_empty(void *, int*);

status_t jgrapht_graph_test_is_simple(void *, int*);

status_t jgrapht_graph_test_has_selfloops(void *, int*);

status_t jgrapht_graph_test_has_multipleedges(void *, int*);

status_t jgrapht_graph_test_is_complete(void *, int*);

status_t jgrapht_graph_test_is_weakly_connected(void *, int*);

status_t jgrapht_graph_test_is_strongly_connected(void *, int*);

status_t jgrapht_graph_test_is_tree(void *, int*);

status_t jgrapht_graph_test_is_forest(void *, int*);

status_t jgrapht_graph_test_is_overfull(void *, int*);

status_t jgrapht_graph_test_is_split(void *, int*);

status_t jgrapht_graph_test_is_bipartite(void *, int*);

status_t jgrapht_graph_test_is_cubic(void *, int*);

status_t jgrapht_graph_test_is_eulerian(void *, int*);

status_t jgrapht_graph_test_is_chordal(void *, int*);

status_t jgrapht_graph_test_is_weakly_chordal(void *, int*);

status_t jgrapht_graph_test_has_ore(void *, int*);

status_t jgrapht_graph_test_is_trianglefree(void *, int*);

status_t jgrapht_graph_test_is_perfect(void *, int*);

status_t jgrapht_graph_test_is_planar(void *, int*);

status_t jgrapht_graph_test_is_kuratowski_subdivision(void *, int*);

status_t jgrapht_graph_test_is_k33_subdivision(void *, int*);

status_t jgrapht_graph_test_is_k5_subdivision(void *, int*);

// iterators

status_t jgrapht_it_next_long(void *, long long*);

status_t jgrapht_it_next_double(void *, double*);

status_t jgrapht_it_next_object(void *, void**);

status_t jgrapht_it_hasnext(void *, int*);

// map

status_t jgrapht_map_create(void**);

status_t jgrapht_map_linked_create(void**);

status_t jgrapht_map_keys_it_create(void *, void**);

status_t jgrapht_map_size(void *, long long*);

status_t jgrapht_map_values_it_create(void *, void**);

status_t jgrapht_map_long_double_put(void *, long long int, double);

status_t jgrapht_map_long_long_put(void *, long long int, long long int);

status_t jgrapht_map_long_double_get(void *, long long int, double*);

status_t jgrapht_map_long_long_get(void *, long long int, long long*);

status_t jgrapht_map_long_contains_key(void *, long long int, int*);

status_t jgrapht_map_long_double_remove(void *, long long int, double*);

status_t jgrapht_map_long_long_remove(void *, long long int, long long*);

status_t jgrapht_map_clear(void *);

// matching

status_t jgrapht_matching_exec_greedy_general_max_card(void *, double*, void**);

status_t jgrapht_matching_exec_custom_greedy_general_max_card(void *, int, double*, void**);

status_t jgrapht_matching_exec_edmonds_general_max_card_dense(void *, double*, void**);

status_t jgrapht_matching_exec_edmonds_general_max_card_sparse(void *, double*, void**);

status_t jgrapht_matching_exec_greedy_general_max_weight(void *, double*, void**);

status_t jgrapht_matching_exec_custom_greedy_general_max_weight(void *, int, double, double*, void**);

status_t jgrapht_matching_exec_pathgrowing_max_weight(void *, double*, void**);

status_t jgrapht_matching_exec_blossom5_general_max_weight(void *, double*, void**);

status_t jgrapht_matching_exec_blossom5_general_min_weight(void *, double*, void**);

status_t jgrapht_matching_exec_blossom5_general_perfect_max_weight(void *, double*, void**);

status_t jgrapht_matching_exec_blossom5_general_perfect_min_weight(void *, double*, void**);

status_t jgrapht_matching_exec_bipartite_max_card(void *, double*, void**);

status_t jgrapht_matching_exec_bipartite_perfect_min_weight(void *, void *, void *, double*, void**);

status_t jgrapht_matching_exec_bipartite_max_weight(void *, double*, void**);

// cleanup

status_t jgrapht_destroy(void *);

// mst

status_t jgrapht_mst_exec_kruskal(void *, double*, void**);

status_t jgrapht_mst_exec_prim(void *, double*, void**);

status_t jgrapht_mst_exec_boruvka(void *, double*, void**);

// partition

status_t jgrapht_partition_exec_bipartite(void *, int*, void**, void**);

// scoring

status_t jgrapht_scoring_exec_alpha_centrality(void *, void**);

status_t jgrapht_scoring_exec_custom_alpha_centrality(void *, double, double, int, double, void**);

status_t jgrapht_scoring_exec_betweenness_centrality(void *, void**);

status_t jgrapht_scoring_exec_custom_betweenness_centrality(void *, int, void**);

status_t jgrapht_scoring_exec_closeness_centrality(void *, void**);

status_t jgrapht_scoring_exec_custom_closeness_centrality(void *, int, int, void**);

status_t jgrapht_scoring_exec_harmonic_centrality(void *, void**);

status_t jgrapht_scoring_exec_custom_harmonic_centrality(void *, int, int, void**);

status_t jgrapht_scoring_exec_pagerank(void *, void**);

status_t jgrapht_scoring_exec_custom_pagerank(void *, double, int, double, void**);

// set

status_t jgrapht_set_create(void**);

status_t jgrapht_set_linked_create(void**);

status_t jgrapht_set_it_create(void *, void**);

status_t jgrapht_set_size(void *, long long*);

status_t jgrapht_set_long_add(void *, long long int, int*);

status_t jgrapht_set_double_add(void *, double, int *);

status_t jgrapht_set_long_remove(void *, long long int);

status_t jgrapht_set_double_remove(void *, double);

status_t jgrapht_set_long_contains(void *, long long int, int*);

status_t jgrapht_set_double_contains(void *, double, int*);

status_t jgrapht_set_clear(void *);

// shortest paths 

status_t jgrapht_sp_exec_dijkstra_get_path_between_vertices(void *, long long int, long long int, void**);

status_t jgrapht_sp_exec_bidirectional_dijkstra_get_path_between_vertices(void *, long long int, long long int, void**);

status_t jgrapht_sp_exec_dijkstra_get_singlesource_from_vertex(void *, long long int, void**);

status_t jgrapht_sp_exec_bellmanford_get_singlesource_from_vertex(void *, long long int, void**);

status_t jgrapht_sp_exec_bfs_get_singlesource_from_vertex(void *, long long int, void**);

status_t jgrapht_sp_exec_johnson_get_allpairs(void *, void**);

status_t jgrapht_sp_exec_floydwarshall_get_allpairs(void *, void**);

status_t jgrapht_sp_singlesource_get_path_to_vertex(void *, long long int, void**);

status_t jgrapht_sp_allpairs_get_path_between_vertices(void *, long long int, long long int, void**);

status_t jgrapht_sp_allpairs_get_singlesource_from_vertex(void *, long long int, void**);

// spanner

status_t jgrapht_spanner_exec_greedy_multiplicative(void *, int, double*, void**);

// tour

status_t jgrapht_tour_tsp_random(void *, long long int, void**);

status_t jgrapht_tour_tsp_greedy_heuristic(void *, void**);

status_t jgrapht_tour_tsp_nearest_insertion_heuristic(void *, void**);

status_t jgrapht_tour_tsp_nearest_neighbor_heuristic(void *, long long int, void**);

status_t jgrapht_tour_metric_tsp_christofides(void *, void**);

status_t jgrapht_tour_metric_tsp_two_approx(void *, void**);

status_t jgrapht_tour_tsp_held_karp(void *, void**);

status_t jgrapht_tour_hamiltonian_palmer(void *, void**);

status_t jgrapht_tour_tsp_two_opt_heuristic(void *, int, double, long long int, void**);

status_t jgrapht_tour_tsp_two_opt_heuristic_improve(void *, double, long long int, void**);

// traverse

status_t jgrapht_traverse_create_bfs_from_all_vertices_vit(void *, void**);

status_t jgrapht_traverse_create_bfs_from_vertex_vit(void *, long long int, void**);

status_t jgrapht_traverse_create_lex_bfs_vit(void *, void**);

status_t jgrapht_traverse_create_dfs_from_all_vertices_vit(void *, void**);

status_t jgrapht_traverse_create_dfs_from_vertex_vit(void *, long long int, void**);

status_t jgrapht_traverse_create_topological_order_vit(void *, void**);

status_t jgrapht_traverse_create_random_walk_from_vertex_vit(void *, long long int, void**);

status_t jgrapht_traverse_create_custom_random_walk_from_vertex_vit(void *, long long int, int, long long int, long long int, void**);

status_t jgrapht_traverse_create_max_cardinality_vit(void *, void**);

status_t jgrapht_traverse_create_degeneracy_ordering_vit(void *, void**);

status_t jgrapht_traverse_create_closest_first_from_vertex_vit(void *, long long int, void**);

status_t jgrapht_traverse_create_custom_closest_first_from_vertex_vit(void *, long long int, double, void**);

// vertex cover

status_t jgrapht_vertexcover_exec_greedy(void *, double*, void**);

status_t jgrapht_vertexcover_exec_greedy_weighted(void *, void *, double*, void**);

status_t jgrapht_vertexcover_exec_clarkson(void *, double*, void**);

status_t jgrapht_vertexcover_exec_clarkson_weighted(void *, void *, double*, void**);

status_t jgrapht_vertexcover_exec_edgebased(void *, double*, void**);

status_t jgrapht_vertexcover_exec_baryehudaeven(void *, double*, void**);

status_t jgrapht_vertexcover_exec_baryehudaeven_weighted(void *, void *, double*, void**);

status_t jgrapht_vertexcover_exec_exact(void *, double*, void**);

status_t jgrapht_vertexcover_exec_exact_weighted(void *, void *, double*, void**);

// vm

void jgrapht_vmLocatorSymbol();

#if defined(__cplusplus)
}
#endif
#endif
