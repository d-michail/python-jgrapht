from time import time
from .. import backend as _backend
from .._internals._drawing import _create_layout_model_2d
from .._internals._callbacks import _create_wrapped_vertex_comparator_callback


def _drawing_alg(name, graph, model, *args):

    alg_method_name = "jgrapht_drawing_exec_" + name

    try:
        alg_method = getattr(_backend, alg_method_name)
    except AttributeError:
        raise NotImplementedError("Algorithm not supported.")

    alg_method(graph.handle, model.handle, *args)


from .._internals._drawing import _create_layout_model_2d as create_layout_model_2d


def random_layout_2d(graph, area, seed=None):
    r"""Random 2d layout. 

    The algorithm assigns vertex coordinates uniformly at random.

    :param graph: the graph to draw
    :param area: the two dimensional area as a tuple (minx, miny, width, height)
    :param seed: seed of the random number generator. If None the system time is used
    :returns: a 2d layout model as an instance of :py:class:`jgrapht.types.LayoutModel2D`.
    """
    if seed is None:
        seed = time.time()
    model = create_layout_model_2d(*area)
    custom = [seed]
    _drawing_alg("random_layout_2d", graph, model, *custom)
    return model


def circular_layout_2d(graph, area, radius, vertex_comparator_cb=None):
    """Circular 2d layout.

    The algorithm places the graph vertices on a circle evenly spaced. The vertices are
    iterated based on the iteration order of the vertex set of the graph. The order can
    be adjusted by providing an external comparator.

    :param graph: the graph to draw
    :param area: the two dimensional area as a tuple (minx, miny, width, height)
    :param radius: radius of the circle
    :param vertex_comparator_cb: a vertex comparator. Should be a function which accepts
      two vertices v1, v2 and return -1, 0, 1 depending of whether v1 < v2, v1 == v2, or 
      v1 > v2 in the ordering
    :returns: a 2d layout model as an instance of :py:class:`jgrapht.types.LayoutModel2D`.
    """
    model = create_layout_model_2d(*area)

    (
        vertex_comparator_f_ptr,
        vertex_comparator_f,
    ) = _create_wrapped_vertex_comparator_callback(vertex_comparator_cb)

    custom = [radius, vertex_comparator_f_ptr]

    _drawing_alg("circular_layout_2d", graph, model, *custom)
    
    return model
