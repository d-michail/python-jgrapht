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
    create_sparse_int_graph as create_sparse_int_graph,
    as_sparse_int_graph as as_sparse_int_graph,
)
from ._internals._attrsg import (
    create_attrs_graph as _create_attrs_graph,
    create_attrs_dag as _create_attrs_dag,
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
    """
    if any_hashable_for_graph_elements:
        if dag:
            if not directed:
                raise ValueError("A dag is always directed")
            if allowing_self_loops:
                raise ValueError("A dag cannot allow self-loops")
            return _create_attrs_dag(allowing_multiple_edges=allowing_multiple_edges, weighted=weighted,
                                     vertex_supplier=vertex_supplier, edge_supplier=edge_supplier)
        else:
            return _create_attrs_graph(directed=directed, allowing_self_loops=allowing_self_loops,
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
