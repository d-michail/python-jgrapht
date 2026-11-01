.. _io/events:

Event-driven import
*******************

.. currentmodule:: jgrapht

:func:`read_events` and :func:`parse_events` stream a document as a sequence of events (vertices,
edges, attributes, counts) without building a graph, for the formats in :func:`event_formats`.
Events are tuples starting with their name; pass a ``callback`` to receive them as they are read,
or omit it to get a list.

Example
=======

.. code-block:: pycon

  >>> import jgrapht as jg
  >>> jg.parse_events('1,2\n2,3\n', 'csv', variant='edge_list')
  [('start',), ('vertex', '1'), ('vertex', '2'), ('edge', ('1', '2', None)), ('vertex', '3'), ('edge', ('2', '3', None)), ('end',)]
  >>> seen = []
  >>> jg.parse_events('p edge 3 2\ne 1 2\ne 2 3\n', 'dimacs', callback=seen.append)
  >>> seen
  [('start',), ('vertex_count', 3), ('edge_count', 2), ('edge', (1, 2, None)), ('edge', (2, 3, None)), ('end',)]
  >>> jg.event_formats()
  ['csv', 'dimacs', 'gexf', 'graph6', 'graphml', 'graphml_edge_list', 'json']

Functions
=========

.. autofunction:: read_events
.. autofunction:: parse_events
.. autofunction:: event_formats
