//! The Python `Graph` class and the `GraphPath` result type.
//!
//! Vertices and edges are arbitrary hashable Python objects. Internally every vertex and edge is
//! mapped to an integer id and the graph itself is a plain `jgrapht` graph over those ids, so
//! algorithms run without calling back into Python.

use std::collections::HashMap;

use jgrapht::{
    DefaultEdge, DiGraph, Graph as _, GraphExt as _, GraphMut as _, IncidenceGraph as _,
    IncomingGraph as _, OutgoingGraph as _, UGraph,
};
use pyo3::prelude::*;
use pyo3::types::{PyDict, PyList};

use crate::attrs::{Attributes, Attrs};
use crate::error::{GraphError, graph_error};
use crate::labels::not_found;

#[derive(Clone)]
pub enum Inner {
    Undirected(UGraph<usize>),
    Directed(DiGraph<usize>),
}

/// Runs `$body` with `$g` bound to a shared reference to the underlying Rust graph.
macro_rules! with_graph {
    ($self:expr, $g:ident => $body:expr) => {
        match &$self.inner {
            Inner::Undirected($g) => $body,
            Inner::Directed($g) => $body,
        }
    };
}

/// Runs `$body` with `$g` bound to a mutable reference to the underlying Rust graph.
macro_rules! with_graph_mut {
    ($self:expr, $g:ident => $body:expr) => {
        match &mut $self.inner {
            Inner::Undirected($g) => $body,
            Inner::Directed($g) => $body,
        }
    };
}

/// A mutable graph whose vertices and edges are arbitrary hashable Python objects.
#[pyclass(module = "jgrapht")]
pub struct Graph {
    inner: Inner,
    vertex_ids: Py<PyDict>,
    vertex_objs: HashMap<usize, Py<PyAny>>,
    edge_ids: Py<PyDict>,
    edge_objs: HashMap<u64, Py<PyAny>>,
    next_vertex_id: usize,
    next_edge_id: u64,
    next_auto_vertex: i64,
    next_auto_edge: i64,
    directed: bool,
    weighted: bool,
    allow_self_loops: bool,
    allow_multiple_edges: bool,
    attrs: Attrs,
}

impl Graph {
    /// Builds a graph from vertex objects and `(source, target, weight)` index triples, where a
    /// weight makes the graph weighted. Used to return graphs computed by algorithms.
    pub fn from_parts(
        py: Python<'_>,
        directed: bool,
        vertices: Vec<Py<PyAny>>,
        edges: Vec<(usize, usize, Option<f64>)>,
    ) -> PyResult<Py<Graph>> {
        Self::from_parts_weighted(py, directed, false, vertices, edges)
    }

    /// Like [`Graph::from_parts`], but the graph is also weighted when `weighted` is set even if
    /// it has no edges.
    pub fn from_parts_weighted(
        py: Python<'_>,
        directed: bool,
        weighted: bool,
        vertices: Vec<Py<PyAny>>,
        edges: Vec<(usize, usize, Option<f64>)>,
    ) -> PyResult<Py<Graph>> {
        let weighted = weighted || edges.iter().any(|(_, _, w)| w.is_some());
        // allow loops / parallel edges exactly when the edge list contains them
        let loops = edges.iter().any(|(s, t, _)| s == t);
        let mut seen = std::collections::HashSet::new();
        let multiple = edges.iter().any(|&(s, t, _)| {
            let key = if directed {
                (s, t)
            } else {
                (s.min(t), s.max(t))
            };
            !seen.insert(key)
        });
        let mut g = Graph::new(py, directed, loops, multiple, weighted);
        for v in &vertices {
            g.add_vertex(py, v.bind(py).clone())?;
        }
        for (s, t, w) in edges {
            g.add_edge(
                py,
                vertices[s].bind(py).clone(),
                vertices[t].bind(py).clone(),
                None,
                w,
            )?;
        }
        Py::new(py, g)
    }

