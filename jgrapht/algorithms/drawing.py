import time

from .. import backend as _backend

from .._internals._results import _build_vertex_set
from .._internals._callbacks import _create_wrapped_int_vertex_comparator_callback

from .._internals._drawing import _create_int_layout_model_2d as create_layout_model_2d


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

    model = create_layout_model_2d(*area)

    custom = [seed]
    _backend.jgrapht_xx_drawing_exec_random_layout_2d(
        graph.handle, model.handle, *custom
    )
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
    actual_vertex_comparator_cb = vertex_comparator_cb

    (
        vertex_comparator_f_ptr,
        vertex_comparator_f,
    ) = _create_wrapped_int_vertex_comparator_callback(actual_vertex_comparator_cb)

    custom = [radius, vertex_comparator_f_ptr]
    _backend.jgrapht_ix_drawing_exec_circular_layout_2d(
        graph.handle, model.handle, *custom
    )
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
    model = create_layout_model_2d(*area)

    custom = [iterations, normalization_factor, seed]
    _backend.jgrapht_xx_drawing_exec_fr_layout_2d(graph.handle, model.handle, *custom)
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

    model = create_layout_model_2d(*area)

    custom = [iterations, normalization_factor, seed, theta, tolerance]
    _backend.jgrapht_xx_drawing_exec_indexed_fr_layout_2d(
        graph.handle, model.handle, *custom
    )
    return model


def two_layered_bipartite_layout_2d(
    graph,
    area,
    vertical=True,
    partition_a=None,
    vertex_comparator_cb=None,
):
    """A two layered bipartite graph layout.

    The algorithm draws a bipartite graph using straight edges. Vertices are arranged along two
    vertical or horizontal lines. No attempt is made to minimize edge crossings.

    The order of the vertices can be adjusted by providing a vertex comparator. Similarly the user
    can also determine the two partitions or can let the algorithm compute them.

    :param graph: the graph to draw
    :param area: the two dimensional area as a tuple (minx, miny, width, height)
    :param vertical: whether to draw a vertical layout or a horizontal
    :param partition_a: a vertex set for one of the two vertices partitions. If None the algorithm
           automatically computes one.
    :param vertex_comparator_cb: a vertex comparator which dictates the order of vertices on the partitions.
           Should be a function which accepts two vertices v1, v2 and return -1, 0, 1 depending of whether
           v1 < v2, v1 == v2, or v1 > v2 in the ordering
    :returns: a 2d layout model as an instance of :py:class:`jgrapht.types.LayoutModel2D`.
    """
    if partition_a is not None:
        partition_a = _build_vertex_set(graph, partition_a)
        partition_handle = partition_a.handle
    else:
        partition_handle = None

    model = create_layout_model_2d(*area)

    if vertex_comparator_cb is not None: 
        actual_vertex_comparator_cb = vertex_comparator_cb
        (
            vertex_comparator_f_ptr,
            vertex_comparator_f,
        ) = _create_wrapped_int_vertex_comparator_callback(actual_vertex_comparator_cb)
    else:
        vertex_comparator_f_ptr = 0

    custom = [partition_handle, vertex_comparator_f_ptr, vertical]
    _backend.jgrapht_ix_drawing_exec_two_layered_bipartite_layout_2d(
        graph.handle, model.handle, *custom
    )
    return model


