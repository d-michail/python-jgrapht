from .. import backend
from .._internals._collections import (
    _JGraphTIntegerSet,
)

def chordal_max_independent_set(graph):
    r"""Find a maximum independent set in a chordal graph.

    The algorithms first computes a perfect elimination ordering and then a
    maximum independent set. Running time :math:`\mathcal{O}(n+m)`. 

    :param graph: the chordal graph. If the graph is not chordal an error is raised
    :returns: an independent set as a vertex set
    """
    res = backend.jgrapht_independent_set_exec_chordal_max_independent_set(graph.handle)
    return _JGraphTIntegerSet(handle=res)
