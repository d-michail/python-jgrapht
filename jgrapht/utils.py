class StringSupplier:
    """A string supplier which returns integers starting from zero with 
       a possible custom prefix.
    """

    def __init__(self, prefix=None, start=0):
        self._count = start
        self._prefix = prefix

    def __call__(self):
        value = self._count
        self._count += 1
        return "{}{}".format("" if self._prefix is None else self._prefix, value)


class IntegerSupplier:
    """An integer supplier which returns integers starting from zero.
    """

    def __init__(self, start=0):
        self._count = start

    def __call__(self):
        value = self._count
        self._count += 1
        return value


def create_vertex_supplier(type="str", prefix="v", start=0):
    """Create a vertex supplier. Vertex suppliers are called whenever an
    any-hashable graph wants to create a new vertex.

    :param type: type can be either 'str' or 'int'
    :param prefix: if a string supplier, a prefix to use
    :param start: where to start counting
    :returns: a vertex supplier
    """
    if type == "int":
        return IntegerSupplier(start=start)
    else:
        return StringSupplier(prefix=prefix, start=start)


def create_edge_supplier(type="str", prefix="e", start=0):
    """Create an edge supplier. Εdge suppliers are called whenever an
    any-hashable graph wants to create a new edge.

    :param type: type can be either 'str' or 'int'
    :param prefix: if a string supplier, a prefix to use
    :param start: where to start counting
    :returns: an edge supplier
    """
    if type == "int":
        return IntegerSupplier(start=start)
    else:
        return StringSupplier(prefix=prefix, start=start)
