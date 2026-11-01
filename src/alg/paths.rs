//! Path enumeration: k shortest paths, disjoint paths, all directed paths, path counting.

use std::cell::RefCell;

use jgrapht::GraphWalk;
use jgrapht::alg::shortestpath::{
    AllDirectedPaths, BhandariKDisjointShortestPaths, BoundedPrunedYenKShortestPath,
    DagAllPathsCounter, EppsteinKShortestPath, SuurballeKDisjointShortestPaths, YenKShortestPath,
};
use pyo3::prelude::*;
use pyo3::types::PyInt;

use crate::error::{GraphError, graph_error};
use crate::graph::GraphPath;
use crate::labels::{EdgeId, Labels, dispatch, dispatch_directed};

/// Wraps a Python predicate ``validator(partial_path, edge) -> bool`` as a path validator. The
/// first exception it raises is remembered in ``failure`` and every later call accepts the edge.
fn validator<'a, E: EdgeId>(
    py: Python<'a>,
    lab: &'a Labels<'a>,
    f: &'a Bound<'a, PyAny>,
    failure: &'a RefCell<Option<PyErr>>,
) -> impl Fn(&GraphWalk<usize, E>, &E) -> bool + Clone + 'a {
    move |partial: &GraphWalk<usize, E>, edge: &E| {
        if failure.borrow().is_some() {
            return true;
        }
        let call = Py::new(py, lab.path(py, partial))
            .and_then(|p| f.call1((p, lab.edge_obj(py, edge.eid()))))
            .and_then(|r| r.is_truthy());
        call.unwrap_or_else(|e| {
            *failure.borrow_mut() = Some(e);
            true
        })
    }
}

/// The ``k`` shortest loopless paths from ``source`` to ``target`` in order of weight (fewer if
/// there are not that many).
///
/// ``algorithm`` is ``"yen"`` (default), ``"bounded_pruned_yen"`` (Yen with pruning and bounds,
/// faster on large graphs; it distinguishes paths by their vertex sequence, so parallel edges
/// give no extra paths) or ``"eppstein"``, which enumerates walks and requires a *simple
/// directed* :class:`Graph` (so it rejects a :class:`SparseGraph` and graphs allowing parallel
/// edges or self-loops). ``path_validator(partial_path, edge)`` (``"yen"`` only) may veto
/// extending a partial :class:`GraphPath` by an edge; an exception it raises is re-raised.
#[pyfunction]
#[pyo3(signature = (graph, source, target, k, algorithm="yen", path_validator=None))]
fn k_shortest_paths(
    py: Python<'_>,
    graph: &Bound<'_, PyAny>,
    source: Bound<'_, PyAny>,
    target: Bound<'_, PyAny>,
    k: usize,
    algorithm: &str,
    path_validator: Option<Bound<'_, PyAny>>,
) -> PyResult<Vec<GraphPath>> {
    if path_validator.is_some() && algorithm != "yen" {
        return Err(GraphError::new_err(
            "path_validator is only supported by the \"yen\" algorithm",
        ));
    }
    dispatch!(graph, |g, lab| {
        let (s, t) = (lab.vertex_id(py, &source)?, lab.vertex_id(py, &target)?);
        let failure: RefCell<Option<PyErr>> = RefCell::new(None);
        let walks = match algorithm {
            "yen" => match &path_validator {
                Some(f) => YenKShortestPath::with_validator(g, validator(py, &lab, f, &failure))
                    .paths(&s, &t, k),
                None => YenKShortestPath::new(g).paths(&s, &t, k),
            },
            "bounded_pruned_yen" => BoundedPrunedYenKShortestPath::new(g).paths(&s, &t, k),
            "eppstein" => EppsteinKShortestPath::new(g).paths(&s, &t, k),
            other => return Err(GraphError::new_err(format!("unknown algorithm {other:?}"))),
        };
        let first_error = failure.borrow_mut().take();
        if let Some(e) = first_error {
            return Err(e);
        }
        Ok(walks
            .map_err(graph_error)?
            .iter()
            .map(|w| lab.path(py, w))
            .collect())
    })
}

