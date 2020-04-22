from enum import Enum

class Status(Enum):
    SUCCESS = 0
    ERROR = 1
    UNSUPPORTED_OPERATION = 2
    ILLEGAL_ARGUMENT = 3
    INVALID_HANDLE = 20
    INVALID_VERTEX = 22
    INVALID_EDGE = 23
    GRAPH_IS_UNWEIGHTED = 51
    GRAPH_NOT_UNDIRECTED = 52
    NO_SUCH_ELEMENT = 100
    MAP_NO_SUCH_KEY = 200
