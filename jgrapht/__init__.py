"""
Python-JGraphT Library
~~~~~~~~~~~~~~~~~~~~~~

JGraphT is an library providing state-of-the-art graph data structures
and algorithms.

See https://github.com/d-michail/python-jgrapht for more details.
"""

from .__version__ import __title__, __description__, __url__, __version__
from .__version__ import __author__, __author_email__, __license__
from .__version__ import __copyright__

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


from ._internals._graphs import (
    create_graph,
    create_sparse_graph,
    as_sparse_graph,
) 
from . import types


# Set default logging handler to avoid "No handler found" warnings.
import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())
