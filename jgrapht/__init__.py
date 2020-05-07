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

from . import backend
from ._wrappers import create_graph

# Create main thread and setup cleanup
import atexit

backend.jgrapht_isolate_create()


def _module_cleanup_function():
    if backend.jgrapht_isolate_is_attached():
        backend.jgrapht_isolate_destroy()


atexit.register(_module_cleanup_function)
del atexit


# Set default logging handler to avoid "No handler found" warnings.
import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())
