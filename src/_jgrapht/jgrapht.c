#include <stdlib.h>
#include <stdio.h>
#include <jgrapht_capi.h>

static graal_isolate_t *isolate = NULL;
static graal_isolatethread_t *thread = NULL;

void jgrapht_thread_create() {
    if (thread == NULL) { 
        if (graal_create_isolate(NULL, &isolate, &thread) != 0) {
            fprintf(stderr, "graal_create_isolate error\n");
            exit(EXIT_FAILURE);
        }
    } 
}

void jgrapht_thread_destroy() { 
    if (thread != NULL) { 
        if (graal_detach_thread(thread) != 0) {
                fprintf(stderr, "graal_detach_thread error\n");
                exit(EXIT_FAILURE);
        }
        thread  = NULL;
        isolate = NULL;
    }
}

int jgrapht_is_thread_attached() {
    return thread != NULL; 
}

int jgrapht_get_errno() { 
    return jgrapht_capi_get_errno(thread);
}

char * jgrapht_get_errno_msg() { 
    return jgrapht_capi_get_errno_msg(thread);
}

void jgrapht_clear_errno() { 
    jgrapht_capi_clear_errno(thread);
}

void jgrapht_destroy(void *handle) { 
    jgrapht_capi_destroy(thread, handle);
}

long long int jgrapht_it_next(void *itHandle) { 
    return jgrapht_capi_it_next(thread, itHandle);
}

int jgrapht_it_hasnext(void *itHandle) { 
    return jgrapht_capi_it_hasnext(thread, itHandle);
}

void * jgrapht_graph_create(int directed, int allowingSelfLoops, int allowingMultipleEdges, int weighted) { 
    return jgrapht_capi_graph_create(thread, directed, allowingSelfLoops, allowingMultipleEdges, weighted);
}

long long int jgrapht_graph_vertices_count(void *gHandle) { 
    return jgrapht_capi_graph_vertices_count(thread, gHandle);
}

long long int jgrapht_graph_edges_count(void *gHandle) { 
    return jgrapht_capi_graph_edges_count(thread, gHandle);
}

long long int jgrapht_graph_add_vertex(void *gHandle) { 
    return jgrapht_capi_graph_add_vertex(thread, gHandle);
}

int jgrapht_graph_remove_vertex(void *gHandle, long long int vertex) { 
    return jgrapht_capi_graph_remove_vertex(thread, gHandle, vertex);
}

int jgrapht_graph_contains_vertex(void *gHandle, long long int vertex) { 
    return jgrapht_capi_graph_contains_vertex(thread, gHandle, vertex);
}

long long int jgrapht_graph_add_edge(void *gHandle, long long int source, long long int target) { 
    return jgrapht_capi_graph_add_edge(thread, gHandle, source, target);
}

int jgrapht_graph_remove_edge(void *gHandle, long long int edge) { 
    return jgrapht_capi_graph_remove_edge(thread, gHandle, edge);
}

int jgrapht_graph_contains_edge(void *gHandle, long long int edge) { 
    return jgrapht_capi_graph_contains_edge(thread, gHandle, edge);
}

int jgrapht_graph_contains_edge_between(void *gHandle, long long int source, long long int target) { 
    return jgrapht_capi_graph_contains_edge_between(thread, gHandle, source, target);
}

long long int jgrapht_graph_degree_of(void *gHandle, long long int vertex) { 
    return jgrapht_capi_graph_degree_of(thread, gHandle, vertex); 
}

long long int jgrapht_graph_indegree_of(void *gHandle, long long int vertex) { 
    return jgrapht_capi_graph_indegree_of(thread, gHandle, vertex);
}

long long int jgrapht_graph_outdegree_of(void *gHandle, long long int vertex) { 
    return jgrapht_capi_graph_outdegree_of(thread, gHandle, vertex);
}

long long int jgrapht_graph_edge_source(void *gHandle, long long int edge) { 
    return jgrapht_capi_graph_edge_source(thread, gHandle, edge);
}

long long int jgrapht_graph_edge_target(void *gHandle, long long int edge) { 
    return jgrapht_capi_graph_edge_target(thread, gHandle, edge);
}

int jgrapht_graph_is_weighted(void *gHandle) { 
    return jgrapht_capi_graph_is_weighted(thread, gHandle);
}

