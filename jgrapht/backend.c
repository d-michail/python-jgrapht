#include <stdlib.h>
#include <stdio.h>

#include <jgrapht_capi_types.h>
#include <jgrapht_capi.h>

#ifdef _WIN32
#define THREAD_LOCAL __declspec( thread )
#else
#define THREAD_LOCAL __thread 
#endif

// single graalVM isolate
static graal_isolate_t *isolate = NULL;

// thread local variable
static THREAD_LOCAL graal_isolatethread_t *thread = NULL;

// library init
void jgrapht_init() {
    // do we need to synchronize here, or does the GIL protect us?
    if (isolate == NULL) { 
        // create isolate and attach thread
        if (graal_create_isolate(NULL, &isolate, &thread) != 0) {
            fprintf(stderr, "graal_create_isolate error\n");
            exit(EXIT_FAILURE);
        }
    } else if (thread == NULL) {
        // attach thread
        if (graal_attach_thread(isolate, &thread) != 0) { 
            fprintf(stderr, "graal_attach_thread error\n");
            exit(EXIT_FAILURE);
        }
    }
}

// library cleanup
void jgrapht_cleanup() {
    // let the JVM cleanup for itself
}

int jgrapht_is_initialized() { 
    return thread != NULL && isolate != NULL;
}

#define LAZY_THREAD_ATTACH \
    if (thread == NULL) { \
        if (graal_attach_thread(isolate, &thread) != 0) {    \
            fprintf(stderr, "graal_attach_thread error\n");  \
            exit(EXIT_FAILURE);                              \
        }                                                    \
    }

// error

void jgrapht_error_clear_errno() {
    LAZY_THREAD_ATTACH
    jgrapht_capi_error_clear_errno(thread);
}

status_t jgrapht_error_get_errno() { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_error_get_errno(thread);
}

char * jgrapht_error_get_errno_msg() {
    LAZY_THREAD_ATTACH
    return jgrapht_capi_error_get_errno_msg(thread);
}

void jgrapht_error_print_stack_trace() { 
    LAZY_THREAD_ATTACH
    jgrapht_capi_error_print_stack_trace(thread);
}

// vm

void jgrapht_vmLocatorSymbol() {
    LAZY_THREAD_ATTACH
    vmLocatorSymbol(thread);
}

// attribute store

int jgrapht_attributes_store_create(void** res) {
    LAZY_THREAD_ATTACH
    return jgrapht_capi_attributes_store_create(thread, res);
}

int jgrapht_attributes_store_put_boolean_attribute(void *store, int element, char* key, int value) {
    LAZY_THREAD_ATTACH 
    return jgrapht_capi_attributes_store_put_boolean_attribute(thread, store, element, key, value);
}

int jgrapht_attributes_store_put_int_attribute(void *store, int element, char* key, int value) {
    LAZY_THREAD_ATTACH
    return jgrapht_capi_attributes_store_put_int_attribute(thread, store, element, key, value);
}

int jgrapht_attributes_store_put_long_attribute(void *store, int element, char* key, long long int value) {
    LAZY_THREAD_ATTACH
    return jgrapht_capi_attributes_store_put_long_attribute(thread, store, element, key, value);
}

int jgrapht_attributes_store_put_double_attribute(void *store, int element, char* key, double value) {
    LAZY_THREAD_ATTACH
    return jgrapht_capi_attributes_store_put_double_attribute(thread, store, element, key, value);
}

int jgrapht_attributes_store_put_string_attribute(void *store, int element, char* key, char* value) {
    LAZY_THREAD_ATTACH
    return jgrapht_capi_attributes_store_put_string_attribute(thread, store, element, key, value);
}

int jgrapht_attributes_store_remove_attribute(void *store, int element, char* key) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_attributes_store_remove_attribute(thread, store, element, key);
}

int jgrapht_attributes_registry_create(void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_attributes_registry_create(thread, res);
}

int jgrapht_attributes_registry_register_attribute(void *registry, char* name, char* category, char* type, char* default_value) {
    LAZY_THREAD_ATTACH
    return jgrapht_capi_attributes_registry_register_attribute(thread, registry, name, category, type, default_value);
}

int jgrapht_attributes_registry_unregister_attribute(void *registry, char* name, char* category, char* type, char* default_value) {
    LAZY_THREAD_ATTACH
    return jgrapht_capi_attributes_registry_unregister_attribute(thread, registry, name, category, type, default_value);
}

// clique

int jgrapht_clique_exec_bron_kerbosch(void *g, long long int timeout, void** res) {
    LAZY_THREAD_ATTACH 
    return jgrapht_capi_clique_exec_bron_kerbosch(thread, g, timeout, res);
}

int jgrapht_clique_exec_bron_kerbosch_pivot(void *g, long long int timeout, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_clique_exec_bron_kerbosch_pivot(thread, g, timeout, res);
}

int jgrapht_clique_exec_bron_kerbosch_pivot_degeneracy_ordering(void *g, long long int timeout, void** res) {
    LAZY_THREAD_ATTACH
    return jgrapht_capi_clique_exec_bron_kerbosch_pivot_degeneracy_ordering(thread, g, timeout, res);
}

int jgrapht_clique_exec_chordal_max_clique(void *g, void** res) {
    LAZY_THREAD_ATTACH
    return jgrapht_capi_clique_exec_chordal_max_clique(thread, g, res);
}

// clustering

int jgrapht_clustering_exec_k_spanning_tree(void *g, int k, void**res) {
    LAZY_THREAD_ATTACH
    return jgrapht_capi_clustering_exec_k_spanning_tree(thread, g, k, res);
}

int jgrapht_clustering_exec_label_propagation(void *g, int max_iterations, long long int seed, void** res) {
    LAZY_THREAD_ATTACH
    return jgrapht_capi_clustering_exec_label_propagation(thread, g, max_iterations, seed, res);
}

int jgrapht_clustering_get_number_clusters(void *clustering, int* res) {
    LAZY_THREAD_ATTACH
    return jgrapht_capi_clustering_get_number_clusters(thread, clustering, res);
}

int jgrapht_clustering_ith_cluster_vit(void *clustering, int i, void** res) {
    LAZY_THREAD_ATTACH
    return jgrapht_capi_clustering_ith_cluster_vit(thread, clustering, i, res);
}

// coloring

int jgrapht_coloring_exec_greedy(void *g, int* colors_res, void** res) {
    LAZY_THREAD_ATTACH
    return jgrapht_capi_coloring_exec_greedy(thread, g, colors_res, res);
}

int jgrapht_coloring_exec_greedy_smallestdegreelast(void *g, int* colors_res, void** res) {
    LAZY_THREAD_ATTACH
    return jgrapht_capi_coloring_exec_greedy_smallestdegreelast(thread, g, colors_res, res);
}

int jgrapht_coloring_exec_backtracking_brown(void *g, int* colors_res, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_coloring_exec_backtracking_brown(thread, g, colors_res, res);
}

int jgrapht_coloring_exec_greedy_largestdegreefirst(void *g, int* colors_res, void** res) {
    LAZY_THREAD_ATTACH
    return jgrapht_capi_coloring_exec_greedy_largestdegreefirst(thread, g, colors_res, res);
}

int jgrapht_coloring_exec_greedy_random(void *g, int* colors_res, void** res) {
    LAZY_THREAD_ATTACH
    return jgrapht_capi_coloring_exec_greedy_random(thread, g, colors_res, res);
}

int jgrapht_coloring_exec_greedy_random_with_seed(void * g, long long int seed, int* colors_res, void** res) {
    LAZY_THREAD_ATTACH
    return jgrapht_capi_coloring_exec_greedy_random_with_seed(thread, g, seed, colors_res, res);
}

int jgrapht_coloring_exec_greedy_dsatur(void *g, int* colors_res, void** res) {
    LAZY_THREAD_ATTACH
    return jgrapht_capi_coloring_exec_greedy_dsatur(thread, g, colors_res, res);
}

int jgrapht_coloring_exec_color_refinement(void *g, int* colors_res, void** res) {
    LAZY_THREAD_ATTACH
    return jgrapht_capi_coloring_exec_color_refinement(thread, g, colors_res, res);
}

int jgrapht_coloring_exec_chordal_minimum_coloring(void *g, int* colors_res, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_coloring_exec_chordal_minimum_coloring(thread, g, colors_res, res);
}

// connectivity

int jgrapht_connectivity_strong_exec_kosaraju(void *g, int* is_connected_res, void** res) {
    LAZY_THREAD_ATTACH 
    return jgrapht_capi_connectivity_strong_exec_kosaraju(thread, g, is_connected_res, res);
}

int jgrapht_connectivity_strong_exec_gabow(void *g, int* is_connected_res, void** res) {
    LAZY_THREAD_ATTACH
    return jgrapht_capi_connectivity_strong_exec_gabow(thread, g, is_connected_res, res);
}

int jgrapht_connectivity_weak_exec_bfs(void *g, int* is_connected_res, void** res) {
    LAZY_THREAD_ATTACH
    return jgrapht_capi_connectivity_weak_exec_bfs(thread, g, is_connected_res, res);
}

// cut

int jgrapht_cut_mincut_exec_stoer_wagner(void *g, double* weight, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_cut_mincut_exec_stoer_wagner(thread, g, weight, res);
}

int jgrapht_cut_gomoryhu_exec_gusfield(void *g, void** gh_res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_cut_gomoryhu_exec_gusfield(thread, g, gh_res);
}

int jgrapht_cut_gomoryhu_min_st_cut(void *gh, int source, int sink, double* value_res, void** source_partition_res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_cut_gomoryhu_min_st_cut(thread, gh, source, sink, value_res, source_partition_res);
}

int jgrapht_cut_gomoryhu_min_cut(void *gh, double* value_res, void** source_partition_res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_cut_gomoryhu_min_cut(thread, gh, value_res, source_partition_res);
}

