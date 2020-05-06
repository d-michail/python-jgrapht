
.. _exceptions:

.. currentmodule:: jgrapht.exceptions

Exceptions
**********

Exceptions and errors used in the library. We follow the naming of exceptions 
used in the original backend library, in order to help debug issues. If an exception 
is thrown in the backend the original error message is also propagated.

.. autoexception:: jgrapht.exceptions.IllegalArgumentError
.. autoexception:: jgrapht.exceptions.UnsupportedOperationError
.. autoexception:: jgrapht.exceptions.NoSuchElementError
.. autoexception:: jgrapht.exceptions.IndexOutOfBoundsError
.. autoexception:: jgrapht.exceptions.NullPointerError
.. autoexception:: jgrapht.exceptions.ClassCastError
.. autoexception:: jgrapht.exceptions.GraphExportError
.. autoexception:: jgrapht.exceptions.GraphImportError
.. autoexception:: jgrapht.exceptions.InputOutputError

All the above exceptions have the following error as a base class. In the case that
a backend exception is not mapped explicitly to one of the above, we simply raise 
an instance of :class:`jgrapht.exceptions.Error` with the appropriate message.

.. autoexception:: jgrapht.exceptions.Error

