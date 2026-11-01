use pyo3::prelude::*;
use pyo3::types::PyList;

mod alg;
mod attrs;
mod error;
mod formats;
mod generators;
mod graph;
mod labels;
mod sparse;
mod unmodifiable;

#[pymodule]
fn _jgrapht_rs(py: Python<'_>, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<graph::Graph>()?;
    m.add_class::<sparse::SparseGraph>()?;
    m.add_class::<graph::GraphPath>()?;
    m.add_class::<attrs::Attributes>()?;
    m.add("GraphError", py.get_type::<error::GraphError>())?;
    alg::register(m)?;
    generators::register(m)?;
    formats::register(m)?;
    unmodifiable::register(m)?;

    // everything registered above that is not private is public API
    let mut public: Vec<String> = m
        .dir()?
        .iter()
        .map(|name| name.extract::<String>())
        .collect::<PyResult<_>>()?;
    public.retain(|name| !name.starts_with('_'));
    public.sort();
    m.add("__all__", PyList::new(py, public)?)?;
    Ok(())
}
