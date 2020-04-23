
"""
Python JGraphT Library
~~~~~~~~~~~~~~~~~~~~~~

"""

import atexit
from . import jgrapht as backend

from .__version__ import __title__, __description__, __url__, __version__
from .__version__ import __author__, __author_email__, __license__
from .__version__ import __copyright__

# Create main thread and setup cleanup
backend.jgrapht_thread_create()

def module_cleanup_function():
    if backend.jgrapht_is_thread_attached():
        backend.jgrapht_thread_destroy()

atexit.register(module_cleanup_function)


# Set default logging handler to avoid "No handler found" warnings.
import logging
from logging import NullHandler
logging.getLogger(__name__).addHandler(NullHandler())