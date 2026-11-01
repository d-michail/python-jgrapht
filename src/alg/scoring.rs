//! Centrality and clustering scores.

use jgrapht::alg::scoring::{self as sc, ApBetweennessCentrality};
use pyo3::prelude::*;
use pyo3::types::PyDict;

use crate::labels::{EdgeId, dispatch};

/// Degree of each vertex, optionally divided by ``n - 1``.
#[pyfunction]
#[pyo3(signature = (graph, normalize=false))]
fn degree_centrality<'py>(
    py: Python<'py>,
    graph: &Bound<'py, PyAny>,
    normalize: bool,
) -> PyResult<Bound<'py, PyDict>> {
    dispatch!(graph, |g, lab| lab
        .vertex_dict(py, sc::degree_centrality(g, normalize)))
}

/// Closeness centrality of each vertex; ``weighted`` uses edge weights as distances.
#[pyfunction]
#[pyo3(signature = (graph, weighted=false))]
fn closeness_centrality<'py>(
    py: Python<'py>,
    graph: &Bound<'py, PyAny>,
    weighted: bool,
) -> PyResult<Bound<'py, PyDict>> {
    dispatch!(graph, |g, lab| lab
        .vertex_dict(py, sc::closeness_centrality(g, weighted)))
}

/// Harmonic centrality of each vertex; ``weighted`` uses edge weights as distances.
#[pyfunction]
#[pyo3(signature = (graph, weighted=false))]
fn harmonic_centrality<'py>(
    py: Python<'py>,
    graph: &Bound<'py, PyAny>,
    weighted: bool,
) -> PyResult<Bound<'py, PyDict>> {
    dispatch!(graph, |g, lab| lab
        .vertex_dict(py, sc::harmonic_centrality(g, weighted)))
}

/// Betweenness centrality of each vertex (Brandes' algorithm), as floats. With ``weighted`` the
/// shortest paths use the edge weights.
///
/// With ``normalize`` the scores are divided by the number of pairs of other vertices: ordered
/// pairs, ``(n - 1)(n - 2)``, in a directed graph and unordered pairs, ``(n - 1)(n - 2) / 2``, in
/// an undirected one, so a vertex on every shortest path scores 1. This is deliberately not the
/// convention of :func:`exact_betweenness_centrality`, which divides undirected scores by
/// ``(n - 1)(n - 2)`` and therefore gives half of this value.
#[pyfunction]
#[pyo3(signature = (graph, weighted=false, normalize=true))]
fn betweenness_centrality<'py>(
    py: Python<'py>,
    graph: &Bound<'py, PyAny>,
    weighted: bool,
    normalize: bool,
) -> PyResult<Bound<'py, PyDict>> {
    dispatch!(graph, |g, lab| {
        lab.vertex_dict(
            py,
            sc::betweenness_centrality(g, weighted, normalize).vertices,
        )
    })
}

/// Betweenness centrality of each edge (Brandes' algorithm). Undirected scores count each pair of
/// vertices once. ``normalize`` is accepted for symmetry with :func:`betweenness_centrality` but
/// has no effect: edge scores are never normalized.
#[pyfunction]
#[pyo3(signature = (graph, weighted=false, normalize=true))]
fn edge_betweenness_centrality<'py>(
    py: Python<'py>,
    graph: &Bound<'py, PyAny>,
    weighted: bool,
    normalize: bool,
) -> PyResult<Bound<'py, PyDict>> {
    dispatch!(graph, |g, lab| {
        let b = sc::betweenness_centrality(g, weighted, normalize);
        lab.edge_dict(py, b.edges.into_iter().map(|(e, x)| (e.eid(), x)))
    })
}

/// PageRank by power iteration.
#[pyfunction]
#[pyo3(signature = (graph, damping=0.85, max_iterations=100, tolerance=1e-8))]
fn pagerank<'py>(
    py: Python<'py>,
    graph: &Bound<'py, PyAny>,
    damping: f64,
    max_iterations: usize,
    tolerance: f64,
) -> PyResult<Bound<'py, PyDict>> {
    dispatch!(graph, |g, lab| lab.vertex_dict(
        py,
        sc::pagerank(g, damping, max_iterations, tolerance)
    ))
}

/// Eigenvector centrality by power iteration (L2-normalised).
#[pyfunction]
#[pyo3(signature = (graph, max_iterations=100, tolerance=1e-8))]
fn eigenvector_centrality<'py>(
    py: Python<'py>,
    graph: &Bound<'py, PyAny>,
    max_iterations: usize,
    tolerance: f64,
) -> PyResult<Bound<'py, PyDict>> {
    dispatch!(graph, |g, lab| lab.vertex_dict(
        py,
        sc::eigenvector_centrality(g, max_iterations, tolerance)
    ))
}

