//! Derived graphs: copies, subgraphs, unions and re-interpretations of a graph.
//!
//! Each function returns a new, independent :class:`Graph` that keeps the vertex and edge objects of its input (the integers for a
//! :class:`SparseGraph`).

use std::collections::HashMap;

use jgrapht::{Graph as _, GraphExt as _};
use pyo3::prelude::*;
use pyo3::types::PyDict;

use crate::error::GraphError;
use crate::graph::Graph;
use crate::labels::{EdgeId, dispatch, spec_value};

type Attrs = Option<Py<PyDict>>;

/// The attributes of `a` updated by those of `b`, in a new dict, so that neither input changes.
fn merged(py: Python<'_>, a: &Attrs, b: &Attrs) -> PyResult<Attrs> {
    let Some(b) = b.as_ref().filter(|d| !d.bind(py).is_empty()) else {
        return Ok(a.as_ref().map(|d| d.clone_ref(py)));
    };
    let out = match a {
        Some(a) => a.bind(py).copy()?,
        None => PyDict::new(py),
    };
    out.update(b.bind(py).as_mapping())?;
    Ok(Some(out.unbind()))
}

/// The content of a graph, detached from its Rust representation.
struct Parts {
    directed: bool,
    weighted: bool,
    loops: bool,
    multi: bool,
    vertices: Vec<Py<PyAny>>,
    /// `(edge object, source index, target index, weight)`
    edges: Vec<(Py<PyAny>, usize, usize, Option<f64>)>,
    /// The attributes of each vertex and each edge (indexed like `vertices` and `edges`), and of
    /// the graph. They are the originals' dicts; `build` stores shallow copies.
    vertex_attrs: Vec<Attrs>,
    edge_attrs: Vec<Attrs>,
    graph_attrs: Attrs,
}

