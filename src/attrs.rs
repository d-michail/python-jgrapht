//! Vertex, edge and graph attributes.
//!
//! Every graph owns an [`Attrs`]: one `dict` per vertex and per edge that has attributes, and one
//! `dict` for the graph as a whole. The dicts are created when first asked for, so a graph without
//! attributes pays for nothing. The stores sit behind a mutex so that attributes can be read and
//! changed while an algorithm holds a shared borrow of the graph, for example from a callback.
//!
//! Python sees them through [`Attributes`], a mapping from a vertex (or edge) to its live `dict`.

use std::collections::HashMap;
use std::sync::Mutex;

use pyo3::exceptions::PyKeyError;
use pyo3::prelude::*;
use pyo3::types::{PyDict, PyList, PyTuple};

use crate::error::GraphError;
use crate::graph::Graph;
use crate::sparse::SparseGraph;

type Store = Mutex<HashMap<u64, Py<PyDict>>>;

/// The attribute stores of one graph, keyed by the internal vertex and edge ids.
#[derive(Default)]
pub struct Attrs {
    vertices: Store,
    edges: Store,
    graph: Mutex<Option<Py<PyDict>>>,
}

impl Attrs {
    fn store(&self, edges: bool) -> &Store {
        if edges { &self.edges } else { &self.vertices }
    }

    /// The dict of the graph, created on first use.
    pub fn graph_dict(&self, py: Python<'_>) -> Py<PyDict> {
        let mut slot = self.graph.lock().expect("attribute lock");
        slot.get_or_insert_with(|| PyDict::new(py).unbind())
            .clone_ref(py)
    }

    /// The dict of the vertex or edge, created on first use.
    pub fn dict(&self, py: Python<'_>, edges: bool, key: u64) -> Py<PyDict> {
        let mut store = self.store(edges).lock().expect("attribute lock");
        store
            .entry(key)
            .or_insert_with(|| PyDict::new(py).unbind())
            .clone_ref(py)
    }

    /// The dict of the vertex or edge if it has one, empty or not.
    pub fn existing(&self, py: Python<'_>, edges: bool, key: u64) -> Option<Py<PyDict>> {
        let store = self.store(edges).lock().expect("attribute lock");
        store.get(&key).map(|d| d.clone_ref(py))
    }

    /// Forgets the attributes of a removed vertex or edge.
    pub fn remove(&self, edges: bool, key: u64) {
        self.store(edges).lock().expect("attribute lock").remove(&key);
    }

    /// The keys that have at least one attribute, in ascending order.
    fn keys(&self, py: Python<'_>, edges: bool) -> Vec<u64> {
        let dicts: Vec<(u64, Py<PyDict>)> = {
            let store = self.store(edges).lock().expect("attribute lock");
            store.iter().map(|(k, d)| (*k, d.clone_ref(py))).collect()
        };
        let mut keys: Vec<u64> = dicts
            .into_iter()
            .filter(|(_, d)| !d.bind(py).is_empty())
            .map(|(k, _)| k)
            .collect();
        keys.sort_unstable();
        keys
    }

    /// A shallow copy of `source`, stored for the vertex or edge `key`; nothing if it is empty.
    pub fn store_copy(&self, py: Python<'_>, edges: bool, key: u64, source: &Bound<'_, PyDict>) {
        if source.is_empty() {
            return;
        }
        let copy = source.copy().expect("copy of a dict");
        self.store(edges)
            .lock()
            .expect("attribute lock")
            .insert(key, copy.unbind());
        let _ = py;
    }

    /// Replaces the graph's dict content by a shallow copy of `source`.
    pub fn store_graph_copy(&self, py: Python<'_>, source: &Bound<'_, PyDict>) {
        if source.is_empty() {
            return;
        }
        let target = self.graph_dict(py);
        target.bind(py).update(source.as_mapping()).expect("update of a dict");
    }
}

