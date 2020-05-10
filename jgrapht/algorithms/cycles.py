from .. import backend
from .._internals._paths import (
    _JGraphTGraphPath,
    _JGraphTGraphPathIterator,
)
from .._internals._collections import (
    _JGraphTLongListIterator
)


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



def fundamental_cycle_basis(graph, variant='bfswithqueue'):
    """Compute a fundamental cycle basis.

    TODO
    """

    TECHNIQUE = {
        'paton': 'paton',
        'bfswithqueue': 'queue_bfs',
        'bfswithstack': 'stack_bfs',
    }

    alg_name = TECHNIQUE.get(variant, 'bfswithqueue')
    alg_method_name = 'jgrapht_cycles_fundamental_basis_exec_' + alg_name

    try:
        alg_method = getattr(backend, alg_method_name)
    except AttributeError:
        raise NotImplementedError("Algorithm not supported.")

    weight, cycles_it = alg_method(graph.handle)

    return weight, _JGraphTGraphPathIterator(cycles_it)


def enumerate_simple_cycles(graph, variant='tarjan'): 
    """Enumerate simple cycles in a directed graph.

    TODO
    """

    TECHNIQUE = {
        'Tarjan': 'tarjan',
        'Tiernan': 'tiernan',
        'Szwarcfiter-Lauer': 'szwarcfiter_lauer',
        'Hawick-James': 'hawick_james',
        'Johnson': 'johnson'
    }

    alg_name = TECHNIQUE.get(variant, 'tarjan')
    alg_method_name = 'jgrapht_cycles_simple_enumeration_exec_' + alg_name

    try:
        alg_method = getattr(backend, alg_method_name)
    except AttributeError:
        raise NotImplementedError("Algorithm not supported.")

    cycles_it = alg_method(graph.handle)
    return _JGraphTLongListIterator(cycles_it)

