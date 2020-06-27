from .. import backend as _backend

from .._internals._collections import _JGraphTIntegerIntegerMap

from .._internals._anyhashableg import _is_anyhashable_graph
from .._internals._anyhashableg_collections import _AnyHashableGraphVertexIntegerMap


def _wrap_result(graph, num_colors, color_map_handle):
    if _is_anyhashable_graph(graph):
        return num_colors, _AnyHashableGraphVertexIntegerMap(color_map_handle, graph)
    else:
        return num_colors, _JGraphTIntegerIntegerMap(color_map_handle)


def greedy_smallestnotusedcolor(graph):
    """The greedy coloring algorithm.
 
    The algorithm iterates over all vertices and assigns the smallest possible color that is not
    used by any neighbors. Subclasses may provide a different vertex ordering.

    :param graph: The input graph. Either directed or undirected.
    :returns: A vertex coloring as a tuple. First component is the number of colors, second is a
      dictionary from vertices to integers.
    """
    num_colors, color_map_handle = _backend.jgrapht_coloring_exec_greedy(graph.handle)
    return _wrap_result(graph, num_colors, color_map_handle)


def greedy_smallestdegreelast(graph):
    r"""The smallest degree last greedy coloring algorithm.
 
    This is the greedy coloring algorithm with the smallest-last ordering of the vertices. The basic
    idea is as follows: Assuming that vertices :math:`v_{k+1}, \dotso, v_n` have been already selected,
    choose :math:`v_k` so that the degree of :math:`v_k` in the subgraph induced by
    :math:`V - $(v_{k+1}, \dotso, v_n)` is minimal. See the following paper for details.
  
    * D. Matula, G. Marble, and J. Isaacson. Graph coloring algorithms in Graph Theory and Computing.
      Academic Press, 104--122, 1972.

    :param graph: The input graph. Either directed or undirected.
    :returns: A vertex coloring as a tuple. First component is the number of colors, second is a
      dictionary from vertices to integers.
    """
    (
        num_colors,
        color_map_handle,
    ) = _backend.jgrapht_coloring_exec_greedy_smallestdegreelast(graph.handle)
    return _wrap_result(graph, num_colors, color_map_handle)


def greedy_largestdegreefirst(graph):
    """The largest degree first greedy coloring algorithm.
 
    This is the greedy coloring algorithm which orders the vertices by non-increasing degree. See the
    following paper for details.
 
    * D. J. A. Welsh and M. B. Powell. An upper bound for the chromatic number of a graph and its 
      application to timetabling problems. The Computer Journal, 10(1):85--86, 1967.
 
    :param graph: The input graph. Either directed or undirected.
    :returns: A vertex coloring as a tuple. First component is the number of colors, second is a
      dictionary from vertices to integers.
    """
    (
        num_colors,
        color_map_handle,
    ) = _backend.jgrapht_coloring_exec_greedy_largestdegreefirst(graph.handle)
    return _wrap_result(graph, num_colors, color_map_handle)


def greedy_random(graph, seed=None):
    """The greedy coloring algorithm with a random vertex ordering.

    :param graph: The input graph. Either directed or undirected.
    :param seed: Seed for the random number generator. If None then the time 
                 is used to select a seed.
    :returns: A vertex coloring as a tuple. First component is the number of colors, second is a
      dictionary from vertices to integers.
    """
    if seed is None:
        num_colors, color_map_handle = _backend.jgrapht_coloring_exec_greedy_random(
            graph.handle
        )
    else:
        (
            num_colors,
            color_map_handle,
        ) = _backend.jgrapht_coloring_exec_greedy_random_with_seed(graph.handle, seed)
    return _wrap_result(graph, num_colors, color_map_handle)


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
    :returns: A vertex coloring as a tuple. First component is the number of colors, second is a
      dictionary from vertices to integers.             
    """
    num_colors, color_map_handle = _backend.jgrapht_coloring_exec_greedy_dsatur(
        graph.handle
    )
    return _wrap_result(graph, num_colors, color_map_handle)


def color_refinement(graph):
    r"""Color refinement algorithm. Finds the coarsest stable coloring of a graph based on a given
    :math:`\alpha` coloring as described in the following 
    `paper <https://doi.org/10.1007/s00224-016-9686-0>`_: 
    
    * C. Berkholz, P. Bonsma, and M. Grohe. Tight lower and upper bounds for the complexity of
      canonical colour refinement. Theory of Computing Systems, 60(4), p581--614, 2017.
 
    The complexity of this algorithm is :math:`\mathcal{O}((n + m) \log n)`.

    :param graph: The input graph. Either directed or undirected.
    :returns: A vertex coloring as a tuple. First component is the number of colors, second is a
      dictionary from vertices to integers.
    """
    num_colors, color_map_handle = _backend.jgrapht_coloring_exec_color_refinement(
        graph.handle
    )
    return _wrap_result(graph, num_colors, color_map_handle)


def backtracking_brown(graph):
    """Brown backtracking graph coloring algorithm.

    :param graph: The input graph. Either directed or undirected.
    :returns: A vertex coloring as a tuple. First component is the number of colors, second is a
      dictionary from vertices to integers.
    """
    num_colors, color_map_handle = _backend.jgrapht_coloring_exec_backtracking_brown(
        graph.handle
    )
    return _wrap_result(graph, num_colors, color_map_handle)


def chordal_min_coloring(graph):
    r"""Find a minimum vertex coloring for a chordal graph.

    The algorithms first computes a perfect elimination ordering and then a
    vertex coloring. Running time :math:`\mathcal{O}(n+m)`. 

    :param graph: the chordal graph. If the graph is not chordal an error is raised
    :returns: A vertex coloring as a tuple. First component is the number of colors, second is a
      dictionary from vertices to integers.
    """
    (
        num_colors,
        color_map_handle,
    ) = _backend.jgrapht_coloring_exec_chordal_minimum_coloring(graph.handle)
    return _wrap_result(graph, num_colors, color_map_handle)