int jgrapht_cut_gomoryhu_tree(void *gh, void** tree_res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_cut_gomoryhu_tree(thread, gh, tree_res);
}

int jgrapht_cut_oddmincutset_exec_padberg_rao(void *g, void *odd_vertices, int use_tree_compression, double* value_res, void** source_partition_res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_cut_oddmincutset_exec_padberg_rao(thread, g, odd_vertices, use_tree_compression, value_res, source_partition_res);
}

// cycles

int jgrapht_cycles_eulerian_exec_hierholzer(void *g, int* is_eulerian_res, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_cycles_eulerian_exec_hierholzer(thread, g, is_eulerian_res, res);
}

int jgrapht_cycles_chinese_postman_exec_edmonds_johnson(void *g, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_cycles_chinese_postman_exec_edmonds_johnson(thread, g, res);
}

int jgrapht_cycles_simple_enumeration_exec_tarjan(void *g, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_cycles_simple_enumeration_exec_tarjan(thread, g, res);
}

int jgrapht_cycles_simple_enumeration_exec_tiernan(void *g, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_cycles_simple_enumeration_exec_tiernan(thread, g, res);
}

int jgrapht_cycles_simple_enumeration_exec_szwarcfiter_lauer(void *g, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_cycles_simple_enumeration_exec_szwarcfiter_lauer(thread, g, res);
}

int jgrapht_cycles_simple_enumeration_exec_johnson(void *g, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_cycles_simple_enumeration_exec_johnson(thread, g, res);
}

int jgrapht_cycles_simple_enumeration_exec_hawick_james(void *g, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_cycles_simple_enumeration_exec_hawick_james(thread, g, res);
}

int jgrapht_cycles_fundamental_basis_exec_queue_bfs(void *g, double* weight_res, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_cycles_fundamental_basis_exec_queue_bfs(thread, g, weight_res, res);
}

int jgrapht_cycles_fundamental_basis_exec_stack_bfs(void *g, double* weight_res, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_cycles_fundamental_basis_exec_stack_bfs(thread, g, weight_res, res);
}

int jgrapht_cycles_fundamental_basis_exec_paton(void *g, double* weight_res, void** res) {
    LAZY_THREAD_ATTACH
    return jgrapht_capi_cycles_fundamental_basis_exec_paton(thread, g, weight_res, res);
}

// drawing

int jgrapht_drawing_layout_model_2d_create(double x_min, double y_min, double width, double height, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_drawing_layout_model_2d_create(thread, x_min, y_min, width, height, res);
}

int jgrapht_drawing_layout_model_2d_get_drawable_area(void *model, double* x_min, double* y_min, double* width, double* height) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_drawing_layout_model_2d_get_drawable_area(thread, model, x_min, y_min, width, height);
}

int jgrapht_drawing_layout_model_2d_get_vertex(void *model, int vertex, double* x_res, double* y_res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_drawing_layout_model_2d_get_vertex(thread, model, vertex, x_res, y_res);
}

int jgrapht_drawing_layout_model_2d_put_vertex(void *model, int vertex, double x, double y) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_drawing_layout_model_2d_put_vertex(thread, model, vertex, x, y);
}

int jgrapht_drawing_layout_model_2d_get_fixed(void *model, int vertex, int* res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_drawing_layout_model_2d_get_fixed(thread, model, vertex, res);
}

int jgrapht_drawing_layout_model_2d_set_fixed(void *model, int vertex, int res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_drawing_layout_model_2d_set_fixed(thread, model, vertex, res);
}

int jgrapht_drawing_exec_random_layout_2d(void *g, void *model, long long int seed) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_drawing_exec_random_layout_2d(thread, g, model, seed);
}

int jgrapht_drawing_exec_circular_layout_2d(void *g, void *model, double radius, void *vertex_comparator_fptr) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_drawing_exec_circular_layout_2d(thread, g, model, radius, vertex_comparator_fptr);
}

int jgrapht_drawing_exec_fr_layout_2d(void *g, void *model, int iterations, double norm_factor, long long int seed) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_drawing_exec_fr_layout_2d(thread, g, model, iterations, norm_factor, seed);
}

int jgrapht_drawing_exec_indexed_fr_layout_2d(void *g, void *model, int iterations, double norm_factor, long long int seed, double theta, double tolerance) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_drawing_exec_indexed_fr_layout_2d(thread, g, model, iterations, norm_factor, seed, theta, iterations);
}

// exporter

int jgrapht_export_file_dimacs(void *g, char* filename, dimacs_format_t format, int export_edge_weights, void* vertex_id_store) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_export_file_dimacs(thread, g, filename, format, export_edge_weights, vertex_id_store);
}

int jgrapht_export_string_dimacs(void *g, dimacs_format_t format, int export_edge_weights, void* vertex_id_store, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_export_string_dimacs(thread, g, format, export_edge_weights, vertex_id_store, res);
}

int jgrapht_export_file_gml(void *g, char* filename, int export_edge_weights, int export_vertex_labels, int export_edge_labels, void* vertex_attribute_store, void* edge_attribute_store, void* vertex_id_store) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_export_file_gml(thread, g, filename, export_edge_weights, export_vertex_labels, export_edge_labels, vertex_attribute_store, edge_attribute_store, vertex_id_store);
}

int jgrapht_export_string_gml(void *g, int export_edge_weights, int export_vertex_labels, int export_edge_labels, void* vertex_attribute_store, void* edge_attribute_store, void* vertex_id_store, void **res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_export_string_gml(thread, g, export_edge_weights, export_vertex_labels, export_edge_labels, vertex_attribute_store, edge_attribute_store, vertex_id_store, res);
}

int jgrapht_export_file_json(void *g, char* filename, void* vertex_attribute_store, void* edge_attribute_store, void* vertex_id_store) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_export_file_json(thread, g, filename, vertex_attribute_store, edge_attribute_store, vertex_id_store);
}

int jgrapht_export_string_json(void *g, void* vertex_attribute_store, void* edge_attribute_store, void* vertex_id_store, void **res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_export_string_json(thread, g, vertex_attribute_store, edge_attribute_store, vertex_id_store, res);
}

int jgrapht_export_file_lemon(void *g, char* filename, int export_edge_weights, int escape_strings_as_java, void* vertex_id_store) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_export_file_lemon(thread, g, filename, export_edge_weights, escape_strings_as_java, vertex_id_store);
}

int jgrapht_export_string_lemon(void *g, int export_edge_weights, int escape_strings_as_java, void* vertex_id_store, void **res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_export_string_lemon(thread, g, export_edge_weights, escape_strings_as_java, vertex_id_store, res);
}

int jgrapht_export_file_csv(void *g, char* filename, csv_format_t format, int export_edge_weights, int matrix_format_nodeid,
        int matrix_format_zero_when_no_edge, void* vertex_id_store) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_export_file_csv(thread, g, filename, format, export_edge_weights, matrix_format_nodeid, matrix_format_zero_when_no_edge, vertex_id_store);
}

int jgrapht_export_string_csv(void *g, csv_format_t format, int export_edge_weights, int matrix_format_nodeid,
        int matrix_format_zero_when_no_edge, void* vertex_id_store, void **res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_export_string_csv(thread, g, format, export_edge_weights, matrix_format_nodeid, matrix_format_zero_when_no_edge, vertex_id_store, res);
}

int jgrapht_export_file_gexf(void *g, char* filename, void *attributes_registry, void *vertex_attribute_store, void *edge_attribute_store, 
        void* vertex_id_store, void* edge_id_store, int export_edge_weights, int export_edge_labels, int export_edge_types, int export_meta) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_export_file_gexf(thread, g, filename, attributes_registry, vertex_attribute_store, edge_attribute_store, 
            vertex_id_store, edge_id_store, export_edge_weights, export_edge_labels, export_edge_types, export_meta);
}

int jgrapht_export_string_gexf(void *g,void *attributes_registry, void *vertex_attribute_store, void *edge_attribute_store, 
        void* vertex_id_store, void* edge_id_store, int export_edge_weights, int export_edge_labels, int export_edge_types, int export_meta, void **res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_export_string_gexf(thread, g, attributes_registry, vertex_attribute_store, edge_attribute_store, 
            vertex_id_store, edge_id_store, export_edge_weights, export_edge_labels, export_edge_types, export_meta, res);
}

int jgrapht_export_file_dot(void *g, char* filename, void *vertex_attribute_store, void *edge_attribute_store, void* vertex_id_store) {
    LAZY_THREAD_ATTACH 
    return jgrapht_capi_export_file_dot(thread, g, filename, vertex_attribute_store, edge_attribute_store, vertex_id_store);
}

int jgrapht_export_string_dot(void *g, void *vertex_attribute_store, void *edge_attribute_store, void* vertex_id_store, void **res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_export_string_dot(thread, g, vertex_attribute_store, edge_attribute_store, vertex_id_store, res);
}

int jgrapht_export_file_graph6(void *g, char* filename) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_export_file_graph6(thread, g, filename);
}

int jgrapht_export_string_graph6(void *g, void **res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_export_string_graph6(thread, g, res);
}

int jgrapht_export_file_sparse6(void *g, char* filename) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_export_file_sparse6(thread, g, filename);
}

int jgrapht_export_string_sparse6(void *g, void **res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_export_string_sparse6(thread, g, res);
}

int jgrapht_export_file_graphml(void *g, char* filename, void *attributes_registry, void *vertex_attribute_store, 
        void *edge_attribute_store, void* vertex_id_store, int export_edge_weights, int export_vertex_labels, int export_edge_labels) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_export_file_graphml(thread, g, filename, attributes_registry, vertex_attribute_store, edge_attribute_store,
            vertex_id_store, export_edge_weights, export_vertex_labels, export_edge_labels);
}

