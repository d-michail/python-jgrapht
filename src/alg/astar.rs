//! A* search with a Python heuristic callback.

use std::cell::RefCell;

use jgrapht::alg::shortestpath::AStar;
use pyo3::prelude::*;

use crate::error::graph_error;
use crate::graph::GraphPath;
use crate::labels::{EdgeId, dispatch};

/// A* shortest path from ``source`` to ``target``, or ``None`` if unreachable.
///
/// ``heuristic(vertex, target)`` must return a non-negative estimate of the remaining distance
/// that never overestimates it. If omitted the estimate is always ``0`` (Dijkstra). An exception
/// raised by the heuristic aborts the search and is re-raised.
#[pyfunction]
#[pyo3(signature = (graph, source, target, heuristic=None))]
fn astar_shortest_path(
    py: Python<'_>,
    graph: &Bound<'_, PyAny>,
    source: Bound<'_, PyAny>,
    target: Bound<'_, PyAny>,
    heuristic: Option<Bound<'_, PyAny>>,
) -> PyResult<Option<GraphPath>> {
    dispatch!(graph, |g, lab| {
        let (s, t) = (lab.vertex_id(py, &source)?, lab.vertex_id(py, &target)?);
        let failure: RefCell<Option<PyErr>> = RefCell::new(None);
        let estimate = |v: &usize, t: &usize| -> f64 {
            let Some(h) = &heuristic else { return 0.0 };
            if failure.borrow().is_some() {
                return 0.0;
            }
            let call = h
                .call1((lab.vertex_obj(py, *v), lab.vertex_obj(py, *t)))
                .and_then(|r| r.extract::<f64>());
            match call {
                Ok(x) => x,
                Err(e) => {
                    *failure.borrow_mut() = Some(e);
                    0.0
                }
            }
        };
        let walk = AStar::new(g, estimate).path(&s, &t);
        if let Some(e) = failure.into_inner() {
            return Err(e);
        }
        Ok(walk.map_err(graph_error)?.map(|w| {
            GraphPath::new(
                lab.vertices(py, w.vertex_list().iter().copied()),
                lab.edges(py, w.edge_list().iter().map(|e| e.eid())),
                w.weight(),
            )
        }))
    })
}

pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(astar_shortest_path, m)?)?;
    Ok(())
}
