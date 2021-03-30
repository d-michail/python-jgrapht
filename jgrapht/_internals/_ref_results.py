from .. import backend
from ._wrappers import _JGraphTRefIterator, _JGraphTRefObjectIterator
from . import _refcount


def _jgrapht_ref_iterator_to_python_set(handle):
    """Return a Python set from a ref iterator in the JVM.
    Takes ownership.
    """
    it = _JGraphTRefIterator(handle_it)
    return set(it)


def _jgrapht_ref_iterator_to_python_list(handle):
    """Return a Python set from a ref iterator in the JVM.
    Takes ownership.
    """
    it = _JGraphTRefIterator(handle)
    return list(it)


def _jgrapht_ref_set_to_python_set(handle, owner=True):
    """Return a Python set from a set with references in the JVM."""
    result = set()
    it_handle = backend.jgrapht_set_it_create(handle)
    has_next = backend.jgrapht_it_hasnext(it_handle)
    while has_next:
        value = backend.jgrapht_it_next_ref(it_handle, False)
        result.add(_refcount._swig_ptr_to_obj(value))
        has_next = backend.jgrapht_it_hasnext(it_handle)
    if owner:
        backend.jgrapht_handles_destroy(handle)
    return result
