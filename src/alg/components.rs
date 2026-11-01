//! Connectivity: components, articulation points, bridges, k-connectivity and basic properties.

use jgrapht::alg::connectivity::{
    BlockCutpointGraph, ConnectivityInspector, GabowStrongConnectivityInspector,
    KConnectivityFlowAlgorithm, KosarajuStrongConnectivityInspector, biconnectivity,
    block_cut_tree as rust_block_cut_tree, condensation as rust_condensation,
    connected_component_of as rust_component_of, connected_components as rust_connected_components,
    strongly_connected_components as rust_strongly_connected_components,
    strongly_connected_components_kosaraju as rust_kosaraju,
};
use jgrapht::alg::interfaces::StrongConnectivityAlgorithm;
use jgrapht::graph::props;
use jgrapht::{Graph as _, GraphExt as _};
use pyo3::IntoPyObjectExt;
use pyo3::prelude::*;

use crate::error::graph_error;
use crate::graph::Graph;
use crate::labels::{EdgeId, dispatch, dispatch_directed};

/// Connected components (edge direction ignored), as lists of vertices.
#[pyfunction]
fn connected_components(py: Python<'_>, graph: &Bound<'_, PyAny>) -> PyResult<Vec<Vec<Py<PyAny>>>> {
    dispatch!(graph, |g, lab| {
        Ok(rust_connected_components(g)
            .into_iter()
            .map(|c| lab.vertices(py, c))
            .collect())
    })
}

/// Strongly connected components of a directed graph, as lists of vertices. ``algorithm`` is
/// ``"tarjan"`` (default), ``"kosaraju"`` or ``"gabow"``; they find the same components.
#[pyfunction]
#[pyo3(signature = (graph, algorithm="tarjan"))]
fn strongly_connected_components(
    py: Python<'_>,
    graph: &Bound<'_, PyAny>,
    algorithm: &str,
) -> PyResult<Vec<Vec<Py<PyAny>>>> {
    dispatch_directed!(graph, |g, lab| {
        let comps: Vec<Vec<usize>> = match algorithm {
            "tarjan" => rust_strongly_connected_components(g),
            "kosaraju" => rust_kosaraju(g),
            "gabow" => sets(GabowStrongConnectivityInspector::new(g).strongly_connected_sets()),
            "kosaraju_inspector" => {
                sets(KosarajuStrongConnectivityInspector::new(g).strongly_connected_sets())
            }
            other => {
                return Err(crate::error::GraphError::new_err(format!(
                    "unknown algorithm {other:?}"
                )));
            }
        };
        Ok(comps.into_iter().map(|c| lab.vertices(py, c)).collect())
    })
}

fn sets(components: &[std::collections::HashSet<usize>]) -> Vec<Vec<usize>> {
    components
        .iter()
        .map(|c| {
            let mut v: Vec<usize> = c.iter().copied().collect();
            v.sort_unstable();
            v
        })
        .collect()
}

/// The (weakly) connected component containing ``vertex``, as a list of vertices.
#[pyfunction]
fn connected_component_of(
    py: Python<'_>,
    graph: &Bound<'_, PyAny>,
    vertex: Bound<'_, PyAny>,
) -> PyResult<Vec<Py<PyAny>>> {
    dispatch!(graph, |g, lab| {
        let v = lab.vertex_id(py, &vertex)?;
        Ok(lab.vertices(py, rust_component_of(g, &v).unwrap_or_default()))
    })
}

/// Whether ``target`` can be reached from ``source`` ignoring edge directions (they lie in the
/// same connected component).
#[pyfunction]
fn path_exists(
    py: Python<'_>,
    graph: &Bound<'_, PyAny>,
    source: Bound<'_, PyAny>,
    target: Bound<'_, PyAny>,
) -> PyResult<bool> {
    dispatch!(graph, |g, lab| {
        let (s, t) = (lab.vertex_id(py, &source)?, lab.vertex_id(py, &target)?);
        ConnectivityInspector::new()
            .path_exists(g, &s, &t)
            .map_err(crate::error::graph_error)
    })
}

/// The block-cutpoint graph of an undirected graph as ``(tree, nodes, cutpoints)``: ``tree`` is a
/// :class:`Graph` on ``0..len(nodes)`` joining each cutpoint node to the blocks containing it;
/// ``nodes[i]`` lists the vertices of node ``i`` (the first nodes are the blocks, the rest are
/// single cutpoints) and ``cutpoints`` lists the articulation points.
#[pyfunction]
#[allow(clippy::type_complexity)]
fn block_cutpoint_graph(
    py: Python<'_>,
    graph: &Bound<'_, PyAny>,
) -> PyResult<(Py<Graph>, Vec<Vec<Py<PyAny>>>, Vec<Py<PyAny>>)> {
    dispatch!(graph, |g, lab| {
        let bc = BlockCutpointGraph::new(g);
        let tree = bc.graph();
        let order: Vec<usize> = tree.vertices_cloned().collect();
        let index: std::collections::HashMap<usize, usize> =
            order.iter().enumerate().map(|(i, v)| (*v, i)).collect();
        let edges = tree
            .edges_cloned()
            .map(|e| {
                let (a, b) = tree.edge_endpoints(&e).expect("edge of the tree");
                (index[a], index[b], None)
            })
            .collect();
        let vertices = order
            .iter()
            .map(|v| (*v).into_py_any(py))
            .collect::<PyResult<Vec<_>>>()?;
        let out = Graph::from_parts(py, false, vertices, edges)?;
        let nodes = (0..order.len())
            .map(|n| {
                let mut vs: Vec<usize> = bc.node(n).iter().copied().collect();
                vs.sort_unstable();
                lab.vertices(py, vs)
            })
            .collect();
        Ok((out, nodes, lab.vertices(py, bc.cutpoints().iter().copied())))
    })
}

