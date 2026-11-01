//! Distance-based graph metrics.

use jgrapht::alg::metrics::{GraphMeasurer, girth as rust_girth};
use pyo3::prelude::*;
use pyo3::types::PyDict;

use crate::error::graph_error;
use crate::labels::dispatch;

/// Diameter (largest eccentricity), or ``None`` if the graph is not (strongly) connected.
/// Edge weights are distances.
#[pyfunction]
fn diameter(graph: &Bound<'_, PyAny>) -> PyResult<Option<f64>> {
    dispatch!(graph, |g, _lab| Ok(GraphMeasurer::new(g)
        .map_err(graph_error)?
        .diameter()))
}

/// Radius (smallest eccentricity), or ``None`` if the graph is not (strongly) connected.
#[pyfunction]
fn radius(graph: &Bound<'_, PyAny>) -> PyResult<Option<f64>> {
    dispatch!(graph, |g, _lab| Ok(GraphMeasurer::new(g)
        .map_err(graph_error)?
        .radius()))
}

/// Eccentricity of every vertex as ``{vertex: eccentricity}``.
#[pyfunction]
fn eccentricities<'py>(py: Python<'py>, graph: &Bound<'py, PyAny>) -> PyResult<Bound<'py, PyDict>> {
    dispatch!(graph, |g, lab| {
        let m = GraphMeasurer::new(g).map_err(graph_error)?;
        lab.vertex_dict(py, m.vertex_eccentricity_map())
    })
}

/// Vertices whose eccentricity equals the radius.
#[pyfunction]
fn graph_center(py: Python<'_>, graph: &Bound<'_, PyAny>) -> PyResult<Vec<Py<PyAny>>> {
    dispatch!(graph, |g, lab| {
        Ok(lab.vertices(
            py,
            GraphMeasurer::new(g).map_err(graph_error)?.graph_center(),
        ))
    })
}

/// Vertices whose eccentricity equals the diameter.
#[pyfunction]
fn graph_periphery(py: Python<'_>, graph: &Bound<'_, PyAny>) -> PyResult<Vec<Py<PyAny>>> {
    dispatch!(graph, |g, lab| {
        Ok(lab.vertices(
            py,
            GraphMeasurer::new(g)
                .map_err(graph_error)?
                .graph_periphery(),
        ))
    })
}

/// Vertices ``u`` with some ``v`` such that ``d(u, v) = ecc(u) = ecc(v)``.
#[pyfunction]
fn graph_pseudo_periphery(py: Python<'_>, graph: &Bound<'_, PyAny>) -> PyResult<Vec<Py<PyAny>>> {
    dispatch!(graph, |g, lab| {
        Ok(lab.vertices(
            py,
            GraphMeasurer::new(g)
                .map_err(graph_error)?
                .graph_pseudo_periphery(),
        ))
    })
}

/// Length of the shortest cycle, or ``None`` for an acyclic graph.
#[pyfunction]
fn girth(graph: &Bound<'_, PyAny>) -> PyResult<Option<usize>> {
    dispatch!(graph, |g, _lab| Ok(rust_girth(g)))
}

pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(diameter, m)?)?;
    m.add_function(wrap_pyfunction!(radius, m)?)?;
    m.add_function(wrap_pyfunction!(eccentricities, m)?)?;
    m.add_function(wrap_pyfunction!(graph_center, m)?)?;
    m.add_function(wrap_pyfunction!(graph_periphery, m)?)?;
    m.add_function(wrap_pyfunction!(graph_pseudo_periphery, m)?)?;
    m.add_function(wrap_pyfunction!(girth, m)?)?;
    Ok(())
}