/// Katz centrality ``x = alpha * A^T x + beta``.
#[pyfunction]
#[pyo3(signature = (graph, alpha=0.1, beta=1.0, max_iterations=100, tolerance=1e-8))]
fn katz_centrality<'py>(
    py: Python<'py>,
    graph: &Bound<'py, PyAny>,
    alpha: f64,
    beta: f64,
    max_iterations: usize,
    tolerance: f64,
) -> PyResult<Bound<'py, PyDict>> {
    dispatch!(graph, |g, lab| {
        lab.vertex_dict(
            py,
            sc::katz_centrality(g, alpha, beta, max_iterations, tolerance),
        )
    })
}

/// Core number (k-core index) of each vertex.
#[pyfunction]
fn coreness<'py>(py: Python<'py>, graph: &Bound<'py, PyAny>) -> PyResult<Bound<'py, PyDict>> {
    dispatch!(graph, |g, lab| lab.vertex_dict(py, sc::coreness(g)))
}

/// Local clustering coefficient of each vertex.
#[pyfunction]
fn local_clustering_coefficients<'py>(
    py: Python<'py>,
    graph: &Bound<'py, PyAny>,
) -> PyResult<Bound<'py, PyDict>> {
    dispatch!(graph, |g, lab| lab
        .vertex_dict(py, sc::local_clustering_coefficients(g)))
}

/// Average of the local clustering coefficients.
#[pyfunction]
fn average_clustering_coefficient(graph: &Bound<'_, PyAny>) -> PyResult<f64> {
    dispatch!(graph, |g, _lab| Ok(sc::average_clustering_coefficient(g)))
}

/// Global clustering coefficient (transitivity).
#[pyfunction]
fn global_clustering_coefficient(graph: &Bound<'_, PyAny>) -> PyResult<f64> {
    dispatch!(graph, |g, _lab| Ok(sc::global_clustering_coefficient(g)))
}

/// Number of triangles.
#[pyfunction]
fn count_triangles(graph: &Bound<'_, PyAny>) -> PyResult<usize> {
    dispatch!(graph, |g, _lab| Ok(sc::count_triangles(g)))
}

/// Betweenness centrality of each vertex computed exactly in arbitrary-precision decimal
/// arithmetic, as ``{vertex: decimal.Decimal}``. ``precision`` is the number of significant
/// digits (default: unlimited, which raises :class:`GraphError` if some score has a
/// non-terminating decimal expansion). With ``normalize`` the scores are divided by
/// ``(n - 1)(n - 2)``; for undirected graphs this is half the normalization of
/// :func:`betweenness_centrality`, so the maximum possible score is 1/2 rather than 1.
#[pyfunction]
#[pyo3(signature = (graph, normalize=false, precision=None))]
fn exact_betweenness_centrality<'py>(
    py: Python<'py>,
    graph: &Bound<'py, PyAny>,
    normalize: bool,
    precision: Option<usize>,
) -> PyResult<Bound<'py, PyDict>> {
    let decimal = py.import("decimal")?.getattr("Decimal")?;
    dispatch!(graph, |g, lab| {
        let precision = precision.unwrap_or(sc::APFLOAT_INFINITE_PRECISION);
        let scores = ApBetweennessCentrality::with_precision(g, normalize, precision)
            .map_err(crate::error::graph_error)?;
        let out = PyDict::new(py);
        for (v, score) in scores.scores() {
            out.set_item(lab.vertex_obj(py, *v), decimal.call1((score.to_string(),))?)?;
        }
        Ok(out)
    })
}

pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(exact_betweenness_centrality, m)?)?;
    m.add_function(wrap_pyfunction!(degree_centrality, m)?)?;
    m.add_function(wrap_pyfunction!(closeness_centrality, m)?)?;
    m.add_function(wrap_pyfunction!(harmonic_centrality, m)?)?;
    m.add_function(wrap_pyfunction!(betweenness_centrality, m)?)?;
    m.add_function(wrap_pyfunction!(edge_betweenness_centrality, m)?)?;
    m.add_function(wrap_pyfunction!(pagerank, m)?)?;
    m.add_function(wrap_pyfunction!(eigenvector_centrality, m)?)?;
    m.add_function(wrap_pyfunction!(katz_centrality, m)?)?;
    m.add_function(wrap_pyfunction!(coreness, m)?)?;
    m.add_function(wrap_pyfunction!(local_clustering_coefficients, m)?)?;
    m.add_function(wrap_pyfunction!(average_clustering_coefficient, m)?)?;
    m.add_function(wrap_pyfunction!(global_clustering_coefficient, m)?)?;
    m.add_function(wrap_pyfunction!(count_triangles, m)?)?;
    Ok(())
}
