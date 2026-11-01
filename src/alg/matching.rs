//! Matchings in undirected graphs.

use indexmap::IndexSet;
use jgrapht::GraphExt as _;
use jgrapht::alg::matching::blossom::{
    BlossomVOptions, DualUpdateStrategy, InitializationType, KolmogorovWeightedMatching,
    KolmogorovWeightedPerfectMatching, ObjectiveSense,
};
use jgrapht::alg::matching::{
    DenseEdmonds, GreedyMaximumCardinalityMatching, GreedyWeightedMatching, HopcroftKarp,
    KuhnMunkres, MatchingAlgorithm, MaximumWeightBipartiteMatching, PathGrowingWeightedMatching,
    SparseEdmonds,
};
use jgrapht::alg::partition;
use pyo3::prelude::*;
use pyo3::types::PySet;

use crate::error::{GraphError, graph_error};
use crate::labels::{EdgeId, dispatch_undirected};

/// A matching: a set of edges no two of which share a vertex.
#[pyclass(module = "jgrapht", frozen)]
pub struct Matching {
    edges: Vec<Py<PyAny>>,
    weight: f64,
    matched: Py<PySet>,
    perfect: bool,
}

#[pymethods]
impl Matching {
    /// The matched edges.
    #[getter]
    fn edges(&self, py: Python<'_>) -> Vec<Py<PyAny>> {
        self.edges.iter().map(|e| e.clone_ref(py)).collect()
    }

    /// Total weight of the matched edges. The maximum cardinality algorithms
    /// (:func:`maximum_matching`, :func:`bipartite_maximum_matching`) report the number of
    /// edges instead.
    #[getter]
    fn weight(&self) -> f64 {
        self.weight
    }

    /// The matched vertices, as a set.
    #[getter]
    fn matched_vertices(&self, py: Python<'_>) -> Py<PySet> {
        self.matched.clone_ref(py)
    }

    /// Whether ``v`` is an endpoint of a matched edge.
    fn is_matched(&self, py: Python<'_>, v: Bound<'_, PyAny>) -> PyResult<bool> {
        self.matched.bind(py).contains(v)
    }

    /// Whether every vertex of the graph is matched.
    fn is_perfect(&self) -> bool {
        self.perfect
    }

    fn __len__(&self) -> usize {
        self.edges.len()
    }

    fn __iter__<'py>(&self, py: Python<'py>) -> PyResult<Bound<'py, PyAny>> {
        Ok(pyo3::types::PyList::new(py, self.edges(py))?
            .try_iter()?
            .into_any())
    }

    fn __repr__(&self) -> String {
        format!(
            "Matching(size={}, weight={:?})",
            self.edges.len(),
            self.weight
        )
    }
}

/// Runs `$algo` (an expression yielding a `Result<Matching<usize, E>>`) and converts the result.
macro_rules! run {
    ($py:expr, $g:expr, $lab:expr, $algo:expr) => {{
        let m = $algo.map_err(graph_error)?;
        let matched = PySet::empty($py)?;
        for e in m.edges() {
            let (s, t) = $g.edge_endpoints(e).expect("matched edge is in the graph");
            matched.add($lab.vertex_obj($py, *s))?;
            matched.add($lab.vertex_obj($py, *t))?;
        }
        Ok(Matching {
            edges: $lab.edges($py, m.edges().iter().map(|e| e.eid())),
            weight: m.weight(),
            matched: matched.unbind(),
            perfect: m.is_perfect(),
        })
    }};
}

fn unknown(name: &str) -> PyErr {
    GraphError::new_err(format!("unknown algorithm {name:?}"))
}

/// A maximum cardinality matching in a general undirected graph.
/// ``algorithm`` is ``"sparse_edmonds"`` (default), ``"dense_edmonds"`` (both exact, Edmonds'
/// blossom algorithm) or ``"greedy"`` (a maximal matching, a 1/2-approximation).
#[pyfunction]
#[pyo3(signature = (graph, algorithm="sparse_edmonds"))]
fn maximum_matching(
    py: Python<'_>,
    graph: &Bound<'_, PyAny>,
    algorithm: &str,
) -> PyResult<Matching> {
    dispatch_undirected!(graph, |g, lab| {
        match algorithm {
            "sparse_edmonds" => run!(
                py,
                g,
                lab,
                SparseEdmonds::new(g).and_then(|mut a| a.matching())
            ),
            "dense_edmonds" => run!(
                py,
                g,
                lab,
                DenseEdmonds::new(g).and_then(|mut a| a.matching())
            ),
            "greedy" => run!(
                py,
                g,
                lab,
                GreedyMaximumCardinalityMatching::new(g, true).and_then(|mut a| a.matching())
            ),
            other => Err(unknown(other)),
        }
    })
}

