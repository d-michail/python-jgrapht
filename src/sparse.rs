//! The Python `SparseGraph` class: an immutable graph on the integer vertices `0..n` whose edges
//! are the integers `0..m` in input order, backed by `jgrapht`'s compressed sparse row graphs.

use jgrapht::graph::sparse::{
    SparseIntDirectedGraph, SparseIntDirectedWeightedGraph, SparseIntUndirectedGraph,
    SparseIntUndirectedWeightedGraph,
};
use jgrapht::{
    Graph as _, GraphExt as _, IncidenceGraph as _, IncomingGraph as _, OutgoingGraph as _,
};
use pyo3::prelude::*;

use crate::attrs::{Attributes, Attrs};
use crate::error::{GraphError, graph_error};

pub enum SparseInner {
    Undirected(SparseIntUndirectedGraph),
    UndirectedWeighted(SparseIntUndirectedWeightedGraph),
    Directed(SparseIntDirectedGraph),
    DirectedWeighted(SparseIntDirectedWeightedGraph),
}

macro_rules! with_sparse {
    ($self:expr, $g:ident => $body:expr) => {
        match &$self.inner {
            SparseInner::Undirected($g) => $body,
            SparseInner::UndirectedWeighted($g) => $body,
            SparseInner::Directed($g) => $body,
            SparseInner::DirectedWeighted($g) => $body,
        }
    };
}

/// An immutable graph on vertices ``0..n`` and edges ``0..m``, stored in compressed sparse row form.
///
/// Edges are numbered in the order given. Only edge weights of weighted graphs can be changed.
#[pyclass(module = "jgrapht")]
pub struct SparseGraph {
    inner: SparseInner,
    num_vertices: usize,
    directed: bool,
    weighted: bool,
    attrs: Attrs,
}

impl SparseGraph {
    /// The same as the Python constructor, for use from Rust.
    pub fn create(
        num_vertices: usize,
        edges: Vec<(usize, usize)>,
        directed: bool,
        weights: Option<Vec<f64>>,
    ) -> PyResult<Self> {
        Self::new(num_vertices, edges, directed, weights)
    }

    pub fn inner(&self) -> &SparseInner {
        &self.inner
    }

    pub fn attrs_ref(&self) -> &Attrs {
        &self.attrs
    }

    pub fn check_vertex(&self, v: &Bound<'_, PyAny>) -> PyResult<usize> {
        match v.extract::<usize>() {
            Ok(id) if id < self.num_vertices => Ok(id),
            _ => Err(crate::labels::not_found("vertex", v)),
        }
    }

    pub fn check_edge_obj(&self, e: &Bound<'_, PyAny>) -> PyResult<usize> {
        match e.extract::<usize>() {
            Ok(id) => self.check_edge(id),
            Err(_) => Err(crate::labels::not_found("edge", e)),
        }
    }

    fn check_edge(&self, e: usize) -> PyResult<usize> {
        if e < with_sparse!(self, g => g.edge_count()) {
            Ok(e)
        } else {
            Err(GraphError::new_err(format!("edge {e} not found in graph")))
        }
    }
}

#[pymethods]
impl SparseGraph {
    /// ``SparseGraph(num_vertices, edges, directed=False, weights=None)``
    ///
    /// ``edges`` is a list of ``(source, target)`` pairs; ``weights``, if given, holds one weight
    /// per edge.
    #[new]
    #[pyo3(signature = (num_vertices, edges, directed=false, weights=None))]
    fn new(
        num_vertices: usize,
        edges: Vec<(usize, usize)>,
        directed: bool,
        weights: Option<Vec<f64>>,
    ) -> PyResult<Self> {
        let weighted = weights.is_some();
        let inner = match weights {
            None if directed => SparseInner::Directed(
                SparseIntDirectedGraph::new(num_vertices, &edges).map_err(graph_error)?,
            ),
            None => SparseInner::Undirected(
                SparseIntUndirectedGraph::new(num_vertices, &edges).map_err(graph_error)?,
            ),
            Some(ws) => {
                if ws.len() != edges.len() {
                    return Err(GraphError::new_err("weights must have one entry per edge"));
                }
                let weighted: Vec<(usize, usize, f64)> =
                    edges.iter().zip(ws).map(|(&(s, t), w)| (s, t, w)).collect();
                if directed {
                    SparseInner::DirectedWeighted(
                        SparseIntDirectedWeightedGraph::new(num_vertices, &weighted)
                            .map_err(graph_error)?,
                    )
                } else {
                    SparseInner::UndirectedWeighted(
                        SparseIntUndirectedWeightedGraph::new(num_vertices, &weighted)
                            .map_err(graph_error)?,
                    )
                }
            }
        };
        Ok(SparseGraph {
            inner,
            num_vertices,
            directed,
            weighted,
            attrs: Attrs::default(),
        })
    }

    #[getter]
    fn directed(&self) -> bool {
        self.directed
    }

    #[getter]
    fn weighted(&self) -> bool {
        self.weighted
    }

    fn vertices(&self) -> Vec<usize> {
        (0..self.num_vertices).collect()
    }

    fn edges(&self) -> Vec<usize> {
        (0..self.edge_count()).collect()
    }