    /// A new `Graph` with this graph's flags and the vertices, edges and weights of `inner` (a
    /// modified copy of this graph's Rust graph). Vertex and edge objects of `self` are reused;
    /// edges that did not exist in `self` get fresh integer objects.
    pub fn rebuild_from(&self, py: Python<'_>, inner: &Inner) -> PyResult<Py<Graph>> {
        let mut g = Graph::new(
            py,
            self.directed,
            self.allow_self_loops,
            self.allow_multiple_edges,
            self.weighted,
        );
        macro_rules! copy {
            ($src:expr) => {{
                let src = $src;
                for id in src.vertices() {
                    g.add_vertex(py, self.vertex_obj(py, *id).bind(py).clone())?;
                }
                for e in src.edges_cloned().collect::<Vec<_>>() {
                    let (u, v) = src.edge_endpoints(&e).expect("edge of the graph");
                    let object = self.edge_objs.get(&e.0).map(|o| o.bind(py).clone());
                    let weight = self.weighted.then(|| src.weight_of(&e));
                    g.add_edge(
                        py,
                        self.vertex_obj(py, *u).bind(py).clone(),
                        self.vertex_obj(py, *v).bind(py).clone(),
                        object,
                        weight,
                    )?;
                }
            }};
        }
        match inner {
            Inner::Undirected(src) => copy!(src),
            Inner::Directed(src) => copy!(src),
        }
        // the vertices and edges that were kept keep (a copy of) their attributes
        for (&old, obj) in &self.vertex_objs {
            if let (Some(d), Ok(Some(new))) = (
                self.attrs.existing(py, false, old as u64),
                g.vertex_ids.bind(py).get_item(obj.bind(py)),
            ) {
                g.attrs
                    .store_copy(py, false, new.extract::<u64>()?, d.bind(py));
            }
        }
        for (&old, obj) in &self.edge_objs {
            if let (Some(d), Ok(Some(new))) = (
                self.attrs.existing(py, true, old),
                g.edge_ids.bind(py).get_item(obj.bind(py)),
            ) {
                g.attrs.store_copy(py, true, new.extract::<u64>()?, d.bind(py));
            }
        }
        g.attrs
            .store_graph_copy(py, self.attrs.graph_dict(py).bind(py));
        Py::new(py, g)
    }

    pub fn edge_id(&self, py: Python<'_>, e: &Bound<'_, PyAny>) -> PyResult<u64> {
        self.edge_id_of(py, e)
    }

    /// `(directed, weighted, allow_self_loops, allow_multiple_edges)`.
    pub fn flags(&self) -> (bool, bool, bool, bool) {
        (
            self.directed,
            self.weighted,
            self.allow_self_loops,
            self.allow_multiple_edges,
        )
    }

    pub fn inner(&self) -> &Inner {
        &self.inner
    }

    pub fn id_of(&self, py: Python<'_>, v: &Bound<'_, PyAny>) -> PyResult<usize> {
        match self.vertex_ids.bind(py).get_item(v)? {
            Some(id) => id.extract(),
            None => Err(not_found("vertex", v)),
        }
    }

    fn edge_id_of(&self, py: Python<'_>, e: &Bound<'_, PyAny>) -> PyResult<u64> {
        match self.edge_ids.bind(py).get_item(e)? {
            Some(id) => id.extract(),
            None => Err(not_found("edge", e)),
        }
    }

    pub fn vertex_obj(&self, py: Python<'_>, id: usize) -> Py<PyAny> {
        self.vertex_objs[&id].clone_ref(py)
    }

    pub fn edge_obj(&self, py: Python<'_>, id: u64) -> Py<PyAny> {
        self.edge_objs[&id].clone_ref(py)
    }

    fn edge_objs_of(&self, py: Python<'_>, ids: impl IntoIterator<Item = u64>) -> Vec<Py<PyAny>> {
        ids.into_iter().map(|id| self.edge_obj(py, id)).collect()
    }

    pub fn attrs_ref(&self) -> &Attrs {
        &self.attrs
    }

    fn forget_edge(&mut self, py: Python<'_>, id: u64) -> PyResult<()> {
        self.attrs.remove(true, id);
        if let Some(obj) = self.edge_objs.remove(&id) {
            self.edge_ids.bind(py).del_item(obj)?;
        }
        Ok(())
    }
}

#[pymethods]
impl Graph {
    #[new]
    #[pyo3(signature = (directed=false, allow_self_loops=false, allow_multiple_edges=false, weighted=false))]
    pub fn new(
        py: Python<'_>,
        directed: bool,
        allow_self_loops: bool,
        allow_multiple_edges: bool,
        weighted: bool,
    ) -> Self {
        let ty = jgrapht::GraphType {
            self_loops: allow_self_loops,
            multiple_edges: allow_multiple_edges,
            weighted,
            ..jgrapht::GraphType::simple()
        };
        let inner = if directed {
            Inner::Directed(DiGraph::with_graph_type(ty))
        } else {
            Inner::Undirected(UGraph::with_graph_type(ty))
        };
        Graph {
            inner,
            vertex_ids: PyDict::new(py).unbind(),
            vertex_objs: HashMap::new(),
            edge_ids: PyDict::new(py).unbind(),
            edge_objs: HashMap::new(),
            next_vertex_id: 0,
            next_edge_id: 0,
            next_auto_vertex: 0,
            next_auto_edge: 0,
            directed,
            weighted,
            allow_self_loops,
            allow_multiple_edges,
            attrs: Attrs::default(),
        }
    }