/// Blossom V tuning knobs; see :func:`weighted_matching`.
fn blossom_options(
    initialization: &str,
    dual_update: &str,
    update_duals_before: bool,
    update_duals_after: bool,
) -> PyResult<BlossomVOptions> {
    let init = match initialization {
        "greedy" => InitializationType::Greedy,
        "none" => InitializationType::None,
        "fractional" => InitializationType::Fractional,
        other => {
            return Err(GraphError::new_err(format!(
                "unknown initialization {other:?}"
            )));
        }
    };
    let dual = match dual_update {
        "fixed_delta" => DualUpdateStrategy::MultipleTreeFixedDelta,
        "connected_components" => DualUpdateStrategy::MultipleTreeConnectedComponents,
        other => {
            return Err(GraphError::new_err(format!(
                "unknown dual update strategy {other:?}"
            )));
        }
    };
    Ok(BlossomVOptions::new(
        init,
        dual,
        update_duals_before,
        update_duals_after,
    ))
}

fn objective(name: &str) -> PyResult<ObjectiveSense> {
    match name {
        "minimize" => Ok(ObjectiveSense::Minimize),
        "maximize" => Ok(ObjectiveSense::Maximize),
        other => Err(GraphError::new_err(format!("unknown objective {other:?}"))),
    }
}

/// A maximum weight matching in a general undirected graph.
///
/// ``algorithm`` is ``"path_growing"`` (default; a 1/2-approximation), ``"greedy"`` (also a
/// 1/2-approximation) or ``"blossom"`` (exact, Kolmogorov's Blossom V; ``objective`` is
/// ``"maximize"`` (default) or ``"minimize"``). Blossom V can be tuned with ``initialization``
/// (``"greedy"``, ``"none"`` or ``"fractional"``), ``dual_update`` (``"fixed_delta"`` or
/// ``"connected_components"``), ``update_duals_before`` and ``update_duals_after``.
#[pyfunction]
#[pyo3(signature = (
    graph, algorithm="path_growing", objective="maximize", initialization="greedy",
    dual_update="fixed_delta", update_duals_before=true, update_duals_after=false,
))]
fn weighted_matching(
    py: Python<'_>,
    graph: &Bound<'_, PyAny>,
    algorithm: &str,
    objective: &str,
    initialization: &str,
    dual_update: &str,
    update_duals_before: bool,
    update_duals_after: bool,
) -> PyResult<Matching> {
    let sense = self::objective(objective)?;
    let options = blossom_options(
        initialization,
        dual_update,
        update_duals_before,
        update_duals_after,
    )?;
    dispatch_undirected!(graph, |g, lab| {
        match algorithm {
            "path_growing" => run!(
                py,
                g,
                lab,
                PathGrowingWeightedMatching::new(g).and_then(|mut a| a.matching())
            ),
            "greedy" => run!(
                py,
                g,
                lab,
                GreedyWeightedMatching::new(g, false).and_then(|mut a| a.matching())
            ),
            "blossom" => run!(
                py,
                g,
                lab,
                KolmogorovWeightedMatching::with_options_and_objective(g, options, sense)
                    .and_then(|mut a| a.matching())
            ),
            other => Err(unknown(other)),
        }
    })
}

/// A minimum or maximum weight perfect matching (Kolmogorov's Blossom V). ``objective`` is
/// ``"minimize"`` (default) or ``"maximize"``; the tuning options are those of
/// :func:`weighted_matching`. Raises :class:`GraphError` if the graph has no perfect matching.
#[pyfunction]
#[pyo3(signature = (
    graph, objective="minimize", initialization="greedy", dual_update="fixed_delta",
    update_duals_before=true, update_duals_after=false,
))]
fn perfect_matching(
    py: Python<'_>,
    graph: &Bound<'_, PyAny>,
    objective: &str,
    initialization: &str,
    dual_update: &str,
    update_duals_before: bool,
    update_duals_after: bool,
) -> PyResult<Matching> {
    let sense = self::objective(objective)?;
    let options = blossom_options(
        initialization,
        dual_update,
        update_duals_before,
        update_duals_after,
    )?;
    dispatch_undirected!(graph, |g, lab| {
        run!(
            py,
            g,
            lab,
            KolmogorovWeightedPerfectMatching::with_options_and_objective(g, options, sense)
                .and_then(|mut a| a.matching())
        )
    })
}

