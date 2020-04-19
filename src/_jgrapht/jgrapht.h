#ifndef __JGRAPHT_H
#define __JGRAPHT_H

#if defined(__cplusplus)
extern "C" {
#endif

// library init

void jgrapht_thread_create();

void jgrapht_thread_destroy();

int jgrapht_is_thread_attached();

// errors

int jgrapht_get_errno();

void jgrapht_clear_errno();

char *jgrapht_get_errno_msg();

// cleanup

void jgrapht_destroy(void *);

// iterators

long long int jgrapht_it_next(void *);

int jgrapht_it_hasnext(void *);

// graph

void * jgrapht_graph_create(int, int, int, int);

long long int jgrapht_graph_vertices_count(void *);

long long int jgrapht_graph_edges_count(void *);

long long int jgrapht_graph_add_vertex(void *);

int jgrapht_graph_remove_vertex(void *, long long int);

int jgrapht_graph_contains_vertex(void *, long long int);

long long int jgrapht_graph_add_edge(void *, long long int, long long int);

int jgrapht_graph_remove_edge(void *, long long int);

int jgrapht_graph_contains_edge(void *, long long int);

int jgrapht_graph_contains_edge_between(void *, long long int, long long int);

long long int jgrapht_graph_degree_of(void *, long long int);

long long int jgrapht_graph_indegree_of(void *, long long int);

long long int jgrapht_graph_outdegree_of(void *, long long int);

long long int jgrapht_graph_edge_source(void *, long long int);

long long int jgrapht_graph_edge_target(void *, long long int);

int jgrapht_graph_is_weighted(void *);

int jgrapht_graph_is_directed(void *);

int jgrapht_graph_is_undirected(void *);

int jgrapht_graph_is_allowing_selfloops(void *);

int jgrapht_graph_is_allowing_multipleedges(void *);

double jgrapht_graph_get_edge_weight(void *, long long int);

void jgrapht_graph_set_edge_weight(void *, long long int, double);

void * jgrapht_graph_create_all_vit(void *);

void * jgrapht_graph_create_all_eit(void *);

void * jgrapht_graph_create_between_eit(void *, long long int, long long int);

void * jgrapht_graph_vertex_create_eit(void *, long long int);

void * jgrapht_graph_vertex_create_out_eit(void *, long long int);

void * jgrapht_graph_vertex_create_in_eit(void *, long long int);

// map

void * jgrapht_map_create();

void * jgrapht_map_keys_it_create(void *);

void * jgrapht_map_values_it_create(void *);

void jgrapht_map_long_double_put(void *, long long int, double);

double jgrapht_map_long_double_get(void *, long long int);

int jgrapht_map_long_contains_key(void *, long long int);

// mst

void * jgrapht_mst_exec_kruskal(void *);

void * jgrapht_mst_exec_prim(void *);

double jgrapht_mst_get_weight(void *);

void * jgrapht_mst_create_eit(void *);

// vertex cover

void * jgrapht_vertexcover_exec_greedy_uniform(void *);

void * jgrapht_vertexcover_exec_greedy_weighted(void *, void *);

double jgrapht_vertexcover_get_weight(void *);

void * jgrapht_vertexcover_create_vit(void *);

// vm

void jgrapht_vmLocatorSymbol();

#if defined(__cplusplus)
}
#endif
#endif
