[![PyPI](https://img.shields.io/pypi/v/jgrapht)](https://pypi.org/project/jgrapht)
[![Python](https://img.shields.io/pypi/pyversions/jgrapht)](https://pypi.org/project/jgrapht)
[![CI](https://github.com/d-michail/python-jgrapht-rs/actions/workflows/CI.yml/badge.svg)](https://github.com/d-michail/python-jgrapht-rs/actions/workflows/CI.yml)
[![Documentation Status](https://readthedocs.org/projects/python-jgrapht-rs/badge/?version=latest)](https://python-jgrapht-rs.readthedocs.io/en/latest/?badge=latest)
[![License: EPL-2.0 OR LGPL-2.1+](https://img.shields.io/badge/license-EPL--2.0%20OR%20LGPL--2.1%2B-blue.svg)](license-EPL.txt)

# Python-JGraphT

Python bindings for the [JGraphT](https://jgrapht.org) graph library.

JGraphT is a free library that provides mathematical graph-theory objects and algorithms. It has
very efficient and generic graph data structures and a sizeable collection of sophisticated
algorithms, and it is written with stability, performance and interoperability in mind. It includes
algorithms from many application domains, such as path planning, routing, network analysis,
combinatorial optimization and computational biology.

The original library is written in Java. This package uses [`jgrapht`](https://crates.io/crates/jgrapht),
a Rust port of it ([source](https://github.com/d-michail/jgrapht-rs)), and is built with
[PyO3](https://pyo3.rs) and [maturin](https://www.maturin.rs/). The result is a *native,
self-contained extension* with *no dependency* on the JVM or on GraalVM.

This is **JGraphT for Python 2.0**, a complete rewrite that replaces the 1.x `jgrapht` package, which
wrapped the GraalVM-built `jgrapht-capi` shared library. It is **not backward compatible** with 1.x.

## Features

* **Two graph classes.** `Graph` is mutable; its vertices and edges are any hashable Python
  objects. `SparseGraph` is immutable and compact, with the integer vertices `0..n-1` and edges
  `0..m-1`. Every algorithm accepts both.
* **Algorithms** (about 200 functions): shortest paths (Dijkstra, Bellman-Ford, A\* with a Python
  heuristic, Floyd-Warshall, Johnson, k shortest paths, contraction hierarchies, transit nodes),
  spanning trees, maximum flow and minimum cuts, minimum-cost flow, matchings, connectivity and
  components, cycles and Eulerian tours, TSP heuristics, coloring, cliques and independent sets,
  isomorphism, centrality and other scores, clustering, planarity and drawing layouts, and more.
  See the [API reference](https://python-jgrapht-rs.readthedocs.io/en/latest/api/index.html).
* **Generators:** structured families, random graphs, the 44 named graphs and NETGEN flow
  instances, as either graph class.
* **Graph I/O:** CSV, DIMACS, DOT, GEXF, GML, graph6, GraphML, JSON and TSPLIB are read; all of
  these except TSPLIB, plus LEMON, matrices and Visio, are written. Attributes, weights, event
  streams, and TSPLIB tours are supported.
* **Attributes:** vertices, edges and the graph itself carry attribute dicts
  (`g.vertex_attrs[v]["color"] = "red"`), which the readers fill and the writers write.
* **Derived graphs:** copies, induced and edge subgraphs, unions, reversed, undirected and
  re-weighted versions, and a read-only wrapper.
* **Drawing and conversion:** `jgrapht.drawing` draws graphs with matplotlib, and `jgrapht.convert`
  converts to and from NetworkX and pydot. Both need the optional package they work with.

## Examples

```python
import jgrapht as jg

g = jg.Graph(weighted=True)
for v in "abcd":
    g.add_vertex(v)
g.add_edge("a", "b", edge="ab", weight=1.0)   # edge objects are any hashable; omit for ints
g.add_edge("b", "c", weight=2.0)
g.add_edge("c", "d", weight=1.0)
print(jg.shortest_path(g, "a", "d"))
# GraphPath(vertices=['a', 'b', 'c', 'd'], weight=4.0)

# compact immutable graph on vertices 0..n-1, edges numbered in input order
s = jg.SparseGraph(4, [(0, 1), (1, 2), (2, 3)], weights=[1.0, 2.0, 1.0])
print(jg.shortest_path(s, 0, 3).edges)         # [0, 1, 2]
print(jg.connected_components(s))              # [[0, 1, 2, 3]]

# generators and named graphs
p = jg.named_graph("petersen")
print(jg.girth(p), jg.diameter(p))             # 5 2.0
grid = jg.grid_graph(10, 10, sparse=True)

# reading and writing
text = jg.graph_to_string(p, "gml")
h = jg.parse_graph(text, "gml")
jg.write_graph(g, "graph.graphml", "graphml", vertex_id=str, edge_weights=True)
g2 = jg.read_graph("graph.graphml", "graphml", weighted=True)
```

Python callbacks are supported where the algorithm takes a function (A\* heuristics, isomorphism
predicates, vertex and edge attribute functions for export); an exception raised in a callback
stops the algorithm and propagates to the caller. Failures of the library itself raise
`jgrapht.GraphError`, a `ValueError`.

## Installation

Prebuilt wheels for CPython 3.10 to 3.14 are published on [PyPI](https://pypi.org/project/jgrapht/)
for Linux (x86-64), Windows and macOS (Apple silicon). On a recent machine installing is as easy as:

```bash
pip install jgrapht
```

If your pip is old, upgrade it first:

```bash
pip install --upgrade pip
pip install jgrapht
```

To use a virtual environment, or to install in your user directory:

```bash
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install jgrapht

pip install --user jgrapht      # alternatively, without a virtual environment
```

Check the installation:

```bash
python -c "import jgrapht; print(jgrapht.__version__)"
```

Drawing and conversion use optional packages, which you can install together with this one:

```bash
pip install "jgrapht[plot]"       # matplotlib, for jgrapht.drawing
pip install "jgrapht[networkx]"   # for jgrapht.convert.to_nx and from_nx
pip install "jgrapht[pydot]"      # for jgrapht.convert.to_pydot and from_pydot
```

### Building from source

This needs Python 3.10+ and a Rust toolchain (stable, 1.88+). Cargo downloads the `jgrapht` and
`jgrapht-io` crates from crates.io, so the build needs network access.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install maturin pytest
maturin develop          # builds the extension and installs it into the venv
pytest
```

Use `maturin develop --release` for an optimized build. Rebuild after every change in `src/`.

## Documentation

Full documentation is at <https://python-jgrapht-rs.readthedocs.io>: an
[API reference](https://python-jgrapht-rs.readthedocs.io/en/latest/api/index.html), tutorials, and an
example gallery. (The documentation of the 1.x series is at <https://python-jgrapht.readthedocs.io>.)
The sources are in [`docs/`](docs) (Sphinx) and [`examples/`](examples); design
notes are in [`docs/design/`](docs/design). See [CHANGELOG.md](CHANGELOG.md) for what each release
adds.

To build the HTML documentation locally (warnings are errors):

```bash
pip install -e ".[docs]"
python -m sphinx -W -b html docs docs/_build/html
```

## Development

* `src/` holds the extension: `graph.rs` and `sparse.rs` (the graph classes), `labels.rs` (dispatch
  from Python graphs to the Rust graph types), `alg/` (one module per algorithm family),
  `generators.rs` and `formats.rs`.
* `tests/` holds the pytest suite, including ports of the `jgrapht-io` parity tests. A guard test
  requires every public name to appear in `docs/api/` and every public callable to have a
  docstring.
* `.github/workflows/` holds the CI workflow and the manual TestPyPI and tag-triggered PyPI
  publishing workflows.

## Citing

Are you using the software in your research? We would appreciate it if you cite the following
publication. Citing software is as important as citing any other source. If you are not sure whether
to cite something, [Shouldacite](https://bit.ly/shouldacite) can help you decide.

```bibtex
@article{jgrapht,
  title = {{J}{G}raph{T}--{A} {J}ava {L}ibrary for {G}raph {D}ata {S}tructures and {A}lgorithms},
  author = {Michail, Dimitrios and Kinable, Joris and Naveh, Barak and Sichi, John V.},
  year = {2020},
  issue_date = {May 2020},
  publisher = {Association for Computing Machinery},
  address = {New York, NY, USA},
  volume = {46},
  number = {2},
  journal = {ACM Trans. Math. Softw.},
  month = may,
  articleno = {16},
  numpages = {29},
}
```

## License

This library may be used under the terms of either the

* [Eclipse Public License (EPL) 2.0](license-EPL.txt), or the
* [GNU Lesser General Public License (LGPL) 2.1 or later](license-LGPL.txt),

like the `jgrapht` crate and JGraphT. As a recipient, you may choose which license to receive the
code under. This library is distributed WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. Please refer to the licenses for details.

SPDX-License-Identifier: EPL-2.0 OR LGPL-2.1-or-later

## Author

(C) Copyright 2026, by Dimitrios Michail

Enjoy!