int jgrapht_export_string_graphml(void *g, void *attributes_registry, void *vertex_attribute_store, 
        void *edge_attribute_store, void* vertex_id_store, int export_edge_weights, int export_vertex_labels, int export_edge_labels, void **res) { 
    LAZY_THREAD_ATTACH        
    return jgrapht_capi_export_string_graphml(thread, g, attributes_registry, vertex_attribute_store, edge_attribute_store,
            vertex_id_store, export_edge_weights, export_vertex_labels, export_edge_labels, res);
}

// flow

int jgrapht_maxflow_exec_push_relabel(void *g, int source, int sink, double* valueRes, void** flowMapRes, void** cutSourcePartitionRes) {
    LAZY_THREAD_ATTACH 
    return jgrapht_capi_maxflow_exec_push_relabel(thread, g, source, sink, valueRes, flowMapRes, cutSourcePartitionRes);
}

int jgrapht_maxflow_exec_dinic(void *g, int source, int sink, double* valueRes, void** flowMapRes, void** cutSourcePartitionRes) {
    LAZY_THREAD_ATTACH 
    return jgrapht_capi_maxflow_exec_dinic(thread, g, source, sink, valueRes, flowMapRes, cutSourcePartitionRes);    
}

int jgrapht_maxflow_exec_edmonds_karp(void *g, int source, int sink, double* valueRes, void** flowMapRes, void** cutSourcePartitionRes) {
    LAZY_THREAD_ATTACH 
    return jgrapht_capi_maxflow_exec_edmonds_karp(thread, g, source, sink, valueRes, flowMapRes, cutSourcePartitionRes);
}

int jgrapht_mincostflow_exec_capacity_scaling(void *g, void *node_supply_fptr, void *arc_capacity_lower_bound_fptr, \
   void *arc_capacity_upper_bound_fptr, int scaling_factor, double* cost_res, void** flow_res, void** dual_res) {
    LAZY_THREAD_ATTACH 
    return jgrapht_capi_mincostflow_exec_capacity_scaling(thread, g, node_supply_fptr, arc_capacity_lower_bound_fptr, \
        arc_capacity_upper_bound_fptr, scaling_factor, cost_res, flow_res, dual_res);
}

int jgrapht_equivalentflowtree_exec_gusfield(void *g, void** eft_res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_equivalentflowtree_exec_gusfield(thread, g, eft_res);
}

int jgrapht_equivalentflowtree_max_st_flow(void *eft, int source, int sink, double* value_res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_equivalentflowtree_max_st_flow(thread, eft, source, sink, value_res);
}

int jgrapht_equivalentflowtree_tree(void *eft, void** tree_res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_equivalentflowtree_tree(thread, eft, tree_res);
}

// generate

int jgrapht_generate_barabasi_albert(void *g, int m0, int m, int n, long long int seed) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_generate_barabasi_albert(thread, g, m0, m, n, seed);
}

int jgrapht_generate_barabasi_albert_forest(void *g, int t, int n, long long int seed) {
    LAZY_THREAD_ATTACH
    return jgrapht_capi_generate_barabasi_albert_forest(thread, g, t, n, seed);
}

int jgrapht_generate_complete(void *g, int nodes) {
    LAZY_THREAD_ATTACH
    return jgrapht_capi_generate_complete(thread, g, nodes);
}

int jgrapht_generate_bipartite_complete(void *g, int a, int b) {
    LAZY_THREAD_ATTACH
    return jgrapht_capi_generate_bipartite_complete(thread, g, a, b);
}

int jgrapht_generate_empty(void *g, int nodes) {
    LAZY_THREAD_ATTACH
    return jgrapht_capi_generate_empty(thread, g, nodes);
}

int jgrapht_generate_gnm_random(void *g, int n, int m, int loops, int multiple_edges, long long int seed) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_generate_gnm_random(thread, g, n, m, loops, multiple_edges, seed);
}

int jgrapht_generate_gnp_random(void *g, int n, double p, int create_loops, long long int seed) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_generate_gnp_random(thread, g, n, p, create_loops, seed);
}

int jgrapht_generate_ring(void *g, int n) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_generate_ring(thread, g, n);
}

int jgrapht_generate_scalefree(void *g, int n, long long int seed) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_generate_scalefree(thread, g, n, seed);
}

int jgrapht_generate_watts_strogatz(void *g, int n, int k, double p, int add_instead_of_rewire, long long int seed) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_generate_watts_strogatz(thread, g, n, k, p, add_instead_of_rewire, seed);
}

int jgrapht_generate_kleinberg_smallworld(void *g, int n, int p, int q, int r, long long int seed) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_generate_kleinberg_smallworld(thread, g, n, p, q, r, seed);
}

int jgrapht_generate_complement(void *g, void *g_source, int generate_self_loops) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_generate_complement(thread, g, g_source, generate_self_loops);
}

int jgrapht_generate_generalized_petersen(void *g, int n, int k) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_generate_generalized_petersen(thread, g, n, k);
}

int jgrapht_generate_grid(void *g, int rows, int cols) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_generate_grid(thread, g, rows, cols);
}

int jgrapht_generate_hypercube(void *g, int dims) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_generate_hypercube(thread, g, dims);
}

int jgrapht_generate_linear(void *g, int n) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_generate_linear(thread, g, n);
}

int jgrapht_generate_random_regular(void *g, int n, int d, long long int seed) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_generate_random_regular(thread, g, n, d, seed);
}

int jgrapht_generate_star(void *g, int order) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_generate_star(thread, g, order);
}

int jgrapht_generate_wheel(void *g, int size, int inward_spokes) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_generate_wheel(thread, g, size, inward_spokes);
}

int jgrapht_generate_windmill(void *g, int m, int n, int dutch) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_generate_windmill(thread, g, m, n, dutch);
}

int jgrapht_generate_linearized_chord_diagram(void *g, int n, int m, long long int seed) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_generate_linearized_chord_diagram(thread, g, n, m, seed);
}

// graph

int jgrapht_graph_create(int directed, int allowing_self_loops, int allowing_multiple_edges, int weighted, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_graph_create(thread, directed, allowing_self_loops, allowing_multiple_edges, weighted, res);
}

int jgrapht_graph_sparse_create(int directed, int weighted, int num_vertices, void *edges, void**res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_graph_sparse_create(thread, directed, weighted, num_vertices, edges, res);
}

int jgrapht_graph_vertices_count(void *g, int* res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_graph_vertices_count(thread, g, res);
}

int jgrapht_graph_edges_count(void *g, int* res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_graph_edges_count(thread, g, res);
}

int jgrapht_graph_add_vertex(void *g, int* res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_graph_add_vertex(thread, g, res);
}

int jgrapht_graph_add_given_vertex(void *g, int vertex, int *res) {
    LAZY_THREAD_ATTACH
    return jgrapht_capi_graph_add_given_vertex(thread, g, vertex, res);
}

int jgrapht_graph_remove_vertex(void *g, int v, int* res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_graph_remove_vertex(thread, g, v, res);
}

int jgrapht_graph_contains_vertex(void *g, int v, int* res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_graph_contains_vertex(thread, g, v, res);
}

int jgrapht_graph_add_edge(void *g, int u, int v, int* res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_graph_add_edge(thread, g, u, v, res);
}

int jgrapht_graph_add_given_edge(void *g, int u, int v, int edge, int* res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_graph_add_given_edge(thread, g, u, v, edge, res);
}

int jgrapht_graph_remove_edge(void *g, int e, int* res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_graph_remove_edge(thread, g, e, res);
}

int jgrapht_graph_contains_edge(void *g, int e, int* res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_graph_contains_edge(thread, g, e, res);
}

int jgrapht_graph_contains_edge_between(void *g, int u, int v, int* res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_graph_contains_edge_between(thread, g, u, v, res);
}

int jgrapht_graph_degree_of(void *g, int v, int* res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_graph_degree_of(thread, g, v, res);
}

int jgrapht_graph_indegree_of(void *g, int v, int* res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_graph_indegree_of(thread, g, v, res);
}

int jgrapht_graph_outdegree_of(void *g, int v, int* res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_graph_outdegree_of(thread, g, v, res);
}

int jgrapht_graph_edge_source(void *g, int v, int* res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_graph_edge_source(thread, g, v, res);
}

int jgrapht_graph_edge_target(void *g, int v, int* res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_graph_edge_target(thread, g, v, res);
}

int jgrapht_graph_is_weighted(void *g, int* res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_graph_is_weighted(thread, g, res);
}

int jgrapht_graph_is_directed(void *g, int* res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_graph_is_directed(thread, g, res);
}

int jgrapht_graph_is_undirected(void *g, int* res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_graph_is_undirected(thread, g, res);
}

int jgrapht_graph_is_allowing_selfloops(void *g, int* res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_graph_is_allowing_selfloops(thread, g, res);
}

int jgrapht_graph_is_allowing_multipleedges(void *g, int* res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_graph_is_allowing_multipleedges(thread, g, res);
}

int jgrapht_graph_is_allowing_cycles(void *g, int* res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_graph_is_allowing_cycles(thread, g, res);
}

int jgrapht_graph_is_modifiable(void *g, int* res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_graph_is_modifiable(thread, g, res);
}

int jgrapht_graph_get_edge_weight(void *g, int e, double* res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_graph_get_edge_weight(thread, g, e, res);
}

int jgrapht_graph_set_edge_weight(void *g, int e, double weight) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_graph_set_edge_weight(thread, g, e, weight);
}

int jgrapht_graph_create_all_vit(void *g, void** res)  { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_graph_create_all_vit(thread, g, res);
}

int jgrapht_graph_create_all_eit(void *g, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_graph_create_all_eit(thread, g, res);
}

int jgrapht_graph_create_between_eit(void *g, int u, int v, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_graph_create_between_eit(thread, g, u, v, res);
}

int jgrapht_graph_vertex_create_eit(void *g, int v, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_graph_vertex_create_eit(thread, g, v, res);
}

int jgrapht_graph_vertex_create_out_eit(void *g, int v, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_graph_vertex_create_out_eit(thread, g, v, res);
}

