//! Capacitated minimum spanning trees and cyclic-exchange local augmentation.

use std::collections::HashMap;

use jgrapht::GraphExt as _;
use jgrapht::alg::capacitated::{
    AhujaOrlinSharma, AhujaOrlinSharmaOptions, CapacitatedSpanningTreeAlgorithm, EsauWilliams,
};
use jgrapht::alg::cyclic_exchange::AhujaOrlinSharmaCyclicExchange;
use pyo3::prelude::*;
use pyo3::types::PyDict;

use crate::error::{GraphError, graph_error};
use crate::graph::GraphPath;
use crate::labels::{EdgeId, dispatch, dispatch_directed, spec_value};

/// A capacitated spanning tree: the tree edges grouped into the subtrees hanging off the root.
#[pyclass(module = "jgrapht", frozen)]
pub struct CapacitatedSpanningTree {
    edges: Vec<Py<PyAny>>,
    weight: f64,
    partition: Vec<(Vec<Py<PyAny>>, f64)>,
    labels: Py<PyDict>,
}

#[pymethods]
impl CapacitatedSpanningTree {
    /// The edges of the tree.
    #[getter]
    fn edges(&self, py: Python<'_>) -> Vec<Py<PyAny>> {
        self.edges.iter().map(|e| e.clone_ref(py)).collect()
    }

    /// The total weight of the tree.
    #[getter]
    fn weight(&self) -> f64 {
        self.weight
    }

    /// The subtrees below the root as ``[(vertices, total_demand), ...]``.
    #[getter]
    fn partition(&self, py: Python<'_>) -> Vec<(Vec<Py<PyAny>>, f64)> {
        self.partition
            .iter()
            .map(|(vs, d)| (vs.iter().map(|v| v.clone_ref(py)).collect(), *d))
            .collect()
    }

    /// ``{vertex: index of its subtree in partition}`` for every vertex except the root.
    #[getter]
    fn labels(&self, py: Python<'_>) -> Py<PyDict> {
        self.labels.clone_ref(py)
    }

    fn __repr__(&self) -> String {
        format!(
            "CapacitatedSpanningTree(subtrees={}, weight={:?})",
            self.partition.len(),
            self.weight
        )
    }
}

/// A minimum spanning tree in which every subtree hanging off ``root`` has total demand at most
/// ``capacity`` (a heuristic; the tree is not necessarily optimal).
///
/// ``demands`` gives each vertex's demand as a dict (missing vertices demand 1), a callable or a
/// constant. ``algorithm`` is ``"esau_williams"`` (default) or ``"ahuja_orlin_sharma"``
/// (a local search whose ``length_bound``, ``best_improvement``, ``use_vertex_operation``,
/// ``use_subtree_operation``, ``use_tabu_search``, ``tabu_time`` and
/// ``upper_limit_tabu_exchanges`` tune the search). ``number_of_operations`` is the number of
/// randomized restarts / passes and ``seed`` makes the run reproducible (Esau-Williams).
#[pyfunction]
#[pyo3(signature = (
    graph, root, capacity, demands, algorithm="esau_williams", number_of_operations=1, seed=None,
    length_bound=3, best_improvement=false, use_vertex_operation=true, use_subtree_operation=true,
    use_tabu_search=true, tabu_time=10, upper_limit_tabu_exchanges=50,
))]
#[allow(clippy::too_many_arguments)]
fn capacitated_minimum_spanning_tree(
    py: Python<'_>,
    graph: &Bound<'_, PyAny>,
    root: Bound<'_, PyAny>,
    capacity: f64,
    demands: Bound<'_, PyAny>,
    algorithm: &str,
    number_of_operations: usize,
    seed: Option<u64>,
    length_bound: usize,
    best_improvement: bool,
    use_vertex_operation: bool,
    use_subtree_operation: bool,
    use_tabu_search: bool,
    tabu_time: usize,
    upper_limit_tabu_exchanges: usize,
) -> PyResult<CapacitatedSpanningTree> {
    dispatch!(graph, |g, lab| {
        let r = lab.vertex_id(py, &root)?;
        let mut d: HashMap<usize, f64> = HashMap::new();
        for v in g.vertices_cloned() {
            d.insert(v, spec_value(&demands, lab.vertex_obj(py, v), 1.0)?);
        }
        let tree = match algorithm {
            "esau_williams" => {
                let mut a = EsauWilliams::new(g, r, capacity, d, number_of_operations)
                    .map_err(graph_error)?;
                if let Some(s) = seed {
                    a = a.with_seed(s);
                }
                a.capacitated_spanning_tree()
            }
            "ahuja_orlin_sharma" => {
                let options = AhujaOrlinSharmaOptions {
                    best_improvement,
                    number_of_operations,
                    use_vertex_operation,
                    use_subtree_operation,
                    use_tabu_search,
                    tabu_time,
                    upper_limit_tabu_exchanges,
                };
                AhujaOrlinSharma::with_options(g, r, capacity, d, length_bound, options)
                    .and_then(|mut a| a.capacitated_spanning_tree())
            }
            other => return Err(GraphError::new_err(format!("unknown algorithm {other:?}"))),
        }
        .map_err(graph_error)?;
        let mut keys: Vec<usize> = tree.partition.keys().copied().collect();
        keys.sort_unstable();
        let index: HashMap<usize, usize> = keys.iter().enumerate().map(|(i, k)| (*k, i)).collect();
        let relabelled = PyDict::new(py);
        for (v, l) in &tree.labels {
            relabelled.set_item(lab.vertex_obj(py, *v), index[l])?;
        }
        Ok(CapacitatedSpanningTree {
            edges: lab.edges(py, tree.edges.iter().map(|e| e.eid())),
            weight: tree.weight,
            partition: keys
                .iter()
                .map(|k| {
                    let part = &tree.partition[k];
                    (lab.vertices(py, part.first.iter().copied()), part.second)
                })
                .collect(),
            labels: relabelled.unbind(),
        })
    })
}

/// A negative-cost improving cycle for the cyclic-exchange neighbourhood of Ahuja, Orlin and
/// Sharma: a cycle in the directed graph whose vertices all carry distinct ``labels`` (a dict
/// ``{vertex: int}`` covering every vertex), of at most ``length_bound`` vertices. Returns the
/// cycle as a :class:`GraphPath`, or ``None`` if there is no such cycle of negative cost.
#[pyfunction]
#[pyo3(signature = (graph, labels, length_bound, best_improvement=false))]
fn cyclic_exchange_augmentation(
    py: Python<'_>,
    graph: &Bound<'_, PyAny>,
    labels: &Bound<'_, PyDict>,
    length_bound: usize,
    best_improvement: bool,
) -> PyResult<Option<GraphPath>> {
    dispatch_directed!(graph, |g, lab| {
        let mut map: HashMap<usize, i64> = HashMap::new();
        for (v, l) in labels.iter() {
            map.insert(lab.vertex_id(py, &v)?, l.extract()?);
        }
        let a = AhujaOrlinSharmaCyclicExchange::new(g, length_bound, &map, best_improvement)
            .map_err(graph_error)?;
        let cycle = a.local_augmentation_cycle();
        // the backend reports "no improving cycle" as an empty walk of enormous weight
        Ok((!cycle.vertex_list().is_empty()).then(|| lab.path(py, &cycle)))
    })
}

pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<CapacitatedSpanningTree>()?;
    m.add_function(wrap_pyfunction!(capacitated_minimum_spanning_tree, m)?)?;
    m.add_function(wrap_pyfunction!(cyclic_exchange_augmentation, m)?)?;
    Ok(())
}
