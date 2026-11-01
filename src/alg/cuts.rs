//! Minimum cuts and cut trees.

use indexmap::IndexSet;
use jgrapht::alg::flow::{
    BoykovKolmogorov, Dinic, EdmondsKarp, GusfieldEquivalentFlowTree, GusfieldGomoryHuCutTree,
    MinimumStCutAlgorithm, PadbergRaoOddMinimumCutset, PushRelabel,
};
use jgrapht::alg::stoer_wagner::StoerWagnerMinimumCut;
use jgrapht::{Graph as _, GraphExt as _};
use pyo3::prelude::*;

use crate::error::{GraphError, graph_error};
use crate::graph::Graph;
use crate::labels::{EdgeId, dispatch, dispatch_undirected};

/// A minimum cut: a partition of the vertices into a source side and a sink side.
#[pyclass(module = "jgrapht", frozen)]
pub struct MinimumCut {
    capacity: f64,
    source_partition: Vec<Py<PyAny>>,
    sink_partition: Vec<Py<PyAny>>,
    cut_edges: Vec<Py<PyAny>>,
}

#[pymethods]
impl MinimumCut {
    /// The total capacity (weight) of the cut edges.
    #[getter]
    fn capacity(&self) -> f64 {
        self.capacity
    }

    /// The vertices on the source side.
    #[getter]
    fn source_partition(&self, py: Python<'_>) -> Vec<Py<PyAny>> {
        self.source_partition
            .iter()
            .map(|v| v.clone_ref(py))
            .collect()
    }

    /// The vertices on the sink side.
    #[getter]
    fn sink_partition(&self, py: Python<'_>) -> Vec<Py<PyAny>> {
        self.sink_partition
            .iter()
            .map(|v| v.clone_ref(py))
            .collect()
    }

    /// The edges crossing the cut.
    #[getter]
    fn cut_edges(&self, py: Python<'_>) -> Vec<Py<PyAny>> {
        self.cut_edges.iter().map(|e| e.clone_ref(py)).collect()
    }

    fn __repr__(&self) -> String {
        format!(
            "MinimumCut(capacity={:?}, cut_edges={})",
            self.capacity,
            self.cut_edges.len()
        )
    }
}

macro_rules! to_cut {
    ($py:expr, $lab:expr, $cut:expr) => {{
        let c = $cut;
        MinimumCut {
            capacity: c.capacity(),
            source_partition: $lab.vertices($py, c.source_partition().iter().copied()),
            sink_partition: $lab.vertices($py, c.sink_partition().iter().copied()),
            cut_edges: $lab.edges($py, c.cut_edges().iter().map(|e| e.eid())),
        }
    }};
}

fn unknown(name: &str) -> PyErr {
    GraphError::new_err(format!("unknown algorithm {name:?}"))
}

/// A minimum ``source``-``sink`` cut, using edge weights as capacities. ``algorithm`` is
/// ``"dinic"`` (default), ``"edmonds_karp"``, ``"push_relabel"`` or ``"boykov_kolmogorov"``.
#[pyfunction]
#[pyo3(signature = (graph, source, sink, algorithm="dinic"))]
fn minimum_st_cut(
    py: Python<'_>,
    graph: &Bound<'_, PyAny>,
    source: Bound<'_, PyAny>,
    sink: Bound<'_, PyAny>,
    algorithm: &str,
) -> PyResult<MinimumCut> {
    dispatch!(graph, |g, lab| {
        let (s, t) = (lab.vertex_id(py, &source)?, lab.vertex_id(py, &sink)?);
        let cut = match algorithm {
            "dinic" => Dinic::new(g).and_then(|mut a| a.minimum_cut(&s, &t)),
            "edmonds_karp" => EdmondsKarp::new(g).and_then(|mut a| a.minimum_cut(&s, &t)),
            "push_relabel" => PushRelabel::new(g).and_then(|mut a| a.minimum_cut(&s, &t)),
            "boykov_kolmogorov" => BoykovKolmogorov::new(g).and_then(|mut a| a.minimum_cut(&s, &t)),
            other => return Err(unknown(other)),
        }
        .map_err(graph_error)?;
        Ok(to_cut!(py, lab, cut))
    })
}

