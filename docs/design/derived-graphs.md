# Derived graphs: copies, and one live wrapper

Status: **decided.** Derived graphs are independent copies; the only live wrapper is
`as_unmodifiable`.

## Background

The `jgrapht` crate builds subgraphs, unions, reversed, undirected and re-weighted graphs as
wrappers over a base graph (`AsSubgraph`, `MaskSubgraph`, `GraphUnion`, `AsUndirected`,
`EdgeReversed`, `AsWeighted`, `AsUnweighted`, `Unmodifiable`) that follow later changes of the base.
The Python package returns independent copies instead (`copy_graph`, `induced_subgraph`,
`edge_subgraph`, `graph_union`, `as_undirected`, `reverse_edges`, `as_weighted`, `as_unweighted`;
`src/alg/derived.rs`, built through `Parts`). A copy goes stale when the original changes and never
writes through.

## The constraint

Every algorithm dispatches (`dispatch!` in `src/labels.rs`) on the six concrete Rust graph types
behind `Graph` and `SparseGraph`, and the compiler builds one copy of the algorithm per type. A
wrapper type is a different type, so supporting it means more compiled copies of every algorithm.

## What was tried

Two derived graphs, `as_undirected` and `reverse_edges`, were made live: a Python class holding a
reference to the base, and `dispatch!` borrowed the base's Rust graph and wrapped it for the
duration of one call. Nothing was copied or cached, nothing went stale, and no algorithm needed
editing. But the compiled code grows with each one (release build, baseline 1m40s and 13.0 MB;
with `as_undirected` 2m06s and 17.9 MB; with `reverse_edges` as well 2m39s and 22.3 MB), because both
change every directed base type and every dispatch macro carries the extra copies. Nesting one
wrapper in another cannot be dispatched without listing the combinations.

A cached copy that is rebuilt when the original changes (needs a modification counter on every
graph) was also considered and rejected.

## Decision

* The derived graphs stay copies, documented as such.
* `as_unmodifiable` (`src/unmodifiable.rs`) is live, because it does not change what an algorithm
  sees: `unwrap_readonly` replaces it by its base graph before dispatch, so it adds no compiled
  code. It holds a reference to the graph, shows its current state, and raises `GraphError` on every
  modification. It is accepted by every function that takes one graph, not by functions that take two
  (use `copy_graph` first), and cannot wrap another wrapper.
