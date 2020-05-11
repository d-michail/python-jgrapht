from .. import backend
from .._internals._collections import (
    _JGraphTIntegerSetIterator
)

def is_weakly_connected(graph):
  """TODO
  """
  connected, sets = backend.jgrapht_connectivity_weak_exec_bfs(graph.handle)
  return connected, _JGraphTIntegerSetIterator(sets)


def is_strongly_connected_gabow(graph):
  """TODO
  """
  connected, sets = backend.jgrapht_connectivity_strong_exec_gabow(graph.handle)
  return connected, _JGraphTIntegerSetIterator(sets)


def is_strongly_connected_kosaraju(graph):
  """TODO
  """
  connected, sets = backend.jgrapht_connectivity_strong_exec_kosaraju(graph.handle)
  return connected, _JGraphTIntegerSetIterator(sets)  


def is_connected(graph): 
  """TODO
  """
  if graph.type.directed:
    return is_strongly_connected_kosaraju(graph)
  else:
    return is_weakly_connected(graph)

