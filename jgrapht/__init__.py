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
# The graph API.
#
# Graphs always use integer vertex and edges.
#
from ._internals._graphs import (
    create_graph,
    create_directed_graph,
    create_undirected_graph,
    create_dag,
    create_sparse_graph,
    as_sparse_graph,
)

#
# The property graph API.
#
# Property graphs allow the use of any hashable
# for the vertices and edges.
#
from ._internals._pg import (
    create_property_graph,
    create_directed_property_graph,
    create_undirected_property_graph,
    create_property_dag,
    is_property_graph,
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
