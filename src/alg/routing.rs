//! Advanced shortest-path algorithms: ALT, bidirectional A*, contraction hierarchies,
//! transit node routing, many-to-many and multi-objective paths, and negative cycles.
//!
//! Precomputed structures (hierarchies, routing tables) are built and queried inside one call, so
//! functions that benefit from precomputation take a whole batch of queries.

use std::cell::RefCell;
use std::collections::HashSet;

use jgrapht::GraphExt as _;
use jgrapht::alg::shortestpath::{
    AStar, AltAdmissibleHeuristic, BellmanFord, BellmanFordError, BidirectionalAStarShortestPath,
    ContractionHierarchyBidirectionalDijkstra, ContractionHierarchyManyToMany,
    ContractionHierarchyPrecomputation, DefaultManyToManyShortestPaths, Dijkstra,
    DijkstraClosestFirstIterator, DijkstraManyToManyShortestPaths,
    LabelCorrectingMultiObjectiveShortestPath, MartinShortestPath, ShortestPathAlgorithm,
    TransitNodeRoutingPrecomputation, TreeMeasurer,
};
use pyo3::prelude::*;
use pyo3::types::PyDict;

use crate::error::{GraphError, graph_error};
use crate::graph::GraphPath;
use crate::labels::{EdgeId, dispatch};

fn unknown(name: &str) -> PyErr {
    GraphError::new_err(format!("unknown algorithm {name:?}"))
}

/// Shortest path using the ALT (A*, landmarks, triangle inequality) heuristic: distances from
/// and to the ``landmarks`` give a lower bound on the remaining distance. With ``bidirectional``
/// the search runs from both ends. Returns ``None`` if the target is unreachable.
#[pyfunction]
#[pyo3(signature = (graph, source, target, landmarks, bidirectional=false))]
fn alt_shortest_path(
    py: Python<'_>,
    graph: &Bound<'_, PyAny>,
    source: Bound<'_, PyAny>,
    target: Bound<'_, PyAny>,
    landmarks: Vec<Bound<'_, PyAny>>,
    bidirectional: bool,
) -> PyResult<Option<GraphPath>> {
    dispatch!(graph, |g, lab| {
        let (s, t) = (lab.vertex_id(py, &source)?, lab.vertex_id(py, &target)?);
        let ids: Vec<usize> = landmarks
            .iter()
            .map(|v| lab.vertex_id(py, v))
            .collect::<PyResult<_>>()?;
        let alt = AltAdmissibleHeuristic::new(g, ids).map_err(graph_error)?;
        let estimate = |a: &usize, b: &usize| alt.cost_estimate(a, b);
        let walk = if bidirectional {
            BidirectionalAStarShortestPath::new(g, estimate).path(&s, &t)
        } else {
            AStar::new(g, estimate).path(&s, &t)
        }
        .map_err(graph_error)?;
        Ok(walk.map(|w| lab.path(py, &w)))
    })
}

/// Bidirectional A* shortest path. ``heuristic(vertex, target)`` must be admissible and
/// consistent; it is also used (with the roles swapped) for the backward search. An exception
/// raised by the heuristic aborts the search and is re-raised.
#[pyfunction]
fn bidirectional_astar_shortest_path(
    py: Python<'_>,
    graph: &Bound<'_, PyAny>,
    source: Bound<'_, PyAny>,
    target: Bound<'_, PyAny>,
    heuristic: Bound<'_, PyAny>,
) -> PyResult<Option<GraphPath>> {
    dispatch!(graph, |g, lab| {
        let (s, t) = (lab.vertex_id(py, &source)?, lab.vertex_id(py, &target)?);
        let failure: RefCell<Option<PyErr>> = RefCell::new(None);
        let estimate = |a: &usize, b: &usize| -> f64 {
            if failure.borrow().is_some() {
                return 0.0;
            }
            heuristic
                .call1((lab.vertex_obj(py, *a), lab.vertex_obj(py, *b)))
                .and_then(|r| r.extract::<f64>())
                .unwrap_or_else(|e| {
                    *failure.borrow_mut() = Some(e);
                    0.0
                })
        };
        let walk = BidirectionalAStarShortestPath::new(g, estimate).path(&s, &t);
        let first_error = failure.borrow_mut().take();
        if let Some(e) = first_error {
            return Err(e);
        }
        Ok(walk.map_err(graph_error)?.map(|w| lab.path(py, &w)))
    })
}

