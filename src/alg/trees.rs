//! Spanning trees, arborescences, Steiner trees and spanners.

use jgrapht::alg::decomposition::{
    EliminationHeuristic, tree_decomposition as rust_tree_decomposition, treewidth_upper_bound,
};
use jgrapht::alg::interfaces::{AllLowestCommonAncestors, LowestCommonAncestorAlgorithm};
use jgrapht::alg::lca::{
    BinaryLiftingLcaFinder, EulerTourRmqLcaFinder, HeavyPathLcaFinder, NaiveLcaFinder,
    TarjanLcaFinder,
};
use jgrapht::alg::spanner::greedy_spanner;
use jgrapht::alg::spanning::{self, maximum_arborescence, minimum_arborescence};
use jgrapht::alg::steiner::{dreyfus_wagner_weight, kmb_steiner_tree};
use pyo3::prelude::*;

use crate::error::{GraphError, graph_error};
use crate::labels::{EdgeId, dispatch, dispatch_directed};

/// Minimum spanning forest as ``(total_weight, edges)``.
/// ``algorithm`` is ``"kruskal"``, ``"prim"`` or ``"boruvka"``.
#[pyfunction]
#[pyo3(signature = (graph, algorithm="kruskal"))]
fn minimum_spanning_tree(
    py: Python<'_>,
    graph: &Bound<'_, PyAny>,
    algorithm: &str,
) -> PyResult<(f64, Vec<Py<PyAny>>)> {
    dispatch!(graph, |g, lab| {
        let tree = match algorithm {
            "kruskal" => spanning::kruskal(g),
            "prim" => spanning::prim(g),
            "boruvka" => spanning::boruvka(g),
            other => return Err(GraphError::new_err(format!("unknown algorithm {other:?}"))),
        };
        Ok((
            tree.weight,
            lab.edges(py, tree.edges.iter().map(|e| e.eid())),
        ))
    })
}

/// The minimum weight spanning arborescence of a directed graph rooted at ``root``
/// (Chu-Liu/Edmonds) as ``(weight, edges)``. Raises :class:`GraphError` if some vertex is
/// unreachable from the root.
#[pyfunction]
fn minimum_arborescence_tree(
    py: Python<'_>,
    graph: &Bound<'_, PyAny>,
    root: Bound<'_, PyAny>,
) -> PyResult<(f64, Vec<Py<PyAny>>)> {
    dispatch_directed!(graph, |g, lab| {
        let r = lab.vertex_id(py, &root)?;
        let t = minimum_arborescence(g, &r).map_err(graph_error)?;
        Ok((t.weight, lab.edges(py, t.edges.iter().map(|e| e.eid()))))
    })
}

/// The maximum weight spanning arborescence of a directed graph rooted at ``root``.
#[pyfunction]
fn maximum_arborescence_tree(
    py: Python<'_>,
    graph: &Bound<'_, PyAny>,
    root: Bound<'_, PyAny>,
) -> PyResult<(f64, Vec<Py<PyAny>>)> {
    dispatch_directed!(graph, |g, lab| {
        let r = lab.vertex_id(py, &root)?;
        let t = maximum_arborescence(g, &r).map_err(graph_error)?;
        Ok((t.weight, lab.edges(py, t.edges.iter().map(|e| e.eid()))))
    })
}

/// An approximate minimum Steiner tree (Kou-Markowsky-Berman, 2-approximation) connecting the
/// ``terminals`` in an undirected graph, as ``(weight, edges)``.
#[pyfunction]
fn steiner_tree(
    py: Python<'_>,
    graph: &Bound<'_, PyAny>,
    terminals: Vec<Bound<'_, PyAny>>,
) -> PyResult<(f64, Vec<Py<PyAny>>)> {
    dispatch!(graph, |g, lab| {
        let ts: Vec<usize> = terminals
            .iter()
            .map(|v| lab.vertex_id(py, v))
            .collect::<PyResult<_>>()?;
        let t = kmb_steiner_tree(g, &ts).map_err(graph_error)?;
        Ok((t.weight, lab.edges(py, t.edges.iter().map(|e| e.eid()))))
    })
}

