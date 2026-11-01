//! Translation between Python objects and the integer ids used by the Rust graphs.

use jgrapht::DefaultEdge;
use pyo3::prelude::*;
use pyo3::types::PyDict;

use crate::error::GraphError;
use crate::graph::{Graph, GraphPath};
use crate::sparse::SparseGraph;

/// Edge types that can be reported to Python as a `u64` id.
pub trait EdgeId {
    fn eid(&self) -> u64;
    /// The edge with the given id (the inverse of [`EdgeId::eid`]).
    fn from_eid(id: u64) -> Self;
}

impl EdgeId for usize {
    fn eid(&self) -> u64 {
        *self as u64
    }
    fn from_eid(id: u64) -> Self {
        id as usize
    }
}

impl EdgeId for DefaultEdge {
    fn eid(&self) -> u64 {
        self.0
    }
    fn from_eid(id: u64) -> Self {
        DefaultEdge(id)
    }
}

/// How vertices and edges of a Python-visible graph map to and from Python objects.
pub enum Labels<'a> {
    /// Arbitrary hashable objects, stored in the graph.
    Dynamic(&'a Graph),
    /// The integers `0..n` (vertices) and `0..m` (edges).
    Sparse(&'a SparseGraph),
}

impl Labels<'_> {
    /// The attribute stores of the graph.
    pub fn attrs(&self) -> &crate::attrs::Attrs {
        match self {
            Labels::Dynamic(g) => g.attrs_ref(),
            Labels::Sparse(g) => g.attrs_ref(),
        }
    }

    pub fn vertex_id(&self, py: Python<'_>, v: &Bound<'_, PyAny>) -> PyResult<usize> {
        match self {
            Labels::Dynamic(g) => g.id_of(py, v),
            Labels::Sparse(g) => g.check_vertex(v),
        }
    }

    /// The id of an edge given as a Python object, or an error if the graph has no such edge.
    pub fn edge_id(&self, py: Python<'_>, e: &Bound<'_, PyAny>) -> PyResult<u64> {
        match self {
            Labels::Dynamic(g) => g.edge_id(py, e),
            Labels::Sparse(g) => g.check_edge_obj(e).map(|id| id as u64),
        }
    }

    pub fn vertex_obj(&self, py: Python<'_>, id: usize) -> Py<PyAny> {
        match self {
            Labels::Dynamic(g) => g.vertex_obj(py, id),
            Labels::Sparse(_) => id
                .into_pyobject(py)
                .expect("int conversion")
                .into_any()
                .unbind(),
        }
    }

    pub fn edge_obj(&self, py: Python<'_>, id: u64) -> Py<PyAny> {
        match self {
            Labels::Dynamic(g) => g.edge_obj(py, id),
            Labels::Sparse(_) => id
                .into_pyobject(py)
                .expect("int conversion")
                .into_any()
                .unbind(),
        }
    }

    /// A `{vertex: value}` dict.
    pub fn vertex_dict<'py, T: for<'a> IntoPyObject<'a>>(
        &self,
        py: Python<'py>,
        items: impl IntoIterator<Item = (usize, T)>,
    ) -> PyResult<Bound<'py, PyDict>> {
        let out = PyDict::new(py);
        for (id, value) in items {
            out.set_item(self.vertex_obj(py, id), value)?;
        }
        Ok(out)
    }

    /// A `{edge: value}` dict.
    pub fn edge_dict<'py, T: for<'a> IntoPyObject<'a>>(
        &self,
        py: Python<'py>,
        items: impl IntoIterator<Item = (u64, T)>,
    ) -> PyResult<Bound<'py, PyDict>> {
        let out = PyDict::new(py);
        for (id, value) in items {
            out.set_item(self.edge_obj(py, id), value)?;
        }
        Ok(out)
    }

    /// Converts a Rust walk into a [`GraphPath`].
    pub fn path<E: EdgeId>(&self, py: Python<'_>, w: &jgrapht::GraphWalk<usize, E>) -> GraphPath {
        GraphPath::new(
            self.vertices(py, w.vertex_list().iter().copied()),
            self.edges(py, w.edge_list().iter().map(|e| e.eid())),
            w.weight(),
        )
    }

    pub fn vertices(&self, py: Python<'_>, ids: impl IntoIterator<Item = usize>) -> Vec<Py<PyAny>> {
        ids.into_iter().map(|id| self.vertex_obj(py, id)).collect()
    }

    pub fn edges(&self, py: Python<'_>, ids: impl IntoIterator<Item = u64>) -> Vec<Py<PyAny>> {
        ids.into_iter().map(|id| self.edge_obj(py, id)).collect()
    }
}

pub fn type_error(obj: &Bound<'_, PyAny>) -> PyErr {
    pyo3::exceptions::PyTypeError::new_err(format!(
        "expected a Graph or SparseGraph, got {}",
        obj.get_type()
            .name()
            .map(|n| n.to_string())
            .unwrap_or_default()
    ))
}

