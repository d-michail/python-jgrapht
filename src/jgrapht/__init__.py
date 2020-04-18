
import atexit
from . import jgrapht

# Create thread
jgrapht.jgrapht_thread_create()

# Register cleanup
atexit.register(jgrapht.jgrapht_thread_destroy)
