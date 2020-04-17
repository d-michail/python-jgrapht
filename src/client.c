#include <stdio.h>
#include <stdlib.h>

#include <pjgrapht.h>

int main(int argc, char **argv) { 

	pjgrapht_thread_create();
	
	printf("Current errno=%d\n", pjgrapht_get_errno());

	void* g = pjgrapht_create_graph(1, 1, 1);
	printf("Current errno=%d\n", pjgrapht_get_errno());

	
	long v0 = pjgrapht_graph_add_vertex(g);
	long v1 = pjgrapht_graph_add_vertex(g);
	long v2 = pjgrapht_graph_add_vertex(g);

	printf("Graph has %lld vertices\n", pjgrapht_graph_vertices_count(g));

	void *vit = pjgrapht_graph_create_all_vit(g);
	while(pjgrapht_it_hasnext(vit)) { 
		printf("Vertex %lld\n", pjgrapht_it_next(vit));
	}
	pjgrapht_destroy(vit);

	pjgrapht_graph_add_edge(g, v0, v1);
	pjgrapht_graph_add_edge(g, v1, v2);
	pjgrapht_graph_add_edge(g, v2, v0);

	printf("Graph has %lld edges\n", pjgrapht_graph_edges_count(g));

	void *mst = pjgrapht_mst_exec_kruskal(g);
	printf("MST weight: %lf\n", pjgrapht_mst_get_weight(mst));
	void *mst_eit = pjgrapht_mst_create_eit(mst);
	while(pjgrapht_it_hasnext(mst_eit)) { 
		printf("edge %lld\n", pjgrapht_it_next(mst_eit));
	}
	pjgrapht_destroy(mst_eit);
	pjgrapht_destroy(mst);

	pjgrapht_destroy(g);
	
	pjgrapht_thread_destroy();

  	return EXIT_SUCCESS;

}
