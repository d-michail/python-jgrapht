from . import jgrapht
from . import status

class Error(Exception):
    """Base class for exceptions in this module.

    Attributes:
        message -- explanation of the error
    """
    def __init__(self, message):
        self.message = message    

class InvalidVertexError(Error):
    """Exception raised for graph errors.

    Attributes:
        message -- explanation of the error
    """
    def __init__(self, message):
        self.message = message

class IllegalArgumentError(Error):
    """Exception raised for generic errors.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message

class UnsupportedOperationError(Error):
    """Exception raised for unsupported errors.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message

class IllegalArgumentError(Error):
    """Exception raised for illegal argument errors.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message

class NoSuchElementError(Error):
    """Exception raised for iterator errors.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message

class IndexOutOfBoundsError(Error):
    """Exception raised for class cast errors.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message

class NullPointerError(Error):
    """Exception raised for class cast errors.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message        

class ClassCastError(Error):
    """Exception raised for class cast errors.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message        

def raise_status():
    errno = jgrapht.jgrapht_get_errno()
    if errno == status.Status.SUCCESS.value:
        return
    errno_msg = jgrapht.jgrapht_get_errno_msg()
    if errno == status.Status.ILLEGAL_ARGUMENT.value:
        raise IllegalArgumentError(errno_msg)    
    if errno == status.Status.UNSUPPORTED_OPERATION.value:
        raise UnsupportedOperationError(errno_msg)    
    if errno == status.Status.INDEX_OUT_OF_BOUNDS.value:
        raise IndexOutOfBoundsError(errno_msg)
    if errno == status.Status.NO_SUCH_ELEMENT.value:
        raise NoSuchElementError(errno_msg)
    if errno == status.Status.NULL_POINTER.value:
        raise NullPointerError(errno_msg)
    if errno == status.Status.CLASS_CAST.value:
        raise ClassCastError(errno_msg)
    if errno != status.Status.SUCCESS.value:
        raise Error(errno_msg)        