impl Parts {
    fn extract(py: Python<'_>, graph: &Bound<'_, PyAny>) -> PyResult<Parts> {
        let (flags, ()) = match graph.extract::<PyRef<'_, Graph>>() {
            Ok(g) => (Some(g.flags()), ()),
            Err(_) => (None, ()),
        };
        dispatch!(graph, |g, lab| {
            let ids: Vec<usize> = g.vertices_cloned().collect();
            let index: HashMap<usize, usize> =
                ids.iter().enumerate().map(|(i, v)| (*v, i)).collect();
            let weighted = g.graph_type().weighted;
            let edge_ids: Vec<_> = g.edges_cloned().collect();
            let edges = edge_ids
                .iter()
                .map(|e| {
                    let (s, t) = g.edge_endpoints(e).expect("edge of the graph");
                    (
                        lab.edge_obj(py, e.eid()),
                        index[s],
                        index[t],
                        weighted.then(|| g.weight_of(e)),
                    )
                })
                .collect();
            let (directed, weighted, loops, multi) =
                flags.unwrap_or((g.graph_type().directed, weighted, true, true));
            let attrs = lab.attrs();
            Ok(Parts {
                directed,
                weighted,
                loops,
                multi,
                vertices: ids.iter().map(|v| lab.vertex_obj(py, *v)).collect(),
                edges,
                vertex_attrs: ids
                    .iter()
                    .map(|v| attrs.existing(py, false, *v as u64))
                    .collect(),
                edge_attrs: edge_ids
                    .iter()
                    .map(|e| attrs.existing(py, true, e.eid()))
                    .collect(),
                graph_attrs: Some(attrs.graph_dict(py)),
            })
        })
    }

    fn build(mut self, py: Python<'_>) -> PyResult<Py<Graph>> {
        // allow loops and parallel edges wherever the result needs them
        let mut seen = std::collections::HashSet::new();
        for (_, s, t, _) in &self.edges {
            self.loops |= s == t;
            let key = if self.directed {
                (*s, *t)
            } else {
                (*s.min(t), *s.max(t))
            };
            self.multi |= !seen.insert(key);
        }
        let mut g = Graph::new(py, self.directed, self.loops, self.multi, self.weighted);
        for (v, attrs) in self.vertices.iter().zip(&self.vertex_attrs) {
            g.add_vertex(py, v.bind(py).clone())?;
            if let Some(d) = attrs {
                let id = g.id_of(py, v.bind(py))?;
                g.attrs_ref().store_copy(py, false, id as u64, d.bind(py));
            }
        }
        for ((obj, s, t, w), attrs) in self.edges.into_iter().zip(&self.edge_attrs) {
            let added = g.add_edge(
                py,
                self.vertices[s].bind(py).clone(),
                self.vertices[t].bind(py).clone(),
                Some(obj.into_bound(py)),
                if self.weighted {
                    Some(w.unwrap_or(1.0))
                } else {
                    None
                },
            )?;
            if let (Some(added), Some(d)) = (added, attrs) {
                let id = g.edge_id(py, added.bind(py))?;
                g.attrs_ref().store_copy(py, true, id, d.bind(py));
            }
        }
        if let Some(d) = &self.graph_attrs {
            g.attrs_ref().store_graph_copy(py, d.bind(py));
        }
        Py::new(py, g)
    }

    /// Keeps the vertices with `keep[i]` and the edges with `edge_keep` whose ends are kept.
    fn restrict(self, py: Python<'_>, keep: &[bool], edge_keep: &[bool]) -> Parts {
        let mut renumber = vec![usize::MAX; self.vertices.len()];
        let mut vertices = Vec::new();
        let mut vertex_attrs = Vec::new();
        for (i, v) in self.vertices.iter().enumerate() {
            if keep[i] {
                renumber[i] = vertices.len();
                vertices.push(v.clone_ref(py));
                vertex_attrs.push(self.vertex_attrs[i].as_ref().map(|d| d.clone_ref(py)));
            }
        }
        let mut edges = Vec::new();
        let mut edge_attrs = Vec::new();
        for (i, (o, s, t, w)) in self.edges.iter().enumerate() {
            if edge_keep[i] && keep[*s] && keep[*t] {
                edges.push((o.clone_ref(py), renumber[*s], renumber[*t], *w));
                edge_attrs.push(self.edge_attrs[i].as_ref().map(|d| d.clone_ref(py)));
            }
        }
        Parts {
            vertices,
            edges,
            vertex_attrs,
            edge_attrs,
            ..self
        }
    }
}

fn vertex_index(
    py: Python<'_>,
    parts: &Parts,
    objects: &Bound<'_, PyAny>,
) -> PyResult<HashMap<usize, ()>> {
    let lookup = PyDict::new(py);
    for (i, v) in parts.vertices.iter().enumerate() {
        lookup.set_item(v, i)?;
    }
    let mut out = HashMap::new();
    for obj in objects.try_iter()? {
        let obj = obj?;
        match lookup.get_item(&obj)? {
            Some(i) => {
                out.insert(i.extract::<usize>()?, ());
            }
            None => return Err(crate::labels::not_found("vertex", &obj)),
        }
    }
    Ok(out)
}

/// An independent :class:`Graph` with the vertices, edges and weights of ``graph``.
///
/// For a :class:`Graph` the copy has the same flags (``directed``, ``weighted``, ...); for a
/// :class:`SparseGraph` it allows self-loops and parallel edges. Vertex and edge objects are
/// shared, not copied.
#[pyfunction]
fn copy_graph(py: Python<'_>, graph: &Bound<'_, PyAny>) -> PyResult<Py<Graph>> {
    Parts::extract(py, graph)?.build(py)
}

/// The subgraph induced by ``vertices``: those vertices and every edge between them.
#[pyfunction]
fn induced_subgraph(
    py: Python<'_>,
    graph: &Bound<'_, PyAny>,
    vertices: &Bound<'_, PyAny>,
) -> PyResult<Py<Graph>> {
    let parts = Parts::extract(py, graph)?;
    let chosen = vertex_index(py, &parts, vertices)?;
    let keep: Vec<bool> = (0..parts.vertices.len())
        .map(|i| chosen.contains_key(&i))
        .collect();
    let edge_keep = vec![true; parts.edges.len()];
    parts.restrict(py, &keep, &edge_keep).build(py)
}

