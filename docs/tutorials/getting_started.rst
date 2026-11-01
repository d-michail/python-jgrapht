.. _tutorials/getting_started:

Getting started
===============

.. currentmodule:: jgrapht

This tutorial walks through the most common things you do with the library: build a graph, ask
it questions, run an algorithm and save the result. The other tutorials go into more detail.

Creating a graph
----------------

A :class:`~jgrapht.Graph` can have any hashable Python object as a vertex. Create the graph, then add
vertices and edges. :meth:`~jgrapht.Graph.add_edge` returns the edge (a fresh integer unless you
pass your own object with ``edge=``).

.. code-block:: pycon

  >>> import jgrapht as jg
  >>> g = jg.Graph(weighted=True)
  >>> for city in ['Athens', 'Patras', 'Larissa', 'Volos']:
  ...     _ = g.add_vertex(city)
  >>> g.add_edge('Athens', 'Patras', weight=215.0)
  0
  >>> g.add_edge('Athens', 'Larissa', weight=350.0)
  1
  >>> g.add_edge('Larissa', 'Volos', weight=60.0)
  2
  >>> g.add_edge('Athens', 'Volos', weight=330.0)
  3
  >>> g
  Graph(directed=False, weighted=True, vertices=4, edges=4)

Asking questions
----------------

.. code-block:: pycon

  >>> len(g), g.edge_count()
  (4, 4)
  >>> g.vertices()
  ['Athens', 'Patras', 'Larissa', 'Volos']
  >>> g.neighbors_of('Athens')
  ['Patras', 'Larissa', 'Volos']
  >>> g.degree_of('Athens')
  3
  >>> [(g.edge_source(e), g.edge_target(e), g.edge_weight(e)) for e in g.edges()]
  [('Athens', 'Patras', 215.0), ('Athens', 'Larissa', 350.0), ('Larissa', 'Volos', 60.0), ('Athens', 'Volos', 330.0)]

Running an algorithm
--------------------

Algorithms are functions that take the graph first. A shortest path comes back as a :class:`~jgrapht.GraphPath`.

.. code-block:: pycon

  >>> path = jg.shortest_path(g, 'Patras', 'Volos')
  >>> path.vertices
  ['Patras', 'Athens', 'Volos']
  >>> path.weight
  545.0
  >>> jg.minimum_spanning_tree(g)[0]
  605.0
  >>> jg.is_connected(g)
  True

Things that do not exist are ``None``: asking for a path between vertices in different components gives no path.

.. code-block:: pycon

  >>> _ = g.add_vertex('Rhodes')
  >>> jg.shortest_path(g, 'Patras', 'Rhodes')

Saving and loading
------------------

.. code-block:: pycon

  >>> text = jg.graph_to_string(g, 'graphml', vertex_id=str, edge_weights=True)
  >>> h = jg.parse_graph(text, 'graphml', weighted=True)
  >>> sorted(h.vertices())
  ['Athens', 'Larissa', 'Patras', 'Rhodes', 'Volos']

See :doc:`io` for the other formats. Next: :doc:`graph` and :doc:`sparse_graph` describe the two
graph classes, and :doc:`algorithms` how results look.

