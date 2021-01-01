from .. import backend as _backend

from .._internals._results import (
    _wrap_vertex_set,
)


def chordal_max_independent_set(graph):
    r"""Find a maximum independent set in a chordal graph.

    The algorithms first computes a perfect elimination ordering and then a
    maximum independent set. Running time :math:`\mathcal{O}(n+m)`. 

    :param graph: the chordal graph. If the graph is not chordal an error is raised
    :returns: an independent set as a vertex set
    """
    res = _backend.jgrapht_xx_independent_set_exec_chordal_max_independent_set(
        graph.handle
    )
    return _wrap_vertex_set(graph, res)