/// The exact weight of a minimum Steiner tree (Dreyfus-Wagner; at most 16 terminals).
#[pyfunction]
fn steiner_tree_weight(
    py: Python<'_>,
    graph: &Bound<'_, PyAny>,
    terminals: Vec<Bound<'_, PyAny>>,
) -> PyResult<f64> {
    dispatch!(graph, |g, lab| {
        let ts: Vec<usize> = terminals
            .iter()
            .map(|v| lab.vertex_id(py, v))
            .collect::<PyResult<_>>()?;
        dreyfus_wagner_weight(g, &ts).map_err(graph_error)
    })
}

/// A greedy ``(2k - 1)``-spanner of an undirected graph: a sparse subgraph in which every
/// distance is stretched by at most ``2k - 1``. Returns the kept edges.
#[pyfunction]
fn greedy_multiplicative_spanner(
    py: Python<'_>,
    graph: &Bound<'_, PyAny>,
    k: usize,
) -> PyResult<Vec<Py<PyAny>>> {
    dispatch!(graph, |g, lab| {
        let edges = greedy_spanner(g, k).map_err(graph_error)?;
        Ok(lab.edges(py, edges.iter().map(|e| e.eid())))
    })
}

/// The lowest common ancestor of each ``(a, b)`` pair in the tree (or forest) rooted at
/// ``root`` (one vertex, or a ``list`` of roots for a forest), in the same order; ``None`` for a
/// pair without a common ancestor (for example in different trees).
///
/// ``algorithm`` is ``"binary_lifting"`` (default), ``"euler_tour"`` (Euler tour with range
/// minimum queries), ``"heavy_path"``, ``"tarjan"`` (offline) or ``"naive"`` (for directed
/// acyclic graphs; ignores ``root`` and returns one lowest common ancestor, see
/// :func:`all_lowest_common_ancestors` for all of them).
#[pyfunction]
#[pyo3(signature = (graph, root, pairs, algorithm="binary_lifting"))]
fn lowest_common_ancestors(
    py: Python<'_>,
    graph: &Bound<'_, PyAny>,
    root: Bound<'_, PyAny>,
    pairs: Vec<(Bound<'_, PyAny>, Bound<'_, PyAny>)>,
    algorithm: &str,
) -> PyResult<Vec<Option<Py<PyAny>>>> {
    if algorithm == "naive" {
        return dispatch_directed!(graph, |g, lab| {
            let queries = lca_queries(py, &lab, &pairs)?;
            let finder = NaiveLcaFinder::new(g).map_err(graph_error)?;
            let found = finder.batch_lca(&queries).map_err(graph_error)?;
            Ok(found
                .into_iter()
                .map(|v| v.map(|v| lab.vertex_obj(py, v)))
                .collect())
        });
    }
    dispatch!(graph, |g, lab| {
        let roots: Vec<usize> = match root.cast::<pyo3::types::PyList>() {
            Ok(list) => list
                .iter()
                .map(|r| lab.vertex_id(py, &r))
                .collect::<PyResult<_>>()?,
            Err(_) => vec![lab.vertex_id(py, &root)?],
        };
        let queries = lca_queries(py, &lab, &pairs)?;
        let found =
            match algorithm {
                "binary_lifting" => BinaryLiftingLcaFinder::with_roots(g, &roots)
                    .and_then(|f| f.batch_lca(&queries)),
                "euler_tour" => {
                    EulerTourRmqLcaFinder::with_roots(g, &roots).and_then(|f| f.batch_lca(&queries))
                }
                "heavy_path" => HeavyPathLcaFinder::with_roots(g, roots.clone())
                    .and_then(|f| f.batch_lca(&queries)),
                "tarjan" => TarjanLcaFinder::with_roots(g, roots.clone())
                    .and_then(|f| f.batch_lca(&queries)),
                other => return Err(GraphError::new_err(format!("unknown algorithm {other:?}"))),
            }
            .map_err(graph_error)?;
        Ok(found
            .into_iter()
            .map(|v| v.map(|v| lab.vertex_obj(py, v)))
            .collect())
    })
}

