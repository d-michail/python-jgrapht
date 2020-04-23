from enum import Enum

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