/// Vertices in order of increasing distance from ``source`` (Dijkstra's order) as
/// ``[(vertex, distance)]``, optionally only those within ``radius``.
#[pyfunction]
#[pyo3(signature = (graph, source, radius=None))]
fn closest_first(
    py: Python<'_>,
    graph: &Bound<'_, PyAny>,
    source: Bound<'_, PyAny>,
    radius: Option<f64>,
) -> PyResult<Vec<(Py<PyAny>, f64)>> {
    dispatch!(graph, |g, lab| {
        let s = lab.vertex_id(py, &source)?;
        let mut it = match radius {
            Some(r) => DijkstraClosestFirstIterator::with_radius(g, &s, r),
            None => DijkstraClosestFirstIterator::new(g, &s),
        }
        .map_err(graph_error)?;
        let order: Vec<usize> = it.by_ref().collect();
        let paths = it.paths();
        Ok(order
            .into_iter()
            .map(|v| (lab.vertex_obj(py, v), paths.dist[&v]))
            .collect())
    })
}

/// The center of a tree: its vertices of minimum eccentricity (one or two).
#[pyfunction]
fn tree_center(py: Python<'_>, graph: &Bound<'_, PyAny>) -> PyResult<Vec<Py<PyAny>>> {
    dispatch!(graph, |g, lab| {
        Ok(lab.vertices(
            py,
            TreeMeasurer::new(g).graph_center().map_err(graph_error)?,
        ))
    })
}

/// A negative-weight cycle reachable from ``source`` as a closed :class:`GraphPath`, or
/// ``None`` if there is none (Bellman-Ford).
#[pyfunction]
fn negative_cycle(
    py: Python<'_>,
    graph: &Bound<'_, PyAny>,
    source: Bound<'_, PyAny>,
) -> PyResult<Option<GraphPath>> {
    dispatch!(graph, |g, lab| {
        let s = lab.vertex_id(py, &source)?;
        match BellmanFord::new(g).paths_from(&s) {
            Ok(_) => Ok(None),
            Err(BellmanFordError::NegativeCycle(c)) => Ok(Some(lab.path(py, c.cycle()))),
            Err(BellmanFordError::Graph(e)) => Err(graph_error(e)),
        }
    })
}