pub fn not_found(what: &str, obj: &Bound<'_, PyAny>) -> PyErr {
    let repr = obj.repr().map(|r| r.to_string()).unwrap_or_default();
    GraphError::new_err(format!("{what} {repr} not found in graph"))
}

/// Runs `$body` once per concrete Rust graph type behind a `Graph` or `SparseGraph` Python object,
/// with `$g` bound to the Rust graph (vertex type `usize`) and `$lab` to its [`Labels`].
macro_rules! dispatch {
    ($obj:expr, |$g:ident, $lab:ident| $body:expr) => {{
        let obj = &$crate::unmodifiable::unwrap_readonly($obj);
        if let Ok(gr) = obj.extract::<::pyo3::PyRef<'_, $crate::graph::Graph>>() {
            let $lab = $crate::labels::Labels::Dynamic(&gr);
            match gr.inner() {
                $crate::graph::Inner::Undirected($g) => $body,
                $crate::graph::Inner::Directed($g) => $body,
            }
        } else if let Ok(sg) = obj.extract::<::pyo3::PyRef<'_, $crate::sparse::SparseGraph>>() {
            let $lab = $crate::labels::Labels::Sparse(&sg);
            match sg.inner() {
                $crate::sparse::SparseInner::Undirected($g) => $body,
                $crate::sparse::SparseInner::UndirectedWeighted($g) => $body,
                $crate::sparse::SparseInner::Directed($g) => $body,
                $crate::sparse::SparseInner::DirectedWeighted($g) => $body,
            }
        } else {
            Err($crate::labels::type_error(obj))
        }
    }};
}
pub(crate) use dispatch;

/// Like [`dispatch!`], but only for the directed graph types; any other graph is a `GraphError`.
macro_rules! dispatch_directed {
    ($obj:expr, |$g:ident, $lab:ident| $body:expr) => {{
        let obj = &$crate::unmodifiable::unwrap_readonly($obj);
        let not_directed = || $crate::error::GraphError::new_err("graph must be directed");
        if let Ok(gr) = obj.extract::<::pyo3::PyRef<'_, $crate::graph::Graph>>() {
            let $lab = $crate::labels::Labels::Dynamic(&gr);
            match gr.inner() {
                $crate::graph::Inner::Directed($g) => $body,
                _ => Err(not_directed()),
            }
        } else if let Ok(sg) = obj.extract::<::pyo3::PyRef<'_, $crate::sparse::SparseGraph>>() {
            let $lab = $crate::labels::Labels::Sparse(&sg);
            match sg.inner() {
                $crate::sparse::SparseInner::Directed($g) => $body,
                $crate::sparse::SparseInner::DirectedWeighted($g) => $body,
                _ => Err(not_directed()),
            }
        } else {
            Err($crate::labels::type_error(obj))
        }
    }};
}
pub(crate) use dispatch_directed;

/// Like [`dispatch!`], but only for the undirected graph types; any other graph is a `GraphError`.
macro_rules! dispatch_undirected {
    ($obj:expr, |$g:ident, $lab:ident| $body:expr) => {{
        let obj = &$crate::unmodifiable::unwrap_readonly($obj);
        let not_undirected = || $crate::error::GraphError::new_err("graph must be undirected");
        if let Ok(gr) = obj.extract::<::pyo3::PyRef<'_, $crate::graph::Graph>>() {
            let $lab = $crate::labels::Labels::Dynamic(&gr);
            match gr.inner() {
                $crate::graph::Inner::Undirected($g) => $body,
                _ => Err(not_undirected()),
            }
        } else if let Ok(sg) = obj.extract::<::pyo3::PyRef<'_, $crate::sparse::SparseGraph>>() {
            let $lab = $crate::labels::Labels::Sparse(&sg);
            match sg.inner() {
                $crate::sparse::SparseInner::Undirected($g) => $body,
                $crate::sparse::SparseInner::UndirectedWeighted($g) => $body,
                _ => Err(not_undirected()),
            }
        } else {
            Err($crate::labels::type_error(obj))
        }
    }};
}
pub(crate) use dispatch_undirected;

