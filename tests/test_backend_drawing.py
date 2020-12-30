import pytest

import jgrapht._backend as _backend

from jgrapht._internals._drawing import (
    _JGraphTIntegerLayoutModel2D
)


def test_layout_model_2d():
    handle = _backend.jgrapht_xx_drawing_layout_model_2d_create(1.0, 1.0, 9.0, 9.0)
    model = _JGraphTIntegerLayoutModel2D(handle)


    model.set_vertex_location(0, (5.0, 7.5))
    assert model.get_vertex_location(0) == (5.0, 7.5)
    assert not model.is_fixed(0)
    model.set_fixed(0, True)
    assert model.is_fixed(0)
    model.set_vertex_location(0, (7.0, 8.0))
    assert model.get_vertex_location(0) == (5.0, 7.5)
    model.set_fixed(0, False)
    assert not model.is_fixed(0)
    model.set_vertex_location(0, (7.0, 8.0))
    assert model.get_vertex_location(0) == (7.0, 8.0)

    repr(model)
