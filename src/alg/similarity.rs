//! Link prediction, SimRank and tree edit distance.

use std::cell::RefCell;

use jgrapht::alg::linkprediction::{Measure, pair_score, predict, simrank as rust_simrank};
use jgrapht::alg::similarity::ZhangShashaTreeEditDistance;
use pyo3::prelude::*;
use pyo3::types::PyDict;

use crate::error::GraphError;
use crate::labels::{dispatch, dispatch_pair};

fn measure(name: &str) -> PyResult<Measure> {
    Ok(match name {
        "common_neighbors" => Measure::CommonNeighbors,
        "total_neighbors" => Measure::TotalNeighbors,
        "jaccard" => Measure::Jaccard,
        "sorensen" => Measure::Sorensen,
        "salton" => Measure::Salton,
        "hub_promoted" => Measure::HubPromoted,
        "hub_depressed" => Measure::HubDepressed,
        "leicht_holme_newman" => Measure::LeichtHolmeNewman,
        "preferential_attachment" => Measure::PreferentialAttachment,
        "adamic_adar" => Measure::AdamicAdar,
        "resource_allocation" => Measure::ResourceAllocation,
        other => return Err(GraphError::new_err(format!("unknown measure {other:?}"))),
    })
}

/// Score of the possible link between ``u`` and ``v``. ``measure`` is one of
/// ``"common_neighbors"`` (default), ``"total_neighbors"``, ``"jaccard"``, ``"sorensen"``,
/// ``"salton"``, ``"hub_promoted"``, ``"hub_depressed"``, ``"leicht_holme_newman"``,
/// ``"preferential_attachment"``, ``"adamic_adar"`` and ``"resource_allocation"``.
#[pyfunction]
#[pyo3(signature = (graph, u, v, measure_name="common_neighbors"))]
fn link_score(
    py: Python<'_>,
    graph: &Bound<'_, PyAny>,
    u: Bound<'_, PyAny>,
    v: Bound<'_, PyAny>,
    measure_name: &str,
) -> PyResult<f64> {
    let m = measure(measure_name)?;
    dispatch!(graph, |g, lab| {
        let (u, v) = (lab.vertex_id(py, &u)?, lab.vertex_id(py, &v)?);
        pair_score(g, m, &u, &v).ok_or_else(|| GraphError::new_err("vertex not found in graph"))
    })
}

/// All non-neighbours of ``u`` with their link prediction score, best first, as a list of
/// ``(vertex, score)``. See :func:`link_score` for ``measure_name``.
#[pyfunction]
#[pyo3(signature = (graph, u, measure_name="common_neighbors"))]
fn predict_links(
    py: Python<'_>,
    graph: &Bound<'_, PyAny>,
    u: Bound<'_, PyAny>,
    measure_name: &str,
) -> PyResult<Vec<(Py<PyAny>, f64)>> {
    let m = measure(measure_name)?;
    dispatch!(graph, |g, lab| {
        let u = lab.vertex_id(py, &u)?;
        let scored =
            predict(g, m, &u).ok_or_else(|| GraphError::new_err("vertex not found in graph"))?;
        Ok(scored
            .into_iter()
            .map(|(v, s)| (lab.vertex_obj(py, v), s))
            .collect())
    })
}

/// SimRank similarity of every pair of vertices as ``{(u, v): score}``.
#[pyfunction]
#[pyo3(signature = (graph, decay=0.8, iterations=10))]
fn simrank<'py>(
    py: Python<'py>,
    graph: &Bound<'py, PyAny>,
    decay: f64,
    iterations: usize,
) -> PyResult<Bound<'py, PyDict>> {
    dispatch!(graph, |g, lab| {
        let out = PyDict::new(py);
        for ((u, v), score) in rust_simrank(g, decay, iterations) {
            out.set_item((lab.vertex_obj(py, u), lab.vertex_obj(py, v)), score)?;
        }
        Ok(out)
    })
}

/// Zhang-Shasha edit distance between two rooted ordered trees. The cost of changing a vertex
/// of ``tree1`` into one of ``tree2`` is ``change_cost(v1, v2)`` (default: 0 if the two vertex
/// objects are equal, else 1); inserting or removing a vertex costs ``insert_cost(v)`` /
/// ``remove_cost(v)`` (default 1). Note that, as in JGraphT, the edit table charges
/// ``remove_cost`` for the insertions along its border, so ``insert_cost`` and ``remove_cost``
/// should be equal for the distance to be symmetric.
#[pyfunction]
#[pyo3(signature = (tree1, tree2, root1, root2, change_cost=None, insert_cost=None, remove_cost=None))]
#[allow(clippy::too_many_arguments)]
fn tree_edit_distance(
    py: Python<'_>,
    tree1: &Bound<'_, PyAny>,
    tree2: &Bound<'_, PyAny>,
    root1: Bound<'_, PyAny>,
    root2: Bound<'_, PyAny>,
    change_cost: Option<Bound<'_, PyAny>>,
    insert_cost: Option<Bound<'_, PyAny>>,
    remove_cost: Option<Bound<'_, PyAny>>,
) -> PyResult<f64> {
    dispatch_pair!(tree1, tree2, |g1, g2, lab1, lab2| {
        let (r1, r2) = (lab1.vertex_id(py, &root1)?, lab2.vertex_id(py, &root2)?);
        let failure: RefCell<Option<PyErr>> = RefCell::new(None);
        let number = |f: &Bound<'_, PyAny>, args: Vec<Py<PyAny>>| -> f64 {
            if failure.borrow().is_some() {
                return 0.0;
            }
            let result = f
                .call1(pyo3::types::PyTuple::new(py, args).expect("tuple"))
                .and_then(|r| r.extract::<f64>());
            result.unwrap_or_else(|e| {
                *failure.borrow_mut() = Some(e);
                0.0
            })
        };
        let change = |a: &usize, b: &usize| -> f64 {
            match &change_cost {
                Some(f) => number(f, vec![lab1.vertex_obj(py, *a), lab2.vertex_obj(py, *b)]),
                None => {
                    let (x, y) = (lab1.vertex_obj(py, *a), lab2.vertex_obj(py, *b));
                    match x.bind(py).eq(y.bind(py)) {
                        Ok(true) => 0.0,
                        Ok(false) => 1.0,
                        Err(e) => {
                            *failure.borrow_mut() = Some(e);
                            0.0
                        }
                    }
                }
            }
        };
        let insert = |v: &usize| match &insert_cost {
            Some(f) => number(f, vec![lab2.vertex_obj(py, *v)]),
            None => 1.0,
        };
        let remove = |v: &usize| match &remove_cost {
            Some(f) => number(f, vec![lab1.vertex_obj(py, *v)]),
            None => 1.0,
        };
        let mut a = ZhangShashaTreeEditDistance::with_costs(g1, r1, g2, r2, insert, remove, change)
            .map_err(crate::error::graph_error)?;
        let distance = a.distance();
        let first_error = failure.borrow_mut().take();
        match first_error {
            Some(e) => Err(e),
            None => Ok(distance),
        }
    })
}

pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(link_score, m)?)?;
    m.add_function(wrap_pyfunction!(predict_links, m)?)?;
    m.add_function(wrap_pyfunction!(simrank, m)?)?;
    m.add_function(wrap_pyfunction!(tree_edit_distance, m)?)?;
    Ok(())
}
