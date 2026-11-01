//! Graph, subgraph and tree isomorphism.
//!
//! Both graphs must be of the same kind (two `Graph` objects of the same directedness, or two
//! `SparseGraph` objects of the same directedness and weighting). The VF2 matchers reject
//! multigraphs, so a `SparseGraph`, which is a multigraph by type, is always rejected by them.

use std::cell::RefCell;
use std::cmp::Ordering;

use jgrapht::alg::isomorphism::{
    AhuForestIsomorphismInspector, AhuRootedTreeIsomorphismInspector,
    AhuUnrootedTreeIsomorphismInspector, ColorRefinementIsomorphismInspector,
    VF2GraphIsomorphismInspector, VF2SubgraphIsomorphismInspector,
};
use pyo3::prelude::*;
use pyo3::types::PyDict;

use crate::labels::{Labels, dispatch_pair, dispatch_pair_undirected};

use crate::error::{GraphError, graph_error};

/// Wraps an optional Python predicate as a comparator, remembering the first error it raises.
fn comparator<'a, T: 'a>(
    matcher: Option<&'a Bound<'a, PyAny>>,
    failure: &'a RefCell<Option<PyErr>>,
    convert: impl Fn(&T, &T) -> PyResult<bool> + 'a,
) -> Option<Box<dyn Fn(&T, &T) -> Ordering + 'a>> {
    matcher?;
    Some(Box::new(move |a: &T, b: &T| {
        if failure.borrow().is_some() {
            return Ordering::Less;
        }
        match convert(a, b) {
            Ok(true) => Ordering::Equal,
            Ok(false) => Ordering::Less,
            Err(e) => {
                *failure.borrow_mut() = Some(e);
                Ordering::Less
            }
        }
    }))
}

fn truthy(py: Python<'_>, f: &Bound<'_, PyAny>, a: Py<PyAny>, b: Py<PyAny>) -> PyResult<bool> {
    let _ = py;
    f.call1((a, b))?.is_truthy()
}

macro_rules! mappings {
    ($py:expr, $inspector:ty, $g1:expr, $g2:expr, $lab1:expr, $lab2:expr,
     $vertex_match:expr, $edge_match:expr, $limit:expr, $reverse:expr) => {{
        let failure: RefCell<Option<PyErr>> = RefCell::new(None);
        let py = $py;
        let vertex_cmp = comparator($vertex_match.as_ref(), &failure, |a: &usize, b: &usize| {
            truthy(
                py,
                $vertex_match.as_ref().expect("checked"),
                $lab1.vertex_obj(py, *a),
                $lab2.vertex_obj(py, *b),
            )
        });
        let edge_cmp = comparator($edge_match.as_ref(), &failure, |a, b| {
            truthy(
                py,
                $edge_match.as_ref().expect("checked"),
                $lab1.edge_obj(py, jgrapht_edge_id(a)),
                $lab2.edge_obj(py, jgrapht_edge_id(b)),
            )
        });
        let inspector = <$inspector>::with_options($g1, $g2, vertex_cmp, edge_cmp, true)
            .map_err(graph_error)?;
        let mut out: Vec<Py<PyAny>> = Vec::new();
        for mapping in inspector.iter() {
            if failure.borrow().is_some() || $limit.is_some_and(|l| out.len() >= l) {
                break;
            }
            let dict = PyDict::new(py);
            for (v1, v2) in mapping.forward_mapping() {
                let (k, v) = if $reverse { (v2, v1) } else { (v1, v2) };
                let (lk, lv) = if $reverse {
                    (&$lab2, &$lab1)
                } else {
                    (&$lab1, &$lab2)
                };
                dict.set_item(lk.vertex_obj(py, *k), lv.vertex_obj(py, *v))?;
            }
            out.push(dict.into_any().unbind());
        }
        let first_error = failure.borrow_mut().take();
        if let Some(e) = first_error {
            return Err(e);
        }
        Ok(out)
    }};
}

fn jgrapht_edge_id<E: crate::labels::EdgeId>(e: &E) -> u64 {
    e.eid()
}