int jgrapht_graph_is_directed(void *gHandle) { 
    return jgrapht_capi_graph_is_directed(thread, gHandle);
}

int jgrapht_graph_is_undirected(void *gHandle) { 
    return jgrapht_capi_graph_is_undirected(thread, gHandle);
}

int jgrapht_graph_is_allowing_selfloops(void *gHandle) { 
    return jgrapht_capi_graph_is_allowing_selfloops(thread, gHandle);
}

int jgrapht_graph_is_allowing_multipleedges(void *gHandle) { 
    return jgrapht_capi_graph_is_allowing_multipleedges(thread, gHandle);
}

double jgrapht_graph_get_edge_weight(void *gHandle, long long int edge) { 
    return jgrapht_capi_graph_get_edge_weight(thread, gHandle, edge);
}

void jgrapht_graph_set_edge_weight(void *gHandle, long long int edge, double weight) { 
    return jgrapht_capi_graph_set_edge_weight(thread, gHandle, edge, weight);
}

void * jgrapht_graph_create_all_vit(void *gHandle) { 
    return jgrapht_capi_graph_create_all_vit(thread, gHandle);
}

void * jgrapht_graph_create_all_eit(void *gHandle) { 
    return jgrapht_capi_graph_create_all_eit(thread, gHandle);
}

void * jgrapht_graph_create_between_eit(void *gHandle, long long int source, long long target) { 
    return jgrapht_capi_graph_create_between_eit(thread, gHandle, source, target);
}

void * jgrapht_graph_vertex_create_eit(void *gHandle, long long int vertex) { 
    return jgrapht_capi_graph_vertex_create_eit(thread, gHandle, vertex);
}

void * jgrapht_graph_vertex_create_out_eit(void *gHandle, long long int vertex) {
    return jgrapht_capi_graph_vertex_create_out_eit(thread, gHandle, vertex);
}

void * jgrapht_graph_vertex_create_in_eit(void *gHandle, long long int vertex) {
    return jgrapht_capi_graph_vertex_create_in_eit(thread, gHandle, vertex);
}

// map

void * jgrapht_map_create() { 
    return jgrapht_capi_map_create(thread);
}

void * jgrapht_map_keys_it_create(void *mapHandle) { 
    return jgrapht_capi_map_keys_it_create(thread, mapHandle);
}

void * jgrapht_map_values_it_create(void *mapHandle) { 
    return jgrapht_capi_map_values_it_create(thread, mapHandle);
}

void jgrapht_map_long_double_put(void *mapHandle, long long int key, double value) { 
    return jgrapht_capi_map_long_double_put(thread, mapHandle, key, value);
}

double jgrapht_map_long_double_get(void *mapHandle, long long int key) { 
    return jgrapht_capi_map_long_double_get(thread, mapHandle, key);
}

int jgrapht_map_long_contains_key(void *mapHandle, long long int key) { 
    return jgrapht_capi_map_long_contains_key(thread, mapHandle, key);
}

// mst

void * jgrapht_mst_exec_kruskal(void *gHandle) { 
    return jgrapht_capi_mst_exec_kruskal(thread, gHandle);
}

void * jgrapht_mst_exec_prim(void *gHandle) {
    return jgrapht_capi_mst_exec_prim(thread, gHandle);
}

double jgrapht_mst_get_weight(void *mstHandle) {
    return jgrapht_capi_mst_get_weight(thread, mstHandle);
}

void * jgrapht_mst_create_eit(void *mstHandle) {
    return jgrapht_capi_mst_create_eit(thread, mstHandle);
}

// vertex cover

void * jgrapht_vertexcover_exec_greedy_uniform(void *gHandle) { 
    return jgrapht_capi_vertexcover_exec_greedy_uniform(thread, gHandle);
}

void * jgrapht_vertexcover_exec_greedy_weighted(void *gHandle, void *weightMapHandle) { 
    return jgrapht_capi_vertexcover_exec_greedy_weighted(thread, gHandle, weightMapHandle);
}

double jgrapht_vertexcover_get_weight(void *vcHandle) { 
    return jgrapht_capi_vertexcover_get_weight(thread, vcHandle);
}

void * jgrapht_vertexcover_create_vit(void *vcHandle) { 
    return jgrapht_capi_vertexcover_create_vit(thread, vcHandle);
}

// vm

void jgrapht_vmLocatorSymbol() {
    vmLocatorSymbol(thread);
}