/// What the attribute mappings need to know about a graph class.
pub trait AttrOwner {
    fn attrs(&self) -> &Attrs;
    fn vertex_key(&self, py: Python<'_>, v: &Bound<'_, PyAny>) -> PyResult<u64>;
    fn edge_key(&self, py: Python<'_>, e: &Bound<'_, PyAny>) -> PyResult<u64>;
    fn vertex_object(&self, py: Python<'_>, key: u64) -> Py<PyAny>;
    fn edge_object(&self, py: Python<'_>, key: u64) -> Py<PyAny>;
}

impl AttrOwner for Graph {
    fn attrs(&self) -> &Attrs {
        self.attrs_ref()
    }
    fn vertex_key(&self, py: Python<'_>, v: &Bound<'_, PyAny>) -> PyResult<u64> {
        self.id_of(py, v).map(|id| id as u64)
    }
    fn edge_key(&self, py: Python<'_>, e: &Bound<'_, PyAny>) -> PyResult<u64> {
        self.edge_id(py, e)
    }
    fn vertex_object(&self, py: Python<'_>, key: u64) -> Py<PyAny> {
        self.vertex_obj(py, key as usize)
    }
    fn edge_object(&self, py: Python<'_>, key: u64) -> Py<PyAny> {
        self.edge_obj(py, key)
    }
}

fn int_object(py: Python<'_>, key: u64) -> Py<PyAny> {
    key.into_pyobject(py).expect("int conversion").into_any().unbind()
}

impl AttrOwner for SparseGraph {
    fn attrs(&self) -> &Attrs {
        self.attrs_ref()
    }
    fn vertex_key(&self, _py: Python<'_>, v: &Bound<'_, PyAny>) -> PyResult<u64> {
        self.check_vertex(v).map(|id| id as u64)
    }
    fn edge_key(&self, _py: Python<'_>, e: &Bound<'_, PyAny>) -> PyResult<u64> {
        self.check_edge_obj(e).map(|id| id as u64)
    }
    fn vertex_object(&self, py: Python<'_>, key: u64) -> Py<PyAny> {
        int_object(py, key)
    }
    fn edge_object(&self, py: Python<'_>, key: u64) -> Py<PyAny> {
        int_object(py, key)
    }
}

/// Runs `$body` with `$o` bound to the graph that owns a mapping, whatever its class.
macro_rules! with_owner {
    ($self:expr, $py:expr, |$o:ident| $body:expr) => {{
        let owner = $self.owner.bind($py);
        if let Ok(g) = owner.extract::<PyRef<'_, Graph>>() {
            let $o: &dyn AttrOwner = &*g;
            $body
        } else {
            let s = owner.extract::<PyRef<'_, SparseGraph>>()?;
            let $o: &dyn AttrOwner = &*s;
            $body
        }
    }};
}

/// A mapping from the vertices (or the edges) of a graph to their attribute dicts.
///
/// ``g.vertex_attrs[v]`` is the live ``dict`` of the vertex ``v``: it is created empty the first
/// time it is asked for, and changing it changes the graph's attributes. Only vertices that have at
/// least one attribute are counted by ``len``, ``in`` and the iteration methods. Removing a vertex
/// or an edge from the graph also removes its attributes. A mapping obtained from an unmodifiable
/// graph is read-only: its dicts are read-only views.
#[pyclass(name = "_Attributes", module = "jgrapht", frozen)]
pub struct Attributes {
    owner: Py<PyAny>,
    edges: bool,
    readonly: bool,
}

impl Attributes {
    pub fn new(owner: Py<PyAny>, edges: bool, readonly: bool) -> Self {
        Attributes {
            owner,
            edges,
            readonly,
        }
    }

    fn key(&self, o: &dyn AttrOwner, py: Python<'_>, obj: &Bound<'_, PyAny>) -> PyResult<u64> {
        if self.edges {
            o.edge_key(py, obj)
        } else {
            o.vertex_key(py, obj)
        }
    }

    fn object(&self, o: &dyn AttrOwner, py: Python<'_>, key: u64) -> Py<PyAny> {
        if self.edges {
            o.edge_object(py, key)
        } else {
            o.vertex_object(py, key)
        }
    }

    /// The value handed to Python for a dict: the dict itself, or a read-only view of it.
    fn present(&self, py: Python<'_>, dict: Py<PyDict>) -> PyResult<Py<PyAny>> {
        if self.readonly {
            read_only(py, dict.into_any())
        } else {
            Ok(dict.into_any())
        }
    }

    fn check_writable(&self) -> PyResult<()> {
        if self.readonly {
            Err(GraphError::new_err("this graph is unmodifiable"))
        } else {
            Ok(())
        }
    }
}

/// A read-only view of a mapping (`types.MappingProxyType`).
pub fn read_only(py: Python<'_>, mapping: Py<PyAny>) -> PyResult<Py<PyAny>> {
    Ok(py
        .import("types")?
        .getattr("MappingProxyType")?
        .call1((mapping,))?
        .unbind())
}

#[pymethods]
impl Attributes {
    fn __getitem__(&self, py: Python<'_>, key: &Bound<'_, PyAny>) -> PyResult<Py<PyAny>> {
        with_owner!(self, py, |o| {
            let k = self.key(o, py, key)?;
            let dict = if self.readonly {
                o.attrs()
                    .existing(py, self.edges, k)
                    .unwrap_or_else(|| PyDict::new(py).unbind())
            } else {
                o.attrs().dict(py, self.edges, k)
            };
            self.present(py, dict)
        })
    }

