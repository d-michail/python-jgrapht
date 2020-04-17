#ifndef __PJGRAPHT_H
#define __PJGRAPHT_H

#if defined(__cplusplus)
extern "C" {
#endif

void pjgrapht_thread_create();

void pjgrapht_thread_destroy();

int pjgrapht_get_errno();

void pjgrapht_clear_errno();

void pjgrapht_destroy(void *);

long long int pjgrapht_it_next(void *);

int pjgrapht_it_hasnext(void *);

void * pjgrapht_create_graph(int, int, int);

long long int pjgrapht_graph_vertices_count(void *);

long long int pjgrapht_graph_edges_count(void *);

long long int pjgrapht_graph_add_vertex(void *);

int pjgrapht_graph_remove_vertex(void *, long long int);

int pjgrapht_graph_contains_vertex(void *, long long int);

long long int pjgrapht_graph_add_edge(void *, long long int, long long int);

int pjgrapht_graph_remove_edge(void *, long long int);

int pjgrapht_graph_contains_edge(void *, long long int);

long long int pjgrapht_graph_degree_of(void *, long long int);

long long int pjgrapht_graph_indegree_of(void *, long long int);

long long int pjgrapht_graph_outdegree_of(void *, long long int);

long long int pjgrapht_graph_edge_source(void *, long long int);

long long int pjgrapht_graph_edge_target(void *, long long int);

int pjgrapht_graph_is_weighted(void *);

int pjgrapht_graph_is_directed(void *);

int pjgrapht_graph_is_undirected(void *);

int pjgrapht_graph_is_allowing_selfloops(void *);

int pjgrapht_graph_is_allowing_multipleedges(void *);

double pjgrapht_graph_get_edge_weight(void *, long long int);

void pjgrapht_graph_set_edge_weight(void *, long long int, double);

void * pjgrapht_graph_create_all_vit(void *);

void * pjgrapht_graph_create_all_eit(void *);

void * pjgrapht_graph_vertex_create_eit(void *, long long int);

void * pjgrapht_graph_vertex_create_out_eit(void *, long long int);

void * pjgrapht_graph_vertex_create_in_eit(void *, long long int);

void * pjgrapht_mst_exec_kruskal(void *);

void * pjgrapht_mst_exec_prim(void *);

double pjgrapht_mst_get_weight(void *);

void * pjgrapht_mst_create_eit(void *);

void pjgrapht_vmLocatorSymbol();

#if defined(__cplusplus)
}
#endif
#endif