    fn vertex_count(&self) -> usize {
        self.num_vertices
    }

    fn edge_count(&self) -> usize {
        with_sparse!(self, g => g.edge_count())
    }

    fn __len__(&self) -> usize {
        self.num_vertices
    }

    fn __contains__(&self, v: Bound<'_, PyAny>) -> bool {
        self.check_vertex(&v).is_ok()
    }

    fn contains_vertex(&self, v: Bound<'_, PyAny>) -> bool {
        self.check_vertex(&v).is_ok()
    }

    fn contains_edge(&self, e: usize) -> bool {
        self.check_edge(e).is_ok()
    }

    fn edge_source(&self, e: usize) -> PyResult<usize> {
        let e = self.check_edge(e)?;
        Ok(with_sparse!(self, g => *g.edge_source(&e).expect("edge is in graph")))
    }

    fn edge_target(&self, e: usize) -> PyResult<usize> {
        let e = self.check_edge(e)?;
        Ok(with_sparse!(self, g => *g.edge_target(&e).expect("edge is in graph")))
    }

    fn edge_weight(&self, e: usize) -> PyResult<f64> {
        let e = self.check_edge(e)?;
        Ok(with_sparse!(self, g => g.edge_weight(&e).expect("edge is in graph")))
    }

    fn set_edge_weight(&mut self, e: usize, weight: f64) -> PyResult<()> {
        let e = self.check_edge(e)?;
        match &mut self.inner {
            SparseInner::UndirectedWeighted(g) => g.set_edge_weight(e, weight).map_err(graph_error),
            SparseInner::DirectedWeighted(g) => g.set_edge_weight(e, weight).map_err(graph_error),
            _ => Err(GraphError::new_err("graph is not weighted")),
        }
    }

    fn edges_between(&self, u: usize, v: usize) -> PyResult<Vec<usize>> {
        let (u, v) = (self.check_vertex_int(u)?, self.check_vertex_int(v)?);
        Ok(with_sparse!(self, g => g.edges_between(&u, &v).copied().collect()))
    }

    fn edges_of(&self, v: usize) -> PyResult<Vec<usize>> {
        let v = self.check_vertex_int(v)?;
        Ok(with_sparse!(self, g => g.edges_of(&v).copied().collect()))
    }

    fn out_edges_of(&self, v: usize) -> PyResult<Vec<usize>> {
        let v = self.check_vertex_int(v)?;
        Ok(with_sparse!(self, g => g.out_edges_of(&v).copied().collect()))
    }

    fn in_edges_of(&self, v: usize) -> PyResult<Vec<usize>> {
        let v = self.check_vertex_int(v)?;
        Ok(with_sparse!(self, g => g.in_edges_of(&v).copied().collect()))
    }

    fn degree_of(&self, v: usize) -> PyResult<usize> {
        let v = self.check_vertex_int(v)?;
        Ok(with_sparse!(self, g => g.degree_of(&v)))
    }

    fn out_degree_of(&self, v: usize) -> PyResult<usize> {
        let v = self.check_vertex_int(v)?;
        Ok(with_sparse!(self, g => g.out_degree_of(&v)))
    }

    fn in_degree_of(&self, v: usize) -> PyResult<usize> {
        let v = self.check_vertex_int(v)?;
        Ok(with_sparse!(self, g => g.in_degree_of(&v)))
    }

    fn neighbors_of(&self, v: usize) -> PyResult<Vec<usize>> {
        let v = self.check_vertex_int(v)?;
        Ok(with_sparse!(self, g => g.neighbor_list_of(&v)))
    }

    /// The attributes of the vertices: a mapping from a vertex number to its ``dict``.
    ///
    /// ``g.vertex_attrs[v]`` is the live dict of the vertex ``v``, created empty on first use.
    /// Only vertices that have attributes are counted by ``len`` and iteration.
    #[getter]
    fn vertex_attrs(slf: &Bound<'_, Self>) -> Attributes {
        Attributes::new(slf.clone().into_any().unbind(), false, false)
    }

    /// The attributes of the edges: a mapping from an edge number to its ``dict``, like
    /// :attr:`vertex_attrs`. The edge weight is not an attribute.
    #[getter]
    fn edge_attrs(slf: &Bound<'_, Self>) -> Attributes {
        Attributes::new(slf.clone().into_any().unbind(), true, false)
    }

    /// The attributes of the graph as a whole: a ``dict``.
    #[getter]
    fn graph_attrs(&self, py: Python<'_>) -> Py<pyo3::types::PyDict> {
        self.attrs.graph_dict(py)
    }

    fn __repr__(&self) -> String {
        format!(
            "SparseGraph(directed={}, weighted={}, vertices={}, edges={})",
            if self.directed { "True" } else { "False" },
            if self.weighted { "True" } else { "False" },
            self.num_vertices,
            self.edge_count(),
        )
    }
}

impl SparseGraph {
    fn check_vertex_int(&self, v: usize) -> PyResult<usize> {
        if v < self.num_vertices {
            Ok(v)
        } else {
            Err(GraphError::new_err(format!(
                "vertex {v} not found in graph"
            )))
        }
    }
}
