//! Traveling salesman and Hamiltonian cycles and paths.

use jgrapht::alg::tour::{
    BacktrackingHamiltonianPath, Christofides, DagHamiltonianPath, FarthestInsertionHeuristicTsp,
    GreedyHeuristicTsp, HamiltonianCycleAlgorithm, HamiltonianCycleImprovementAlgorithm,
    HamiltonianPathAlgorithm, HeldKarpHamiltonianPath, HeldKarpTsp, NearestInsertionHeuristicTsp,
    NearestNeighborHeuristicTsp, PalmerHamiltonianCycle, RandomTourTsp, SearchStatus,
    TwoApproxMetricTsp, TwoOptHeuristicTsp,
};
use pyo3::prelude::*;
use rand::SeedableRng;
use rand::rngs::StdRng;

use crate::error::{GraphError, graph_error};
use crate::graph::GraphPath;
use crate::labels::{dispatch, dispatch_undirected};

fn unknown(name: &str) -> PyErr {
    GraphError::new_err(format!("unknown algorithm {name:?}"))
}

/// A heuristic or exact traveling salesman tour: a closed walk visiting every vertex once, or
/// ``None`` if the graph has none. The graph should be complete; edge weights are the distances.
///
/// ``algorithm`` is ``"held_karp"`` (exact, exponential, for small graphs; also directed graphs)
/// or, for undirected graphs only, ``"nearest_neighbor"`` (default), ``"nearest_insertion"``,
/// ``"farthest_insertion"``, ``"random"``, ``"greedy"``, ``"two_approx"`` (metric),
/// ``"christofides"`` (metric, 3/2-approximation) and ``"two_opt"`` (local improvement of a
/// random tour). ``seed`` makes the randomized ones reproducible.
#[pyfunction]
#[pyo3(signature = (graph, algorithm="nearest_neighbor", seed=None))]
fn traveling_salesman_tour(
    py: Python<'_>,
    graph: &Bound<'_, PyAny>,
    algorithm: &str,
    seed: Option<u64>,
) -> PyResult<Option<GraphPath>> {
    let rng = || match seed {
        Some(s) => StdRng::seed_from_u64(s),
        None => StdRng::from_os_rng(),
    };
    match algorithm {
        "held_karp" => dispatch!(graph, |g, lab| {
            let tour = HeldKarpTsp::new().tour(g).map_err(graph_error)?;
            Ok(tour.map(|w| lab.path(py, &w)))
        }),
        "nearest_neighbor" | "nearest_insertion" | "farthest_insertion" | "random" | "greedy"
        | "two_approx" | "christofides" | "two_opt" => dispatch_undirected!(graph, |g, lab| {
            let tour = match algorithm {
                "nearest_neighbor" => NearestNeighborHeuristicTsp::with_rng(rng()).tour(g),
                "nearest_insertion" => NearestInsertionHeuristicTsp::new().tour(g),
                "farthest_insertion" => FarthestInsertionHeuristicTsp::new().tour(g),
                "random" => RandomTourTsp::with_rng(rng()).tour(g),
                "greedy" => GreedyHeuristicTsp::new().tour(g),
                "two_approx" => TwoApproxMetricTsp::new().tour(g),
                "christofides" => Christofides::new().tour(g),
                _ => TwoOptHeuristicTsp::with_rng(1, rng()).and_then(|mut a| a.tour(g)),
            }
            .map_err(graph_error)?;
            Ok(tour.map(|w| lab.path(py, &w)))
        }),
        other => Err(unknown(other)),
    }
}

/// A Hamiltonian cycle (a closed walk through every vertex exactly once; Palmer's algorithm).
///
/// Requires a *simple* graph (declared without self-loops or parallel edges, so not a
/// :class:`SparseGraph`) with Ore's property: every two non-adjacent vertices have degrees
/// summing to at least the number of vertices. Otherwise :class:`GraphError` is raised.
#[pyfunction]
fn hamiltonian_cycle(py: Python<'_>, graph: &Bound<'_, PyAny>) -> PyResult<Option<GraphPath>> {
    dispatch!(graph, |g, lab| {
        let tour = PalmerHamiltonianCycle::new().tour(g).map_err(graph_error)?;
        Ok(tour.map(|w| lab.path(py, &w)))
    })
}

/// A Hamiltonian path (a path through every vertex exactly once), or ``None`` if there is none.
/// ``algorithm`` is ``"held_karp"`` (default, exact dynamic programme for small graphs),
/// ``"backtracking"`` (exact search) or ``"dag"`` (directed acyclic graphs only).
#[pyfunction]
#[pyo3(signature = (graph, algorithm="held_karp"))]
fn hamiltonian_path(
    py: Python<'_>,
    graph: &Bound<'_, PyAny>,
    algorithm: &str,
) -> PyResult<Option<GraphPath>> {
    dispatch!(graph, |g, lab| {
        let result = match algorithm {
            "held_karp" => HeldKarpHamiltonianPath::new().path(g),
            "backtracking" => BacktrackingHamiltonianPath::new().path(g),
            "dag" => DagHamiltonianPath::new().path(g),
            other => return Err(unknown(other)),
        }
        .map_err(graph_error)?;
        if result.status() == SearchStatus::Aborted {
            return Err(GraphError::new_err(
                "the search was aborted before reaching an answer",
            ));
        }
        Ok(result.path().map(|w| lab.path(py, w)))
    })
}

/// Improves a tour of an undirected graph with 2-opt local search. ``tour`` is a closed
/// :class:`GraphPath` or a list of vertices (visiting each exactly once); ``passes`` bounds the
/// number of improvement sweeps. Returns the (possibly shorter) tour.
#[pyfunction]
#[pyo3(signature = (graph, tour, passes=1, seed=None))]
fn improve_tour(
    py: Python<'_>,
    graph: &Bound<'_, PyAny>,
    tour: Bound<'_, PyAny>,
    passes: usize,
    seed: Option<u64>,
) -> PyResult<GraphPath> {
    dispatch_undirected!(graph, |g, lab| {
        let items: Vec<Bound<'_, PyAny>> = match tour.getattr("vertices") {
            Ok(vs) => vs.extract()?,
            Err(_) => tour.extract()?,
        };
        let mut ids: Vec<usize> = items
            .iter()
            .map(|v| lab.vertex_id(py, v))
            .collect::<PyResult<_>>()?;
        if ids.first() != ids.last() {
            ids.push(ids[0]);
        }
        let walk = jgrapht::GraphWalk::from_vertices(g, ids)
            .ok_or_else(|| GraphError::new_err("the tour does not follow edges of the graph"))?;
        let improved = match seed {
            Some(s) => TwoOptHeuristicTsp::with_seed(passes, s),
            None => TwoOptHeuristicTsp::with_seed(passes, rand::random()),
        }
        .and_then(|mut a| a.improve_tour(g, &walk))
        .map_err(graph_error)?;
        Ok(lab.path(py, &improved))
    })
}

pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(improve_tour, m)?)?;
    m.add_function(wrap_pyfunction!(traveling_salesman_tour, m)?)?;
    m.add_function(wrap_pyfunction!(hamiltonian_cycle, m)?)?;
    m.add_function(wrap_pyfunction!(hamiltonian_path, m)?)?;
    Ok(())
}