def barycenter_greedy_two_layered_bipartite_layout_2d(
    graph,
    area,
    vertical=True,
    partition_a=None,
    vertex_comparator_cb=None,
):
    r"""The barycenter heuristic greedy algorithm for edge crossing minimization in two layered bipartite
    layouts.

    The algorithm draws a bipartite graph using straight edges. Vertices are arranged along two
    vertical or horizontal lines, trying to minimize crossings. This algorithm targets the one-sided
    problem where one of the two layers is considered fixed and the algorithm is allowed to adjust
    the positions of vertices in the other layer.

    The algorithm is described in the following paper: K. Sugiyama, S. Tagawa, and M. Toda. Methods
    for visual understanding of hierarchical system structures. IEEE Transaction on Systems, Man, and
    Cybernetics, 11(2):109–125, 1981.

    The problem of minimizing edge crossings when drawing bipartite graphs as two layered graphs is
    NP-complete. If the coordinates of the nodes in the fixed layer are allowed to vary wildly, then
    the barycenter heuristic can perform badly. If the coordinates of the nodes in the fixed layer
    are :math:`1, 2, 3, \ldots, ...` then it is an :math:`\mathcal{O}(\sqrt{n})`-approximation algorithm.

    :param graph: the graph to draw
    :param area: the two dimensional area as a tuple (minx, miny, width, height)
    :param vertical: whether to draw a vertical layout or a horizontal
    :param partition_a: a vertex set for one of the two vertices partitions. If None the algorithm
           automatically computes one.
    :param vertex_comparator_cb: a vertex comparator which dictates the order of vertices on the partitions.
           Should be a function which accepts two vertices v1, v2 and return -1, 0, 1 depending of whether
           v1 < v2, v1 == v2, or v1 > v2 in the ordering
    :returns: a 2d layout model as an instance of :py:class:`jgrapht.types.LayoutModel2D`.
    """
    if partition_a is not None:
        partition_a = _build_vertex_set(graph, partition_a)
        partition_handle = partition_a.handle
    else:
        partition_handle = None

    model = create_layout_model_2d(*area)

    if vertex_comparator_cb is not None: 
        actual_vertex_comparator_cb = vertex_comparator_cb
        (
            vertex_comparator_f_ptr,
            vertex_comparator_f,
        ) = _create_wrapped_int_vertex_comparator_callback(actual_vertex_comparator_cb)
    else:
        vertex_comparator_f_ptr = 0

    custom = [partition_handle, vertex_comparator_f_ptr, vertical]
    _backend.jgrapht_ix_drawing_exec_barycenter_greedy_two_layered_bipartite_layout_2d(
        graph.handle, model.handle, *custom
    )
    return model


def median_greedy_two_layered_bipartite_layout_2d(
    graph,
    area,
    vertical=True,
    partition_a=None,
    vertex_comparator_cb=None,
):
    """The median heuristic greedy algorithm for edge crossing minimization in two layered bipartite
       layouts.

    The algorithm draws a bipartite graph using straight edges. Vertices are arranged along two
    vertical or horizontal lines, trying to minimize crossings. This algorithm targets the one-sided
    problem where one of the two layers is considered fixed and the algorithm is allowed to adjust
    the positions of vertices in the other layer.

    The algorithm is described in the following paper: Eades, Peter, and Nicholas C. Wormald. "Edge
    crossings in drawings of bipartite graphs." Algorithmica 11.4 (1994): 379-403.

    The problem of minimizing edge crossings when drawing bipartite graphs as two layered graphs is
    NP-complete and the median heuristic is a 3-approximation algorithm.

    :param graph: the graph to draw
    :param area: the two dimensional area as a tuple (minx, miny, width, height)
    :param vertical: whether to draw a vertical layout or a horizontal
    :param partition_a: a vertex set for one of the two vertices partitions. If None the algorithm
           automatically computes one.
    :param vertex_comparator_cb: a vertex comparator which dictates the order of vertices on the partitions.
           Should be a function which accepts two vertices v1, v2 and return -1, 0, 1 depending of whether
           v1 < v2, v1 == v2, or v1 > v2 in the ordering
    :returns: a 2d layout model as an instance of :py:class:`jgrapht.types.LayoutModel2D`.
    """
    if partition_a is not None:
        partition_a = _build_vertex_set(graph, partition_a)
        partition_handle = partition_a.handle
    else:
        partition_handle = None

    model = create_layout_model_2d(*area)

    if vertex_comparator_cb is not None: 
        actual_vertex_comparator_cb = vertex_comparator_cb
        (
            vertex_comparator_f_ptr,
            vertex_comparator_f,
        ) = _create_wrapped_int_vertex_comparator_callback(actual_vertex_comparator_cb)
    else:
        vertex_comparator_f_ptr = 0

    custom = [partition_handle, vertex_comparator_f_ptr, vertical]
    _backend.jgrapht_ix_drawing_exec_median_greedy_two_layered_bipartite_layout_2d(
        graph.handle, model.handle, *custom
    )
    return model