/// The global minimum cut of an undirected weighted graph (Stoer-Wagner) as
/// ``(weight, one_side)``; ``one_side`` is the vertices on one side of the cut.
#[pyfunction]
fn stoer_wagner_minimum_cut(
    py: Python<'_>,
    graph: &Bound<'_, PyAny>,
) -> PyResult<(f64, Vec<Py<PyAny>>)> {
    dispatch_undirected!(graph, |g, lab| {
        let c = StoerWagnerMinimumCut::new(g).map_err(graph_error)?;
        Ok((
            c.min_cut_weight(),
            lab.vertices(py, c.min_cut().iter().copied()),
        ))
    })
}

fn tree_to_graph(
    py: Python<'_>,
    lab: &crate::labels::Labels<'_>,
    tree: &jgrapht::UGraph<usize>,
) -> PyResult<Py<Graph>> {
    let ids: Vec<usize> = tree.vertices().copied().collect();
    let index: std::collections::HashMap<usize, usize> =
        ids.iter().enumerate().map(|(i, v)| (*v, i)).collect();
    let vertices = ids.iter().map(|v| lab.vertex_obj(py, *v)).collect();
    let edges = tree
        .edges_cloned()
        .map(|e| {
            let (s, t) = tree.edge_endpoints(&e).expect("edge of the tree");
            (index[s], index[t], Some(tree.weight_of(&e)))
        })
        .collect();
    Graph::from_parts(py, false, vertices, edges)
}

/// The Gomory-Hu cut tree of an undirected graph (Gusfield) as a weighted :class:`Graph`: the
/// minimum cut between two vertices equals the lightest edge on the tree path between them.
#[pyfunction]
fn gomory_hu_tree(py: Python<'_>, graph: &Bound<'_, PyAny>) -> PyResult<Py<Graph>> {
    dispatch_undirected!(graph, |g, lab| {
        let tree = GusfieldGomoryHuCutTree::new(g)
            .and_then(|mut a| a.gomory_hu_tree())
            .map_err(graph_error)?;
        tree_to_graph(py, &lab, &tree)
    })
}

/// The equivalent flow tree of an undirected graph (Gusfield) as a weighted :class:`Graph`: the
/// maximum flow between two vertices equals the lightest edge on the tree path between them.
#[pyfunction]
fn equivalent_flow_tree(py: Python<'_>, graph: &Bound<'_, PyAny>) -> PyResult<Py<Graph>> {
    dispatch_undirected!(graph, |g, lab| {
        let tree = GusfieldEquivalentFlowTree::new(g)
            .and_then(|mut a| a.equivalent_flow_tree())
            .map_err(graph_error)?;
        tree_to_graph(py, &lab, &tree)
    })
}

/// The minimum cut of an undirected graph that separates the given vertices (an even number
/// of "odd" vertices) into two odd-sized sets (Padberg-Rao), or ``None`` if there are none.
#[pyfunction]
#[pyo3(signature = (graph, odd_vertices, use_tree_compression=false))]
fn minimum_odd_cut(
    py: Python<'_>,
    graph: &Bound<'_, PyAny>,
    odd_vertices: Vec<Bound<'_, PyAny>>,
    use_tree_compression: bool,
) -> PyResult<Option<MinimumCut>> {
    dispatch_undirected!(graph, |g, lab| {
        let odd: IndexSet<usize> = odd_vertices
            .iter()
            .map(|v| lab.vertex_id(py, v))
            .collect::<PyResult<_>>()?;
        let cut = PadbergRaoOddMinimumCutset::new(g)
            .and_then(|mut a| a.minimum_odd_cut(odd, use_tree_compression))
            .map_err(graph_error)?;
        Ok(cut.map(|c| to_cut!(py, lab, c)))
    })
}

pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<MinimumCut>()?;
    m.add_function(wrap_pyfunction!(minimum_st_cut, m)?)?;
    m.add_function(wrap_pyfunction!(stoer_wagner_minimum_cut, m)?)?;
    m.add_function(wrap_pyfunction!(gomory_hu_tree, m)?)?;
    m.add_function(wrap_pyfunction!(equivalent_flow_tree, m)?)?;
    m.add_function(wrap_pyfunction!(minimum_odd_cut, m)?)?;
    Ok(())
}
