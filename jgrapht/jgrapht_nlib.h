#ifndef __JGRAPHT_NLIB_H
#define __JGRAPHT_NLIB_H

#include <graal_isolate.h>


#if defined(__cplusplus)
extern "C" {
#endif

void jgrapht_nlib_clear_errno(graal_isolatethread_t*);

int jgrapht_nlib_get_errno(graal_isolatethread_t*);

void jgrapht_nlib_destroy(graal_isolatethread_t*, void *);

long long int jgrapht_nlib_it_next(graal_isolatethread_t*, void *);

int jgrapht_nlib_it_hasnext(graal_isolatethread_t*, void *);

void * jgrapht_nlib_graph_create(graal_isolatethread_t*, int, int, int, int);

long long int jgrapht_nlib_graph_vertices_count(graal_isolatethread_t*, void *);

long long int jgrapht_nlib_graph_edges_count(graal_isolatethread_t*, void *);

long long int jgrapht_nlib_graph_add_vertex(graal_isolatethread_t*, void *);

int jgrapht_nlib_graph_remove_vertex(graal_isolatethread_t*, void *, long long int);

int jgrapht_nlib_graph_contains_vertex(graal_isolatethread_t*, void *, long long int);

long long int jgrapht_nlib_graph_add_edge(graal_isolatethread_t*, void *, long long int, long long int);

int jgrapht_nlib_graph_remove_edge(graal_isolatethread_t*, void *, long long int);

int jgrapht_nlib_graph_contains_edge(graal_isolatethread_t*, void *, long long int);

int jgrapht_nlib_graph_contains_edge_between(graal_isolatethread_t*, void *, long long int, long long int);

long long int jgrapht_nlib_graph_degree_of(graal_isolatethread_t*, void *, long long int);

long long int jgrapht_nlib_graph_indegree_of(graal_isolatethread_t*, void *, long long int);

long long int jgrapht_nlib_graph_outdegree_of(graal_isolatethread_t*, void *, long long int);

long long int jgrapht_nlib_graph_edge_source(graal_isolatethread_t*, void *, long long int);

long long int jgrapht_nlib_graph_edge_target(graal_isolatethread_t*, void *, long long int);

int jgrapht_nlib_graph_is_weighted(graal_isolatethread_t*, void *);

int jgrapht_nlib_graph_is_directed(graal_isolatethread_t*, void *);

int jgrapht_nlib_graph_is_undirected(graal_isolatethread_t*, void *);

int jgrapht_nlib_graph_is_allowing_selfloops(graal_isolatethread_t*, void *);

int jgrapht_nlib_graph_is_allowing_multipleedges(graal_isolatethread_t*, void *);

double jgrapht_nlib_graph_get_edge_weight(graal_isolatethread_t*, void *, long long int);

void jgrapht_nlib_graph_set_edge_weight(graal_isolatethread_t*, void *, long long int, double);

void * jgrapht_nlib_graph_create_all_vit(graal_isolatethread_t*, void *);

void * jgrapht_nlib_graph_create_all_eit(graal_isolatethread_t*, void *);

void * jgrapht_nlib_graph_create_between_eit(graal_isolatethread_t*, void *, long long int, long long int);

void * jgrapht_nlib_graph_vertex_create_eit(graal_isolatethread_t*, void *, long long int);

void * jgrapht_nlib_graph_vertex_create_out_eit(graal_isolatethread_t*, void *, long long int);

void * jgrapht_nlib_graph_vertex_create_in_eit(graal_isolatethread_t*, void *, long long int);

void * jgrapht_nlib_map_create(graal_isolatethread_t*);

void jgrapht_nlib_map_long_double_put(graal_isolatethread_t*, void *, long long int, double);

double jgrapht_nlib_map_long_double_get(graal_isolatethread_t*, void *, long long int);

int jgrapht_nlib_map_long_double_contains_key(graal_isolatethread_t*, void *, long long int);

void * jgrapht_nlib_mst_exec_kruskal(graal_isolatethread_t*, void *);

void * jgrapht_nlib_mst_exec_prim(graal_isolatethread_t*, void *);

double jgrapht_nlib_mst_get_weight(graal_isolatethread_t*, void *);

void * jgrapht_nlib_mst_create_eit(graal_isolatethread_t*, void *);

void * jgrapht_nlib_vertexcover_exec_greedy_uniform(graal_isolatethread_t*, void *);

void * jgrapht_nlib_vertexcover_exec_greedy_weighted(graal_isolatethread_t*, void *, void *);

double jgrapht_nlib_vertexcover_get_weight(graal_isolatethread_t*, void *);

void * jgrapht_nlib_vertexcover_create_vit(graal_isolatethread_t*, void *);

void vmLocatorSymbol(graal_isolatethread_t* thread);

#if defined(__cplusplus)
}
#endif
#endif