/// Whether the graph is connected (edge direction ignored).
#[pyfunction]
fn is_connected(graph: &Bound<'_, PyAny>) -> PyResult<bool> {
    dispatch!(graph, |g, _lab| Ok(props::is_connected(g)))
}

/// Whether a directed graph is weakly connected.
#[pyfunction]
fn is_weakly_connected(graph: &Bound<'_, PyAny>) -> PyResult<bool> {
    dispatch_directed!(graph, |g, _lab| Ok(props::is_weakly_connected(g)))
}

/// Whether a directed graph is strongly connected.
#[pyfunction]
fn is_strongly_connected(graph: &Bound<'_, PyAny>) -> PyResult<bool> {
    dispatch_directed!(graph, |g, _lab| Ok(props::is_strongly_connected(g)))
}

/// Whether the graph is connected and has no articulation point.
#[pyfunction]
fn is_biconnected(graph: &Bound<'_, PyAny>) -> PyResult<bool> {
    dispatch!(graph, |g, _lab| Ok(props::is_biconnected(g)))
}

/// The articulation points (cut vertices) of the graph, edge direction ignored.
#[pyfunction]
fn articulation_points(py: Python<'_>, graph: &Bound<'_, PyAny>) -> PyResult<Vec<Py<PyAny>>> {
    dispatch!(graph, |g, lab| Ok(
        lab.vertices(py, biconnectivity(g).articulation_points)
    ))
}

/// The bridges (cut edges) of the graph, edge direction ignored.
#[pyfunction]
fn bridges(py: Python<'_>, graph: &Bound<'_, PyAny>) -> PyResult<Vec<Py<PyAny>>> {
    dispatch!(graph, |g, lab| {
        Ok(lab.edges(py, biconnectivity(g).bridges.iter().map(|e| e.eid())))
    })
}

/// The biconnected components (blocks) as lists of vertices.
#[pyfunction]
fn biconnected_components(
    py: Python<'_>,
    graph: &Bound<'_, PyAny>,
) -> PyResult<Vec<Vec<Py<PyAny>>>> {
    dispatch!(graph, |g, lab| {
        Ok(rust_block_cut_tree(g)
            .blocks
            .into_iter()
            .map(|b| lab.vertices(py, b))
            .collect())
    })
}

/// The block-cut tree as ``(blocks, cut_vertices, edges)``: ``blocks`` are vertex lists,
/// ``cut_vertices`` the articulation points, and each edge a pair
/// ``(block_index, cut_vertex_index)``.
#[pyfunction]
#[allow(clippy::type_complexity)]
fn block_cut_tree(
    py: Python<'_>,
    graph: &Bound<'_, PyAny>,
) -> PyResult<(Vec<Vec<Py<PyAny>>>, Vec<Py<PyAny>>, Vec<(usize, usize)>)> {
    dispatch!(graph, |g, lab| {
        let t = rust_block_cut_tree(g);
        Ok((
            t.blocks.into_iter().map(|b| lab.vertices(py, b)).collect(),
            lab.vertices(py, t.cut_vertices),
            t.edges,
        ))
    })
}

/// The condensation of a directed graph as ``(dag, components)``: ``components[i]`` lists the
/// vertices of the ``i``-th strongly connected component, and ``dag`` is a directed
/// :class:`Graph` on ``0..len(components)`` with an edge between components joined by an edge.
#[pyfunction]
fn condensation(
    py: Python<'_>,
    graph: &Bound<'_, PyAny>,
) -> PyResult<(Py<Graph>, Vec<Vec<Py<PyAny>>>)> {
    dispatch_directed!(graph, |g, lab| {
        let (dag, comps) = rust_condensation(g);
        let vertices: Vec<Py<PyAny>> = dag
            .vertices()
            .map(|i| (*i).into_py_any(py))
            .collect::<PyResult<_>>()?;
        let edges = dag
            .edges_cloned()
            .map(|e| {
                let (s, t) = dag.edge_endpoints(&e).expect("edge of the condensation");
                (*s, *t, None)
            })
            .collect();
        let out = Graph::from_parts(py, true, vertices, edges)?;
        Ok((
            out,
            comps.into_iter().map(|c| lab.vertices(py, c)).collect(),
        ))
    })
}