/// All isomorphisms from ``graph1`` to ``graph2`` as ``{vertex_of_graph1: vertex_of_graph2}``
/// dicts (VF2). ``vertex_match(v1, v2)`` and ``edge_match(e1, e2)`` are optional predicates that
/// restrict which vertices / edges may be matched. ``limit`` caps the number of results.
#[pyfunction]
#[pyo3(signature = (graph1, graph2, vertex_match=None, edge_match=None, limit=None))]
fn isomorphisms(
    py: Python<'_>,
    graph1: &Bound<'_, PyAny>,
    graph2: &Bound<'_, PyAny>,
    vertex_match: Option<Bound<'_, PyAny>>,
    edge_match: Option<Bound<'_, PyAny>>,
    limit: Option<usize>,
) -> PyResult<Vec<Py<PyAny>>> {
    dispatch_pair!(graph1, graph2, |g1, g2, lab1, lab2| {
        mappings!(
            py,
            VF2GraphIsomorphismInspector<_>,
            g1,
            g2,
            lab1,
            lab2,
            vertex_match,
            edge_match,
            limit,
            false
        )
    })
}

/// Whether the two graphs are isomorphic (VF2); see :func:`isomorphisms` for the matchers.
#[pyfunction]
#[pyo3(signature = (graph1, graph2, vertex_match=None, edge_match=None))]
fn is_isomorphic(
    py: Python<'_>,
    graph1: &Bound<'_, PyAny>,
    graph2: &Bound<'_, PyAny>,
    vertex_match: Option<Bound<'_, PyAny>>,
    edge_match: Option<Bound<'_, PyAny>>,
) -> PyResult<bool> {
    Ok(!isomorphisms(py, graph1, graph2, vertex_match, edge_match, Some(1))?.is_empty())
}

/// All ways to embed ``pattern`` as an *induced* subgraph of ``graph``, as
/// ``{pattern_vertex: graph_vertex}`` dicts (VF2).
#[pyfunction]
#[pyo3(signature = (graph, pattern, vertex_match=None, edge_match=None, limit=None))]
fn subgraph_isomorphisms(
    py: Python<'_>,
    graph: &Bound<'_, PyAny>,
    pattern: &Bound<'_, PyAny>,
    vertex_match: Option<Bound<'_, PyAny>>,
    edge_match: Option<Bound<'_, PyAny>>,
    limit: Option<usize>,
) -> PyResult<Vec<Py<PyAny>>> {
    dispatch_pair!(graph, pattern, |g1, g2, lab1, lab2| {
        mappings!(
            py,
            VF2SubgraphIsomorphismInspector<_>,
            g1,
            g2,
            lab1,
            lab2,
            vertex_match,
            edge_match,
            limit,
            true
        )
    })
}

/// Whether ``pattern`` is isomorphic to an induced subgraph of ``graph``.
#[pyfunction]
#[pyo3(signature = (graph, pattern, vertex_match=None, edge_match=None))]
fn is_subgraph_isomorphic(
    py: Python<'_>,
    graph: &Bound<'_, PyAny>,
    pattern: &Bound<'_, PyAny>,
    vertex_match: Option<Bound<'_, PyAny>>,
    edge_match: Option<Bound<'_, PyAny>>,
) -> PyResult<bool> {
    Ok(!subgraph_isomorphisms(py, graph, pattern, vertex_match, edge_match, Some(1))?.is_empty())
}

/// An isomorphism between two trees (AHU algorithm) as a ``{vertex1: vertex2}`` dict, or
/// ``None`` if they are not isomorphic. Give both roots to treat the trees as rooted, or neither
/// to compare them as unrooted trees.
#[pyfunction]
#[pyo3(signature = (tree1, tree2, root1=None, root2=None))]
fn tree_isomorphism(
    py: Python<'_>,
    tree1: &Bound<'_, PyAny>,
    tree2: &Bound<'_, PyAny>,
    root1: Option<Bound<'_, PyAny>>,
    root2: Option<Bound<'_, PyAny>>,
) -> PyResult<Option<Py<PyDict>>> {
    match (&root1, &root2) {
        (Some(r1), Some(r2)) => dispatch_pair!(tree1, tree2, |g1, g2, lab1, lab2| {
            let (r1, r2) = (lab1.vertex_id(py, r1)?, lab2.vertex_id(py, r2)?);
            let mapping = AhuRootedTreeIsomorphismInspector::new(g1, &r1, g2, &r2)
                .map_err(graph_error)?
                .mapping()
                .map(|m| m.forward_mapping().clone());
            mapping_dict(py, &lab1, &lab2, mapping)
        }),
        (None, None) => dispatch_pair_undirected!(tree1, tree2, |g1, g2, lab1, lab2| {
            let mapping = AhuUnrootedTreeIsomorphismInspector::new(g1, g2)
                .map_err(graph_error)?
                .mapping()
                .map(|m| m.forward_mapping().clone());
            mapping_dict(py, &lab1, &lab2, mapping)
        }),
        _ => Err(GraphError::new_err("give both roots or neither")),
    }
}