/// Like [`dispatch!`] for two graphs that must be of the same Rust type (both `Graph` or both
/// `SparseGraph`, with the same directedness and weighting); anything else is an error.
macro_rules! dispatch_pair {
    ($a:expr, $b:expr, |$g1:ident, $g2:ident, $lab1:ident, $lab2:ident| $body:expr) => {{
        let (a, b) = (
            &$crate::unmodifiable::unwrap_readonly($a),
            &$crate::unmodifiable::unwrap_readonly($b),
        );
        let mismatch = || {
            $crate::error::GraphError::new_err(
                "both graphs must be of the same kind: both Graph with the same directedness, \
                 or both SparseGraph with the same directedness and weighting",
            )
        };
        if let (Ok(x), Ok(y)) = (
            a.extract::<::pyo3::PyRef<'_, $crate::graph::Graph>>(),
            b.extract::<::pyo3::PyRef<'_, $crate::graph::Graph>>(),
        ) {
            let $lab1 = $crate::labels::Labels::Dynamic(&x);
            let $lab2 = $crate::labels::Labels::Dynamic(&y);
            match (x.inner(), y.inner()) {
                ($crate::graph::Inner::Undirected($g1), $crate::graph::Inner::Undirected($g2)) => {
                    $body
                }
                ($crate::graph::Inner::Directed($g1), $crate::graph::Inner::Directed($g2)) => $body,
                _ => Err(mismatch()),
            }
        } else if let (Ok(x), Ok(y)) = (
            a.extract::<::pyo3::PyRef<'_, $crate::sparse::SparseGraph>>(),
            b.extract::<::pyo3::PyRef<'_, $crate::sparse::SparseGraph>>(),
        ) {
            use $crate::sparse::SparseInner as S;
            let $lab1 = $crate::labels::Labels::Sparse(&x);
            let $lab2 = $crate::labels::Labels::Sparse(&y);
            match (x.inner(), y.inner()) {
                (S::Undirected($g1), S::Undirected($g2)) => $body,
                (S::UndirectedWeighted($g1), S::UndirectedWeighted($g2)) => $body,
                (S::Directed($g1), S::Directed($g2)) => $body,
                (S::DirectedWeighted($g1), S::DirectedWeighted($g2)) => $body,
                _ => Err(mismatch()),
            }
        } else {
            let is_graph = |o: &::pyo3::Bound<'_, ::pyo3::PyAny>| {
                o.extract::<::pyo3::PyRef<'_, $crate::graph::Graph>>()
                    .is_ok()
                    || o.extract::<::pyo3::PyRef<'_, $crate::sparse::SparseGraph>>()
                        .is_ok()
            };
            if is_graph(a) && is_graph(b) {
                Err(mismatch())
            } else {
                Err($crate::labels::type_error(if is_graph(a) { b } else { a }))
            }
        }
    }};
}
pub(crate) use dispatch_pair;

/// Like [`dispatch_pair!`], but only for undirected graph types.
macro_rules! dispatch_pair_undirected {
    ($a:expr, $b:expr, |$g1:ident, $g2:ident, $lab1:ident, $lab2:ident| $body:expr) => {{
        let (a, b) = (
            &$crate::unmodifiable::unwrap_readonly($a),
            &$crate::unmodifiable::unwrap_readonly($b),
        );
        let mismatch = || {
            $crate::error::GraphError::new_err(
                "both graphs must be undirected and of the same kind (two Graph or two SparseGraph)",
            )
        };
        if let (Ok(x), Ok(y)) = (
            a.extract::<::pyo3::PyRef<'_, $crate::graph::Graph>>(),
            b.extract::<::pyo3::PyRef<'_, $crate::graph::Graph>>(),
        ) {
            let $lab1 = $crate::labels::Labels::Dynamic(&x);
            let $lab2 = $crate::labels::Labels::Dynamic(&y);
            match (x.inner(), y.inner()) {
                ($crate::graph::Inner::Undirected($g1), $crate::graph::Inner::Undirected($g2)) => $body,
                _ => Err(mismatch()),
            }
        } else if let (Ok(x), Ok(y)) = (
            a.extract::<::pyo3::PyRef<'_, $crate::sparse::SparseGraph>>(),
            b.extract::<::pyo3::PyRef<'_, $crate::sparse::SparseGraph>>(),
        ) {
            use $crate::sparse::SparseInner as S;
            let $lab1 = $crate::labels::Labels::Sparse(&x);
            let $lab2 = $crate::labels::Labels::Sparse(&y);
            match (x.inner(), y.inner()) {
                (S::Undirected($g1), S::Undirected($g2)) => $body,
                (S::UndirectedWeighted($g1), S::UndirectedWeighted($g2)) => $body,
                _ => Err(mismatch()),
            }
        } else {
            Err($crate::labels::type_error(a))
        }
    }};
}
pub(crate) use dispatch_pair_undirected;

/// A per-vertex or per-edge value given as a ``dict`` (missing keys use ``default``), a callable
/// taking the vertex / edge, or a constant.
pub fn spec_value(spec: &Bound<'_, PyAny>, key: Py<PyAny>, default: f64) -> PyResult<f64> {
    let py = spec.py();
    if let Ok(d) = spec.cast::<PyDict>() {
        return match d.get_item(key.bind(py))? {
            Some(v) => v.extract(),
            None => Ok(default),
        };
    }
    if spec.is_callable() {
        return spec.call1((key,))?.extract();
    }
    spec.extract()
}

pub fn as_i32(x: f64, what: &str) -> PyResult<i32> {
    if x.fract() != 0.0 || x < i32::MIN as f64 || x > i32::MAX as f64 {
        return Err(GraphError::new_err(format!(
            "{what} must be an integer, got {x}"
        )));
    }
    Ok(x as i32)
}