fn lca_queries(
    py: Python<'_>,
    lab: &crate::labels::Labels<'_>,
    pairs: &[(Bound<'_, PyAny>, Bound<'_, PyAny>)],
) -> PyResult<Vec<(usize, usize)>> {
    pairs
        .iter()
        .map(|(a, b)| Ok((lab.vertex_id(py, a)?, lab.vertex_id(py, b)?)))
        .collect()
}

/// All lowest common ancestors of ``a`` and ``b`` in a directed acyclic graph (there can be
/// several), as a list.
#[pyfunction]
fn all_lowest_common_ancestors(
    py: Python<'_>,
    graph: &Bound<'_, PyAny>,
    a: Bound<'_, PyAny>,
    b: Bound<'_, PyAny>,
) -> PyResult<Vec<Py<PyAny>>> {
    dispatch_directed!(graph, |g, lab| {
        let (x, y) = (lab.vertex_id(py, &a)?, lab.vertex_id(py, &b)?);
        let set = NaiveLcaFinder::new(g)
            .and_then(|f| f.lca_set(&x, &y))
            .map_err(graph_error)?;
        let mut ids: Vec<usize> = set.into_iter().collect();
        ids.sort_unstable();
        Ok(lab.vertices(py, ids))
    })
}

/// A tree decomposition of the graph (edge direction ignored) as ``(bags, tree_edges)``: ``bags``
/// are lists of vertices and each tree edge a pair of bag indices. ``heuristic`` chooses the
/// elimination order: ``"min_fill"`` (default) or ``"min_degree"``.
#[pyfunction]
#[pyo3(signature = (graph, heuristic="min_fill"))]
#[allow(clippy::type_complexity)]
fn tree_decomposition(
    py: Python<'_>,
    graph: &Bound<'_, PyAny>,
    heuristic: &str,
) -> PyResult<(Vec<Vec<Py<PyAny>>>, Vec<(usize, usize)>)> {
    let h = match heuristic {
        "min_fill" => EliminationHeuristic::MinFill,
        "min_degree" => EliminationHeuristic::MinDegree,
        other => return Err(GraphError::new_err(format!("unknown heuristic {other:?}"))),
    };
    dispatch!(graph, |g, lab| {
        let d = rust_tree_decomposition(g, h);
        Ok((
            d.bags.into_iter().map(|b| lab.vertices(py, b)).collect(),
            d.tree_edges,
        ))
    })
}

/// An upper bound on the treewidth, from a min-fill tree decomposition.
#[pyfunction]
fn treewidth(graph: &Bound<'_, PyAny>) -> PyResult<usize> {
    dispatch!(graph, |g, _lab| Ok(treewidth_upper_bound(g)))
}

pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(tree_decomposition, m)?)?;
    m.add_function(wrap_pyfunction!(treewidth, m)?)?;
    m.add_function(wrap_pyfunction!(lowest_common_ancestors, m)?)?;
    m.add_function(wrap_pyfunction!(all_lowest_common_ancestors, m)?)?;
    m.add_function(wrap_pyfunction!(minimum_spanning_tree, m)?)?;
    m.add_function(wrap_pyfunction!(minimum_arborescence_tree, m)?)?;
    m.add_function(wrap_pyfunction!(maximum_arborescence_tree, m)?)?;
    m.add_function(wrap_pyfunction!(steiner_tree, m)?)?;
    m.add_function(wrap_pyfunction!(steiner_tree_weight, m)?)?;
    m.add_function(wrap_pyfunction!(greedy_multiplicative_spanner, m)?)?;
    Ok(())
}
