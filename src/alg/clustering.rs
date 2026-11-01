//! Clustering and modularity.

use std::collections::HashSet;

use jgrapht::alg::clustering::{
    GirvanNewmanClustering, GreedyModularityAlgorithm, UndirectedModularityMeasurer,
    k_spanning_tree_clustering as rust_k_spanning_tree,
    label_propagation as rust_label_propagation,
};
use jgrapht::alg::interfaces::ClusteringAlgorithm;
use pyo3::prelude::*;
use rand::SeedableRng;
use rand::rngs::StdRng;

use crate::error::graph_error;
use crate::labels::{dispatch, dispatch_undirected};

fn rng(seed: Option<u64>) -> StdRng {
    match seed {
        Some(s) => StdRng::seed_from_u64(s),
        None => StdRng::from_os_rng(),
    }
}

/// Communities found by label propagation, as lists of vertices. ``seed`` makes it reproducible.
#[pyfunction]
#[pyo3(signature = (graph, max_iterations=100, seed=None))]
fn label_propagation_clustering(
    py: Python<'_>,
    graph: &Bound<'_, PyAny>,
    max_iterations: usize,
    seed: Option<u64>,
) -> PyResult<Vec<Vec<Py<PyAny>>>> {
    dispatch!(graph, |g, lab| {
        let clusters = rust_label_propagation(g, max_iterations, &mut rng(seed));
        Ok(clusters.into_iter().map(|c| lab.vertices(py, c)).collect())
    })
}

/// ``k`` clusters obtained by cutting the ``k - 1`` heaviest edges of a minimum spanning tree.
#[pyfunction]
fn k_spanning_tree_clustering(
    py: Python<'_>,
    graph: &Bound<'_, PyAny>,
    k: usize,
) -> PyResult<Vec<Vec<Py<PyAny>>>> {
    dispatch!(graph, |g, lab| {
        let clusters = rust_k_spanning_tree(g, k).map_err(graph_error)?;
        Ok(clusters.into_iter().map(|c| lab.vertices(py, c)).collect())
    })
}

/// ``k`` clusters from the Girvan-Newman algorithm (repeatedly removing the edge of highest
/// betweenness).
#[pyfunction]
fn girvan_newman_clustering(
    py: Python<'_>,
    graph: &Bound<'_, PyAny>,
    k: usize,
) -> PyResult<Vec<Vec<Py<PyAny>>>> {
    dispatch!(graph, |g, lab| {
        let clustering = GirvanNewmanClustering::new(g, k)
            .and_then(|a| a.clustering())
            .map_err(graph_error)?;
        Ok(clustering
            .iter()
            .map(|c| lab.vertices(py, c.iter().copied()))
            .collect())
    })
}

/// Communities from greedy modularity maximization (Clauset-Newman-Moore).
#[pyfunction]
fn greedy_modularity_clustering(
    py: Python<'_>,
    graph: &Bound<'_, PyAny>,
) -> PyResult<Vec<Vec<Py<PyAny>>>> {
    dispatch!(graph, |g, lab| {
        let clustering = GreedyModularityAlgorithm::new(g)
            .clustering()
            .map_err(graph_error)?;
        Ok(clustering
            .iter()
            .map(|c| lab.vertices(py, c.iter().copied()))
            .collect())
    })
}

/// The modularity of a partition of an undirected graph; ``clusters`` is a list of vertex
/// collections covering every vertex exactly once.
#[pyfunction]
fn modularity(
    py: Python<'_>,
    graph: &Bound<'_, PyAny>,
    clusters: Vec<Vec<Bound<'_, PyAny>>>,
) -> PyResult<f64> {
    dispatch_undirected!(graph, |g, lab| {
        let sets: Vec<HashSet<usize>> = clusters
            .iter()
            .map(|c| {
                c.iter()
                    .map(|v| lab.vertex_id(py, v))
                    .collect::<PyResult<_>>()
            })
            .collect::<PyResult<_>>()?;
        UndirectedModularityMeasurer::new(g)
            .and_then(|m| m.modularity(&sets))
            .map_err(graph_error)
    })
}

pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(label_propagation_clustering, m)?)?;
    m.add_function(wrap_pyfunction!(k_spanning_tree_clustering, m)?)?;
    m.add_function(wrap_pyfunction!(girvan_newman_clustering, m)?)?;
    m.add_function(wrap_pyfunction!(greedy_modularity_clustering, m)?)?;
    m.add_function(wrap_pyfunction!(modularity, m)?)?;
    Ok(())
}
