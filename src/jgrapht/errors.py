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

def check_last_error(message=None):
    errno = jgrapht.jgrapht_get_errno()
    if errno == status.Status.INVALID_VERTEX.value:
        raise GraphError('Invalid vertex' if message is None else message)
    if errno != status.Status.SUCCESS.value:
        raise GenericError('Operation failed' if message is None else message)        