int jgrapht_graph_vertex_create_in_eit(void *g, int v, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_graph_vertex_create_in_eit(thread, g, v, res);
}

int jgrapht_graph_as_undirected(void *g, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_graph_as_undirected(thread, g, res);
}

int jgrapht_graph_as_unmodifiable(void *g, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_graph_as_unmodifiable(thread, g, res);
}

int jgrapht_graph_as_unweighted(void *g, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_graph_as_unweighted(thread, g, res);
}

int jgrapht_graph_as_edgereversed(void *g, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_graph_as_edgereversed(thread, g, res);
}

int jgrapht_graph_as_weighted(void *g, void *weight_function, int cache_weights, int write_weights_through, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_graph_as_weighted(thread, g, weight_function, cache_weights, write_weights_through, res);
}

int jgrapht_graph_as_masked_subgraph(void *g, void *vertex_mask_function, void *edge_mask_function, void** res) {
    LAZY_THREAD_ATTACH
    return jgrapht_capi_graph_as_masked_subgraph(thread, g, vertex_mask_function, edge_mask_function, res);
}

int jgrapht_graph_as_subgraph(void *g, void *vertex_set, void *edge_set, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_graph_as_subgraph(thread, g, vertex_set, edge_set, res);
}

int jgrapht_graph_as_graph_union(void *g1, void *g2, void *weight_combiner_function, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_graph_as_graph_union(thread, g1, g2, weight_combiner_function, res);
}

int jgrapht_graph_dag_create(int allowing_multiple_edges, int weighted, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_graph_dag_create(thread, allowing_multiple_edges, weighted, res);
}

int jgrapht_graph_dag_topological_it(void *g, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_graph_dag_topological_it(thread, g, res);
}

int jgrapht_graph_dag_vertex_descendants(void *g, int vertex, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_graph_dag_vertex_descendants(thread, g, vertex, res);
}

int jgrapht_graph_dag_vertex_ancestors(void *g, int vertex, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_graph_dag_vertex_ancestors(thread, g, vertex, res);
}

// graph metrics

int jgrapht_graph_metrics_diameter(void *g, double* diameter) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_graph_metrics_diameter(thread, g, diameter);
}

int jgrapht_graph_metrics_radius(void *g, double* radius) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_graph_metrics_radius(thread, g, radius);
}

int jgrapht_graph_metrics_girth(void *g, int* girth) {
    LAZY_THREAD_ATTACH
    return jgrapht_capi_graph_metrics_girth(thread, g, girth);
}

int jgrapht_graph_metrics_triangles(void *g, long long int* triangles) {
    LAZY_THREAD_ATTACH
    return jgrapht_capi_graph_metrics_triangles(thread, g, triangles);
}

int jgrapht_graph_metrics_measure_graph(void *g, double* diameter_res, double* radius_res, void** center_res, void** periphery_res, void** pseudo_periphery_res, void** vertex_eccentricity_map_res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_graph_metrics_measure_graph(thread, g, diameter_res, radius_res, center_res, periphery_res, pseudo_periphery_res, vertex_eccentricity_map_res);
}

// graph test

int jgrapht_graph_test_is_empty(void *g, int* res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_graph_test_is_empty(thread, g, res);
}

int jgrapht_graph_test_is_simple(void *g, int* res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_graph_test_is_simple(thread, g, res);
}

int jgrapht_graph_test_has_selfloops(void *g, int* res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_graph_test_has_selfloops(thread, g, res);
}

int jgrapht_graph_test_has_multipleedges(void *g, int* res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_graph_test_has_multipleedges(thread, g, res);
}

int jgrapht_graph_test_is_complete(void *g, int* res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_graph_test_is_complete(thread, g, res);
}

int jgrapht_graph_test_is_weakly_connected(void *g, int* res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_graph_test_is_weakly_connected(thread, g, res);
}

int jgrapht_graph_test_is_strongly_connected(void *g, int* res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_graph_test_is_strongly_connected(thread, g, res);
}

int jgrapht_graph_test_is_tree(void *g, int* res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_graph_test_is_tree(thread, g, res);
}

int jgrapht_graph_test_is_forest(void *g, int* res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_graph_test_is_forest(thread, g, res); 
}

int jgrapht_graph_test_is_overfull(void *g, int* res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_graph_test_is_overfull(thread, g, res);
}

int jgrapht_graph_test_is_split(void *g, int* res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_graph_test_is_split(thread, g, res);
}

int jgrapht_graph_test_is_bipartite(void *g, int* res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_graph_test_is_bipartite(thread, g, res);
}

int jgrapht_graph_test_is_cubic(void *g, int* res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_graph_test_is_cubic(thread, g, res);
}

int jgrapht_graph_test_is_eulerian(void *g, int* res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_graph_test_is_eulerian(thread, g, res);
}

int jgrapht_graph_test_is_chordal(void *g, int* res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_graph_test_is_chordal(thread, g, res);
}

int jgrapht_graph_test_is_weakly_chordal(void *g, int* res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_graph_test_is_weakly_chordal(thread, g, res);
}

int jgrapht_graph_test_has_ore(void *g, int* res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_graph_test_has_ore(thread, g, res);
}

int jgrapht_graph_test_is_trianglefree(void *g, int* res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_graph_test_is_trianglefree(thread, g, res);
}

int jgrapht_graph_test_is_perfect(void *g, int* res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_graph_test_is_perfect(thread, g, res);
}

int jgrapht_graph_test_is_planar(void *g, int* res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_graph_test_is_planar(thread, g, res);
}

int jgrapht_graph_test_is_kuratowski_subdivision(void *g, int* res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_graph_test_is_kuratowski_subdivision(thread, g, res);
}

int jgrapht_graph_test_is_k33_subdivision(void *g, int* res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_graph_test_is_k33_subdivision(thread, g, res);
}

int jgrapht_graph_test_is_k5_subdivision(void *g, int* res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_graph_test_is_k5_subdivision(thread, g, res);
}

// handles

int jgrapht_handles_destroy(void *handle) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_handles_destroy(thread, handle);
}

int jgrapht_handles_get_ccharpointer(void *handle, char** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_handles_get_ccharpointer(thread, handle, res);
}

int jgrapht_handles_get_edge_pair(void *handle, int* s, int* t) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_handles_get_edge_pair(thread, handle, s, t);
}

int jgrapht_handles_get_edge_triple(void *handle, int* s, int* t, double* w) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_handles_get_edge_triple(thread, handle, s, t, w);
}

int jgrapht_handles_get_str_edge_triple(void *handle, char** s, char** t, double* w) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_handles_get_str_edge_triple(thread, handle, s, t, w);
}

int jgrapht_handles_get_graphpath(void *graph_path, double* weight, int* start_vertex, int* end_vertex, void** eit) {
    LAZY_THREAD_ATTACH
    return jgrapht_capi_handles_get_graphpath(thread, graph_path, weight, start_vertex, end_vertex, eit);
}

// importers

int jgrapht_import_file_dimacs(void *g, char* filename, void *import_vertex_id_fptr, void *v_notify_fptr, void *e_notify_fptr) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_import_file_dimacs(thread, g, filename, import_vertex_id_fptr, v_notify_fptr, e_notify_fptr);
}

int jgrapht_import_string_dimacs(void *g, char* input, void *import_vertex_id_fptr, void *v_notify_fptr, void *e_notify_fptr) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_import_string_dimacs(thread, g, input, import_vertex_id_fptr, v_notify_fptr, e_notify_fptr);
}

int jgrapht_import_file_gml(void *g, char* filename, void *import_vertex_id_fptr, void *vertex_attribute_fptr, void *edge_attribute_fptr, void *v_notify_fptr, void *e_notify_fptr) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_import_file_gml(thread, g, filename, import_vertex_id_fptr, vertex_attribute_fptr, edge_attribute_fptr, v_notify_fptr, e_notify_fptr);
}

int jgrapht_import_string_gml(void *g, char* input, void *import_vertex_id_fptr, void *vertex_attribute_fptr, void *edge_attribute_fptr, void *v_notify_fptr, void *e_notify_fptr) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_import_string_gml(thread, g, input, import_vertex_id_fptr, vertex_attribute_fptr, edge_attribute_fptr, v_notify_fptr, e_notify_fptr);
}

int jgrapht_import_file_json(void *g, char* filename, void *import_vertex_id_fptr, void *vertex_attribute_fptr, void *edge_attribute_fptr, void *v_notify_fptr, void *e_notify_fptr) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_import_file_json(thread, g, filename, import_vertex_id_fptr, vertex_attribute_fptr, edge_attribute_fptr, v_notify_fptr, e_notify_fptr);
}

int jgrapht_import_string_json(void *g, char* input, void *import_vertex_id_fptr, void *vertex_attribute_fptr, void *edge_attribute_fptr, void *v_notify_fptr, void *e_notify_fptr) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_import_string_json(thread, g, input, import_vertex_id_fptr, vertex_attribute_fptr, edge_attribute_fptr, v_notify_fptr, e_notify_fptr);
}

int jgrapht_import_file_csv(void *g, char* filename, void *import_vertex_id_fptr, void *v_notify_fptr, void *e_notify_fptr, csv_format_t format, int import_edge_weights, int matrix_format_nodeid, int matrix_format_zero_when_no_edge) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_import_file_csv(thread, g, filename, import_vertex_id_fptr, v_notify_fptr, e_notify_fptr, format, import_edge_weights, matrix_format_nodeid, matrix_format_zero_when_no_edge);
}

int jgrapht_import_string_csv(void *g, char* input, void *import_vertex_id_fptr, void *v_notify_fptr, void *e_notify_fptr, csv_format_t format, int import_edge_weights, int matrix_format_nodeid, int matrix_format_zero_when_no_edge) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_import_string_csv(thread, g, input, import_vertex_id_fptr, v_notify_fptr, e_notify_fptr, format, import_edge_weights, matrix_format_nodeid, matrix_format_zero_when_no_edge);
}

