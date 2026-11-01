//! Conversion of `jgrapht` errors into Python exceptions.

use pyo3::PyErr;
use pyo3::create_exception;
use pyo3::exceptions::PyValueError;

create_exception!(
    jgrapht,
    GraphError,
    PyValueError,
    "Raised when a graph operation fails (missing vertex, forbidden loop, negative cycle, ...)."
);

pub fn graph_error(error: jgrapht::GraphError) -> PyErr {
    GraphError::new_err(error.to_string())
}