/// The two vertex sets of a bipartite graph: the given ones, or a computed bipartition.
macro_rules! sides {
    ($g:expr, $lab:expr, $py:expr, $left:expr, $right:expr) => {{
        match ($left, $right) {
            (Some(l), Some(r)) => {
                let ids = |items: &Vec<Bound<'_, PyAny>>| -> PyResult<Vec<usize>> {
                    items.iter().map(|v| $lab.vertex_id($py, v)).collect()
                };
                (ids(&l)?, ids(&r)?)
            }
            (None, None) => partition::bipartite_partition($g).ok_or_else(|| {
                GraphError::new_err("graph is not bipartite; supply the partitions")
            })?,
            _ => return Err(GraphError::new_err("give both partitions or neither")),
        }
    }};
}

/// A maximum cardinality matching in a bipartite graph (Hopcroft-Karp). If the two vertex sets
/// are omitted, a bipartition of the graph is computed.
#[pyfunction]
#[pyo3(signature = (graph, left=None, right=None))]
fn bipartite_maximum_matching(
    py: Python<'_>,
    graph: &Bound<'_, PyAny>,
    left: Option<Vec<Bound<'_, PyAny>>>,
    right: Option<Vec<Bound<'_, PyAny>>>,
) -> PyResult<Matching> {
    dispatch_undirected!(graph, |g, lab| {
        let (l, r) = sides!(g, lab, py, left, right);
        run!(
            py,
            g,
            lab,
            HopcroftKarp::new(g, l, r).and_then(|mut a| a.matching())
        )
    })
}

/// A maximum weight matching in a bipartite graph. If the two vertex sets are omitted, a
/// bipartition of the graph is computed.
#[pyfunction]
#[pyo3(signature = (graph, left=None, right=None))]
fn bipartite_maximum_weight_matching(
    py: Python<'_>,
    graph: &Bound<'_, PyAny>,
    left: Option<Vec<Bound<'_, PyAny>>>,
    right: Option<Vec<Bound<'_, PyAny>>>,
) -> PyResult<Matching> {
    dispatch_undirected!(graph, |g, lab| {
        let (l, r) = sides!(g, lab, py, left, right);
        let (l, r): (IndexSet<usize>, IndexSet<usize>) =
            (l.into_iter().collect(), r.into_iter().collect());
        run!(
            py,
            g,
            lab,
            MaximumWeightBipartiteMatching::new(g, l, r).and_then(|mut a| a.matching())
        )
    })
}

/// A minimum weight perfect matching in a *complete* bipartite graph with equally sized sides
/// (Kuhn-Munkres / Hungarian method). If the vertex sets are omitted, a bipartition is computed.
#[pyfunction]
#[pyo3(signature = (graph, left=None, right=None))]
fn bipartite_minimum_weight_perfect_matching(
    py: Python<'_>,
    graph: &Bound<'_, PyAny>,
    left: Option<Vec<Bound<'_, PyAny>>>,
    right: Option<Vec<Bound<'_, PyAny>>>,
) -> PyResult<Matching> {
    dispatch_undirected!(graph, |g, lab| {
        let (l, r) = sides!(g, lab, py, left, right);
        let (l, r): (IndexSet<usize>, IndexSet<usize>) =
            (l.into_iter().collect(), r.into_iter().collect());
        run!(py, g, lab, KuhnMunkres::new(g, l, r).matching())
    })
}

pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<Matching>()?;
    m.add_function(wrap_pyfunction!(maximum_matching, m)?)?;
    m.add_function(wrap_pyfunction!(weighted_matching, m)?)?;
    m.add_function(wrap_pyfunction!(perfect_matching, m)?)?;
    m.add_function(wrap_pyfunction!(bipartite_maximum_matching, m)?)?;
    m.add_function(wrap_pyfunction!(bipartite_maximum_weight_matching, m)?)?;
    m.add_function(wrap_pyfunction!(
        bipartite_minimum_weight_perfect_matching,
        m
    )?)?;
    Ok(())
}
