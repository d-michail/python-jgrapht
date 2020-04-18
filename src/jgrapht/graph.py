from . import jgrapht
from . import status
from . import errors

class Graph:

    def __init__(self):
        self._g_handle = jgrapht.jgrapht_create_graph(1,1,1)
        errors.check_last_error()

    def addVertex(self):
        v = jgrapht.jgrapht_graph_add_vertex(self._g_handle)
        errors.check_last_error()
        return v

    def removeVertex(self, vertex):
        res = jgrapht.jgrapht_graph_remove_vertex(self._g_handle, vertex)
        errors.check_last_error()
        return res 

    def verticesCount(self):
        res = jgrapht.jgrapht_graph_vertices_count(self._g_handle)
        errors.check_last_error()        
        return res 


