
class Error(Exception):
    """Base class for exceptions in this module.

    Attributes:
        message -- explanation of the error
    """
    def __init__(self, message):
        self.message = message    


class UnsupportedOperationError(Error):
    """Exception raised for unsupported operations.

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
    """Exception raised for element access errors.

    Attributes:
        message -- explanation of the error
    """
    def __init__(self, message):
        self.message = message


class NullPointerError(Error):
    """Exception raised for null dereference errors.

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

class GraphExportError(Error):
    """Exception raised for export errors.

    Attributes:
        message -- explanation of the error
    """
    def __init__(self, message):
        self.message = message

class GraphImportError(Error):
    """Exception raised for import errors.

    Attributes:
        message -- explanation of the error
    """
    def __init__(self, message):
        self.message = message

class InputOutputError(Error):
    """Exception raised for IO errors.

    Attributes:
        message -- explanation of the error
    """
    def __init__(self, message):
        self.message = message
                        