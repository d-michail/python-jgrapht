//! Graph transformations that produce a new graph.

use std::collections::HashMap;

use jgrapht::alg::transform::{
    complement_into, contract_edge as rust_contract_edge, line_graph_into, line_graph_weighted_into,
};
use jgrapht::alg::transitive::{TransitiveClosure, TransitiveReduction};
use jgrapht::{
    DefaultEdge, DiGraph, Graph as _, GraphExt as _, GraphMut as _, GraphMutExt as _, UGraph,
};
use pyo3::prelude::*;

use crate::error::graph_error;
use crate::graph::Graph;
use crate::labels::{EdgeId, dispatch, dispatch_directed};

/// The edges of `g` between distinct vertices as index pairs into `order`.
fn index_pairs<G, I>(order: &[usize], edges: I) -> Vec<(usize, usize, Option<f64>)>
where
    G: jgrapht::Graph<Vertex = usize>,
    I: IntoIterator<Item = (usize, usize)>,
{
    let index: HashMap<usize, usize> = order.iter().enumerate().map(|(i, v)| (*v, i)).collect();
    edges
        .into_iter()
        .map(|(s, t)| (index[&s], index[&t], None))
        .collect::<Vec<_>>()
}

/// The complement of a graph as a new :class:`Graph` on the same vertices: an edge wherever the
/// original has none. ``loops`` also adds self-loops where the original has none.
#[pyfunction]
#[pyo3(signature = (graph, loops=false))]
fn complement(py: Python<'_>, graph: &Bound<'_, PyAny>, loops: bool) -> PyResult<Py<Graph>> {
    dispatch!(graph, |g, lab| {
        let order: Vec<usize> = g.vertices_cloned().collect();
        let directed = g.graph_type().directed;
        let edges = if directed {
            let mut t = DiGraph::<usize>::with_loops();
            complement_into(g, &mut t, loops).map_err(graph_error)?;
            index_pairs::<DiGraph<usize>, _>(&order, t.edges_cloned().map(|e| endpoints(&t, &e)))
        } else {
            let mut t = UGraph::<usize>::with_loops();
            complement_into(g, &mut t, loops).map_err(graph_error)?;
            index_pairs::<UGraph<usize>, _>(&order, t.edges_cloned().map(|e| endpoints(&t, &e)))
        };
        Graph::from_parts(py, directed, lab.vertices(py, order), edges)
    })
}

fn endpoints<G: jgrapht::Graph>(g: &G, e: &G::Edge) -> (G::Vertex, G::Vertex)
where
    G::Vertex: Clone,
{
    let (s, t) = g.edge_endpoints(e).expect("edge of the graph");
    (s.clone(), t.clone())
}

/// The line graph as a new :class:`Graph` whose vertices are the *edges* of the original: two
/// are joined when the original edges share a vertex (for a directed graph, when one ends where
/// the other starts). With ``weight``, a callable ``weight(edge1, edge2)``, the line graph is
/// weighted and each new edge gets that weight.
#[pyfunction]
#[pyo3(signature = (graph, weight=None))]
fn line_graph(
    py: Python<'_>,
    graph: &Bound<'_, PyAny>,
    weight: Option<Bound<'_, PyAny>>,
) -> PyResult<Py<Graph>> {
    dispatch!(graph, |g, lab| {
        let directed = g.graph_type().directed;
        let originals: Vec<_> = g.edges_cloned().collect();
        let index: HashMap<_, usize> = originals
            .iter()
            .cloned()
            .enumerate()
            .map(|(i, e)| (e, i))
            .collect();
        let failure: std::cell::RefCell<Option<PyErr>> = std::cell::RefCell::new(None);
        let weigh = |a: &_, b: &_| -> f64 {
            let Some(f) = &weight else { return 1.0 };
            if failure.borrow().is_some() {
                return 0.0;
            }
            f.call1((
                lab.edge_obj(py, EdgeId::eid(a)),
                lab.edge_obj(py, EdgeId::eid(b)),
            ))
            .and_then(|r| r.extract::<f64>())
            .unwrap_or_else(|e| {
                *failure.borrow_mut() = Some(e);
                0.0
            })
        };
        let mut pairs: Vec<(usize, usize, Option<f64>)> = Vec::new();
        macro_rules! build {
            ($t:expr) => {{
                let mut t = $t;
                if weight.is_some() {
                    line_graph_weighted_into(g, &mut t, weigh).map_err(graph_error)?;
                } else {
                    line_graph_into(g, &mut t).map_err(graph_error)?;
                }
                for e in t.edges_cloned() {
                    let (s, d) = endpoints(&t, &e);
                    pairs.push((
                        index[&s],
                        index[&d],
                        weight.as_ref().map(|_| t.weight_of(&e)),
                    ));
                }
            }};
        }
        if directed {
            build!(DiGraph::<_>::simple().weighted());
        } else {
            build!(UGraph::<_>::simple().weighted());
        }
        let first_error = failure.borrow_mut().take();
        if let Some(e) = first_error {
            return Err(e);
        }
        let vertices = lab.edges(py, originals.iter().map(|e| e.eid()));
        Graph::from_parts(py, directed, vertices, pairs)
    })
}

