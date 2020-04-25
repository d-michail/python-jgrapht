
from enum import Enum
from .exceptions import *
from .backend import jgrapht_get_errno, jgrapht_get_errno_msg, jgrapht_clear_errno


class Status(Enum):
    """Error status corresponding to the errors coming from the JGraphT native library."""
    SUCCESS = 0
    ERROR = 1
    ILLEGAL_ARGUMENT = 2
    UNSUPPORTED_OPERATION = 3
    INDEX_OUT_OF_BOUNDS = 4    
    NO_SUCH_ELEMENT = 5
    NULL_POINTER = 6
    CLASS_CAST = 7


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