    #[getter]
    fn directed(&self) -> bool {
        self.directed
    }

    #[getter]
    fn weighted(&self) -> bool {
        self.weighted
    }

    #[getter]
    fn allow_self_loops(&self) -> bool {
        self.allow_self_loops
    }

    #[getter]
    fn allow_multiple_edges(&self) -> bool {
        self.allow_multiple_edges
    }

    /// The attributes of the vertices: a mapping from a vertex to its ``dict``.
    ///
    /// ``g.vertex_attrs[v]`` is the live dict of the vertex ``v``, created empty on first use.
    /// Only vertices that have attributes are counted by ``len`` and iteration. Removing a vertex
    /// removes its attributes.
    #[getter]
    fn vertex_attrs(slf: &Bound<'_, Self>) -> Attributes {
        Attributes::new(slf.clone().into_any().unbind(), false, false)
    }

    /// The attributes of the edges: a mapping from an edge to its ``dict``, like
    /// :attr:`vertex_attrs`. The edge weight is not an attribute.
    #[getter]
    fn edge_attrs(slf: &Bound<'_, Self>) -> Attributes {
        Attributes::new(slf.clone().into_any().unbind(), true, false)
    }

    /// The attributes of the graph as a whole: a ``dict``.
    #[getter]
    fn graph_attrs(&self, py: Python<'_>) -> Py<PyDict> {
        self.attrs.graph_dict(py)
    }

    // ---- vertices ----

    /// Adds a vertex; returns ``False`` if it was already present.
    pub fn add_vertex(&mut self, py: Python<'_>, v: Bound<'_, PyAny>) -> PyResult<bool> {
        if self.vertex_ids.bind(py).contains(&v)? {
            return Ok(false);
        }
        let id = self.next_vertex_id;
        self.next_vertex_id += 1;
        with_graph_mut!(self, g => g.add_vertex(id));
        self.vertex_ids.bind(py).set_item(&v, id)?;
        self.vertex_objs.insert(id, v.unbind());
        Ok(true)
    }

    /// Adds a fresh integer-labelled vertex and returns it.
    fn new_vertex(&mut self, py: Python<'_>) -> PyResult<Py<PyAny>> {
        loop {
            let candidate = self.next_auto_vertex.into_pyobject(py)?.into_any();
            self.next_auto_vertex += 1;
            if self.add_vertex(py, candidate.clone())? {
                return Ok(candidate.unbind());
            }
        }
    }

    /// Removes a vertex and its incident edges; returns ``False`` if it was not present.
    fn remove_vertex(&mut self, py: Python<'_>, v: Bound<'_, PyAny>) -> PyResult<bool> {
        let Some(id) = self.vertex_ids.bind(py).get_item(&v)? else {
            return Ok(false);
        };
        let id: usize = id.extract()?;
        let incident: Vec<u64> = with_graph!(self, g => g.edges_of(&id).map(|e| e.0).collect());
        with_graph_mut!(self, g => g.remove_vertex(&id));
        for e in incident {
            self.forget_edge(py, e)?;
        }
        self.vertex_ids.bind(py).del_item(&v)?;
        self.vertex_objs.remove(&id);
        self.attrs.remove(false, id as u64);
        Ok(true)
    }

    fn contains_vertex(&self, py: Python<'_>, v: Bound<'_, PyAny>) -> PyResult<bool> {
        self.vertex_ids.bind(py).contains(&v)
    }

    fn __contains__(&self, py: Python<'_>, v: Bound<'_, PyAny>) -> PyResult<bool> {
        self.contains_vertex(py, v)
    }