int jgrapht_import_file_gexf(void *g, char* filename, void *import_vertex_id_fptr, int validate_schema, void *vertex_attribute_fptr, void *edge_attribute_fptr, void *v_notify_fptr, void *e_notify_fptr) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_import_file_gexf(thread, g, filename, import_vertex_id_fptr, validate_schema, vertex_attribute_fptr, edge_attribute_fptr, v_notify_fptr, e_notify_fptr);
}

int jgrapht_import_string_gexf(void *g, char* input, void *import_vertex_id_fptr, int validate_schema, void *vertex_attribute_fptr, void *edge_attribute_fptr, void *v_notify_fptr, void *e_notify_fptr) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_import_string_gexf(thread, g, input, import_vertex_id_fptr, validate_schema, vertex_attribute_fptr, edge_attribute_fptr, v_notify_fptr, e_notify_fptr);
}

int jgrapht_import_file_graphml_simple(void *g, char* filename, void *import_vertex_id_fptr, int validate_schema, void *vertex_attribute_fptr, void *edge_attribute_fptr, void *v_notify_fptr, void *e_notify_fptr) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_import_file_graphml_simple(thread, g, filename, import_vertex_id_fptr, validate_schema, vertex_attribute_fptr, edge_attribute_fptr, v_notify_fptr, e_notify_fptr);
}

int jgrapht_import_string_graphml_simple(void *g, char* input, void *import_vertex_id_fptr, int validate_schema, void *vertex_attribute_fptr, void *edge_attribute_fptr, void *v_notify_fptr, void *e_notify_fptr) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_import_string_graphml_simple(thread, g, input, import_vertex_id_fptr, validate_schema, vertex_attribute_fptr, edge_attribute_fptr, v_notify_fptr, e_notify_fptr);
}    

int jgrapht_import_file_graphml(void *g, char* filename, void *import_vertex_id_fptr, int validate_schema, void *vertex_attribute_fptr, void *edge_attribute_fptr, void *v_notify_fptr, void *e_notify_fptr) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_import_file_graphml(thread, g, filename, import_vertex_id_fptr, validate_schema, vertex_attribute_fptr, edge_attribute_fptr, v_notify_fptr, e_notify_fptr);
}

int jgrapht_import_string_graphml(void *g, char* input, void *import_vertex_id_fptr, int validate_schema, void *vertex_attribute_fptr, void *edge_attribute_fptr, void *v_notify_fptr, void *e_notify_fptr) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_import_string_graphml(thread, g, input, import_vertex_id_fptr, validate_schema, vertex_attribute_fptr, edge_attribute_fptr, v_notify_fptr, e_notify_fptr);
}

int jgrapht_import_file_dot(void *g, char* filename, void *import_vertex_id_fptr, void *vertex_attribute_fptr, void *edge_attribute_fptr, void *v_notify_fptr, void *e_notify_fptr) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_import_file_dot(thread, g, filename, import_vertex_id_fptr, vertex_attribute_fptr, edge_attribute_fptr, v_notify_fptr, e_notify_fptr);
}

int jgrapht_import_string_dot(void *g, char* input, void *import_vertex_id_fptr, void *vertex_attribute_fptr, void *edge_attribute_fptr, void *v_notify_fptr, void *e_notify_fptr) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_import_string_dot(thread, g, input, import_vertex_id_fptr, vertex_attribute_fptr, edge_attribute_fptr, v_notify_fptr, e_notify_fptr);
}

int jgrapht_import_file_graph6sparse6(void *g, char* filename, void *import_vertex_id_fptr, void *vertex_attribute_fptr, void *edge_attribute_fptr, void *v_notify_fptr, void *e_notify_fptr) {
    LAZY_THREAD_ATTACH
    return jgrapht_capi_import_file_graph6sparse6(thread, g, filename, import_vertex_id_fptr, vertex_attribute_fptr, edge_attribute_fptr, v_notify_fptr, e_notify_fptr);
}

int jgrapht_import_string_graph6sparse6(void *g, char* input, void *import_vertex_id_fptr, void *vertex_attribute_fptr, void *edge_attribute_fptr, void *v_notify_fptr, void *e_notify_fptr) {
    LAZY_THREAD_ATTACH
    return jgrapht_capi_import_string_graph6sparse6(thread, g, input, import_vertex_id_fptr, vertex_attribute_fptr, edge_attribute_fptr, v_notify_fptr, e_notify_fptr);
}

// edgelist

int jgrapht_import_edgelist_noattrs_file_dimacs(char* filename, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_import_edgelist_noattrs_file_dimacs(thread, filename, res);
}

int jgrapht_import_edgelist_noattrs_string_dimacs(char* input, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_import_edgelist_noattrs_string_dimacs(thread, input, res);
}

int jgrapht_import_edgelist_attrs_file_dimacs(char* filename, void *vertex_attribute_fptr, void *edge_attribute_fptr, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_import_edgelist_attrs_file_dimacs(thread, filename, vertex_attribute_fptr, edge_attribute_fptr, res);    
}

int jgrapht_import_edgelist_attrs_string_dimacs(char* input, void *vertex_attribute_fptr, void *edge_attribute_fptr, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_import_edgelist_attrs_string_dimacs(thread, input, vertex_attribute_fptr, edge_attribute_fptr, res);        
}

int jgrapht_import_edgelist_noattrs_file_gml(char* filename, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_import_edgelist_noattrs_file_gml(thread, filename, res);
}

int jgrapht_import_edgelist_noattrs_string_gml(char* input, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_import_edgelist_noattrs_string_gml(thread, input, res);
}

int jgrapht_import_edgelist_attrs_file_gml(char* filename, void *vertex_attribute_fptr, void *edge_attribute_fptr, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_import_edgelist_attrs_file_gml(thread, filename, vertex_attribute_fptr, edge_attribute_fptr, res);    
}

int jgrapht_import_edgelist_attrs_string_gml(char* input, void *vertex_attribute_fptr, void *edge_attribute_fptr, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_import_edgelist_attrs_string_gml(thread, input, vertex_attribute_fptr, edge_attribute_fptr, res);        
}

int jgrapht_import_edgelist_noattrs_file_json(char* filename, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_import_edgelist_noattrs_file_json(thread, filename, res);
}

int jgrapht_import_edgelist_noattrs_string_json(char* input, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_import_edgelist_noattrs_string_json(thread, input, res);
}

int jgrapht_import_edgelist_attrs_file_json(char* filename, void *vertex_attribute_fptr, void *edge_attribute_fptr, void** res) {
    LAZY_THREAD_ATTACH
    return jgrapht_capi_import_edgelist_attrs_file_json(thread, filename, vertex_attribute_fptr, edge_attribute_fptr, res);
}

int jgrapht_import_edgelist_attrs_string_json(char* input, void *vertex_attribute_fptr, void *edge_attribute_fptr, void** res) {
    LAZY_THREAD_ATTACH
    return jgrapht_capi_import_edgelist_attrs_string_json(thread, input, vertex_attribute_fptr, edge_attribute_fptr, res);
}

int jgrapht_import_edgelist_noattrs_file_csv(char* filename, csv_format_t format, int export_edge_weights, int matrix_format_nodeid, int matrix_format_zero_when_no_edge, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_import_edgelist_noattrs_file_csv(thread, filename, format, export_edge_weights, matrix_format_nodeid, matrix_format_zero_when_no_edge, res);
}

int jgrapht_import_edgelist_noattrs_string_csv(char* input, csv_format_t format, int export_edge_weights, int matrix_format_nodeid, int matrix_format_zero_when_no_edge, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_import_edgelist_noattrs_string_csv(thread, input, format, export_edge_weights, matrix_format_nodeid, matrix_format_zero_when_no_edge, res);    
}

int jgrapht_import_edgelist_attrs_file_csv(char* filename, void *vertex_attribute_fptr, void *edge_attribute_fptr, csv_format_t format, int export_edge_weights, int matrix_format_nodeid, int matrix_format_zero_when_no_edge, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_import_edgelist_attrs_file_csv(thread, filename, vertex_attribute_fptr, edge_attribute_fptr, format, export_edge_weights, matrix_format_nodeid, matrix_format_zero_when_no_edge, res);    
}

int jgrapht_import_edgelist_attrs_string_csv(char* input, void *vertex_attribute_fptr, void *edge_attribute_fptr, csv_format_t format, int export_edge_weights, int matrix_format_nodeid, int matrix_format_zero_when_no_edge, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_import_edgelist_attrs_string_csv(thread, input, vertex_attribute_fptr, edge_attribute_fptr, format, export_edge_weights, matrix_format_nodeid, matrix_format_zero_when_no_edge, res);    
}

int jgrapht_import_edgelist_noattrs_file_gexf(char* filename, int validate_schema, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_import_edgelist_noattrs_file_gexf(thread, filename, validate_schema, res);
}

int jgrapht_import_edgelist_noattrs_string_gexf(char* input, int validate_schema, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_import_edgelist_noattrs_string_gexf(thread, input, validate_schema, res);
}

int jgrapht_import_edgelist_attrs_file_gexf(char* filename, int validate_schema, void *vertex_attribute_fptr, void *edge_attribute_fptr, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_import_edgelist_attrs_file_gexf(thread, filename, validate_schema, vertex_attribute_fptr, edge_attribute_fptr, res);
}

int jgrapht_import_edgelist_attrs_string_gexf(char* input, int validate_schema, void *vertex_attribute_fptr, void *edge_attribute_fptr, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_import_edgelist_attrs_string_gexf(thread, input, validate_schema, vertex_attribute_fptr, edge_attribute_fptr, res);
}

int jgrapht_import_edgelist_noattrs_file_graphml_simple(char* filename, int validate_schema, void** res) {
    LAZY_THREAD_ATTACH
    return jgrapht_capi_import_edgelist_noattrs_file_graphml_simple(thread, filename, validate_schema, res);
}

