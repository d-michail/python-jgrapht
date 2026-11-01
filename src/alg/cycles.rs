//! Cycles: detection, enumeration, bases, Eulerian tours, minimum mean cycles and chordality.

use jgrapht::Graph as _;
use jgrapht::alg::connectivity::connected_components;
use jgrapht::alg::cycle::{
    ChinesePostman, ChordalityInspector, CycleBasisAlgorithm, CycleDetector, DirectedSimpleCycles,
    EulerianCycleAlgorithm, HawickJamesSimpleCycles, HierholzerEulerianCycle,
    HowardMinimumMeanCycle, IterationOrder, JohnsonSimpleCycles, MinimumCycleMeanAlgorithm,
    PatonCycleBase, QueueBFSFundamentalCycleBasis, StackBFSFundamentalCycleBasis,
    SzwarcfiterLauerSimpleCycles, TarjanSimpleCycles, TiernanSimpleCycles,
    simple_cycle_to_graph_path,
};
use pyo3::prelude::*;

use crate::error::{GraphError, graph_error};
use crate::graph::GraphPath;
use crate::labels::{EdgeId, dispatch, dispatch_directed, dispatch_undirected};

fn is_directed(graph: &Bound<'_, PyAny>) -> PyResult<bool> {
    graph.getattr("directed")?.extract()
}

/// Whether the graph contains a cycle. A self-loop is a cycle; so is a pair of parallel edges in
/// an undirected graph.
#[pyfunction]
fn has_cycle(graph: &Bound<'_, PyAny>) -> PyResult<bool> {
    if is_directed(graph)? {
        dispatch_directed!(graph, |g, _lab| Ok(CycleDetector::new(g).detect_cycles()))
    } else {
        dispatch_undirected!(graph, |g, _lab| {
            // a forest has exactly (vertices - components) edges
            Ok(g.edge_count() + connected_components(g).len() > g.vertex_count())
        })
    }
}

/// All vertices of a directed graph that lie on some cycle.
#[pyfunction]
fn vertices_on_cycles(py: Python<'_>, graph: &Bound<'_, PyAny>) -> PyResult<Vec<Py<PyAny>>> {
    dispatch_directed!(graph, |g, lab| {
        Ok(lab.vertices(py, CycleDetector::new(g).find_cycles()))
    })
}

/// Every simple cycle of a directed graph, each as a list of vertices. ``algorithm`` is
/// ``"johnson"`` (default), ``"tarjan"``, ``"tiernan"``, ``"szwarcfiter_lauer"`` or
/// ``"hawick_james"``. The number of cycles can be exponential.
#[pyfunction]
#[pyo3(signature = (graph, algorithm="johnson"))]
fn simple_cycles(
    py: Python<'_>,
    graph: &Bound<'_, PyAny>,
    algorithm: &str,
) -> PyResult<Vec<Vec<Py<PyAny>>>> {
    dispatch_directed!(graph, |g, lab| {
        let cycles = match algorithm {
            "johnson" => JohnsonSimpleCycles::new(g).and_then(|mut a| a.find_simple_cycles()),
            "tarjan" => TarjanSimpleCycles::with_graph(g).find_simple_cycles(),
            "tiernan" => TiernanSimpleCycles::with_graph(g).find_simple_cycles(),
            "szwarcfiter_lauer" => SzwarcfiterLauerSimpleCycles::with_graph(g).find_simple_cycles(),
            "hawick_james" => HawickJamesSimpleCycles::with_graph(g).find_simple_cycles(),
            other => return Err(GraphError::new_err(format!("unknown algorithm {other:?}"))),
        }
        .map_err(graph_error)?;
        Ok(cycles.into_iter().map(|c| lab.vertices(py, c)).collect())
    })
}

/// A cycle basis of an undirected graph, as a list of cycles, each a list of edges.
/// ``algorithm`` is ``"paton"`` (default; needs a graph without parallel edges),
/// ``"queue_bfs"`` or ``"stack_bfs"`` (fundamental bases).
#[pyfunction]
#[pyo3(signature = (graph, algorithm="paton"))]
fn cycle_basis(
    py: Python<'_>,
    graph: &Bound<'_, PyAny>,
    algorithm: &str,
) -> PyResult<Vec<Vec<Py<PyAny>>>> {
    dispatch_undirected!(graph, |g, lab| {
        let basis = match algorithm {
            "paton" => PatonCycleBase::new(g).and_then(|mut a| a.cycle_basis()),
            "queue_bfs" => QueueBFSFundamentalCycleBasis::new(g).and_then(|mut a| a.cycle_basis()),
            "stack_bfs" => StackBFSFundamentalCycleBasis::new(g).and_then(|mut a| a.cycle_basis()),
            other => return Err(GraphError::new_err(format!("unknown algorithm {other:?}"))),
        }
        .map_err(graph_error)?;
        Ok(basis
            .cycles()
            .iter()
            .map(|c| lab.edges(py, c.iter().map(|e| e.eid())))
            .collect())
    })
}

/// Whether the graph has an Eulerian cycle (a closed walk using every edge exactly once).
#[pyfunction]
fn is_eulerian(graph: &Bound<'_, PyAny>) -> PyResult<bool> {
    dispatch!(graph, |g, _lab| Ok(
        HierholzerEulerianCycle::new().is_eulerian(g)
    ))
}

