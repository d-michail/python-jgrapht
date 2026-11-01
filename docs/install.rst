.. _install:

Install
=======

Prebuilt wheels are published on `PyPI <https://pypi.org/project/jgrapht/>`_. The package replaces
the 1.x ``jgrapht`` package, so installation is::

  $ pip install jgrapht

Python 3.10 or newer is required. On platforms without a prebuilt wheel, the package is built from
source, as described below.

Building from source
--------------------

Build with `maturin <https://www.maturin.rs/>`_, which needs a Rust toolchain (stable, 1.88 or newer)
in addition to Python. Cargo downloads the ``jgrapht`` backend crates from crates.io, so the
build needs network access::

  $ python -m venv venv
  $ source venv/bin/activate
  $ pip install --upgrade pip
  $ pip install maturin pytest
  $ maturin develop

Use ``maturin develop --release`` for an optimized build, and run the tests with ``pytest``.

Building the documentation
--------------------------

::

  $ pip install -e ".[docs]"
  $ python -m sphinx -W -b html docs docs/_build/html

Checking the installation
-------------------------

.. code-block:: pycon

  >>> import jgrapht as jg
  >>> jg.__version__
  '2.0.0'
  >>> jg.shortest_path(jg.path_graph(3), 0, 2).weight
  2.0
