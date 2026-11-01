//! Structural properties: bipartiteness, acyclicity and topological order.

use jgrapht::alg::partition;
use jgrapht::alg::planar::{BoyerMyrvoldPlanarityInspector, PlanarityResult};
use jgrapht::graph::props;
use jgrapht::traverse::topological_sort as rust_topological_sort;
use pyo3::prelude::*;

use crate::labels::{EdgeId, dispatch, dispatch_directed};
use jgrapht::GraphExt as _;
use pyo3::types::PyDict;

/// Whether the graph is bipartite (edge direction ignored).
#[pyfunction]
fn is_bipartite(graph: &Bound<'_, PyAny>) -> PyResult<bool> {
    dispatch!(graph, |g, _lab| Ok(partition::is_bipartite(g)))
}

/// The two sides of a bipartition as ``(left, right)``, or ``None`` if not bipartite.
#[pyfunction]
#[allow(clippy::type_complexity)]
fn bipartite_partition(
    py: Python<'_>,
    graph: &Bound<'_, PyAny>,
) -> PyResult<Option<(Vec<Py<PyAny>>, Vec<Py<PyAny>>)>> {
    dispatch!(graph, |g, lab| {
        Ok(partition::bipartite_partition(g)
            .map(|(a, b)| (lab.vertices(py, a), lab.vertices(py, b))))
    })
}

/// Whether a directed graph has no cycles.
#[pyfunction]
fn is_dag(graph: &Bound<'_, PyAny>) -> PyResult<bool> {
    dispatch_directed!(graph, |g, _lab| Ok(props::is_dag(g)))
}

/// A topological ordering of a directed graph, or ``None`` if it contains a cycle.
#[pyfunction]
fn topological_sort(py: Python<'_>, graph: &Bound<'_, PyAny>) -> PyResult<Option<Vec<Py<PyAny>>>> {
    dispatch_directed!(graph, |g, lab| {
        Ok(rust_topological_sort(g).map(|order| lab.vertices(py, order)))
    })
}

/// Whether the graph is planar (Boyer-Myrvold), edge direction ignored.
#[pyfunction]
fn is_planar(graph: &Bound<'_, PyAny>) -> PyResult<bool> {
    dispatch!(graph, |g, _lab| Ok(
        BoyerMyrvoldPlanarityInspector::new(g).is_planar()
    ))
}

/// A planar embedding as ``{vertex: [edges in clockwise order around it]}``, or ``None`` if the
/// graph is not planar.
#[pyfunction]
fn planar_embedding<'py>(
    py: Python<'py>,
    graph: &Bound<'py, PyAny>,
) -> PyResult<Option<Bound<'py, PyDict>>> {
    dispatch!(graph, |g, lab| {
        let PlanarityResult::Planar(embedding) = BoyerMyrvoldPlanarityInspector::new(g).planarity()
        else {
            return Ok(None);
        };
        let out = PyDict::new(py);
        for (v, edges) in embedding.iter() {
            out.set_item(
                lab.vertex_obj(py, *v),
                lab.edges(py, edges.iter().map(|e| e.eid())),
            )?;
        }
        Ok(Some(out))
    })
}

/// A subdivision of K5 or K3,3 contained in a non-planar graph, as ``(vertices, edges)``, or
/// ``None`` if the graph is planar.
#[pyfunction]
#[allow(clippy::type_complexity)]
fn kuratowski_subdivision(
    py: Python<'_>,
    graph: &Bound<'_, PyAny>,
) -> PyResult<Option<(Vec<Py<PyAny>>, Vec<Py<PyAny>>)>> {
    dispatch!(graph, |g, lab| {
        let PlanarityResult::NonPlanar(sub) = BoyerMyrvoldPlanarityInspector::new(g).planarity()
        else {
            return Ok(None);
        };
        Ok(Some((
            lab.vertices(py, sub.vertices_cloned()),
            lab.edges(py, sub.edges_cloned().map(|e| e.eid())),
        )))
    })
}

pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(is_planar, m)?)?;
    m.add_function(wrap_pyfunction!(planar_embedding, m)?)?;
    m.add_function(wrap_pyfunction!(kuratowski_subdivision, m)?)?;
    m.add_function(wrap_pyfunction!(is_bipartite, m)?)?;
    m.add_function(wrap_pyfunction!(bipartite_partition, m)?)?;
    m.add_function(wrap_pyfunction!(is_dag, m)?)?;
    m.add_function(wrap_pyfunction!(topological_sort, m)?)?;
    Ok(())
}
