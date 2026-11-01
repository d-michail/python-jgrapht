//! Single-source and all-pairs shortest paths.

use jgrapht::alg::shortestpath::{
    BellmanFord, BfsShortestPath, BidirectionalDijkstraShortestPath, DeltaStepping, Dijkstra,
    FloydWarshallShortestPaths, JohnsonShortestPaths, ParallelDeltaSteppingShortestPath,
    ShortestPathAlgorithm, SingleSourcePaths,
};
use jgrapht::{Graph as _, GraphExt as _, IncidenceGraph};
use pyo3::prelude::*;
use pyo3::types::PyDict;

use crate::error::{GraphError, graph_error};
use crate::graph::GraphPath;
use crate::labels::{EdgeId, dispatch};

fn unknown_algorithm(name: &str) -> PyErr {
    GraphError::new_err(format!("unknown algorithm {name:?}"))
}

/// Runs the single-source shortest path algorithm called `name` from `s`.
fn single_source<G>(g: &G, name: &str, s: &usize) -> PyResult<SingleSourcePaths<usize, G::Edge>>
where
    G: IncidenceGraph<Vertex = usize>,
{
    match name {
        "dijkstra" => Dijkstra::new(g).single_source(s),
        "bidirectional_dijkstra" => BidirectionalDijkstraShortestPath::new(g).single_source(s),
        "bfs" => BfsShortestPath::new(g).single_source(s),
        "delta_stepping" => DeltaStepping::new(g).single_source(s),
        "bellman_ford" => BellmanFord::new(g).single_source(s),
        "floyd_warshall" => FloydWarshallShortestPaths::new(g).and_then(|a| a.single_source(s)),
        "johnson" => JohnsonShortestPaths::new(g).and_then(|a| a.single_source(s)),
        "delta_stepping_parallel" => ParallelDeltaSteppingShortestPath::new(g).single_source(s),
        other => return Err(unknown_algorithm(other)),
    }
    .map_err(graph_error)
}

/// Shortest path from ``source`` to ``target``, or ``None`` if unreachable.
///
/// ``algorithm`` is ``"dijkstra"`` (default), ``"bidirectional_dijkstra"``, ``"delta_stepping"``,
/// ``"delta_stepping_parallel"`` (all for non-negative weights), ``"bfs"`` (fewest edges, weights ignored), or ``"bellman_ford"``,
/// ``"floyd_warshall"`` and ``"johnson"`` (these allow negative weights; a negative cycle raises
/// :class:`GraphError`).
#[pyfunction]
#[pyo3(signature = (graph, source, target, algorithm="dijkstra"))]
fn shortest_path(
    py: Python<'_>,
    graph: &Bound<'_, PyAny>,
    source: Bound<'_, PyAny>,
    target: Bound<'_, PyAny>,
    algorithm: &str,
) -> PyResult<Option<GraphPath>> {
    dispatch!(graph, |g, lab| {
        let (s, t) = (lab.vertex_id(py, &source)?, lab.vertex_id(py, &target)?);
        if !g.contains_vertex(&s) || !g.contains_vertex(&t) {
            return Err(GraphError::new_err("vertex not found in graph"));
        }
        let walk = single_source(g, algorithm, &s)?.path(&t);
        Ok(walk.map(|w| {
            GraphPath::new(
                lab.vertices(py, w.vertex_list().iter().copied()),
                lab.edges(py, w.edge_list().iter().map(|e| e.eid())),
                w.weight(),
            )
        }))
    })
}

/// Distances from ``source`` to every reachable vertex, as a ``{vertex: distance}`` dict.
/// See :func:`shortest_path` for ``algorithm``.
#[pyfunction]
#[pyo3(signature = (graph, source, algorithm="dijkstra"))]
fn single_source_distances<'py>(
    py: Python<'py>,
    graph: &Bound<'py, PyAny>,
    source: Bound<'py, PyAny>,
    algorithm: &str,
) -> PyResult<Bound<'py, PyDict>> {
    dispatch!(graph, |g, lab| {
        let s = lab.vertex_id(py, &source)?;
        let paths = single_source(g, algorithm, &s)?;
        lab.vertex_dict(py, paths.dist.iter().map(|(id, d)| (*id, *d)))
    })
}

/// The shortest path to every reachable vertex from ``source`` as ``{vertex: GraphPath}``.
/// See :func:`shortest_path` for ``algorithm``.
#[pyfunction]
#[pyo3(signature = (graph, source, algorithm="dijkstra"))]
fn single_source_paths<'py>(
    py: Python<'py>,
    graph: &Bound<'py, PyAny>,
    source: Bound<'py, PyAny>,
    algorithm: &str,
) -> PyResult<Bound<'py, PyDict>> {
    dispatch!(graph, |g, lab| {
        let s = lab.vertex_id(py, &source)?;
        let paths = single_source(g, algorithm, &s)?;
        let out = PyDict::new(py);
        for t in paths.dist.keys() {
            if let Some(w) = paths.path(t) {
                out.set_item(lab.vertex_obj(py, *t), lab.path(py, &w))?;
            }
        }
        Ok(out)
    })
}

/// All-pairs shortest path distances as ``{source: {target: distance}}`` (reachable pairs only).
/// ``algorithm`` is ``"floyd_warshall"`` (default) or ``"johnson"``.
#[pyfunction]
#[pyo3(signature = (graph, algorithm="floyd_warshall"))]
fn all_pairs_distances<'py>(
    py: Python<'py>,
    graph: &Bound<'py, PyAny>,
    algorithm: &str,
) -> PyResult<Bound<'py, PyDict>> {
    dispatch!(graph, |g, lab| {
        let paths = match algorithm {
            "floyd_warshall" => FloydWarshallShortestPaths::new(g)
                .map_err(graph_error)?
                .all_pairs()
                .clone(),
            "johnson" => JohnsonShortestPaths::new(g)
                .map_err(graph_error)?
                .all_pairs()
                .clone(),
            other => return Err(unknown_algorithm(other)),
        };
        let out = PyDict::new(py);
        for s in g.vertices_cloned() {
            let row = paths
                .from_source(&s)
                .map(|p| p.dist.clone())
                .unwrap_or_default();
            out.set_item(lab.vertex_obj(py, s), lab.vertex_dict(py, row)?)?;
        }
        Ok(out)
    })
}

pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(shortest_path, m)?)?;
    m.add_function(wrap_pyfunction!(single_source_distances, m)?)?;
    m.add_function(wrap_pyfunction!(single_source_paths, m)?)?;
    m.add_function(wrap_pyfunction!(all_pairs_distances, m)?)?;
    Ok(())
}
