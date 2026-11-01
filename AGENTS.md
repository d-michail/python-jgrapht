# AGENTS.md

Guidance for AI coding agents working in this repository.

## Project

`python-jgrapht` is the Python package `jgrapht` (2.0 series): PyO3 bindings for the
[`jgrapht`](https://crates.io/crates/jgrapht) Rust crate, built with maturin. It is a complete
rewrite and **not backward compatible** with the 1.x series (which wrapped `jgrapht-capi`).
Licensed EPL-2.0 OR LGPL-2.1-or-later.

## Layout

* `src/` – Rust extension (crate `_jgrapht_rs`, Python module `jgrapht._jgrapht_rs`):
  `graph.rs` / `sparse.rs` (the `Graph` and `SparseGraph` classes), `labels.rs` (dispatch from
  Python graphs to Rust graph types), `alg/` (one module per algorithm family), `generators.rs`,
  `formats.rs`, `error.rs`.
* `python/jgrapht/` – Python package (`__init__.py` re-exports the public API, `__version__.py`).
* `tests/` – pytest suite (including ports of `jgrapht-io` parity tests; data in `tests/data`).
* `docs/` – Sphinx docs (`docs/api/`, `docs/tutorials/`, `docs/design/`); `examples/` – sphinx-gallery
  examples.
* `CHANGELOG.md` – update it for user-visible changes.

## Build and test

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install maturin pytest
maturin develop          # rebuild the extension after ANY change in src/
pytest                   # full suite
cargo check --all-targets
```

Docs (warnings are errors, as in CI):

```bash
pip install -e ".[docs]"
python -m sphinx -W -b html docs docs/_build/html
```

Requires Python 3.10+ and stable Rust 1.88+ (edition 2024). The build needs network access to
fetch crates from crates.io. Tests run against the installed extension, so rebuild with
`maturin develop` before running `pytest` after Rust changes.

## Conventions

* Every public name must appear in `docs/api/` and every public callable must have a docstring;
  `tests/test_api_surface.py` enforces this. When adding an API, update `__init__.py`, the docs,
  tests, and the changelog together.
* Algorithms accept both `Graph` (mutable, hashable Python vertices/edges) and `SparseGraph`
  (immutable, ints `0..n-1` / `0..m-1`).
* Library failures raise `jgrapht.GraphError` (a `ValueError`). Exceptions raised in Python
  callbacks must propagate to the caller.
* CI (`.github/workflows/CI.yml`) builds and tests on Linux, Windows and macOS for Python
  3.10–3.14; keep changes portable.
* Do not commit `.venv/`, `target/`, or built `.so` files.

## Git

* **Never add `Co-Authored-By` trailers** (or any other AI attribution lines) to commit
  messages or pull request descriptions.
* Work on a branch and open a PR against `main`; do not commit directly to `main`.
* Only commit or push when asked.