fn mapping_dict(
    py: Python<'_>,
    lab1: &Labels<'_>,
    lab2: &Labels<'_>,
    mapping: Option<indexmap::IndexMap<usize, usize>>,
) -> PyResult<Option<Py<PyDict>>> {
    let Some(map) = mapping else { return Ok(None) };
    let dict = PyDict::new(py);
    for (v1, v2) in &map {
        dict.set_item(lab1.vertex_obj(py, *v1), lab2.vertex_obj(py, *v2))?;
    }
    Ok(Some(dict.unbind()))
}

/// An isomorphism between two rooted forests (AHU) as a ``{vertex1: vertex2}`` dict, or
/// ``None`` if they are not isomorphic. ``roots1`` and ``roots2`` list the root of each tree.
#[pyfunction]
fn forest_isomorphism(
    py: Python<'_>,
    forest1: &Bound<'_, PyAny>,
    forest2: &Bound<'_, PyAny>,
    roots1: Vec<Bound<'_, PyAny>>,
    roots2: Vec<Bound<'_, PyAny>>,
) -> PyResult<Option<Py<PyDict>>> {
    dispatch_pair!(forest1, forest2, |g1, g2, lab1, lab2| {
        let r1: Vec<usize> = roots1
            .iter()
            .map(|r| lab1.vertex_id(py, r))
            .collect::<PyResult<_>>()?;
        let r2: Vec<usize> = roots2
            .iter()
            .map(|r| lab2.vertex_id(py, r))
            .collect::<PyResult<_>>()?;
        let mapping = AhuForestIsomorphismInspector::new(g1, r1, g2, r2)
            .map_err(graph_error)?
            .mapping()
            .map(|m| m.forward_mapping().clone());
        mapping_dict(py, &lab1, &lab2, mapping)
    })
}

/// Decides isomorphism by color refinement (1-dimensional Weisfeiler-Leman). Returns
/// ``(True, mapping)`` or ``(False, None)`` when refinement decides, and ``(None, None)`` when it
/// cannot (it is complete only for graphs that refine to a discrete coloring and for forests).
#[pyfunction]
fn color_refinement_isomorphism(
    py: Python<'_>,
    graph1: &Bound<'_, PyAny>,
    graph2: &Bound<'_, PyAny>,
) -> PyResult<(Option<bool>, Option<Py<PyDict>>)> {
    dispatch_pair!(graph1, graph2, |g1, g2, lab1, lab2| {
        let mut inspector =
            ColorRefinementIsomorphismInspector::new(g1, g2).map_err(graph_error)?;
        match inspector.isomorphism_exists() {
            Err(_) => Ok((None, None)),
            Ok(false) => Ok((Some(false), None)),
            Ok(true) => {
                let mapping = inspector
                    .mappings()
                    .into_iter()
                    .next()
                    .map(|m| m.forward_mapping().clone());
                Ok((Some(true), mapping_dict(py, &lab1, &lab2, mapping)?))
            }
        }
    })
}

pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(forest_isomorphism, m)?)?;
    m.add_function(wrap_pyfunction!(color_refinement_isomorphism, m)?)?;
    m.add_function(wrap_pyfunction!(isomorphisms, m)?)?;
    m.add_function(wrap_pyfunction!(is_isomorphic, m)?)?;
    m.add_function(wrap_pyfunction!(subgraph_isomorphisms, m)?)?;
    m.add_function(wrap_pyfunction!(is_subgraph_isomorphic, m)?)?;
    m.add_function(wrap_pyfunction!(tree_isomorphism, m)?)?;
    Ok(())
}