/// A copy of a :class:`Graph` with ``edge`` contracted: its two endpoints merge into the source
/// vertex, whose edges now include those of the target. The original graph is unchanged.
/// (A :class:`SparseGraph` is immutable and cannot be contracted.)
#[pyfunction]
fn contract_edge(
    py: Python<'_>,
    graph: &Bound<'_, PyAny>,
    edge: Bound<'_, PyAny>,
) -> PyResult<Py<Graph>> {
    let Ok(g) = graph.extract::<PyRef<'_, Graph>>() else {
        return Err(crate::error::GraphError::new_err(
            "contract_edge needs a Graph (a SparseGraph is immutable)",
        ));
    };
    let id = g.edge_id(py, &edge)?;
    let mut inner = g.inner().clone();
    match &mut inner {
        crate::graph::Inner::Undirected(u) => rust_contract_edge(u, &DefaultEdge(id)),
        crate::graph::Inner::Directed(d) => rust_contract_edge(d, &DefaultEdge(id)),
    }
    .map_err(graph_error)?;
    g.rebuild_from(py, &inner)
}

/// A copy of a directed graph without self-loops or parallel edges, ready for closure/reduction.
fn simple_copy<G: jgrapht::Graph<Vertex = usize>>(g: &G) -> DiGraph<usize> {
    let mut t = DiGraph::<usize>::simple();
    t.add_vertices(g.vertices_cloned());
    for e in g.edges_cloned() {
        let (s, d) = endpoints(g, &e);
        if s != d {
            let _ = t.add_edge(&s, &d);
        }
    }
    t
}

fn graph_from_digraph(
    py: Python<'_>,
    lab: &crate::labels::Labels<'_>,
    t: &DiGraph<usize>,
) -> PyResult<Py<Graph>> {
    let order: Vec<usize> = t.vertices_cloned().collect();
    let edges =
        index_pairs::<DiGraph<usize>, _>(&order, t.edges_cloned().map(|e| endpoints(t, &e)));
    Graph::from_parts(py, true, lab.vertices(py, order), edges)
}

/// The transitive closure of a directed graph as a new :class:`Graph`: an edge ``u -> v``
/// whenever ``v`` is reachable from ``u``. Self-loops and parallel edges are dropped first.
#[pyfunction]
fn transitive_closure(py: Python<'_>, graph: &Bound<'_, PyAny>) -> PyResult<Py<Graph>> {
    dispatch_directed!(graph, |g, lab| {
        let mut t = simple_copy(g);
        TransitiveClosure::INSTANCE
            .close_simple_directed_graph(&mut t)
            .map_err(graph_error)?;
        graph_from_digraph(py, &lab, &t)
    })
}

/// The transitive reduction of a directed graph as a new :class:`Graph`: the fewest edges with
/// the same reachability.
#[pyfunction]
fn transitive_reduction(py: Python<'_>, graph: &Bound<'_, PyAny>) -> PyResult<Py<Graph>> {
    dispatch_directed!(graph, |g, lab| {
        let mut t = simple_copy(g);
        TransitiveReduction::INSTANCE
            .reduce(&mut t)
            .map_err(graph_error)?;
        graph_from_digraph(py, &lab, &t)
    })
}

pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(complement, m)?)?;
    m.add_function(wrap_pyfunction!(line_graph, m)?)?;
    m.add_function(wrap_pyfunction!(contract_edge, m)?)?;
    m.add_function(wrap_pyfunction!(transitive_closure, m)?)?;
    m.add_function(wrap_pyfunction!(transitive_reduction, m)?)?;
    Ok(())
}