int jgrapht_import_edgelist_noattrs_string_graphml_simple(char* input, int validate_schema, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_import_edgelist_noattrs_string_graphml_simple(thread, input, validate_schema, res);
}

int jgrapht_import_edgelist_attrs_file_graphml_simple(char* filename, int validate_schema, void *vertex_attribute_fptr, void *edge_attribute_fptr, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_import_edgelist_attrs_file_graphml_simple(thread, filename, validate_schema, vertex_attribute_fptr, edge_attribute_fptr, res);
}

int jgrapht_import_edgelist_attrs_string_graphml_simple(char* input, int validate_schema, void *vertex_attribute_fptr, void *edge_attribute_fptr, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_import_edgelist_attrs_string_graphml_simple(thread, input, validate_schema, vertex_attribute_fptr, edge_attribute_fptr, res);
}

int jgrapht_import_edgelist_noattrs_file_graphml(char* filename, int validate_schema, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_import_edgelist_noattrs_file_graphml(thread, filename, validate_schema, res);
}

int jgrapht_import_edgelist_noattrs_string_graphml(char* input, int validate_schema, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_import_edgelist_noattrs_string_graphml(thread, input, validate_schema, res);
}

int jgrapht_import_edgelist_attrs_file_graphml(char* filename, int validate_schema, void *vertex_attribute_fptr, void *edge_attribute_fptr, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_import_edgelist_attrs_file_graphml(thread, filename, validate_schema, vertex_attribute_fptr, edge_attribute_fptr, res);
}

int jgrapht_import_edgelist_attrs_string_graphml(char* input, int validate_schema, void *vertex_attribute_fptr, void *edge_attribute_fptr, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_import_edgelist_attrs_string_graphml(thread, input, validate_schema, vertex_attribute_fptr, edge_attribute_fptr, res);
}

int jgrapht_import_edgelist_noattrs_file_dot(char* filename, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_import_edgelist_noattrs_file_dot(thread, filename, res);
}

int jgrapht_import_edgelist_noattrs_string_dot(char* input, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_import_edgelist_noattrs_string_dot(thread, input, res);
}

int jgrapht_import_edgelist_attrs_file_dot(char* filename, void *vertex_attribute_fptr, void *edge_attribute_fptr, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_import_edgelist_attrs_file_dot(thread, filename, vertex_attribute_fptr, edge_attribute_fptr, res);
}

int jgrapht_import_edgelist_attrs_string_dot(char* input, void *vertex_attribute_fptr, void *edge_attribute_fptr, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_import_edgelist_attrs_string_dot(thread, input, vertex_attribute_fptr, edge_attribute_fptr, res);
}

int jgrapht_import_edgelist_noattrs_file_graph6sparse6(char* filename, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_import_edgelist_noattrs_file_graph6sparse6(thread, filename, res);
}

int jgrapht_import_edgelist_noattrs_string_graph6sparse6(char* input, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_import_edgelist_noattrs_string_graph6sparse6(thread, input, res);
}

int jgrapht_import_edgelist_attrs_file_graph6sparse6(char* filename, void *vertex_attribute_fptr, void *edge_attribute_fptr, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_import_edgelist_attrs_file_graph6sparse6(thread, filename, vertex_attribute_fptr, edge_attribute_fptr, res);
}

int jgrapht_import_edgelist_attrs_string_graph6sparse6(char* input, void *vertex_attribute_fptr, void *edge_attribute_fptr, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_import_edgelist_attrs_string_graph6sparse6(thread, input, vertex_attribute_fptr, edge_attribute_fptr, res);
}

// independent set

int jgrapht_independent_set_exec_chordal_max_independent_set(void *g, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_independent_set_exec_chordal_max_independent_set(thread, g, res);
}

// isomorphism

int jgrapht_isomorphism_exec_vf2(void *g1, void *g2, int* exist_iso_res, void** graph_mapping_it_res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_isomorphism_exec_vf2(thread, g1, g2, exist_iso_res, graph_mapping_it_res);
}

int jgrapht_isomorphism_exec_vf2_subgraph(void *g1, void *g2, int* exist_iso_res, void** graph_mapping_it_res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_isomorphism_exec_vf2_subgraph(thread, g1, g2, exist_iso_res, graph_mapping_it_res);
}

int jgrapht_isomorphism_graph_mapping_edge_correspondence(void *graph_mapping, int edge, int forward, int* exists_edge_res, int* edge_res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_isomorphism_graph_mapping_edge_correspondence(thread, graph_mapping, edge, forward, exists_edge_res, edge_res);
}

int jgrapht_isomorphism_graph_mapping_vertex_correspondence(void *graph_mapping, int vertex, int forward, int* exist_vertex_res, int* vertex_res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_isomorphism_graph_mapping_vertex_correspondence(thread, graph_mapping, vertex, forward, exist_vertex_res, vertex_res);
}

// iterators

int jgrapht_it_next_int(void *it, int* res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_it_next_int(thread, it, res);
}

int jgrapht_it_next_double(void *it, double* res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_it_next_double(thread, it, res);
}

int jgrapht_it_next_edge_triple(void *it, int *source, int *target, double* weight) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_it_next_edge_triple(thread, it, source, target, weight);
}

int jgrapht_it_next_str_edge_triple(void *it, char **source, char **target, double* weight) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_it_next_str_edge_triple(thread, it, source, target, weight);
}

int jgrapht_it_next_object(void *it, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_it_next_object(thread, it, res);
}

int jgrapht_it_hasnext(void *it, int* res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_it_hasnext(thread, it, res);
}

// list

int jgrapht_list_create(void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_list_create(thread, res);
}

int jgrapht_list_it_create(void *list, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_list_it_create(thread, list, res);
}

int jgrapht_list_size(void *list, int* res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_list_size(thread, list, res);
}

int jgrapht_list_int_add(void *list, int e, int* res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_list_int_add(thread, list, e, res);
}

int jgrapht_list_double_add(void *list, double e, int* res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_list_double_add(thread, list, e, res);
}

int jgrapht_list_edge_pair_add(void *list, int source, int target, int* res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_list_edge_pair_add(thread, list, source, target, res);
}

int jgrapht_list_edge_triple_add(void *list, int source, int target, double weight, int* res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_list_edge_triple_add(thread, list, source, target, weight, res);
}

int jgrapht_list_int_remove(void *list, int e) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_list_int_remove(thread, list, e);
}

int jgrapht_list_double_remove(void *list, double e) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_list_double_remove(thread, list, e);
}

int jgrapht_list_int_contains(void *list, int e, int* res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_list_int_contains(thread, list, e, res);
}

int jgrapht_list_double_contains(void *list , double e, int* res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_list_double_contains(thread, list, e, res);
}

int jgrapht_list_clear(void *list) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_list_clear(thread, list);
}

// listenable

int jgrapht_listenable_as_listenable(void *g, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_listenable_as_listenable(thread, g, res);
}

int jgrapht_listenable_create_graph_listener(void *event_fptr, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_listenable_create_graph_listener(thread, event_fptr, res);
}

int jgrapht_listenable_add_graph_listener(void *g, void *listener) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_listenable_add_graph_listener(thread, g, listener);
}

int jgrapht_listenable_remove_graph_listener(void *g, void *listener) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_listenable_remove_graph_listener(thread, g, listener);
}

// map

int jgrapht_map_create(void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_map_create(thread, res);
}

int jgrapht_map_linked_create(void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_map_linked_create(thread, res);
}

int jgrapht_map_keys_it_create(void *map, void** res) {
    LAZY_THREAD_ATTACH 
    return jgrapht_capi_map_keys_it_create(thread, map, res);
}

int jgrapht_map_size(void *map, int* res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_map_size(thread, map, res);
}

int jgrapht_map_values_it_create(void *map, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_map_values_it_create(thread, map, res);
}

int jgrapht_map_int_double_put(void *map, int key, double value) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_map_int_double_put(thread, map, key, value);
}

int jgrapht_map_int_int_put(void *map, int key, int value) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_map_int_int_put(thread, map, key, value);
}

int jgrapht_map_int_string_put(void *map, int key, char* value) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_map_int_string_put(thread, map, key, value);
}

int jgrapht_map_int_double_get(void *map, int key, double* res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_map_int_double_get(thread, map, key, res);
}

int jgrapht_map_int_int_get(void *map, int key, int* res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_map_int_int_get(thread, map, key, res);
}

int jgrapht_map_int_string_get(void *map, int key, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_map_int_string_get(thread, map, key, res);
}

int jgrapht_map_int_contains_key(void *map, int key, int* res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_map_int_contains_key(thread, map, key, res);
}

int jgrapht_map_int_double_remove(void *map, int key, double* res) {
    LAZY_THREAD_ATTACH
    return jgrapht_capi_map_int_double_remove(thread, map, key, res);
}

int jgrapht_map_int_int_remove(void *map, int key, int* res) {
    LAZY_THREAD_ATTACH
    return jgrapht_capi_map_int_int_remove(thread, map, key, res);
}

int jgrapht_map_int_string_remove(void *map, int key, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_map_int_string_remove(thread, map, key, res);
}

int jgrapht_map_clear(void *map) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_map_clear(thread, map);
}

// matching

int jgrapht_matching_exec_greedy_general_max_card(void *g, double* weight_res, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_matching_exec_greedy_general_max_card(thread, g, weight_res, res);
}

int jgrapht_matching_exec_custom_greedy_general_max_card(void *g, int sort, double* weight_res, void** res) {
    LAZY_THREAD_ATTACH
    return jgrapht_capi_matching_exec_custom_greedy_general_max_card(thread, g, sort, weight_res, res);
}

int jgrapht_matching_exec_edmonds_general_max_card_dense(void *g, double* weight_res, void** res) {
    LAZY_THREAD_ATTACH
    return jgrapht_capi_matching_exec_edmonds_general_max_card_dense(thread, g, weight_res, res);
}

