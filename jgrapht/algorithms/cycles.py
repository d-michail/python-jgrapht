from .. import backend
from .._internals._wrappers import _JGraphTGraphPath



def eulerian_cycle(graph):
    """Run Hierholzer's algorithm to check if a graph is eulerian and if yes
    construst an Euler cycle.

    TODO

    :param graph: The input graph
    :returns: An euler cycle as a :py:class:`.GraphPath` or None
    """
    is_eulerian, gp = backend.jgrapht_cycles_eulerian_exec_hierholzer(graph.handle)
    return _JGraphTGraphPath(gp) if is_eulerian else None


def chinese_postman(graph):
    """Run Edmonds-Johnson algorithm to solve the chinese postman problem. 

    TODO
    """
    gp = backend.jgrapht_cycles_chinese_postman_exec_edmonds_johnson(graph.handle)
    return _JGraphTGraphPath(gp)




