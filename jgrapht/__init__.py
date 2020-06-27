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

# Create main thread and setup cleanup
from . import backend
import atexit

backend.jgrapht_isolate_create()
del backend


def _module_cleanup_function():
    from . import backend

    if backend.jgrapht_isolate_is_attached():
        backend.jgrapht_isolate_destroy()


atexit.register(_module_cleanup_function)
del atexit

# Set default logging handler to avoid "No handler found" warnings.
import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())

#
# The graph API
#
from ._internals._graphs import (
    create_int_graph as _create_int_graph,
    create_int_dag as _create_int_dag,
    create_sparse_int_graph as create_sparse_graph,
    as_sparse_int_graph as as_sparse_graph,
)
from ._internals._anyhashableg import (
    create_anyhashable_graph as _create_anyhashable_graph,
    create_anyhashable_dag as _create_anyhashable_dag,
)


def create_graph(directed=True,
                 allowing_self_loops=False,
                 allowing_multiple_edges=False,
                 weighted=True,
                 dag=False,
                 any_hashable_for_graph_elements=False,
                 vertex_supplier=None,
                 edge_supplier=None,
                 ):
    """Create a graph.

    By default this function creates graphs with integer vertices. When parameter
    `any_hashable_for_graph_elements` is true, the returned graph will be able to (a) have any
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
    :param any_hashable_for_graph_elements: if True then the graph will allow the use of any
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
    if any_hashable_for_graph_elements:
        if dag:
            if not directed:
                raise ValueError("A dag is always directed")
            if allowing_self_loops:
                raise ValueError("A dag cannot allow self-loops")
            return _create_anyhashable_dag(allowing_multiple_edges=allowing_multiple_edges, weighted=weighted,
                                           vertex_supplier=vertex_supplier, edge_supplier=edge_supplier)
        else:
            return _create_anyhashable_graph(directed=directed, allowing_self_loops=allowing_self_loops,
                                             allowing_multiple_edges=allowing_multiple_edges, weighted=weighted,
                                             vertex_supplier=vertex_supplier, edge_supplier=edge_supplier)
    else:
        if dag:
            if not directed:
                raise ValueError("A dag is always directed")
            if allowing_self_loops:
                raise ValueError("A dag cannot allow self-loops")
            return _create_int_dag(allowing_multiple_edges=allowing_multiple_edges, weighted=weighted)
        else:
            return _create_int_graph(directed=directed, allowing_self_loops=allowing_self_loops,
                                     allowing_multiple_edges=allowing_multiple_edges, weighted=weighted)


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
