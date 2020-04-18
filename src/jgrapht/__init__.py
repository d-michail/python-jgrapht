
import atexit
from . import jgrapht

# Create thread
print('Creating thread')
jgrapht.jgrapht_thread_create()


def module_cleanup_function():
    print('Destroying thread')
    jgrapht.jgrapht_thread_destroy()

# Register cleanup
atexit.register(module_cleanup_function)