    /// The vertices, in insertion order.
    fn vertices<'py>(&self, py: Python<'py>) -> PyResult<Bound<'py, PyList>> {
        let items = with_graph!(self, g => g.vertices().map(|id| self.vertex_obj(py, *id)).collect::<Vec<_>>());
        PyList::new(py, items)
    }

    fn __iter__<'py>(&self, py: Python<'py>) -> PyResult<Bound<'py, PyAny>> {
        Ok(self.vertices(py)?.try_iter()?.into_any())
    }

    fn __len__(&self) -> usize {
        with_graph!(self, g => g.vertex_count())
    }

    // ---- edges ----

    /// Adds an edge between existing vertices and returns the edge object.
    ///
    /// ``edge`` is the (hashable) edge object; when omitted a fresh integer is used. Returns
    /// ``None`` if the graph rejects the edge (a parallel edge in a graph without multiple
    /// edges, or an edge object already present with the same endpoints).
    #[pyo3(signature = (u, v, edge=None, weight=None))]
    pub fn add_edge(
        &mut self,
        py: Python<'_>,
        u: Bound<'_, PyAny>,
        v: Bound<'_, PyAny>,
        edge: Option<Bound<'_, PyAny>>,
        weight: Option<f64>,
    ) -> PyResult<Option<Py<PyAny>>> {
        if weight.is_some() && !self.weighted {
            return Err(GraphError::new_err("graph is not weighted"));
        }
        let (u, v) = (self.id_of(py, &u)?, self.id_of(py, &v)?);
        let edge = match edge {
            Some(e) => e,
            None => loop {
                let candidate = self.next_auto_edge.into_pyobject(py)?.into_any();
                self.next_auto_edge += 1;
                if !self.edge_ids.bind(py).contains(&candidate)? {
                    break candidate;
                }
            },
        };
        let (id, is_new) = match self.edge_ids.bind(py).get_item(&edge)? {
            Some(id) => (id.extract::<u64>()?, false),
            None => {
                let id = self.next_edge_id;
                self.next_edge_id += 1;
                (id, true)
            }
        };
        let added = with_graph_mut!(self, g => g.add_edge_with(&u, &v, DefaultEdge(id)))
            .map_err(graph_error)?;
        if !added {
            return Ok(None);
        }
        if let Some(w) = weight {
            with_graph_mut!(self, g => g.set_edge_weight(&DefaultEdge(id), w))
                .map_err(graph_error)?;
        }
        if is_new {
            self.edge_ids.bind(py).set_item(&edge, id)?;
            self.edge_objs.insert(id, edge.clone().unbind());
        }
        Ok(Some(edge.unbind()))
    }

    /// Removes an edge; returns ``False`` if it was not present.
    fn remove_edge(&mut self, py: Python<'_>, e: Bound<'_, PyAny>) -> PyResult<bool> {
        let Some(id) = self.edge_ids.bind(py).get_item(&e)? else {
            return Ok(false);
        };
        let id: u64 = id.extract()?;
        with_graph_mut!(self, g => g.remove_edge(&DefaultEdge(id)));
        self.forget_edge(py, id)?;
        Ok(true)
    }

    fn contains_edge(&self, py: Python<'_>, e: Bound<'_, PyAny>) -> PyResult<bool> {
        self.edge_ids.bind(py).contains(&e)
    }

    /// The edges, in insertion order.
    fn edges(&self, py: Python<'_>) -> Vec<Py<PyAny>> {
        self.edge_objs_of(
            py,
            with_graph!(self, g => g.edges().map(|e| e.0).collect::<Vec<_>>()),
        )
    }

    fn edge_count(&self) -> usize {
        with_graph!(self, g => g.edge_count())
    }

    fn edge_source(&self, py: Python<'_>, e: Bound<'_, PyAny>) -> PyResult<Py<PyAny>> {
        let id = self.edge_id_of(py, &e)?;
        let v = with_graph!(self, g => g.edge_source(&DefaultEdge(id)).copied());
        Ok(self.vertex_obj(py, v.expect("edge is in graph")))
    }

    fn edge_target(&self, py: Python<'_>, e: Bound<'_, PyAny>) -> PyResult<Py<PyAny>> {
        let id = self.edge_id_of(py, &e)?;
        let v = with_graph!(self, g => g.edge_target(&DefaultEdge(id)).copied());
        Ok(self.vertex_obj(py, v.expect("edge is in graph")))
    }

    fn edge_weight(&self, py: Python<'_>, e: Bound<'_, PyAny>) -> PyResult<f64> {
        let id = self.edge_id_of(py, &e)?;
        Ok(with_graph!(self, g => g.edge_weight(&DefaultEdge(id))).expect("edge is in graph"))
    }

    fn set_edge_weight(
        &mut self,
        py: Python<'_>,
        e: Bound<'_, PyAny>,
        weight: f64,
    ) -> PyResult<()> {
        if !self.weighted {
            return Err(GraphError::new_err("graph is not weighted"));
        }
        let id = self.edge_id_of(py, &e)?;
        with_graph_mut!(self, g => g.set_edge_weight(&DefaultEdge(id), weight)).map_err(graph_error)
    }

    /// The edges from ``u`` to ``v`` (either direction in an undirected graph).
    fn edges_between(
        &self,
        py: Python<'_>,
        u: Bound<'_, PyAny>,
        v: Bound<'_, PyAny>,
    ) -> PyResult<Vec<Py<PyAny>>> {
        let (u, v) = (self.id_of(py, &u)?, self.id_of(py, &v)?);
        let ids: Vec<u64> = with_graph!(self, g => g.edges_between(&u, &v).map(|e| e.0).collect());
        Ok(self.edge_objs_of(py, ids))
    }

    // ---- incidence ----

    /// Edges incident to ``v`` (incoming and outgoing).
    fn edges_of(&self, py: Python<'_>, v: Bound<'_, PyAny>) -> PyResult<Vec<Py<PyAny>>> {
        let v = self.id_of(py, &v)?;
        let ids: Vec<u64> = with_graph!(self, g => g.edges_of(&v).map(|e| e.0).collect());
        Ok(self.edge_objs_of(py, ids))
    }

    fn out_edges_of(&self, py: Python<'_>, v: Bound<'_, PyAny>) -> PyResult<Vec<Py<PyAny>>> {
        let v = self.id_of(py, &v)?;
        let ids: Vec<u64> = with_graph!(self, g => g.out_edges_of(&v).map(|e| e.0).collect());
        Ok(self.edge_objs_of(py, ids))
    }

    fn in_edges_of(&self, py: Python<'_>, v: Bound<'_, PyAny>) -> PyResult<Vec<Py<PyAny>>> {
        let v = self.id_of(py, &v)?;
        let ids: Vec<u64> = with_graph!(self, g => g.in_edges_of(&v).map(|e| e.0).collect());
        Ok(self.edge_objs_of(py, ids))
    }

    fn degree_of(&self, py: Python<'_>, v: Bound<'_, PyAny>) -> PyResult<usize> {
        let v = self.id_of(py, &v)?;
        Ok(with_graph!(self, g => g.degree_of(&v)))
    }

    fn out_degree_of(&self, py: Python<'_>, v: Bound<'_, PyAny>) -> PyResult<usize> {
        let v = self.id_of(py, &v)?;
        Ok(with_graph!(self, g => g.out_degree_of(&v)))
    }

    fn in_degree_of(&self, py: Python<'_>, v: Bound<'_, PyAny>) -> PyResult<usize> {
        let v = self.id_of(py, &v)?;
        Ok(with_graph!(self, g => g.in_degree_of(&v)))
    }

    /// Vertices adjacent to ``v``.
    fn neighbors_of(&self, py: Python<'_>, v: Bound<'_, PyAny>) -> PyResult<Vec<Py<PyAny>>> {
        let v = self.id_of(py, &v)?;
        Ok(with_graph!(self, g => g
            .neighbor_list_of(&v)
            .into_iter()
            .map(|id| self.vertex_obj(py, id))
            .collect()))
    }

    fn __repr__(&self) -> String {
        format!(
            "Graph(directed={}, weighted={}, vertices={}, edges={})",
            if self.directed { "True" } else { "False" },
            if self.weighted { "True" } else { "False" },
            with_graph!(self, g => g.vertex_count()),
            with_graph!(self, g => g.edge_count()),
        )
    }
}

