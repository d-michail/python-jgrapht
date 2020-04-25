
"""
Python JGraphT Library
~~~~~~~~~~~~~~~~~~~~~~

"""

from .__version__ import __title__, __description__, __url__, __version__
from .__version__ import __author__, __author_email__, __license__
from .__version__ import __copyright__

from . import jgrapht as _backend

# Create main thread and setup cleanup
import atexit
_backend.jgrapht_thread_create()

def _module_cleanup_function():
    if _backend.jgrapht_is_thread_attached():
        _backend.jgrapht_thread_destroy()

atexit.register(_module_cleanup_function)
del atexit


# Set default logging handler to avoid "No handler found" warnings.
import logging
from logging import NullHandler
logging.getLogger(__name__).addHandler(NullHandler())