//! Dynamic connectivity in a forest.

use jgrapht::alg::tree_connectivity::TreeDynamicConnectivity as RustConnectivity;
use pyo3::prelude::*;
use pyo3::types::PyDict;

use crate::error::{GraphError, graph_error};

/// Fully dynamic connectivity for a forest: add and remove elements, ``link`` two elements by an
/// edge and ``cut`` that edge again, and ask whether two elements are in the same tree, each in
/// logarithmic time. Elements are arbitrary hashable objects.
#[pyclass(module = "jgrapht")]
pub struct TreeDynamicConnectivity {
    inner: RustConnectivity<usize>,
    ids: Py<PyDict>,
    next_id: usize,
}

impl TreeDynamicConnectivity {
    fn id_of(&self, py: Python<'_>, element: &Bound<'_, PyAny>) -> PyResult<Option<usize>> {
        self.ids
            .bind(py)
            .get_item(element)?
            .map(|v| v.extract())
            .transpose()
    }

    fn id_or_new(&mut self, py: Python<'_>, element: &Bound<'_, PyAny>) -> PyResult<usize> {
        if let Some(id) = self.id_of(py, element)? {
            return Ok(id);
        }
        let id = self.next_id;
        self.next_id += 1;
        self.ids.bind(py).set_item(element, id)?;
        Ok(id)
    }
}

#[pymethods]
impl TreeDynamicConnectivity {
    #[new]
    fn new(py: Python<'_>) -> Self {
        TreeDynamicConnectivity {
            inner: RustConnectivity::new(),
            ids: PyDict::new(py).unbind(),
            next_id: 0,
        }
    }

    /// Adds an element; returns ``False`` if it was already present.
    fn add(&mut self, py: Python<'_>, element: Bound<'_, PyAny>) -> PyResult<bool> {
        let id = self.id_or_new(py, &element)?;
        Ok(self.inner.add(id))
    }

    /// Removes an element (cutting all its links); returns ``False`` if it was absent.
    fn remove(&mut self, py: Python<'_>, element: Bound<'_, PyAny>) -> PyResult<bool> {
        let Some(id) = self.id_of(py, &element)? else {
            return Ok(false);
        };
        let removed = self.inner.remove(&id);
        if removed {
            self.ids.bind(py).del_item(&element)?;
        }
        Ok(removed)
    }

    fn __contains__(&self, py: Python<'_>, element: Bound<'_, PyAny>) -> PyResult<bool> {
        Ok(self
            .id_of(py, &element)?
            .is_some_and(|id| self.inner.contains(&id)))
    }

    /// Whether the two elements are connected by a path of links. An element is never connected
    /// to itself unless it has been linked to something.
    fn connected(
        &self,
        py: Python<'_>,
        a: Bound<'_, PyAny>,
        b: Bound<'_, PyAny>,
    ) -> PyResult<bool> {
        match (self.id_of(py, &a)?, self.id_of(py, &b)?) {
            (Some(x), Some(y)) => Ok(self.inner.connected(&x, &y)),
            _ => Ok(false),
        }
    }

    /// Links two elements (adding them if needed); returns ``False`` if they are the same
    /// element or already connected, since a link would close a cycle.
    fn link(&mut self, py: Python<'_>, a: Bound<'_, PyAny>, b: Bound<'_, PyAny>) -> PyResult<bool> {
        let (x, y) = (self.id_or_new(py, &a)?, self.id_or_new(py, &b)?);
        Ok(self.inner.link(x, y))
    }

    /// Removes the link between two elements; returns ``False`` if they were not linked and
    /// raises :class:`GraphError` if an element is unknown.
    fn cut(&mut self, py: Python<'_>, a: Bound<'_, PyAny>, b: Bound<'_, PyAny>) -> PyResult<bool> {
        let (Some(x), Some(y)) = (self.id_of(py, &a)?, self.id_of(py, &b)?) else {
            return Err(GraphError::new_err("unknown element"));
        };
        self.inner.cut(&x, &y).map_err(graph_error)
    }
}

pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<TreeDynamicConnectivity>()?;
    Ok(())
}
