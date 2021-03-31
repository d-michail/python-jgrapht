from .. import backend
from ._wrappers import _JGraphTRefIterator, _JGraphTRefDirectIterator
from . import _ref_utils


def _jgrapht_ref_iterator_to_python_set(handle, refs_owner=False):
    """Return a Python set from a ref iterator in the JVM.
    Takes ownership.
    """
    if refs_owner: 
        it = _JGraphTRefIterator(handle)
    else:
        it = _JGraphTRefDirectIterator(handle)
    return set(it)


def _jgrapht_ref_iterator_to_python_list(handle, refs_owner=False):
    """Return a Python set from a ref iterator in the JVM.
    Takes ownership.
    """
    if refs_owner: 
        it = _JGraphTRefIterator(handle)
    else:
        it = _JGraphTRefDirectIterator(handle)    
    return list(it)


def _jgrapht_ref_set_to_python_set(handle, owner=True):
    """Return a Python set from a set with references in the JVM."""
    result = set()
    it_handle = backend.jgrapht_set_it_create(handle)
    has_next = backend.jgrapht_it_hasnext(it_handle)
    while has_next:
        value = backend.jgrapht_it_next_ref(it_handle, False)
        result.add(_ref_utils._swig_ptr_to_obj(value))
        has_next = backend.jgrapht_it_hasnext(it_handle)
    if owner:
        backend.jgrapht_handles_destroy(handle)
    return result