    /// Replaces the attributes of ``key`` by those of the mapping ``value``.
    fn __setitem__(
        &self,
        py: Python<'_>,
        key: &Bound<'_, PyAny>,
        value: &Bound<'_, PyAny>,
    ) -> PyResult<()> {
        self.check_writable()?;
        with_owner!(self, py, |o| {
            let k = self.key(o, py, key)?;
            let dict = o.attrs().dict(py, self.edges, k);
            let dict = dict.bind(py);
            let items = PyDict::new(py);
            items.update(value.cast::<pyo3::types::PyMapping>()?)?;
            dict.clear();
            dict.update(items.as_mapping())
        })
    }

    /// Removes all the attributes of ``key``.
    fn __delitem__(&self, py: Python<'_>, key: &Bound<'_, PyAny>) -> PyResult<()> {
        self.check_writable()?;
        with_owner!(self, py, |o| {
            let k = self.key(o, py, key)?;
            match o.attrs().existing(py, self.edges, k) {
                Some(d) if !d.bind(py).is_empty() => {
                    o.attrs().remove(self.edges, k);
                    Ok(())
                }
                _ => Err(PyKeyError::new_err(key.clone().unbind())),
            }
        })
    }

    fn __contains__(&self, py: Python<'_>, key: &Bound<'_, PyAny>) -> PyResult<bool> {
        with_owner!(self, py, |o| {
            Ok(match self.key(o, py, key) {
                Ok(k) => o
                    .attrs()
                    .existing(py, self.edges, k)
                    .is_some_and(|d| !d.bind(py).is_empty()),
                Err(_) => false,
            })
        })
    }

    fn __len__(&self, py: Python<'_>) -> PyResult<usize> {
        with_owner!(self, py, |o| Ok(o.attrs().keys(py, self.edges).len()))
    }

    fn __iter__<'py>(&self, py: Python<'py>) -> PyResult<Bound<'py, PyAny>> {
        self.keys(py)?.bind(py).try_iter().map(|i| i.into_any())
    }

    /// The vertices (or edges) that have attributes.
    fn keys(&self, py: Python<'_>) -> PyResult<Py<PyList>> {
        with_owner!(self, py, |o| {
            let objects: Vec<Py<PyAny>> = o
                .attrs()
                .keys(py, self.edges)
                .into_iter()
                .map(|k| self.object(o, py, k))
                .collect();
            Ok(PyList::new(py, objects)?.unbind())
        })
    }

    /// The attribute dicts of the vertices (or edges) that have attributes.
    fn values(&self, py: Python<'_>) -> PyResult<Py<PyList>> {
        with_owner!(self, py, |o| {
            let mut out = Vec::new();
            for k in o.attrs().keys(py, self.edges) {
                out.push(self.present(py, o.attrs().dict(py, self.edges, k))?);
            }
            Ok(PyList::new(py, out)?.unbind())
        })
    }

    /// ``(vertex, attributes)`` pairs for the vertices (or edges) that have attributes.
    fn items(&self, py: Python<'_>) -> PyResult<Py<PyList>> {
        with_owner!(self, py, |o| {
            let mut out = Vec::new();
            for k in o.attrs().keys(py, self.edges) {
                let dict = self.present(py, o.attrs().dict(py, self.edges, k))?;
                out.push(PyTuple::new(py, [self.object(o, py, k), dict])?);
            }
            Ok(PyList::new(py, out)?.unbind())
        })
    }

    /// The attributes of ``key`` if it has any, else ``default``.
    #[pyo3(signature = (key, default=None))]
    fn get(
        &self,
        py: Python<'_>,
        key: &Bound<'_, PyAny>,
        default: Option<Py<PyAny>>,
    ) -> PyResult<Py<PyAny>> {
        let fallback = default.unwrap_or_else(|| py.None());
        with_owner!(self, py, |o| {
            let Ok(k) = self.key(o, py, key) else {
                return Ok(fallback);
            };
            match o.attrs().existing(py, self.edges, k) {
                Some(d) if !d.bind(py).is_empty() => self.present(py, d),
                _ => Ok(fallback),
            }
        })
    }

    fn __repr__(&self, py: Python<'_>) -> PyResult<String> {
        let what = if self.edges { "edge" } else { "vertex" };
        Ok(format!(
            "{what}_attrs({})",
            self.items(py)?.bind(py).repr()?
        ))
    }
}