/// Up to ``k`` edge-disjoint shortest paths in a directed graph, by increasing weight.
/// ``algorithm`` is ``"suurballe"`` (default; non-negative weights) or ``"bhandari"`` (allows
/// negative weights).
#[pyfunction]
#[pyo3(signature = (graph, source, target, k, algorithm="suurballe"))]
fn k_disjoint_shortest_paths(
    py: Python<'_>,
    graph: &Bound<'_, PyAny>,
    source: Bound<'_, PyAny>,
    target: Bound<'_, PyAny>,
    k: usize,
    algorithm: &str,
) -> PyResult<Vec<GraphPath>> {
    dispatch_directed!(graph, |g, lab| {
        let (s, t) = (lab.vertex_id(py, &source)?, lab.vertex_id(py, &target)?);
        let walks = match algorithm {
            "suurballe" => SuurballeKDisjointShortestPaths::new(g).paths(&s, &t, k),
            "bhandari" => BhandariKDisjointShortestPaths::new(g).paths(&s, &t, k),
            other => return Err(GraphError::new_err(format!("unknown algorithm {other:?}"))),
        }
        .map_err(graph_error)?;
        Ok(walks.iter().map(|w| lab.path(py, w)).collect())
    })
}

/// All paths from ``source`` to ``target`` in a directed graph. With ``simple_only`` (default)
/// no vertex repeats; otherwise ``max_length`` (number of edges) is required to bound the walks.
/// ``path_validator(partial_path, edge)`` may veto extending a partial :class:`GraphPath` by an
/// edge; an exception it raises is re-raised.
#[pyfunction]
#[pyo3(signature = (graph, source, target, simple_only=true, max_length=None, path_validator=None))]
fn all_directed_paths(
    py: Python<'_>,
    graph: &Bound<'_, PyAny>,
    source: Bound<'_, PyAny>,
    target: Bound<'_, PyAny>,
    simple_only: bool,
    max_length: Option<usize>,
    path_validator: Option<Bound<'_, PyAny>>,
) -> PyResult<Vec<GraphPath>> {
    dispatch_directed!(graph, |g, lab| {
        let (s, t) = (lab.vertex_id(py, &source)?, lab.vertex_id(py, &target)?);
        let failure: RefCell<Option<PyErr>> = RefCell::new(None);
        let walks = match &path_validator {
            Some(f) => AllDirectedPaths::with_validator(g, validator(py, &lab, f, &failure))
                .all_paths(&s, &t, simple_only, max_length),
            None => AllDirectedPaths::new(g).all_paths(&s, &t, simple_only, max_length),
        };
        let first_error = failure.borrow_mut().take();
        if let Some(e) = first_error {
            return Err(e);
        }
        Ok(walks
            .map_err(graph_error)?
            .iter()
            .map(|w| lab.path(py, w))
            .collect())
    })
}

/// Number of directed paths from ``source`` to ``target`` in a DAG, as an arbitrary-size int.
#[pyfunction]
fn count_dag_paths<'py>(
    py: Python<'py>,
    graph: &Bound<'py, PyAny>,
    source: Bound<'py, PyAny>,
    target: Bound<'py, PyAny>,
) -> PyResult<Bound<'py, PyAny>> {
    dispatch_directed!(graph, |g, lab| {
        let (s, t) = (lab.vertex_id(py, &source)?, lab.vertex_id(py, &target)?);
        let n = DagAllPathsCounter::count_all_paths(g, &s, &t).map_err(graph_error)?;
        py.get_type::<PyInt>().call1((n.to_string(),))
    })
}

pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(k_shortest_paths, m)?)?;
    m.add_function(wrap_pyfunction!(k_disjoint_shortest_paths, m)?)?;
    m.add_function(wrap_pyfunction!(all_directed_paths, m)?)?;
    m.add_function(wrap_pyfunction!(count_dag_paths, m)?)?;
    Ok(())
}