/// Shortest paths for a batch of ``(source, target)`` pairs as a list (``None`` for an
/// unreachable pair), sharing one precomputation. ``algorithm`` is ``"contraction_hierarchy"``
/// (default; precomputes a hierarchy once, then answers each query with a bidirectional upward
/// search), ``"transit_node_routing"`` (precomputes transit nodes on top of a hierarchy;
/// ``transit_vertex_count`` sets how many) or ``"dijkstra"``. ``parallelism`` is the number of
/// threads for the precomputation.
#[pyfunction]
#[pyo3(signature = (graph, pairs, algorithm="contraction_hierarchy", transit_vertex_count=None, parallelism=1))]
fn batch_shortest_paths(
    py: Python<'_>,
    graph: &Bound<'_, PyAny>,
    pairs: Vec<(Bound<'_, PyAny>, Bound<'_, PyAny>)>,
    algorithm: &str,
    transit_vertex_count: Option<usize>,
    parallelism: usize,
) -> PyResult<Vec<Option<GraphPath>>> {
    dispatch!(graph, |g, lab| {
        let ids: Vec<(usize, usize)> = pairs
            .iter()
            .map(|(s, t)| Ok((lab.vertex_id(py, s)?, lab.vertex_id(py, t)?)))
            .collect::<PyResult<_>>()?;
        let parallelism = parallelism.max(1);
        let mut out = Vec::with_capacity(ids.len());
        match algorithm {
            "contraction_hierarchy" => {
                let h = ContractionHierarchyPrecomputation::with_parallelism(g, parallelism)
                    .contraction_hierarchy()
                    .map_err(graph_error)?;
                let search = ContractionHierarchyBidirectionalDijkstra::new(&h);
                for (s, t) in &ids {
                    out.push(
                        search
                            .path(s, t)
                            .map_err(graph_error)?
                            .map(|w| lab.path(py, &w)),
                    );
                }
            }
            "transit_node_routing" => {
                let h = ContractionHierarchyPrecomputation::with_parallelism(g, parallelism)
                    .contraction_hierarchy()
                    .map_err(graph_error)?;
                let mut pre =
                    TransitNodeRoutingPrecomputation::new(&h).with_parallelism(parallelism);
                if let Some(count) = transit_vertex_count {
                    pre = pre.with_transit_vertex_count(count).map_err(graph_error)?;
                }
                let tnr = jgrapht::alg::shortestpath::TransitNodeRoutingShortestPath::from_routing(
                    pre.transit_node_routing().map_err(graph_error)?,
                );
                for (s, t) in &ids {
                    out.push(
                        tnr.path(s, t)
                            .map_err(graph_error)?
                            .map(|w| lab.path(py, &w)),
                    );
                }
            }
            "dijkstra" => {
                let d = Dijkstra::new(g);
                for (s, t) in &ids {
                    out.push(d.path(s, t).map_err(graph_error)?.map(|w| lab.path(py, &w)));
                }
            }
            other => return Err(unknown(other)),
        }
        Ok(out)
    })
}

/// Shortest paths between every ``source`` and ``target`` as ``{(source, target): GraphPath}``
/// (unreachable pairs are omitted). ``algorithm`` is ``"contraction_hierarchy"`` (default),
/// ``"dijkstra"`` (a forward or backward search per source or target, whichever is fewer) or
/// ``"default"`` (a point-to-point Dijkstra for every pair).
#[pyfunction]
#[pyo3(signature = (graph, sources, targets, algorithm="contraction_hierarchy"))]
fn many_to_many_shortest_paths<'py>(
    py: Python<'py>,
    graph: &Bound<'py, PyAny>,
    sources: Vec<Bound<'py, PyAny>>,
    targets: Vec<Bound<'py, PyAny>>,
    algorithm: &str,
) -> PyResult<Bound<'py, PyDict>> {
    dispatch!(graph, |g, lab| {
        let ids = |vs: &[Bound<'py, PyAny>]| -> PyResult<Vec<usize>> {
            vs.iter().map(|v| lab.vertex_id(py, v)).collect()
        };
        let (ss, ts) = (ids(&sources)?, ids(&targets)?);
        let paths =
            match algorithm {
                "contraction_hierarchy" => {
                    let h = ContractionHierarchyPrecomputation::new(g)
                        .contraction_hierarchy()
                        .map_err(graph_error)?;
                    ContractionHierarchyManyToMany::new(&h).many_to_many(ss.clone(), ts.clone())
                }
                "dijkstra" => DijkstraManyToManyShortestPaths::new(g)
                    .many_to_many_paths(ss.clone(), ts.clone()),
                "default" => DefaultManyToManyShortestPaths::new(g)
                    .many_to_many_paths(ss.clone(), ts.clone()),
                other => return Err(unknown(other)),
            }
            .map_err(graph_error)?;
        let out = PyDict::new(py);
        let (seen_s, seen_t): (HashSet<usize>, HashSet<usize>) =
            (ss.into_iter().collect(), ts.into_iter().collect());
        for s in &seen_s {
            for t in &seen_t {
                if let Some(w) = paths.path(s, t) {
                    out.set_item(
                        (lab.vertex_obj(py, *s), lab.vertex_obj(py, *t)),
                        Py::new(py, lab.path(py, w))?,
                    )?;
                }
            }
        }
        Ok(out)
    })
}

