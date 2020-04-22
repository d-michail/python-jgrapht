
%module jgrapht

%{
#define SWIG_FILE_WITH_INIT
#include "jgrapht.h"
%}

%include <typemaps.i>

// custom typemap to append void** types to the result
%typemap(in,numinputs=0,noblock=1) void **OUTPUT ($*1_ltype temp, int res = SWIG_TMPOBJ) {
    $1 = &temp;
}

%typemap(argout,noblock=1) void **OUTPUT {
    %append_output(SWIG_NewPointerObj(*$1, $*1_descriptor, SWIG_POINTER_NOSHADOW | %newpointer_flags));
}


// library init

void jgrapht_thread_create();

void jgrapht_thread_destroy();

int jgrapht_is_thread_attached();

// clustering

int jgrapht_clustering_exec_k_spanning_tree(void *, int, void** OUTPUT);

int jgrapht_clustering_get_number_clusters(void *, long long* OUTPUT);

int jgrapht_clustering_ith_cluster_vit(void *, int, void** OUTPUT);

// coloring

int jgrapht_coloring_exec_greedy(void *, void** OUTPUT);

int jgrapht_coloring_exec_greedy_smallestdegreelast(void *, void** OUTPUT);

int jgrapht_coloring_exec_backtracking_brown(void *, void** OUTPUT);

int jgrapht_coloring_exec_greedy_largestdegreefirst(void *, void** OUTPUT);

int jgrapht_coloring_exec_greedy_random(void *, void** OUTPUT);

int jgrapht_coloring_exec_greedy_random_with_seed(void *, long long int, void** OUTPUT);

int jgrapht_coloring_exec_greedy_dsatur(void *, void** OUTPUT);

int jgrapht_coloring_exec_color_refinement(void *, void** OUTPUT);

int jgrapht_coloring_get_number_colors(void *, long long* OUTPUT);

int jgrapht_coloring_get_vertex_color_map(void *, void** OUTPUT);

// error

void jgrapht_clear_errno();

int jgrapht_get_errno();

char *jgrapht_get_errno_msg();

// generate

int jgrapht_generate_barabasi_albert(void *, int, int, int, long long int);

int jgrapht_generate_barabasi_albert_forest(void *, int, int, long long int);

int jgrapht_generate_complete(void *, int);

int jgrapht_generate_bipartite_complete(void *, int, int);

int jgrapht_generate_empty(void *, int);

// graph

int jgrapht_graph_create(int, int, int, int, void **OUTPUT);

int jgrapht_graph_vertices_count(void *, long long* OUTPUT);

int jgrapht_graph_edges_count(void *, long long* OUTPUT);

int jgrapht_graph_add_vertex(void *, long long* OUTPUT);

int jgrapht_graph_remove_vertex(void *, long long int, int* OUTPUT);

int jgrapht_graph_contains_vertex(void *, long long int, int* OUTPUT);

int jgrapht_graph_add_edge(void *, long long int, long long int, long long* OUTPUT);

int jgrapht_graph_remove_edge(void *, long long int, int* OUTPUT);

int jgrapht_graph_contains_edge(void *, long long int, int* OUTPUT);

int jgrapht_graph_contains_edge_between(void *, long long int, long long int, int* OUTPUT);

int jgrapht_graph_degree_of(void *, long long int, long long* OUTPUT);

int jgrapht_graph_indegree_of(void *, long long int, long long* OUTPUT);

int jgrapht_graph_outdegree_of(void *, long long int, long long* OUTPUT);

int jgrapht_graph_edge_source(void *, long long int, long long* OUTPUT);

int jgrapht_graph_edge_target(void *, long long int, long long* OUTPUT);

int jgrapht_graph_is_weighted(void *, int* OUTPUT);

int jgrapht_graph_is_directed(void *, int* OUTPUT);

int jgrapht_graph_is_undirected(void *, int* OUTPUT);

int jgrapht_graph_is_allowing_selfloops(void *, int* OUTPUT);

int jgrapht_graph_is_allowing_multipleedges(void *, int* OUTPUT);

int jgrapht_graph_get_edge_weight(void *, long long int, double* OUTPUT);

int jgrapht_graph_set_edge_weight(void *, long long int, double);

