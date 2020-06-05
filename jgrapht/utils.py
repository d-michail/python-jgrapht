from . import backend as _backend


class StringSupplier:

    def __init__(self, prefix=None, start=0):
        self._count = start
        self._prefix = prefix

    def __call__(self):
        value = self._count
        self._count += 1
        return '{}{}'.format(self._prefix, value)


def create_vertex_supplier():
    return StringSupplier(prefix='v')

def create_edge_supplier():
    return StringSupplier(prefix='e')