/// Pareto-optimal paths for several objectives. ``edge_weights`` gives each edge's vector of
/// weights (a dict ``{edge: sequence}`` or a callable; every vector must have the same length).
/// ``algorithm`` is ``"martin"`` (default) or ``"label_correcting"`` (which also accepts
/// ``epsilon``). Returns ``{target: [GraphPath, ...]}`` for every reachable target, or just the
/// list of Pareto-optimal paths when ``target`` is given. ``GraphPath.weight`` is the graph's
/// own edge weight; the objective vectors are the ones you supplied.
#[pyfunction]
#[pyo3(signature = (graph, source, edge_weights, target=None, algorithm="martin", epsilon=None))]
fn multi_objective_shortest_paths(
    py: Python<'_>,
    graph: &Bound<'_, PyAny>,
    source: Bound<'_, PyAny>,
    edge_weights: Bound<'_, PyAny>,
    target: Option<Bound<'_, PyAny>>,
    algorithm: &str,
    epsilon: Option<f64>,
) -> PyResult<Py<PyAny>> {
    dispatch!(graph, |g, lab| {
        let s = lab.vertex_id(py, &source)?;
        let t = target.as_ref().map(|t| lab.vertex_id(py, t)).transpose()?;
        let failure: RefCell<Option<PyErr>> = RefCell::new(None);
        let weight = |e: &_| -> Vec<f64> {
            if failure.borrow().is_some() {
                return Vec::new();
            }
            let key = lab.edge_obj(py, EdgeId::eid(e));
            let value = if let Ok(d) = edge_weights.cast::<PyDict>() {
                d.get_item(key.bind(py)).map(|v| v.map(|v| v.unbind()))
            } else if edge_weights.is_callable() {
                edge_weights.call1((key,)).map(|v| Some(v.unbind()))
            } else {
                Err(pyo3::exceptions::PyTypeError::new_err(
                    "edge_weights must be a dict or a callable",
                ))
            };
            value
                .and_then(|v| match v {
                    Some(v) => v.extract::<Vec<f64>>(py),
                    None => Err(GraphError::new_err("missing weight vector for an edge")),
                })
                .unwrap_or_else(|e| {
                    *failure.borrow_mut() = Some(e);
                    Vec::new()
                })
        };
        let result = match algorithm {
            "martin" => MartinShortestPath::new(g, weight).paths_from(&s),
            "label_correcting" => match epsilon {
                Some(eps) => {
                    LabelCorrectingMultiObjectiveShortestPath::with_epsilon(g, weight, eps)
                }
                None => Ok(LabelCorrectingMultiObjectiveShortestPath::new(g, weight)),
            }
            .and_then(|a| a.paths_from(&s)),
            other => return Err(unknown(other)),
        };
        let first_error = failure.borrow_mut().take();
        if let Some(e) = first_error {
            return Err(e);
        }
        let paths = result.map_err(graph_error)?;
        match t {
            Some(t) => {
                let list: Vec<GraphPath> =
                    paths.paths(&t).iter().map(|w| lab.path(py, w)).collect();
                Ok(pyo3::types::PyList::new(py, list)?.into_any().unbind())
            }
            None => {
                let out = PyDict::new(py);
                for v in g.vertices_cloned() {
                    let ps = paths.paths(&v);
                    if !ps.is_empty() {
                        let list: Vec<GraphPath> = ps.iter().map(|w| lab.path(py, w)).collect();
                        out.set_item(lab.vertex_obj(py, v), list)?;
                    }
                }
                Ok(out.into_any().unbind())
            }
        }
    })
}

pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(alt_shortest_path, m)?)?;
    m.add_function(wrap_pyfunction!(bidirectional_astar_shortest_path, m)?)?;
    m.add_function(wrap_pyfunction!(closest_first, m)?)?;
    m.add_function(wrap_pyfunction!(tree_center, m)?)?;
    m.add_function(wrap_pyfunction!(negative_cycle, m)?)?;
    m.add_function(wrap_pyfunction!(batch_shortest_paths, m)?)?;
    m.add_function(wrap_pyfunction!(many_to_many_shortest_paths, m)?)?;
    m.add_function(wrap_pyfunction!(multi_objective_shortest_paths, m)?)?;
    Ok(())
}
