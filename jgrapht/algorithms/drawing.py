import time

from .. import backend as _backend

from .._internals._callbacks import _create_wrapped_vertex_comparator_callback

from .._internals._anyhashableg import (
    _is_anyhashable_graph,
    _vertex_g_to_anyhashableg as _vertex_g_to_attrsg,
)
from .._internals._drawing import _create_layout_model_2d as create_layout_model_2d
from .._internals._anyhashableg_drawing import (
    _create_anyhashable_graph_layout_model_2d as create_attrs_graph_layout_model_2d,
)


def _drawing_alg(name, graph, model, *args):
    alg_method = getattr(_backend, "jgrapht_drawing_exec_" + name)
    alg_method(graph.handle, model.handle, *args)


def random_layout_2d(graph, area, seed=None):
    r"""Random 2d layout. 

    The algorithm assigns vertex coordinates uniformly at random.

    :param graph: the graph to draw
    :param area: the two dimensional area as a tuple (minx, miny, width, height)
    :param seed: seed for the random number generator. If None the system time is used
    :returns: a 2d layout model as an instance of :py:class:`jgrapht.types.LayoutModel2D`.
    """
    if seed is None:
        seed = int(time.time())

    if _is_anyhashable_graph(graph):
        model = create_attrs_graph_layout_model_2d(graph, *area)
    else:
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
    if _is_anyhashable_graph(graph):
        model = create_attrs_graph_layout_model_2d(graph, *area)

        def actual_vertex_comparator_cb(v1, v2):
            v1 = _vertex_g_to_attrsg(graph, v1)
            v2 = _vertex_g_to_attrsg(graph, v2)
            return vertex_comparator_cb(v1, v2)

    else:
        model = create_layout_model_2d(*area)
        actual_vertex_comparator_cb = vertex_comparator_cb

    (
        vertex_comparator_f_ptr,
        vertex_comparator_f,
    ) = _create_wrapped_vertex_comparator_callback(actual_vertex_comparator_cb)

    custom = [radius, vertex_comparator_f_ptr]
    _drawing_alg("circular_layout_2d", graph, model, *custom)
    return model


def fruchterman_reingold_layout_2d(
    graph, area, iterations=100, normalization_factor=0.5, seed=None
):
    """Fruchterman and Reingold Force-Directed Placement.

    The algorithm belongs in the broad category of
    `force directed graph drawing <https://en.wikipedia.org/wiki/Force-directed_graph_drawing>`_
    algorithms and is described in the paper:
 
      * Thomas M. J. Fruchterman and Edward M. Reingold. Graph drawing by force-directed placement.
        Software: Practice and experience, 21(11):1129--1164, 1991.

    An inverse linear temperature model is used for the annealing schedule.

    :param graph: the graph to draw
    :param area: the two dimensional area as a tuple (minx, miny, width, height)
    :param iterations: number of iterations
    :param normalization_factor: normalization factor when calculating optimal distance
    :param seed: seed for the random number generator. If None the system time is used    
    :returns: a 2d layout model as an instance of :py:class:`jgrapht.types.LayoutModel2D`.
    """
    if seed is None:
        seed = int(time.time())

    if _is_anyhashable_graph(graph):
        model = create_attrs_graph_layout_model_2d(graph, *area)
    else:
        model = create_layout_model_2d(*area)

    custom = [iterations, normalization_factor, seed]
    _drawing_alg("fr_layout_2d", graph, model, *custom)
    return model


def fruchterman_reingold_indexed_layout_2d(
    graph,
    area,
    iterations=100,
    normalization_factor=0.5,
    seed=None,
    theta=0.5,
    tolerance=None,
):
    """Fruchterman and Reingold Force-Directed Placement.

    The algorithm belongs in the broad category of
    `force directed graph drawing <https://en.wikipedia.org/wiki/Force-directed_graph_drawing>`_
    algorithms and is described in the paper:
 
      * Thomas M. J. Fruchterman and Edward M. Reingold. Graph drawing by force-directed placement.
        Software: Practice and experience, 21(11):1129--1164, 1991.

    This implementation uses the
    `Barnes-Hut <https://en.wikipedia.org/wiki/Barnes%E2%80%93Hut_simulation>`_
    indexing technique with a `QuadTree <https://en.wikipedia.org/wiki/Quadtree>`_.
    The Barnes-Hut indexing technique is described in the following paper:

       * J. Barnes and P. Hut. A hierarchical O(N log N) force-calculation algorithm. Nature.
         324(4):446--449, 1986.

    An inverse linear temperature model is used for the annealing schedule.

    :param graph: the graph to draw
    :param area: the two dimensional area as a tuple (minx, miny, width, height)
    :param iterations: number of iterations
    :param normalization_factor: normalization factor when calculating optimal distance
    :param seed: seed for the random number generator. If None the system time is used    
    :param theta: parameter for approximation using the Barnes-Hut technique
    :parram tolerance: tolerance used when comparing floating point values    
    :returns: a 2d layout model as an instance of :py:class:`jgrapht.types.LayoutModel2D`.
    """
    if seed is None:
        seed = int(time.time())
    if tolerance is None:
        tolerance = 1e-9

    if _is_anyhashable_graph(graph):
        model = create_attrs_graph_layout_model_2d(graph, *area)
    else:
        model = create_layout_model_2d(*area)

    custom = [iterations, normalization_factor, seed, theta, tolerance]
    _drawing_alg("indexed_fr_layout_2d", graph, model, *custom)
    return model