int jgrapht_graph_create_all_vit(void *, void** OUTPUT);

int jgrapht_graph_create_all_eit(void *, void** OUTPUT);

int jgrapht_graph_create_between_eit(void *, long long int, long long int, void** OUTPUT);

int jgrapht_graph_vertex_create_eit(void *, long long int, void** OUTPUT);

int jgrapht_graph_vertex_create_out_eit(void *, long long int, void** OUTPUT);

int jgrapht_graph_vertex_create_in_eit(void *, long long int, void** OUTPUT);

int jgrapht_graph_as_undirected(void *, void** OUTPUT);

int jgrapht_graph_as_unmodifiable(void *, void** OUTPUT);

int jgrapht_graph_as_unweighted(void *, void** OUTPUT);

int jgrapht_graph_as_edgereversed(void *, void** OUTPUT);

// graph test

int jgrapht_graph_test_is_empty(void *, int* OUTPUT);

int jgrapht_graph_test_is_simple(void *, int* OUTPUT);

int jgrapht_graph_test_has_selfloops(void *, int* OUTPUT);

int jgrapht_graph_test_has_multipleedges(void *, int* OUTPUT);

int jgrapht_graph_test_is_complete(void *, int* OUTPUT);

int jgrapht_graph_test_is_weakly_connected(void *, int* OUTPUT);

int jgrapht_graph_test_is_strongly_connected(void *, int* OUTPUT);

int jgrapht_graph_test_is_tree(void *, int* OUTPUT);

int jgrapht_graph_test_is_forest(void *, int* OUTPUT);

int jgrapht_graph_test_is_overfull(void *, int* OUTPUT);

int jgrapht_graph_test_is_split(void *, int* OUTPUT);

int jgrapht_graph_test_is_bipartite(void *, int* OUTPUT);

int jgrapht_graph_test_is_cubic(void *, int* OUTPUT);

int jgrapht_graph_test_is_eulerian(void *, int* OUTPUT);

int jgrapht_graph_test_is_chordal(void *, int* OUTPUT);

int jgrapht_graph_test_is_weakly_chordal(void *, int* OUTPUT);

int jgrapht_graph_test_has_ore(void *, int* OUTPUT);

int jgrapht_graph_test_is_trianglefree(void *, int* OUTPUT);

int jgrapht_graph_test_is_perfect(void *, int* OUTPUT);

int jgrapht_graph_test_is_planar(void *, int* OUTPUT);

int jgrapht_graph_test_is_kuratowski_subdivision(void *, int* OUTPUT);

int jgrapht_graph_test_is_k33_subdivision(void *, int* OUTPUT);

int jgrapht_graph_test_is_k5_subdivision(void *, int* OUTPUT);

// iterators

int jgrapht_it_next_long(void *, long long* OUTPUT);

int jgrapht_it_next_double(void *, double* OUTPUT);

int jgrapht_it_hasnext(void *, int* OUTPUT);

// map

int jgrapht_map_create(void** OUTPUT);

int jgrapht_map_linked_create(void** OUTPUT);

int jgrapht_map_keys_it_create(void *, void** OUTPUT);

int jgrapht_map_size(void *, long long* OUTPUT);

int jgrapht_map_values_it_create(void *, void** OUTPUT);

int jgrapht_map_long_double_put(void *, long long int, double);

int jgrapht_map_long_long_put(void *, long long int, long long int);

int jgrapht_map_long_double_get(void *, long long int, double* OUTPUT);

int jgrapht_map_long_long_get(void *, long long int, long long* OUTPUT);

int jgrapht_map_long_contains_key(void *, long long int, int* OUTPUT);

int jgrapht_map_clear(void *);

// matching

int jgrapht_matching_exec_greedy_general_max_card(void *, void** OUTPUT);

int jgrapht_matching_exec_custom_greedy_general_max_card(void *, int, void** OUTPUT);

int jgrapht_matching_exec_edmonds_general_max_card_dense(void *, void** OUTPUT);

int jgrapht_matching_exec_edmonds_general_max_card_sparse(void *, void** OUTPUT);

int jgrapht_matching_exec_greedy_general_max_weight(void *, void** OUTPUT);

int jgrapht_matching_exec_custom_greedy_general_max_weight(void *, int, double, void** OUTPUT);

