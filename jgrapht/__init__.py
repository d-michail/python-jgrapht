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
# The int graph API.
#
# Integer graphs always use integer vertex and edges.
#
from ._internals._graphs import (
    create_graph as create_int_graph,
    create_dag as create_int_dag,
    create_sparse_graph as create_sparse_int_graph,
    as_sparse_graph as as_sparse_int_graph,
)

#
# The graph API.
#
# Graphs allow the use of any hashable for the vertices and edges.
#
from ._internals._attrsg import (
    create_attrs_graph as create_graph,
    create_attrs_dag as create_dag,
)

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
