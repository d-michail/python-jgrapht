
import atexit
from . import jgrapht

# Create thread
print('Creating thread')
jgrapht.jgrapht_thread_create()


def module_cleanup_function():
    print('Destroying thread')
    if jgrapht.jgrapht_is_thread_attached():
        jgrapht.jgrapht_thread_destroy()

# Register cleanup
atexit.register(module_cleanup_function)