int jgrapht_matching_exec_pathgrowing_max_weight(void *, void** OUTPUT);

int jgrapht_matching_exec_blossom5_general_max_weight(void *, void** OUTPUT);

int jgrapht_matching_exec_blossom5_general_min_weight(void *, void** OUTPUT);

int jgrapht_matching_exec_blossom5_general_perfect_max_weight(void *, void** OUTPUT);

int jgrapht_matching_exec_blossom5_general_perfect_min_weight(void *, void** OUTPUT);

int jgrapht_matching_exec_bipartite_max_card(void *, void** OUTPUT);

int jgrapht_matching_exec_bipartite_perfect_min_weight(void *, void *, void *, void** OUTPUT);

int jgrapht_matching_exec_bipartite_max_weight(void *, void** OUTPUT);

int jgrapht_matching_get_weight(void *, double* OUTPUT);

int jgrapht_matching_get_card(void *, long long* OUTPUT);

int jgrapht_matching_create_eit(void *, void** OUTPUT);

// cleanup

int jgrapht_destroy(void *);

// mst

int jgrapht_mst_exec_kruskal(void *, void** OUTPUT);

int jgrapht_mst_exec_prim(void *, void** OUTPUT);

int jgrapht_mst_exec_boruvka(void *, void** OUTPUT);

int jgrapht_mst_get_weight(void *, double* OUTPUT);

int jgrapht_mst_create_eit(void *, void** OUTPUT);

// partition

int jgrapht_partition_exec_bipartite(void *, int* OUTPUT, void** OUTPUT, void** OUTPUT);

// scoring

int jgrapht_scoring_exec_alpha_centrality(void *, void** OUTPUT);

int jgrapht_scoring_exec_custom_alpha_centrality(void *, double, double, int, double, void** OUTPUT);

int jgrapht_scoring_exec_betweenness_centrality(void *, void** OUTPUT);

int jgrapht_scoring_exec_custom_betweenness_centrality(void *, int, void** OUTPUT);

int jgrapht_scoring_exec_closeness_centrality(void *, void** OUTPUT);

int jgrapht_scoring_exec_custom_closeness_centrality(void *, int, int, void** OUTPUT);

int jgrapht_scoring_exec_harmonic_centrality(void *, void** OUTPUT);

int jgrapht_scoring_exec_custom_harmonic_centrality(void *, int, int, void** OUTPUT);

int jgrapht_scoring_exec_pagerank(void *, void** OUTPUT);

int jgrapht_scoring_exec_custom_pagerank(void *, double, int, double, void** OUTPUT);

// set

int jgrapht_set_create(void** OUTPUT);

int jgrapht_set_linked_create(void** OUTPUT);

int jgrapht_set_it_create(void *, void** OUTPUT);

int jgrapht_set_size(void *, long long* OUTPUT);

int jgrapht_set_long_add(void *, long long int);

int jgrapht_set_double_add(void *, double);

int jgrapht_set_long_remove(void *, long long int);

int jgrapht_set_double_remove(void *, double);

int jgrapht_set_long_contains(void *, long long int, int* OUTPUT);

int jgrapht_set_double_contains(void *, double, int* OUTPUT);

int jgrapht_set_clear(void *);

// vertex cover

int jgrapht_vertexcover_exec_greedy(void *, void** OUTPUT);

int jgrapht_vertexcover_exec_greedy_weighted(void *, void *, void** OUTPUT);

int jgrapht_vertexcover_exec_clarkson(void *, void** OUTPUT);

int jgrapht_vertexcover_exec_clarkson_weighted(void *, void *, void** OUTPUT);

int jgrapht_vertexcover_exec_edgebased(void *, void** OUTPUT);

int jgrapht_vertexcover_exec_baryehudaeven(void *, void**);

int jgrapht_vertexcover_exec_baryehudaeven_weighted(void *, void *, void**);

int jgrapht_vertexcover_exec_exact(void *, void**);

int jgrapht_vertexcover_exec_exact_weighted(void *, void *, void**);

int jgrapht_vertexcover_get_weight(void *, double* OUTPUT);

int jgrapht_vertexcover_create_vit(void *, void**);

// vm

void jgrapht_vmLocatorSymbol();
