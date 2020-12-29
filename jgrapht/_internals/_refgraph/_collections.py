from .._wrappers import (
    _HandleWrapper,
    _JGraphTObjectIterator,
)
from .._collections import (
    _JGraphTLongList,
)
from ._graphs import _map_ids_to_objs


class _RefCountLongListIterator(_JGraphTObjectIterator):
    """An iterator which returns lists with longs."""

    def __init__(self, handle, **kwargs):
        super().__init__(handle=handle, **kwargs)

    def __next__(self):
        return list(_map_ids_to_objs(_JGraphTLongList(super().__next__())))

    def __repr__(self):
        return "_RefCountLongListIterator(%r)" % self._handle
