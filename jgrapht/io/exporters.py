import time

from .. import backend
from ..exceptions import UnsupportedOperationError
from .._errors import raise_status
from .._wrappers import JGraphTLongIterator, JGraphTGraphPath

def _export_to_file(name, graph, filename, *args):
    alg_method_name = 'jgrapht_export_file_' + name

    try:
        alg_method = getattr(backend, alg_method_name)
    except AttributeError:
        raise UnsupportedOperationError('Algorithm {} not supported.'.format(name))

    err = alg_method(graph.handle, filename, *args)
    if err:
        raise_status()


DIMACS_FORMATS = dict({ 'shortestpath': backend.DIMACS_FORMAT_SHORTEST_PATH, 
                   'maxclique': backend.DIMACS_FORMAT_MAX_CLIQUE, 
                   'coloring' : backend.DIMACS_FORMAT_COLORING 
})


def dimacs(graph, filename, format="shortestpath"):
    format = DIMACS_FORMATS.get(format, backend.DIMACS_FORMAT_SHORTEST_PATH)
    custom = [ format ]
    return _export_to_file('dimacs', graph, filename, *custom)

