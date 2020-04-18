from . import jgrapht
from . import status

class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class GraphError(Error):
    """Exception raised for graph errors.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message

class GenericError(Error):
    """Exception raised for generic errors.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message

class UnsupportedError(Error):
    """Exception raised for unsupported errors.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message

class InvalidReferenceError(Error):
    """Exception raised for invalid reference errors.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message                        

class IteratorError(Error):
    """Exception raised for iterator errors.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message

def check_last_error(message=None):
    errno = jgrapht.jgrapht_get_errno()
    if errno == status.Status.GENERIC_ERROR.value:
        raise GenericError('An error occured' if message is None else message)
    if errno == status.Status.UNSUPPORTED_OPERATION.value:
        raise UnsupportedError('Unsupported Operation' if message is None else message)    
    if errno == status.Status.INVALID_REFERENCE.value:
        raise InvalidReferenceError('Invalid reference' if message is None else message)
    if errno == status.Status.INVALID_GRAPH.value:
        raise GraphError('Invalid graph' if message is None else message)    
    if errno == status.Status.INVALID_VERTEX.value:
        raise GraphError('Invalid vertex' if message is None else message)
    if errno == status.Status.INVALID_EDGE.value:
        raise GraphError('Invalid edge' if message is None else message)
    if errno == status.Status.GRAPH_CREATION_ERROR.value:
        raise GraphError('Graph creation error' if message is None else message)
    if errno == status.Status.GRAPH_IS_UNWEIGHTED.value:
        raise GraphError('Graph is unweighted' if message is None else message)
    if errno == status.Status.ITERATOR_NO_SUCH_ELEMENT.value:
        raise IteratorError('No such element' if message is None else message)                                                            
    if errno != status.Status.SUCCESS.value:
        raise GenericError('Operation failed' if message is None else message)        
