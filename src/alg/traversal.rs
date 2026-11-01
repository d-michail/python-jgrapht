//! Graph traversals and vertex orderings.

use jgrapht::traverse::{
    Bfs, DegeneracyOrdering, Dfs, DfsPostOrder, LexBfs, MaximumCardinality, RandomWalk,
};
use pyo3::prelude::*;
use pyo3::types::PyDict;
use rand::SeedableRng;
use rand::rngs::StdRng;

use crate::error::graph_error;
use crate::labels::dispatch;

/// Vertices in breadth-first order from ``start``; without ``start`` every component is
/// searched in turn, starting from the vertices in graph order.
#[pyfunction]
#[pyo3(signature = (graph, start=None))]
fn bfs(
    py: Python<'_>,
    graph: &Bound<'_, PyAny>,
    start: Option<Bound<'_, PyAny>>,
) -> PyResult<Vec<Py<PyAny>>> {
    dispatch!(graph, |g, lab| {
        match &start {
            Some(s) => {
                let s = lab.vertex_id(py, s)?;
                Ok(lab.vertices(py, Bfs::new(g, &s).map_err(graph_error)?))
            }
            None => Ok(lab.vertices(py, Bfs::all(g))),
        }
    })
}

/// ``{vertex: number of edges from start}`` for the vertices reachable from ``start``.
#[pyfunction]
fn bfs_depths<'py>(
    py: Python<'py>,
    graph: &Bound<'py, PyAny>,
    start: Bound<'py, PyAny>,
) -> PyResult<Bound<'py, PyDict>> {
    dispatch!(graph, |g, lab| {
        let s = lab.vertex_id(py, &start)?;
        let mut search = Bfs::new(g, &s).map_err(graph_error)?;
        let order: Vec<usize> = search.by_ref().collect();
        let depths = order
            .iter()
            .filter_map(|v| search.depth(v).map(|d| (*v, d)));
        lab.vertex_dict(py, depths)
    })
}

/// Vertices in depth-first (pre-)order from ``start``; without ``start`` every component is
/// searched in turn.
#[pyfunction]
#[pyo3(signature = (graph, start=None))]
fn dfs(
    py: Python<'_>,
    graph: &Bound<'_, PyAny>,
    start: Option<Bound<'_, PyAny>>,
) -> PyResult<Vec<Py<PyAny>>> {
    dispatch!(graph, |g, lab| {
        match &start {
            Some(s) => {
                let s = lab.vertex_id(py, s)?;
                Ok(lab.vertices(py, Dfs::new(g, &s).map_err(graph_error)?))
            }
            None => Ok(lab.vertices(py, Dfs::all(g))),
        }
    })
}

/// Vertices in depth-first post-order (a vertex after all its descendants) from ``start``;
/// without ``start`` every component is searched in turn.
#[pyfunction]
#[pyo3(signature = (graph, start=None))]
fn dfs_postorder(
    py: Python<'_>,
    graph: &Bound<'_, PyAny>,
    start: Option<Bound<'_, PyAny>>,
) -> PyResult<Vec<Py<PyAny>>> {
    dispatch!(graph, |g, lab| {
        match &start {
            Some(s) => {
                let s = lab.vertex_id(py, s)?;
                Ok(lab.vertices(py, DfsPostOrder::new(g, &s).map_err(graph_error)?))
            }
            None => Ok(lab.vertices(py, DfsPostOrder::all(g))),
        }
    })
}

/// A lexicographic breadth-first search order of the vertices.
#[pyfunction]
fn lex_bfs_order(py: Python<'_>, graph: &Bound<'_, PyAny>) -> PyResult<Vec<Py<PyAny>>> {
    dispatch!(graph, |g, lab| Ok(lab.vertices(py, LexBfs::new(g))))
}

/// A maximum cardinality search order: each vertex has the most already-visited neighbours.
#[pyfunction]
fn maximum_cardinality_order(py: Python<'_>, graph: &Bound<'_, PyAny>) -> PyResult<Vec<Py<PyAny>>> {
    dispatch!(graph, |g, lab| Ok(
        lab.vertices(py, MaximumCardinality::new(g))
    ))
}

/// A degeneracy ordering (repeatedly removing a vertex of minimum degree) as
/// ``(order, degeneracy)``.
#[pyfunction]
fn degeneracy_ordering(
    py: Python<'_>,
    graph: &Bound<'_, PyAny>,
) -> PyResult<(Vec<Py<PyAny>>, usize)> {
    dispatch!(graph, |g, lab| {
        let mut it = DegeneracyOrdering::new(g);
        let order: Vec<usize> = it.by_ref().collect();
        Ok((lab.vertices(py, order), it.degeneracy()))
    })
}

/// A random walk of at most ``max_steps`` steps from ``start`` as the list of visited vertices
/// (``start`` first). It stops early at a vertex without outgoing edges. With ``weighted`` the
/// next edge is chosen with probability proportional to its weight. ``seed`` makes it
/// reproducible.
#[pyfunction]
#[pyo3(signature = (graph, start, max_steps, weighted=false, seed=None))]
fn random_walk(
    py: Python<'_>,
    graph: &Bound<'_, PyAny>,
    start: Bound<'_, PyAny>,
    max_steps: usize,
    weighted: bool,
    seed: Option<u64>,
) -> PyResult<Vec<Py<PyAny>>> {
    dispatch!(graph, |g, lab| {
        let s = lab.vertex_id(py, &start)?;
        let rng = match seed {
            Some(x) => StdRng::seed_from_u64(x),
            None => StdRng::from_os_rng(),
        };
        let walk = RandomWalk::new(g, &s, max_steps, weighted, rng).map_err(graph_error)?;
        let visited = walk
            .collect::<jgrapht::Result<Vec<_>>>()
            .map_err(graph_error)?;
        Ok(lab.vertices(py, visited.into_iter().copied()))
    })
}

pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(bfs, m)?)?;
    m.add_function(wrap_pyfunction!(bfs_depths, m)?)?;
    m.add_function(wrap_pyfunction!(dfs, m)?)?;
    m.add_function(wrap_pyfunction!(dfs_postorder, m)?)?;
    m.add_function(wrap_pyfunction!(lex_bfs_order, m)?)?;
    m.add_function(wrap_pyfunction!(maximum_cardinality_order, m)?)?;
    m.add_function(wrap_pyfunction!(degeneracy_ordering, m)?)?;
    m.add_function(wrap_pyfunction!(random_walk, m)?)?;
    Ok(())
}
