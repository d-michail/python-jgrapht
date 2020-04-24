
from .status import Status
from .jgrapht import jgrapht_get_errno, jgrapht_get_errno_msg, jgrapht_clear_errno


class Error(Exception):
    """Base class for exceptions in this module.

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
    """Check the last error and raise the appropriate exception if needed. 

    If an error has been registered, it is cleared and the appropriate exception 
    is raised. Otherwise, nothing happens.
    """
    errno = jgrapht_get_errno()
    if errno == Status.SUCCESS.value:
        return errno
    errno_msg = jgrapht_get_errno_msg()
    jgrapht_clear_errno()
    if errno == Status.ILLEGAL_ARGUMENT.value:
        raise IllegalArgumentError(errno_msg)    
    if errno == Status.UNSUPPORTED_OPERATION.value:
        raise UnsupportedOperationError(errno_msg)    
    if errno == Status.INDEX_OUT_OF_BOUNDS.value:
        raise IndexOutOfBoundsError(errno_msg)
    if errno == Status.NO_SUCH_ELEMENT.value:
        raise NoSuchElementError(errno_msg)
    if errno == Status.NULL_POINTER.value:
        raise NullPointerError(errno_msg)
    if errno == Status.CLASS_CAST.value:
        raise ClassCastError(errno_msg)
    raise Error(errno_msg)        

