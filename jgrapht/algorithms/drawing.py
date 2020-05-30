from time import time
from .. import backend as _backend
from .._internals._drawing import _create_layout_model_2d


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