int jgrapht_matching_exec_edmonds_general_max_card_sparse(void *g, double* weight_res, void** res) {
    LAZY_THREAD_ATTACH
    return jgrapht_capi_matching_exec_edmonds_general_max_card_sparse(thread, g, weight_res, res);
}

int jgrapht_matching_exec_greedy_general_max_weight(void *g, double* weight_res, void** res) {
    LAZY_THREAD_ATTACH
    return jgrapht_capi_matching_exec_greedy_general_max_weight(thread, g, weight_res, res);
}

int jgrapht_matching_exec_custom_greedy_general_max_weight(void *g, int normalize_edge_costs, double epsilon, double* weight_res, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_matching_exec_custom_greedy_general_max_weight(thread, g, normalize_edge_costs, epsilon, weight_res, res);
}

int jgrapht_matching_exec_pathgrowing_max_weight(void *g, double* weight_res, void** res) {
    LAZY_THREAD_ATTACH
    return jgrapht_capi_matching_exec_pathgrowing_max_weight(thread, g, weight_res, res);
}

int jgrapht_matching_exec_blossom5_general_max_weight(void *g, double* weight_res, void** res) {
    LAZY_THREAD_ATTACH
    return jgrapht_capi_matching_exec_blossom5_general_max_weight(thread, g, weight_res, res);
}

int jgrapht_matching_exec_blossom5_general_min_weight(void *g, double* weight_res, void** res) {
    LAZY_THREAD_ATTACH
    return jgrapht_capi_matching_exec_blossom5_general_min_weight(thread, g, weight_res, res);
}

int jgrapht_matching_exec_blossom5_general_perfect_max_weight(void *g, double* weight_res, void** res) {
    LAZY_THREAD_ATTACH
    return jgrapht_capi_matching_exec_blossom5_general_perfect_max_weight(thread, g, weight_res, res);
}

int jgrapht_matching_exec_blossom5_general_perfect_min_weight(void *g, double* weight_res, void** res) {
    LAZY_THREAD_ATTACH
    return jgrapht_capi_matching_exec_blossom5_general_perfect_min_weight(thread, g, weight_res, res);
}

int jgrapht_matching_exec_bipartite_max_card(void *g, double* weight_res, void** res) {
    LAZY_THREAD_ATTACH
    return jgrapht_capi_matching_exec_bipartite_max_card(thread, g, weight_res, res);
}

int jgrapht_matching_exec_bipartite_perfect_min_weight(void *g, void *vertex_set1, void *vertex_set2, double* weight_res, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_matching_exec_bipartite_perfect_min_weight(thread, g, vertex_set1, vertex_set2, weight_res, res);
}

int jgrapht_matching_exec_bipartite_max_weight(void *g, double* weight_res, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_matching_exec_bipartite_max_weight(thread, g, weight_res, res);
}

// mst

int jgrapht_mst_exec_kruskal(void *g, double* weight_res, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_mst_exec_kruskal(thread, g, weight_res, res);
}

int jgrapht_mst_exec_prim(void *g, double* weight_res, void** res) {
    LAZY_THREAD_ATTACH
    return jgrapht_capi_mst_exec_prim(thread, g, weight_res, res);
}

int jgrapht_mst_exec_boruvka(void *g, double* weight_res, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_mst_exec_boruvka(thread, g, weight_res, res);
}

// partition

int jgrapht_partition_exec_bipartite(void *g, int* res, void** vertex_partition1, void** vertex_partition2) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_partition_exec_bipartite(thread, g, res, vertex_partition1, vertex_partition2);
}

// planarity

int jgrapht_planarity_exec_boyer_myrvold(void *g, int* is_planar_res, void** embedding_res, void** kuratowski_subdivision_res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_planarity_exec_boyer_myrvold(thread, g, is_planar_res, embedding_res, kuratowski_subdivision_res);
}

int jgrapht_planarity_embedding_edges_around_vertex(void *embedding, int vertex, void** it_res) {
    LAZY_THREAD_ATTACH
    return jgrapht_capi_planarity_embedding_edges_around_vertex(thread, embedding, vertex, it_res);
}

// scoring

int jgrapht_scoring_exec_alpha_centrality(void *g, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_scoring_exec_alpha_centrality(thread, g, res);
}

int jgrapht_scoring_exec_custom_alpha_centrality(void *g, double damping_factor, double exogenous_factor, int max_iterations, double tolerance, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_scoring_exec_custom_alpha_centrality(thread, g, damping_factor, exogenous_factor, max_iterations, tolerance, res);
}

int jgrapht_scoring_exec_betweenness_centrality(void *g, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_scoring_exec_betweenness_centrality(thread, g, res);
}

int jgrapht_scoring_exec_custom_betweenness_centrality(void *g, int normalize, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_scoring_exec_custom_betweenness_centrality(thread, g, normalize, res);
}

int jgrapht_scoring_exec_closeness_centrality(void *g, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_scoring_exec_closeness_centrality(thread, g, res);
}

int jgrapht_scoring_exec_custom_closeness_centrality(void *g, int incoming, int normalize, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_scoring_exec_custom_closeness_centrality(thread, g, incoming, normalize, res);
}

int jgrapht_scoring_exec_harmonic_centrality(void *g, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_scoring_exec_harmonic_centrality(thread, g, res);
}

int jgrapht_scoring_exec_custom_harmonic_centrality(void *g, int incoming, int normalize, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_scoring_exec_custom_harmonic_centrality(thread, g, incoming, normalize, res);
}

int jgrapht_scoring_exec_pagerank(void *g, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_scoring_exec_pagerank(thread, g, res);
}

int jgrapht_scoring_exec_custom_pagerank(void *g, double damping_factor, int iterations, double tolerance, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_scoring_exec_custom_pagerank(thread, g, damping_factor, iterations, tolerance, res);
}

int jgrapht_scoring_exec_coreness(void *g, int* degeneracy_res, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_scoring_exec_coreness(thread, g, degeneracy_res, res);
}

int jgrapht_scoring_exec_clustering_coefficient(void *g, double* global_res, double* avg_res, void** local_res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_scoring_exec_clustering_coefficient(thread, g, global_res, avg_res, local_res);
}

// set

int jgrapht_set_create(void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_set_create(thread, res);
}

int jgrapht_set_linked_create(void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_set_linked_create(thread, res);
}

int jgrapht_set_it_create(void *set, void**res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_set_it_create(thread, set, res);
}

int jgrapht_set_size(void *set, int* res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_set_size(thread, set, res);
}

int jgrapht_set_int_add(void *set , int elem, int* res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_set_int_add(thread, set, elem, res);
}

int jgrapht_set_double_add(void *set, double elem, int* res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_set_double_add(thread, set, elem, res);
}

int jgrapht_set_int_remove(void *set, int elem) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_set_int_remove(thread, set, elem);
}

int jgrapht_set_double_remove(void *set, double elem) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_set_double_remove(thread, set, elem);
}

int jgrapht_set_int_contains(void *set, int elem, int* res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_set_int_contains(thread, set, elem, res);
}

int jgrapht_set_double_contains(void *set, double elem, int* res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_set_double_contains(thread, set, elem, res);
}

int jgrapht_set_clear(void *set) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_set_clear(thread, set);
}

// shortest paths 

int jgrapht_sp_exec_dijkstra_get_path_between_vertices(void *g, int source, int target, void** res) {
    LAZY_THREAD_ATTACH
    return jgrapht_capi_sp_exec_dijkstra_get_path_between_vertices(thread, g, source, target, res);
}

int jgrapht_sp_exec_bidirectional_dijkstra_get_path_between_vertices(void *g, int source, int target, void** res) {
    LAZY_THREAD_ATTACH
    return jgrapht_capi_sp_exec_bidirectional_dijkstra_get_path_between_vertices(thread, g, source, target, res);
}

int jgrapht_sp_exec_dijkstra_get_singlesource_from_vertex(void *g, int source, void** res) {
    LAZY_THREAD_ATTACH
    return jgrapht_capi_sp_exec_dijkstra_get_singlesource_from_vertex(thread, g, source, res);
}

int jgrapht_sp_exec_bellmanford_get_singlesource_from_vertex(void *g, int source, void** res) {
    LAZY_THREAD_ATTACH
    return jgrapht_capi_sp_exec_bellmanford_get_singlesource_from_vertex(thread, g, source, res);
}

int jgrapht_sp_exec_bfs_get_singlesource_from_vertex(void *g, int source, void** res) {
    LAZY_THREAD_ATTACH
    return jgrapht_capi_sp_exec_bfs_get_singlesource_from_vertex(thread, g, source, res);
}

int jgrapht_sp_exec_johnson_get_allpairs(void *g, void** res) {
    LAZY_THREAD_ATTACH
    return jgrapht_capi_sp_exec_johnson_get_allpairs(thread, g, res);
}

int jgrapht_sp_exec_floydwarshall_get_allpairs(void *g, void** res) {
    LAZY_THREAD_ATTACH
    return jgrapht_capi_sp_exec_floydwarshall_get_allpairs(thread, g, res);
}

int jgrapht_sp_singlesource_get_path_to_vertex(void *singlesource, int target, void** res) {
    LAZY_THREAD_ATTACH
    return jgrapht_capi_sp_singlesource_get_path_to_vertex(thread, singlesource, target, res);
}

int jgrapht_sp_allpairs_get_path_between_vertices(void *allpairs, int source, int target, void** res) {
    LAZY_THREAD_ATTACH
    return jgrapht_capi_sp_allpairs_get_path_between_vertices(thread, allpairs, source, target, res);
}

int jgrapht_sp_allpairs_get_singlesource_from_vertex(void *allpairs, int source, void** res) {
    LAZY_THREAD_ATTACH
    return jgrapht_capi_sp_allpairs_get_singlesource_from_vertex(thread, allpairs, source, res);
}

int jgrapht_sp_exec_astar_get_path_between_vertices(void *g, int source, int target, void *heuristic, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_sp_exec_astar_get_path_between_vertices(thread, g, source, target, heuristic, res);
}