/// The subgraph made of the given ``edges`` and their endpoints.
#[pyfunction]
fn edge_subgraph(
    py: Python<'_>,
    graph: &Bound<'_, PyAny>,
    edges: &Bound<'_, PyAny>,
) -> PyResult<Py<Graph>> {
    let parts = Parts::extract(py, graph)?;
    let lookup = PyDict::new(py);
    for (i, (o, ..)) in parts.edges.iter().enumerate() {
        lookup.set_item(o, i)?;
    }
    let mut edge_keep = vec![false; parts.edges.len()];
    let mut keep = vec![false; parts.vertices.len()];
    for obj in edges.try_iter()? {
        let obj = obj?;
        let i = match lookup.get_item(&obj)? {
            Some(i) => i.extract::<usize>()?,
            None => return Err(crate::labels::not_found("edge", &obj)),
        };
        edge_keep[i] = true;
        keep[parts.edges[i].1] = true;
        keep[parts.edges[i].2] = true;
    }
    parts.restrict(py, &keep, &edge_keep).build(py)
}

/// The union of two graphs of the same kind (both directed or both undirected).
///
/// Vertices are identified by equality of their objects. An edge of ``graph2`` whose object also
/// belongs to ``graph1`` *and* has the same endpoints is the same edge, and the weights are merged
/// with ``weights``: ``"sum"`` (default), ``"first"``, ``"second"``, ``"min"`` or ``"max"``
/// (an edge missing a weight counts as 1). Any other edge of ``graph2`` is added, under a new
/// integer object if its own is taken. The result is weighted if either input is.
#[pyfunction]
#[pyo3(signature = (graph1, graph2, weights="sum"))]
fn graph_union(
    py: Python<'_>,
    graph1: &Bound<'_, PyAny>,
    graph2: &Bound<'_, PyAny>,
    weights: &str,
) -> PyResult<Py<Graph>> {
    let combine: fn(f64, f64) -> f64 = match weights {
        "sum" => |a, b| a + b,
        "first" => |a, _| a,
        "second" => |_, b| b,
        "min" => f64::min,
        "max" => f64::max,
        _ => {
            return Err(GraphError::new_err(format!(
                "unknown weight combiner {weights:?}"
            )));
        }
    };
    let (a, b) = (Parts::extract(py, graph1)?, Parts::extract(py, graph2)?);
    if a.directed != b.directed {
        return Err(GraphError::new_err(
            "cannot unite a directed and an undirected graph",
        ));
    }
    let mut result = Parts {
        weighted: a.weighted || b.weighted,
        loops: a.loops || b.loops,
        multi: a.multi || b.multi,
        ..a
    };
    let vindex = PyDict::new(py);
    for (i, v) in result.vertices.iter().enumerate() {
        vindex.set_item(v, i)?;
    }
    let eindex = PyDict::new(py);
    for (i, (o, ..)) in result.edges.iter().enumerate() {
        eindex.set_item(o, i)?;
    }
    let mut map = Vec::with_capacity(b.vertices.len());
    for (v, attrs) in b.vertices.iter().zip(&b.vertex_attrs) {
        let i = match vindex.get_item(v)? {
            Some(i) => {
                let i = i.extract::<usize>()?;
                // a vertex of both graphs: the attributes of graph2 win
                result.vertex_attrs[i] = merged(py, &result.vertex_attrs[i], attrs)?;
                i
            }
            None => {
                let i = result.vertices.len();
                result.vertices.push(v.clone_ref(py));
                result.vertex_attrs.push(attrs.as_ref().map(|d| d.clone_ref(py)));
                vindex.set_item(v, i)?;
                i
            }
        };
        map.push(i);
    }
    let directed = result.directed;
    let mut next = 0i64;
    let weight = |w: Option<f64>| w.unwrap_or(1.0);
    for ((o, s, t, w), attrs) in b.edges.iter().zip(&b.edge_attrs) {
        let (s, t) = (map[*s], map[*t]);
        if let Some(i) = eindex.get_item(o)? {
            let i = i.extract::<usize>()?;
            let (_, es, et, ew) = &mut result.edges[i];
            let same = (*es, *et) == (s, t) || (!directed && (*es, *et) == (t, s));
            if same {
                if result.weighted {
                    *ew = Some(combine(weight(*ew), weight(*w)));
                }
                result.edge_attrs[i] = merged(py, &result.edge_attrs[i], attrs)?;
                continue;
            }
        }
        let mut obj = o.clone_ref(py);
        while eindex.contains(&obj)? {
            obj = next.into_pyobject(py)?.into_any().unbind();
            next += 1;
        }
        eindex.set_item(&obj, result.edges.len())?;
        result.edges.push((obj, s, t, *w));
        result.edge_attrs.push(attrs.as_ref().map(|d| d.clone_ref(py)));
    }
    result.graph_attrs = merged(py, &result.graph_attrs, &b.graph_attrs)?;
    if result.weighted {
        for e in &mut result.edges {
            e.3 = Some(weight(e.3));
        }
    }
    result.build(py)
}

