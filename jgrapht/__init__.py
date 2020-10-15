"""
Python-JGraphT Library
~~~~~~~~~~~~~~~~~~~~~~

JGraphT is an library providing state-of-the-art graph data structures
and algorithms.

See https://github.com/d-michail/python-jgrapht for more details.
"""

from .__version__ import __title__, __description__, __url__
from .__version__ import __version__, __backend_version__
from .__version__ import __author__, __author_email__, __license__
from .__version__ import __copyright__
from .__version__ import __bibtex__

# Initialize with backend and setup module cleanup
from . import backend
import atexit

backend.jgrapht_init()
del backend


def _module_cleanup_function():
    from . import backend

    backend.jgrapht_cleanup()

atexit.register(_module_cleanup_function)
del atexit

# Set default logging handler to avoid "No handler found" warnings.
import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())

from ._internals._graphs import (
    _create_int_graph,
    _create_int_dag,
    _create_sparse_int_graph,
    _copy_to_sparse_int_graph,
)
from ._internals._anyhashableg import (
    _is_anyhashable_graph,
    _create_anyhashable_graph,
    _create_anyhashable_dag,
    _create_sparse_anyhashable_graph,
    _copy_to_sparse_anyhashable_graph,
)

#
# The graph creation API
#

def create_graph(
    directed=True,
    allowing_self_loops=False,
    allowing_multiple_edges=False,
    weighted=True,
    dag=False,
    any_hashable=False,
    vertex_supplier=None,
    edge_supplier=None,
):
    """Create a graph.

    By default this function creates graphs with integer vertices. When parameter
    `any_hashable` is true, the returned graph will be able to (a) have any
    hashable as vertices and edges, and (b) associate attributes/properties with the vertices
    and edges. Such a any-hashable graph needs to be able to create new objects for vertices
    and edges. This is accomplished by providing two functions called *vertex supplier* and
    *edge supplier*. If not provided by the user, the default implementation creates instances
    of :py:class:`object`.

    :param directed: if True the graph will be directed, otherwise undirected
    :param allowing_self_loops: if True the graph will allow the addition of self-loops
    :param allowing_multiple_edges: if True the graph will allow multiple-edges
    :param weighted: if True the graph will be weighted, otherwise unweighted
    :param dag: if True the graph will be a DAG (directed acyclic graph). An error will be
      raised if either directed is False or allowing_self_loops is True. The returned graph
      will be an instance of :class:`~jgrapht.types.DirectedAcyclicGraph`
    :param any_hashable: if True then the graph will allow the use of any
      hashable as vertices and edges instead of just integers. This also makes the graph
      an instance of :class:`~jgrapht.types.AttributesGraph`
    :param vertex_supplier: used only in the case that the graph allows any hashable as
      vertices/edges. Called everytime the graph needs to create a new vertex. If not given,
      then object instances are used.
    :param edge_supplier: used only in the case that the graph allows any hashable as
      vertices/edges. Called everytime the graph needs to create a new edge. If not given,
      then object instances are used.
    :returns: a graph
    :rtype: :class:`~jgrapht.types.Graph`
    """
    if any_hashable:
        if dag:
            if not directed:
                raise ValueError("A dag is always directed")
            if allowing_self_loops:
                raise ValueError("A dag cannot allow self-loops")
            return _create_anyhashable_dag(
                allowing_multiple_edges=allowing_multiple_edges,
                weighted=weighted,
                vertex_supplier=vertex_supplier,
                edge_supplier=edge_supplier,
            )
        else:
            return _create_anyhashable_graph(
                directed=directed,
                allowing_self_loops=allowing_self_loops,
                allowing_multiple_edges=allowing_multiple_edges,
                weighted=weighted,
                vertex_supplier=vertex_supplier,
                edge_supplier=edge_supplier,
            )
    else:
        if dag:
            if not directed:
                raise ValueError("A dag is always directed")
            if allowing_self_loops:
                raise ValueError("A dag cannot allow self-loops")
            return _create_int_dag(
                allowing_multiple_edges=allowing_multiple_edges, weighted=weighted
            )
        else:
            return _create_int_graph(
                directed=directed,
                allowing_self_loops=allowing_self_loops,
                allowing_multiple_edges=allowing_multiple_edges,
                weighted=weighted,
            )


def create_sparse_graph(
    edgelist,
    num_of_vertices=None,
    directed=True,
    weighted=True,
    any_hashable=False,
    vertex_supplier=None,
    edge_supplier=None,
):
    """Create a sparse graph.

    By default this function creates graphs with integer vertices. When parameter
    `any_hashable` is true, the returned graph will be able to (a) have any
    hashable as vertices and edges, and (b) associate attributes/properties with the vertices
    and edges. Such a any-hashable graph needs to be able to create new objects for vertices
    and edges. This is accomplished by providing two functions called *vertex supplier* and
    *edge supplier*. If not provided by the user, the default implementation creates instances
    of :py:class:`object`.

    The structure (topology) of a sparse graph is unmodifiable, but weights and properties can be
    modified.

    :param edgelist: list of tuple (u,v) or (u,v,weight) for weighted graphs. If `any_hashable` is 
      false, the vertices must be integers.
    :param num_of_vertices: number of vertices in the graph. Vertices always start from 0 
      and increase continuously. If not explicitly given and `any_hashable` is false, the edgelist
      will be traversed in order to find out the number of vertices
    :param directed: if True the graph will be directed, otherwise undirected
    :param weighted: if True the graph will be weighted, otherwise unweighted
    :param any_hashable: if True then the graph will allow the use of any
      hashable as vertices and edges instead of just integers. This also makes the graph
      an instance of :class:`~jgrapht.types.AttributesGraph`
    :param vertex_supplier: used only in the case that the graph allows any hashable as
      vertices/edges. Called everytime the graph needs to create a new vertex. If not given,
      then object instances are used.
    :param edge_supplier: used only in the case that the graph allows any hashable as
      vertices/edges. Called everytime the graph needs to create a new edge. If not given,
      then object instances are used.
    :returns: a graph
    :rtype: :class:`~jgrapht.types.Graph`
    """
    if any_hashable:
        return _create_sparse_anyhashable_graph(
            edgelist=edgelist,
            directed=directed,
            weighted=weighted,
            vertex_supplier=vertex_supplier,
            edge_supplier=edge_supplier,
        )
    else:
        return _create_sparse_int_graph(
            edgelist=edgelist,
            num_of_vertices=num_of_vertices,
            directed=directed,
            weighted=weighted,
        )


def copy_to_sparse_graph(graph):
    """Copy a graph to a sparse graph.

    .. note :: Sparse graphs are unmodifiable w.r.t their structure (topology).
       Attempting to alter one will result in an error being raised. Attributes
       and edge weights can be modified.

    :param graph: the input graph
    :returns: a sparse graph
    :rtype: :class:`jgrapht.types.Graph`
    """
    if _is_anyhashable_graph(graph):
        return _copy_to_sparse_anyhashable_graph(graph)
    else: 
        return _copy_to_sparse_int_graph(graph)


from . import (
    types,
    views,
    properties,
    metrics,
    traversal,
    generators,
    algorithms,
    io,
    utils,
)