/// A path in a graph: vertices, edges and total weight.
#[pyclass(module = "jgrapht", frozen)]
pub struct GraphPath {
    vertices: Vec<Py<PyAny>>,
    edges: Vec<Py<PyAny>>,
    weight: f64,
}

impl GraphPath {
    pub fn new(vertices: Vec<Py<PyAny>>, edges: Vec<Py<PyAny>>, weight: f64) -> Self {
        GraphPath {
            vertices,
            edges,
            weight,
        }
    }
}

#[pymethods]
impl GraphPath {
    #[getter]
    fn vertices(&self, py: Python<'_>) -> Vec<Py<PyAny>> {
        self.vertices.iter().map(|v| v.clone_ref(py)).collect()
    }

    #[getter]
    fn edges(&self, py: Python<'_>) -> Vec<Py<PyAny>> {
        self.edges.iter().map(|e| e.clone_ref(py)).collect()
    }

    #[getter]
    fn weight(&self) -> f64 {
        self.weight
    }

    fn __len__(&self) -> usize {
        self.edges.len()
    }

    fn __repr__(&self, py: Python<'_>) -> PyResult<String> {
        let vs = PyList::new(py, self.vertices(py))?;
        Ok(format!(
            "GraphPath(vertices={}, weight={:?})",
            vs.repr()?,
            self.weight
        ))
    }
}
