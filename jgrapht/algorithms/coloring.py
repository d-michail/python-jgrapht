from .. import backend
from .._errors import raise_status, UnsupportedOperationError
from .._wrappers import JGraphTLongLongMap


def _coloring_alg(name, graph, *args):
    alg_method_name = 'jgrapht_coloring_exec_'
    alg_method_name += name

    try:
        alg_method = getattr(backend, alg_method_name)
    except AttributeError:
        raise UnsupportedOperationError("Algorithm not supported.")    

    err, num_colors, color_map_handle = alg_method(graph.handle, *args)
    if err: 
        raise_status()

    return (num_colors, JGraphTLongLongMap(handle=color_map_handle))


def greedy_smallestnotusedcolor(graph):
    """The greedy coloring algorithm.
 
    The algorithm iterates over all vertices and assigns the smallest possible color that is not
    used by any neighbors. Subclasses may provide a different vertex ordering.

    :param graph: The input graph. Either directed or undirected.
    :returns: A vertex coloring as a dictionary from vertices to integers.
    """
    return _coloring_alg('greedy', graph)

def greedy_smallestdegreelast(graph):
    r"""The smallest degree last greedy coloring algorithm.
 
    This is the greedy coloring algorithm with the smallest-last ordering of the vertices. The basic
    idea is as follows: Assuming that vertices :math:`v_{k+1}, \dotso, v_n` have been already selected,
    choose :math:`v_k` so that the degree of :math:`v_k` in the subgraph induced by
    :math:`V - $(v_{k+1}, \dotso, v_n)` is minimal. See the following paper for details.
  
    * D. Matula, G. Marble, and J. Isaacson. Graph coloring algorithms in Graph Theory and Computing.
      Academic Press, 104--122, 1972.

    :param graph: The input graph. Either directed or undirected.
    :returns: A vertex coloring as a dictionary from vertices to integers.
    """
    return _coloring_alg('greedy_smallestdegreelast', graph)

def greedy_largestdegreefirst(graph):
    """The largest degree first greedy coloring algorithm.
 
    This is the greedy coloring algorithm which orders the vertices by non-increasing degree. See the
    following paper for details.
 
    * D. J. A. Welsh and M. B. Powell. An upper bound for the chromatic number of a graph and its 
      application to timetabling problems. The Computer Journal, 10(1):85--86, 1967.
 
    :param graph: The input graph. Either directed or undirected.
    :returns: A vertex coloring as a dictionary from vertices to integers.    
    """
    return _coloring_alg('greedy_largestdegreefirst', graph)

def greedy_random(graph, seed=None):
    """The greedy coloring algorithm with a random vertex ordering.

    :param graph: The input graph. Either directed or undirected.
    :param seed: Seed for the random number generator. If None then the time 
                 is used to select a seed.
    :returns: A vertex coloring as a dictionary from vertices to integers.             
    """
    if seed is None: 
        return _coloring_alg('greedy_random', graph)
    else:
        return _coloring_alg('greedy_random_with_seed', graph, seed)

def greedy_dsatur(graph):
    r"""The Dsatur greedy coloring algorithm.
   
    This is the greedy coloring algorithm using saturation degree ordering. The saturation degree of
    a vertex is defined as the number of different colors to which it is adjacent. The algorithm
    selects always the vertex with the largest saturation degree. If multiple vertices have the same
    maximum saturation degree, a vertex of maximum degree in the uncolored subgraph is selected.
 
    Note that the DSatur is not optimal in general, but is optimal for bipartite graphs. Compared to
    other simpler greedy ordering heuristics, it is usually considered slower but more efficient
    w.r.t. the number of used colors. See the following papers for details:
 
    * D. Brelaz. New methods to color the vertices of a graph. Communications of ACM, 22(4):251–256, 1979.
    * The smallest hard-to-color graph for algorithm DSATUR. Discrete Mathematics, 236:151--165, 2001.

    This implementation requires :math:`\mathcal{O}(n^2)` running time and space. The following paper
    discusses possible improvements in the running time.

    * J. S. Turner. Almost all $k$-colorable graphs are easy to color. Journal of Algorithms. 9(1):63--82, 1988.
    
    :param graph: The input graph. Either directed or undirected.
    :returns: A vertex coloring as a dictionary from vertices to integers.             
    """
    return _coloring_alg('greedy_dsatur', graph)

def color_refinement(graph):
    r"""Color refinement algorithm. Finds the coarsest stable coloring of a graph based on a given
    :math:`\alpha` coloring as described in the following 
    `paper <https://doi.org/10.1007/s00224-016-9686-0>`_: 
    
    * C. Berkholz, P. Bonsma, and M. Grohe. Tight lower and upper bounds for the complexity of
      canonical colour refinement. Theory of Computing Systems, 60(4), p581--614, 2017.
 
    The complexity of this algorithm is :math:`\mathcal{O}((n + m) \log n)`.

    :param graph: The input graph. Either directed or undirected.
    :returns: A vertex coloring as a dictionary from vertices to integers.             
    """
    return _coloring_alg('color_refinement', graph)

def backtracking_brown(graph):
    """Brown backtracking graph coloring algorithm.

    :param graph: The input graph. Either directed or undirected.
    :returns: A vertex coloring as a dictionary from vertices to integers.
    """
    return _coloring_alg('backtracking_brown', graph)    