/// An Eulerian cycle as a :class:`GraphPath`. Raises :class:`GraphError` if there is none.
#[pyfunction]
fn eulerian_cycle(py: Python<'_>, graph: &Bound<'_, PyAny>) -> PyResult<GraphPath> {
    dispatch!(graph, |g, lab| {
        let walk = HierholzerEulerianCycle::new()
            .eulerian_cycle(g)
            .map_err(graph_error)?;
        Ok(lab.path(py, &walk))
    })
}

/// A shortest closed walk traversing every edge at least once (the Chinese postman problem),
/// for a connected undirected graph or a strongly connected directed graph.
#[pyfunction]
fn chinese_postman(py: Python<'_>, graph: &Bound<'_, PyAny>) -> PyResult<GraphPath> {
    dispatch!(graph, |g, lab| {
        let walk = ChinesePostman::new().cpp_solution(g).map_err(graph_error)?;
        Ok(lab.path(py, &walk))
    })
}

/// The cycle with the smallest mean edge weight in a directed graph (Howard's algorithm), as
/// ``(mean, cycle)``, or ``None`` if the graph is acyclic.
#[pyfunction]
fn minimum_mean_cycle(
    py: Python<'_>,
    graph: &Bound<'_, PyAny>,
) -> PyResult<Option<(f64, GraphPath)>> {
    dispatch_directed!(graph, |g, lab| {
        let mut a = HowardMinimumMeanCycle::new(g);
        Ok(match (a.cycle_mean(), a.cycle()) {
            (Some(mean), Some(cycle)) => Some((mean, lab.path(py, &cycle))),
            _ => None,
        })
    })
}

fn order(name: &str) -> PyResult<IterationOrder> {
    match name {
        "mcs" => Ok(IterationOrder::Mcs),
        "lex_bfs" => Ok(IterationOrder::LexBfs),
        other => Err(GraphError::new_err(format!("unknown order {other:?}"))),
    }
}

/// Whether an undirected graph is chordal (every cycle of length > 3 has a chord). ``order`` is
/// the search used: ``"mcs"`` (default) or ``"lex_bfs"``.
#[pyfunction]
#[pyo3(signature = (graph, order_by="mcs"))]
fn is_chordal(graph: &Bound<'_, PyAny>, order_by: &str) -> PyResult<bool> {
    let o = order(order_by)?;
    dispatch_undirected!(graph, |g, _lab| Ok(
        ChordalityInspector::with_order(g, o).is_chordal()
    ))
}

/// A perfect elimination ordering of a chordal graph, or ``None`` if the graph is not chordal.
#[pyfunction]
#[pyo3(signature = (graph, order_by="mcs"))]
fn perfect_elimination_order(
    py: Python<'_>,
    graph: &Bound<'_, PyAny>,
    order_by: &str,
) -> PyResult<Option<Vec<Py<PyAny>>>> {
    let o = order(order_by)?;
    dispatch_undirected!(graph, |g, lab| {
        let mut inspector = ChordalityInspector::with_order(g, o);
        Ok(inspector
            .perfect_elimination_order()
            .map(|vs| lab.vertices(py, vs.iter().copied())))
    })
}

/// A chordless cycle of length > 3 (a "hole") if the graph is not chordal, else ``None``.
#[pyfunction]
#[pyo3(signature = (graph, order_by="mcs"))]
fn chordal_hole(
    py: Python<'_>,
    graph: &Bound<'_, PyAny>,
    order_by: &str,
) -> PyResult<Option<GraphPath>> {
    let o = order(order_by)?;
    dispatch_undirected!(graph, |g, lab| {
        let mut inspector = ChordalityInspector::with_order(g, o);
        Ok(inspector.hole().map(|w| lab.path(py, w)))
    })
}

/// Turns the edges of a simple cycle (in any order) into a closed :class:`GraphPath`, or returns
/// ``None`` for an empty list. Raises :class:`GraphError` if the edges do not form a simple cycle.
#[pyfunction]
fn cycle_to_path(
    py: Python<'_>,
    graph: &Bound<'_, PyAny>,
    edges: Vec<Bound<'_, PyAny>>,
) -> PyResult<Option<GraphPath>> {
    dispatch!(graph, |g, lab| {
        let ids: Vec<_> = edges
            .iter()
            .map(|e| lab.edge_id(py, e).map(EdgeId::from_eid))
            .collect::<PyResult<_>>()?;
        let walk = simple_cycle_to_graph_path(g, &ids).map_err(graph_error)?;
        Ok(walk.map(|w| lab.path(py, &w)))
    })
}

pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(cycle_to_path, m)?)?;
    m.add_function(wrap_pyfunction!(has_cycle, m)?)?;
    m.add_function(wrap_pyfunction!(vertices_on_cycles, m)?)?;
    m.add_function(wrap_pyfunction!(simple_cycles, m)?)?;
    m.add_function(wrap_pyfunction!(cycle_basis, m)?)?;
    m.add_function(wrap_pyfunction!(is_eulerian, m)?)?;
    m.add_function(wrap_pyfunction!(eulerian_cycle, m)?)?;
    m.add_function(wrap_pyfunction!(chinese_postman, m)?)?;
    m.add_function(wrap_pyfunction!(minimum_mean_cycle, m)?)?;
    m.add_function(wrap_pyfunction!(is_chordal, m)?)?;
    m.add_function(wrap_pyfunction!(perfect_elimination_order, m)?)?;
    m.add_function(wrap_pyfunction!(chordal_hole, m)?)?;
    Ok(())
}
