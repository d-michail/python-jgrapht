//! A read-only wrapper around a graph.
//!
//! The wrapper holds a reference to its base graph, so it always shows the base's current state,
//! and it refuses every modification. Algorithms see straight through it: [`unwrap_readonly`]
//! replaces the wrapper by its base before a graph is dispatched on, so it adds no compiled code.

use pyo3::prelude::*;
use pyo3::types::{PyDict, PyTuple};

use crate::attrs::{Attributes, read_only};
use crate::error::GraphError;
use crate::graph::Graph;
use crate::sparse::SparseGraph;

/// A read-only wrapper around a graph.
///
/// It holds a reference to ``graph`` (a :class:`Graph` or :class:`SparseGraph`), so changes made
/// to ``graph`` by its owner are visible through it, but the wrapper itself cannot be used to
/// modify the graph: every mutating method raises :class:`GraphError`. It can be passed to every
/// algorithm that takes a single graph.
#[pyclass(module = "jgrapht", frozen)]
pub struct UnmodifiableGraph {
    pub base: Py<PyAny>,
}

/// If `obj` is an [`UnmodifiableGraph`], its base graph; otherwise `obj` itself.
pub fn unwrap_readonly<'py>(obj: &Bound<'py, PyAny>) -> Bound<'py, PyAny> {
    match obj.cast::<UnmodifiableGraph>() {
        Ok(wrapper) => wrapper.get().base.bind(obj.py()).clone(),
        Err(_) => obj.clone(),
    }
}

/// Methods that are the base's own, because they only read.
macro_rules! forward {
    ($($name:ident),* $(,)?) => {
        #[pymethods]
        impl UnmodifiableGraph {$(
            #[pyo3(signature = (*args))]
            fn $name<'py>(
                &self,
                py: Python<'py>,
                args: &Bound<'py, PyTuple>,
            ) -> PyResult<Bound<'py, PyAny>> {
                self.base.bind(py).call_method(stringify!($name), args, None)
            }
        )*}
    };
}

forward!(
    vertices,
    edges,
    edge_count,
    contains_vertex,
    contains_edge,
    edge_source,
    edge_target,
    edge_weight,
    edges_between,
    edges_of,
    out_edges_of,
    in_edges_of,
    degree_of,
    out_degree_of,
    in_degree_of,
    neighbors_of
);

/// Methods that modify the graph, which this wrapper does not allow.
macro_rules! refuse {
    ($($name:ident),* $(,)?) => {
        #[pymethods]
        impl UnmodifiableGraph {$(
            #[pyo3(signature = (*_args, **_kwargs))]
            fn $name(
                &self,
                _args: &Bound<'_, PyTuple>,
                _kwargs: Option<&Bound<'_, PyDict>>,
            ) -> PyResult<()> {
                Err(GraphError::new_err("this graph is unmodifiable"))
            }
        )*}
    };
}

refuse!(
    add_vertex,
    new_vertex,
    remove_vertex,
    add_edge,
    remove_edge,
    set_edge_weight
);

#[pymethods]
impl UnmodifiableGraph {
    #[new]
    fn new(graph: &Bound<'_, PyAny>) -> PyResult<Self> {
        if !(graph.is_instance_of::<Graph>() || graph.is_instance_of::<SparseGraph>()) {
            return Err(crate::labels::type_error(graph));
        }
        Ok(UnmodifiableGraph {
            base: graph.clone().unbind(),
        })
    }

    /// The graph this wrapper looks at.
    #[getter]
    fn graph(&self, py: Python<'_>) -> Py<PyAny> {
        self.base.clone_ref(py)
    }

    #[getter]
    fn directed(&self, py: Python<'_>) -> PyResult<bool> {
        self.base.bind(py).getattr("directed")?.extract()
    }

    #[getter]
    fn weighted(&self, py: Python<'_>) -> PyResult<bool> {
        self.base.bind(py).getattr("weighted")?.extract()
    }

    #[getter]
    fn allow_self_loops(&self, py: Python<'_>) -> PyResult<bool> {
        self.base.bind(py).getattr("allow_self_loops")?.extract()
    }

    #[getter]
    fn allow_multiple_edges(&self, py: Python<'_>) -> PyResult<bool> {
        self.base.bind(py).getattr("allow_multiple_edges")?.extract()
    }

    /// A read-only mapping from a vertex to a read-only view of its attributes.
    #[getter]
    fn vertex_attrs(&self, py: Python<'_>) -> Attributes {
        Attributes::new(self.base.clone_ref(py), false, true)
    }

    /// A read-only mapping from an edge to a read-only view of its attributes.
    #[getter]
    fn edge_attrs(&self, py: Python<'_>) -> Attributes {
        Attributes::new(self.base.clone_ref(py), true, true)
    }

    /// A read-only view of the attributes of the graph.
    #[getter]
    fn graph_attrs(&self, py: Python<'_>) -> PyResult<Py<PyAny>> {
        read_only(py, self.base.bind(py).getattr("graph_attrs")?.unbind())
    }

    fn __len__(&self, py: Python<'_>) -> PyResult<usize> {
        self.base.bind(py).len()
    }

    fn __contains__(&self, py: Python<'_>, v: Bound<'_, PyAny>) -> PyResult<bool> {
        self.base.bind(py).contains(v)
    }

    fn __iter__<'py>(&self, py: Python<'py>) -> PyResult<Bound<'py, PyAny>> {
        self.base.bind(py).try_iter().map(|i| i.into_any())
    }

    fn __repr__(&self, py: Python<'_>) -> PyResult<String> {
        Ok(format!("UnmodifiableGraph({})", self.base.bind(py).repr()?))
    }
}

/// A read-only wrapper around ``graph``: it shows the graph's current state, and every attempt to
/// modify the graph through it raises :class:`GraphError`.
///
/// >>> import jgrapht as jg
/// >>> g = jg.path_graph(3)
/// >>> r = jg.as_unmodifiable(g)
/// >>> r.edge_count()
/// 2
/// >>> g.add_edge(0, 2)  # the owner can still modify the graph, and r sees it
/// 2
/// >>> r.edge_count()
/// 3
#[pyfunction]
fn as_unmodifiable(graph: &Bound<'_, PyAny>) -> PyResult<UnmodifiableGraph> {
    UnmodifiableGraph::new(graph)
}

pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<UnmodifiableGraph>()?;
    m.add_function(wrap_pyfunction!(as_unmodifiable, m)?)?;
    Ok(())
}
