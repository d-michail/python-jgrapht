from collections import namedtuple
from ..types import LayoutModel2D
from .. import backend
from ._wrappers import _HandleWrapper

_box2d_class = namedtuple("Box2D", ["min_x", "min_y", "width", "height"])
_point2d_class = namedtuple("Point2D", ["x", "y"])


class _JGraphTLayoutModel2D(_HandleWrapper, LayoutModel2D):
    """A 2D layout model."""

    def __init__(self, handle, **kwargs):
        super().__init__(handle=handle, **kwargs)

    @property
    def area(self):
        res = backend.jgrapht_drawing_layout_model_2d_get_drawable_area(self.handle)
        return _box2d_class(*res)

    def get_vertex_location(self, vertex):
        res = backend.jgrapht_drawing_layout_model_2d_get_vertex(self.handle, vertex)
        return _point2d_class(*res)

    def set_vertex_location(self, vertex, point_2d):
        backend.jgrapht_drawing_layout_model_2d_put_vertex(
            self.handle, vertex, *point_2d
        )

    def is_fixed(self, vertex):
        return backend.jgrapht_drawing_layout_model_2d_get_fixed(self.handle, vertex)

    def set_fixed(self, vertex, fixed):
        backend.jgrapht_drawing_layout_model_2d_set_fixed(self.handle, vertex, fixed)

    def __repr__(self):
        return "_JGraphTLayoutModel2D(%r)" % self._handle


def _create_layout_model_2d(min_x, min_y, width, height):
    """Factory for a 2d layout model."""
    handle = backend.jgrapht_drawing_layout_model_2d_create(min_x, min_y, width, height)
    return _JGraphTLayoutModel2D(handle)
