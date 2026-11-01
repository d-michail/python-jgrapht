//! Heavy-path and Dulmage-Mendelsohn decompositions.

use std::collections::HashSet;

use jgrapht::alg::decomposition::{
    DulmageMendelsohnDecomposition, HeavyPathDecomposition as RustHeavyPath,
};
use pyo3::prelude::*;
use pyo3::types::PyDict;

use crate::error::graph_error;
use crate::labels::{EdgeId, dispatch, dispatch_undirected};

/// A heavy-path decomposition of a rooted tree or forest.
#[pyclass(module = "jgrapht", frozen)]
pub struct HeavyPathDecomposition {
    parent: Py<PyDict>,
    depth: Py<PyDict>,
    subtree_size: Py<PyDict>,
    component: Py<PyDict>,
    heavy_edges: Vec<Py<PyAny>>,
    light_edges: Vec<Py<PyAny>>,
    paths: Vec<Vec<Py<PyAny>>>,
}

#[pymethods]
impl HeavyPathDecomposition {
    /// ``{vertex: parent}``; roots and vertices outside the forest map to ``None``.
    #[getter]
    fn parent(&self, py: Python<'_>) -> Py<PyDict> {
        self.parent.clone_ref(py)
    }

    /// ``{vertex: depth}``: the roots have depth 0 and every other vertex one more than its
    /// parent; vertices outside the forest map to ``None``.
    #[getter]
    fn depth(&self, py: Python<'_>) -> Py<PyDict> {
        self.depth.clone_ref(py)
    }

    /// ``{vertex: size of its subtree}``.
    #[getter]
    fn subtree_size(&self, py: Python<'_>) -> Py<PyDict> {
        self.subtree_size.clone_ref(py)
    }

    /// ``{vertex: index of its tree}``; ``None`` for vertices outside the forest.
    #[getter]
    fn component(&self, py: Python<'_>) -> Py<PyDict> {
        self.component.clone_ref(py)
    }

    /// The heavy edges: those whose child holds more than half of its parent's subtree.
    #[getter]
    fn heavy_edges(&self, py: Python<'_>) -> Vec<Py<PyAny>> {
        self.heavy_edges.iter().map(|e| e.clone_ref(py)).collect()
    }

    /// The light edges.
    #[getter]
    fn light_edges(&self, py: Python<'_>) -> Vec<Py<PyAny>> {
        self.light_edges.iter().map(|e| e.clone_ref(py)).collect()
    }

    /// The vertex lists of the heavy paths.
    #[getter]
    fn paths(&self, py: Python<'_>) -> Vec<Vec<Py<PyAny>>> {
        self.paths
            .iter()
            .map(|p| p.iter().map(|v| v.clone_ref(py)).collect())
            .collect()
    }

    fn __repr__(&self) -> String {
        format!("HeavyPathDecomposition(paths={})", self.paths.len())
    }
}

/// The heavy-path decomposition of the tree or forest rooted at ``roots``: one root vertex, or a
/// ``list`` of root vertices for a forest.
#[pyfunction]
fn heavy_path_decomposition(
    py: Python<'_>,
    graph: &Bound<'_, PyAny>,
    roots: Bound<'_, PyAny>,
) -> PyResult<HeavyPathDecomposition> {
    dispatch!(graph, |g, lab| {
        // a list means several roots; anything else (including a tuple) is one root vertex
        let root_ids: Vec<usize> = match roots.cast::<pyo3::types::PyList>() {
            Ok(list) => list
                .iter()
                .map(|r| lab.vertex_id(py, &r))
                .collect::<PyResult<_>>()?,
            Err(_) => vec![lab.vertex_id(py, &roots)?],
        };
        let d = RustHeavyPath::with_roots(g, root_ids).map_err(graph_error)?;
        let (parent, depth, size, component) = (
            PyDict::new(py),
            PyDict::new(py),
            PyDict::new(py),
            PyDict::new(py),
        );
        for v in d.index_list() {
            let key = lab.vertex_obj(py, *v);
            parent.set_item(&key, d.parent_of(v).map(|p| lab.vertex_obj(py, *p)))?;
            depth.set_item(&key, d.depth_of(v))?;
            size.set_item(&key, d.subtree_size_of(v))?;
            component.set_item(&key, d.component_of(v))?;
        }
        let decomposition = d.path_decomposition().map_err(graph_error)?;
        let paths = decomposition
            .paths()
            .iter()
            .map(|w| lab.vertices(py, w.vertex_list().iter().copied()))
            .collect();
        Ok(HeavyPathDecomposition {
            parent: parent.unbind(),
            depth: depth.unbind(),
            subtree_size: size.unbind(),
            component: component.unbind(),
            heavy_edges: lab.edges(py, d.heavy_edges().iter().map(|e| e.eid())),
            light_edges: lab.edges(py, d.light_edges().iter().map(|e| e.eid())),
            paths,
        })
    })
}

/// The Dulmage-Mendelsohn decomposition of a bipartite graph with sides ``left`` and ``right``
/// as ``(left_dominated, right_dominated, perfectly_matched_sets)``. With ``fine`` the
/// perfectly matched part is split into its irreducible blocks. Each dominated set holds the
/// unmatched vertices of its side together with everything reachable from them by alternating
/// paths, so it can contain vertices of both sides.
#[pyfunction]
#[pyo3(signature = (graph, left, right, fine=false))]
#[allow(clippy::type_complexity)]
fn dulmage_mendelsohn_decomposition(
    py: Python<'_>,
    graph: &Bound<'_, PyAny>,
    left: Vec<Bound<'_, PyAny>>,
    right: Vec<Bound<'_, PyAny>>,
    fine: bool,
) -> PyResult<(Vec<Py<PyAny>>, Vec<Py<PyAny>>, Vec<Vec<Py<PyAny>>>)> {
    dispatch_undirected!(graph, |g, lab| {
        let ids = |side: &[Bound<'_, PyAny>]| -> PyResult<HashSet<usize>> {
            side.iter().map(|v| lab.vertex_id(py, v)).collect()
        };
        let d = DulmageMendelsohnDecomposition::new(g, ids(&left)?, ids(&right)?)
            .decomposition(fine)
            .map_err(graph_error)?;
        let sorted = |s: HashSet<usize>| {
            let mut v: Vec<usize> = s.into_iter().collect();
            v.sort_unstable();
            v
        };
        Ok((
            lab.vertices(py, sorted(d.partition1_dominated)),
            lab.vertices(py, sorted(d.partition2_dominated)),
            d.perfect_matched_sets
                .into_iter()
                .map(|s| lab.vertices(py, sorted(s)))
                .collect(),
        ))
    })
}

pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<HeavyPathDecomposition>()?;
    m.add_function(wrap_pyfunction!(heavy_path_decomposition, m)?)?;
    m.add_function(wrap_pyfunction!(dulmage_mendelsohn_decomposition, m)?)?;
    Ok(())
}