int jgrapht_sp_exec_bidirectional_astar_get_path_between_vertices(void *g, int source, int target, void *heuristic, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_sp_exec_bidirectional_astar_get_path_between_vertices(thread, g, source, target, heuristic, res);
}

int jgrapht_sp_exec_astar_alt_heuristic_get_path_between_vertices(void *g, int source, int target, void *landmarks_set, void** res) {
    LAZY_THREAD_ATTACH
    return jgrapht_capi_sp_exec_astar_alt_heuristic_get_path_between_vertices(thread, g, source, target, landmarks_set, res);
}

int jgrapht_sp_exec_bidirectional_astar_alt_heuristic_get_path_between_vertices(void *g, int source, int target, void *landmarks_set, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_sp_exec_bidirectional_astar_alt_heuristic_get_path_between_vertices(thread, g, source, target, landmarks_set, res);
}

int jgrapht_sp_exec_yen_get_k_loopless_paths_between_vertices(void *g, int source, int target, int k, void**res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_sp_exec_yen_get_k_loopless_paths_between_vertices(thread, g, source, target, k, res);
}

int jgrapht_sp_exec_eppstein_get_k_paths_between_vertices(void *g, int source, int target, int k, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_sp_exec_eppstein_get_k_paths_between_vertices(thread, g, source, target, k, res);
}

int jgrapht_sp_exec_delta_stepping_get_path_between_vertices(void *g, int source, int target, double delta, int parallelism, void**res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_sp_exec_delta_stepping_get_path_between_vertices(thread, g, source, target, delta, parallelism, res);
}

int jgrapht_sp_exec_delta_stepping_get_singlesource_from_vertex(void *g, int source, double delta, int parallelism, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_sp_exec_delta_stepping_get_singlesource_from_vertex(thread, g, source, delta, parallelism, res);
}

// multi objective shortest paths

int jgrapht_multisp_exec_martin_get_multiobjectivesinglesource_from_vertex(void *g, int source, void *cost_function, int dimensions, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_multisp_exec_martin_get_multiobjectivesinglesource_from_vertex(thread, g, source, cost_function, dimensions, res);
}

int jgrapht_multisp_exec_martin_get_paths_between_vertices(void *g, int source, int target, void *cost_function, int dimensions, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_multisp_exec_martin_get_paths_between_vertices(thread, g, source, target, cost_function, dimensions, res);    
}

int jgrapht_multisp_multiobjectivesinglesource_get_paths_to_vertex(void *multiobjectivesinglesource, int target, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_multisp_multiobjectivesinglesource_get_paths_to_vertex(thread, multiobjectivesinglesource, target, res);
}

// spanner

int jgrapht_spanner_exec_greedy_multiplicative(void *g, int k, double* weight, void** res) {
    LAZY_THREAD_ATTACH
    return jgrapht_capi_spanner_exec_greedy_multiplicative(thread, g, k, weight, res);
}

// tour 

int jgrapht_tour_tsp_random(void *g, long long int seed, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_tour_tsp_random(thread, g, seed, res);
}

int jgrapht_tour_tsp_greedy_heuristic(void * g, void** res) {
    LAZY_THREAD_ATTACH
    return jgrapht_capi_tour_tsp_greedy_heuristic(thread, g, res);
}

int jgrapht_tour_tsp_nearest_insertion_heuristic(void * g, void** res) {
    LAZY_THREAD_ATTACH
    return jgrapht_capi_tour_tsp_nearest_insertion_heuristic(thread, g, res);
}

int jgrapht_tour_tsp_nearest_neighbor_heuristic(void *g, long long int seed, void** res) {
    LAZY_THREAD_ATTACH
    return jgrapht_capi_tour_tsp_nearest_neighbor_heuristic(thread, g, seed, res);
}

int jgrapht_tour_metric_tsp_christofides(void *g, void** res) {
    LAZY_THREAD_ATTACH
    return jgrapht_capi_tour_metric_tsp_christofides(thread, g, res);
}

int jgrapht_tour_metric_tsp_two_approx(void *g, void** res) {
    LAZY_THREAD_ATTACH
    return jgrapht_capi_tour_metric_tsp_two_approx(thread, g, res);
}

int jgrapht_tour_tsp_held_karp(void *g, void** res) {
    LAZY_THREAD_ATTACH
    return jgrapht_capi_tour_tsp_held_karp(thread, g, res);
}

int jgrapht_tour_hamiltonian_palmer(void *g, void** res) {
    LAZY_THREAD_ATTACH
    return jgrapht_capi_tour_hamiltonian_palmer(thread, g, res);
}

int jgrapht_tour_tsp_two_opt_heuristic(void *g, int k, double min_cost_improvement, long long int seed, void** res) {
    LAZY_THREAD_ATTACH
    return jgrapht_capi_tour_tsp_two_opt_heuristic(thread, g, k, min_cost_improvement, seed, res);
}

int jgrapht_tour_tsp_two_opt_heuristic_improve(void *graph_path, double min_cost_improvement, long long int seed, void** res) {
    LAZY_THREAD_ATTACH
    return jgrapht_capi_tour_tsp_two_opt_heuristic_improve(thread, graph_path, min_cost_improvement, seed, res);
}

// traverse

int jgrapht_traverse_create_bfs_from_all_vertices_vit(void *g, void** res) {
    LAZY_THREAD_ATTACH
    return jgrapht_capi_traverse_create_bfs_from_all_vertices_vit(thread, g, res);
}

int jgrapht_traverse_create_bfs_from_vertex_vit(void *g, int v, void** res) {
    LAZY_THREAD_ATTACH
    return jgrapht_capi_traverse_create_bfs_from_vertex_vit(thread, g, v, res);
}

int jgrapht_traverse_create_lex_bfs_vit(void *g, void** res) {
    LAZY_THREAD_ATTACH
    return jgrapht_capi_traverse_create_lex_bfs_vit(thread, g, res);
}

int jgrapht_traverse_create_dfs_from_all_vertices_vit(void *g, void** res) {
    LAZY_THREAD_ATTACH
    return jgrapht_capi_traverse_create_dfs_from_all_vertices_vit(thread, g, res);
}

int jgrapht_traverse_create_dfs_from_vertex_vit(void *g, int v, void** res) {
    LAZY_THREAD_ATTACH
    return jgrapht_capi_traverse_create_dfs_from_vertex_vit(thread, g, v, res);
}

int jgrapht_traverse_create_topological_order_vit(void *g, void** res) {
    LAZY_THREAD_ATTACH
    return jgrapht_capi_traverse_create_topological_order_vit(thread, g, res);
}

int jgrapht_traverse_create_random_walk_from_vertex_vit(void *g, int v, void** res) {
    LAZY_THREAD_ATTACH
    return jgrapht_capi_traverse_create_random_walk_from_vertex_vit(thread, g, v, res);
}

int jgrapht_traverse_create_custom_random_walk_from_vertex_vit(void *g, int v, int weighted, long long int max_steps, long long int seed, void** res) {
    LAZY_THREAD_ATTACH
    return jgrapht_capi_traverse_create_custom_random_walk_from_vertex_vit(thread, g, v, weighted, max_steps, seed, res);
}

int jgrapht_traverse_create_max_cardinality_vit(void *g, void** res) {
    LAZY_THREAD_ATTACH
    return jgrapht_capi_traverse_create_max_cardinality_vit(thread, g, res);
}

int jgrapht_traverse_create_degeneracy_ordering_vit(void *g, void** res) {
    LAZY_THREAD_ATTACH
    return jgrapht_capi_traverse_create_degeneracy_ordering_vit(thread, g, res);
}

int jgrapht_traverse_create_closest_first_from_vertex_vit(void *g, int v, void** res) {
    LAZY_THREAD_ATTACH
    return jgrapht_capi_traverse_create_closest_first_from_vertex_vit(thread, g, v, res);
}

int jgrapht_traverse_create_custom_closest_first_from_vertex_vit(void *g, int v, double radius, void** res) {
    LAZY_THREAD_ATTACH
    return jgrapht_capi_traverse_create_custom_closest_first_from_vertex_vit(thread, g, v, radius, res);
}

// vertex cover

int jgrapht_vertexcover_exec_greedy(void *g, double* weight_res, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_vertexcover_exec_greedy(thread, g, weight_res, res);
}

int jgrapht_vertexcover_exec_greedy_weighted(void *g, void *weight_vertex_map, double* weight_res, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_vertexcover_exec_greedy_weighted(thread, g, weight_vertex_map, weight_res, res);
}

int jgrapht_vertexcover_exec_clarkson(void *g, double* weight_res, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_vertexcover_exec_clarkson(thread, g, weight_res, res);
}

int jgrapht_vertexcover_exec_clarkson_weighted(void *g, void *weight_vertex_map, double* weight_res, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_vertexcover_exec_clarkson_weighted(thread, g, weight_vertex_map, weight_res, res);
}

int jgrapht_vertexcover_exec_edgebased(void *g, double* weight_res, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_vertexcover_exec_edgebased(thread, g, weight_res, res);    
}

int jgrapht_vertexcover_exec_baryehudaeven(void *g, double* weight_res, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_vertexcover_exec_baryehudaeven(thread, g, weight_res, res);    
}

int jgrapht_vertexcover_exec_baryehudaeven_weighted(void *g, void *weight_vertex_map, double* weight_res, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_vertexcover_exec_baryehudaeven_weighted(thread, g, weight_vertex_map, weight_res, res);    
}

int jgrapht_vertexcover_exec_exact(void *g, double* weight_res, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_vertexcover_exec_exact(thread, g, weight_res, res);    
}

int jgrapht_vertexcover_exec_exact_weighted(void *g, void *weight_vertex_map, double* weight_res, void** res) { 
    LAZY_THREAD_ATTACH
    return jgrapht_capi_vertexcover_exec_exact_weighted(thread, g, weight_vertex_map, weight_res, res);    
}