/// The graph with the direction of every edge dropped. If both ``u -> v`` and ``v -> u`` exist
/// they become parallel edges, so the result allows parallel edges.
#[pyfunction]
fn as_undirected(py: Python<'_>, graph: &Bound<'_, PyAny>) -> PyResult<Py<Graph>> {
    let mut parts = Parts::extract(py, graph)?;
    if parts.directed {
        parts.directed = false;
        parts.multi = true;
    }
    parts.build(py)
}

/// The directed graph with every edge reversed (an undirected graph is copied unchanged).
#[pyfunction]
fn reverse_edges(py: Python<'_>, graph: &Bound<'_, PyAny>) -> PyResult<Py<Graph>> {
    let mut parts = Parts::extract(py, graph)?;
    if parts.directed {
        for e in &mut parts.edges {
            std::mem::swap(&mut e.1, &mut e.2);
        }
    }
    parts.build(py)
}

/// A weighted copy of ``graph`` with the given edge ``weights``: a dict from edge to weight
/// (missing edges get ``default``), a function of the edge, or a constant.
#[pyfunction]
#[pyo3(signature = (graph, weights, default=1.0))]
fn as_weighted(
    py: Python<'_>,
    graph: &Bound<'_, PyAny>,
    weights: &Bound<'_, PyAny>,
    default: f64,
) -> PyResult<Py<Graph>> {
    let mut parts = Parts::extract(py, graph)?;
    parts.weighted = true;
    for e in &mut parts.edges {
        e.3 = Some(spec_value(weights, e.0.clone_ref(py), default)?);
    }
    parts.build(py)
}

/// A copy of ``graph`` without edge weights.
#[pyfunction]
fn as_unweighted(py: Python<'_>, graph: &Bound<'_, PyAny>) -> PyResult<Py<Graph>> {
    let mut parts = Parts::extract(py, graph)?;
    parts.weighted = false;
    for e in &mut parts.edges {
        e.3 = None;
    }
    parts.build(py)
}

pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(copy_graph, m)?)?;
    m.add_function(wrap_pyfunction!(induced_subgraph, m)?)?;
    m.add_function(wrap_pyfunction!(edge_subgraph, m)?)?;
    m.add_function(wrap_pyfunction!(graph_union, m)?)?;
    m.add_function(wrap_pyfunction!(as_undirected, m)?)?;
    m.add_function(wrap_pyfunction!(reverse_edges, m)?)?;
    m.add_function(wrap_pyfunction!(as_weighted, m)?)?;
    m.add_function(wrap_pyfunction!(as_unweighted, m)?)?;
    Ok(())
}