/// The edge connectivity: the least number of edges whose removal disconnects the graph.
#[pyfunction]
fn edge_connectivity(graph: &Bound<'_, PyAny>) -> PyResult<usize> {
    dispatch!(graph, |g, _lab| Ok(
        KConnectivityFlowAlgorithm::new(g).edge_connectivity()
    ))
}

/// The vertex connectivity: the least number of vertices whose removal disconnects the graph.
#[pyfunction]
fn vertex_connectivity(graph: &Bound<'_, PyAny>) -> PyResult<usize> {
    dispatch!(graph, |g, _lab| {
        KConnectivityFlowAlgorithm::new(g)
            .vertex_connectivity()
            .map_err(graph_error)
    })
}

/// Whether the graph stays connected after removing any ``k - 1`` edges.
#[pyfunction]
fn is_k_edge_connected(graph: &Bound<'_, PyAny>, k: usize) -> PyResult<bool> {
    dispatch!(graph, |g, _lab| Ok(
        KConnectivityFlowAlgorithm::new(g).is_k_edge_connected(k)
    ))
}

/// Whether the graph stays connected after removing any ``k - 1`` vertices.
#[pyfunction]
fn is_k_vertex_connected(graph: &Bound<'_, PyAny>, k: usize) -> PyResult<bool> {
    dispatch!(graph, |g, _lab| {
        KConnectivityFlowAlgorithm::new(g)
            .is_k_vertex_connected(k)
            .map_err(graph_error)
    })
}

macro_rules! property {
    ($(#[$doc:meta])* $name:ident, $path:path) => {
        $(#[$doc])*
        #[pyfunction]
        fn $name(graph: &Bound<'_, PyAny>) -> PyResult<bool> {
            dispatch!(graph, |g, _lab| Ok($path(g)))
        }
    };
}

property!(
    /// Whether the graph has no cycle (edge direction ignored).
    is_forest, props::is_forest
);
property!(
    /// Whether the graph is connected and acyclic.
    is_tree, props::is_tree
);
property!(
    /// Whether the graph has at least one self-loop.
    has_self_loops, props::has_self_loops
);
property!(
    /// Whether the graph has parallel edges.
    has_multiple_edges, props::has_multiple_edges
);
property!(
    /// Whether the graph has neither self-loops nor parallel edges.
    is_simple, props::is_simple
);
property!(
    /// Whether every pair of distinct vertices is adjacent.
    is_complete, props::is_complete
);
property!(
    /// Whether the graph contains no triangle.
    is_triangle_free, props::is_triangle_free
);
property!(
    /// Whether every vertex has degree 3.
    is_cubic, props::is_cubic
);
property!(
    /// Whether the vertices split into a clique and an independent set.
    is_split, props::is_split
);

pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(connected_components, m)?)?;
    m.add_function(wrap_pyfunction!(connected_component_of, m)?)?;
    m.add_function(wrap_pyfunction!(path_exists, m)?)?;
    m.add_function(wrap_pyfunction!(block_cutpoint_graph, m)?)?;
    m.add_function(wrap_pyfunction!(strongly_connected_components, m)?)?;
    m.add_function(wrap_pyfunction!(is_connected, m)?)?;
    m.add_function(wrap_pyfunction!(is_weakly_connected, m)?)?;
    m.add_function(wrap_pyfunction!(is_strongly_connected, m)?)?;
    m.add_function(wrap_pyfunction!(is_biconnected, m)?)?;
    m.add_function(wrap_pyfunction!(articulation_points, m)?)?;
    m.add_function(wrap_pyfunction!(bridges, m)?)?;
    m.add_function(wrap_pyfunction!(biconnected_components, m)?)?;
    m.add_function(wrap_pyfunction!(block_cut_tree, m)?)?;
    m.add_function(wrap_pyfunction!(condensation, m)?)?;
    m.add_function(wrap_pyfunction!(edge_connectivity, m)?)?;
    m.add_function(wrap_pyfunction!(vertex_connectivity, m)?)?;
    m.add_function(wrap_pyfunction!(is_k_edge_connected, m)?)?;
    m.add_function(wrap_pyfunction!(is_k_vertex_connected, m)?)?;
    m.add_function(wrap_pyfunction!(is_forest, m)?)?;
    m.add_function(wrap_pyfunction!(is_tree, m)?)?;
    m.add_function(wrap_pyfunction!(has_self_loops, m)?)?;
    m.add_function(wrap_pyfunction!(has_multiple_edges, m)?)?;
    m.add_function(wrap_pyfunction!(is_simple, m)?)?;
    m.add_function(wrap_pyfunction!(is_complete, m)?)?;
    m.add_function(wrap_pyfunction!(is_triangle_free, m)?)?;
    m.add_function(wrap_pyfunction!(is_cubic, m)?)?;
    m.add_function(wrap_pyfunction!(is_split, m)?)?;
    Ok(())
}
