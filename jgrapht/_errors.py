from enum import Enum
from .exceptions import *
from .backend import (
    jgrapht_error_get_errno, 
    jgrapht_error_get_errno_msg, 
    jgrapht_error_clear_errno,
    jgrapht_error_print_stack_trace,
)
from .backend import (
    STATUS_SUCCESS,
    STATUS_ILLEGAL_ARGUMENT,
    STATUS_UNSUPPORTED_OPERATION,
)
from .backend import (
    STATUS_INDEX_OUT_OF_BOUNDS,
    STATUS_NO_SUCH_ELEMENT,
    STATUS_NULL_POINTER,
)
from .backend import STATUS_CLASS_CAST
from .backend import STATUS_IO_ERROR
from .backend import STATUS_EXPORT_ERROR
from .backend import STATUS_IMPORT_ERROR


def raise_status():
    """Check the last error and raise the appropriate exception if needed. 

    If an error has been registered, it is cleared and the appropriate exception 
    is raised. Otherwise, nothing happens.
    """
    errno = jgrapht_error_get_errno()
    if errno == STATUS_SUCCESS:
        return errno
    errno_msg = jgrapht_error_get_errno_msg()
    #jgrapht_error_print_stack_trace()
    jgrapht_error_clear_errno()
    if errno == STATUS_ILLEGAL_ARGUMENT:
        raise IllegalArgumentError(errno_msg)
    if errno == STATUS_UNSUPPORTED_OPERATION:
        raise UnsupportedOperationError(errno_msg)
    if errno == STATUS_INDEX_OUT_OF_BOUNDS:
        raise IndexOutOfBoundsError(errno_msg)
    if errno == STATUS_NO_SUCH_ELEMENT:
        raise NoSuchElementError(errno_msg)
    if errno == STATUS_NULL_POINTER:
        raise NullPointerError(errno_msg)
    if errno == STATUS_CLASS_CAST:
        raise ClassCastError(errno_msg)
    if errno == STATUS_IO_ERROR:
        raise InputOutputError(errno_msg)
    if errno == STATUS_EXPORT_ERROR:
        raise GraphExportError(errno_msg)
    if errno == STATUS_IMPORT_ERROR:
        raise GraphImportError(errno_msg)
    raise Error(errno_msg)
