//! Graph algorithms exposed as module-level functions.
//!
//! One submodule per family; each registers its own functions and result classes. Every function
//! accepts a `Graph` or a `SparseGraph`.

mod astar;
mod capacitated;
mod clustering;
mod coloring;
mod components;
mod cuts;
mod cycles;
mod decompositions;
mod drawing;
mod dynamic;
mod flow;
mod isomorphism;
mod matching;
mod metrics;
mod paths;
mod routing;
mod scoring;
mod shortestpaths;
mod similarity;
mod structure;
mod subsets;
mod tours;
mod transforms;
mod traversal;
mod trees;
mod derived;

use pyo3::prelude::*;

pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    astar::register(m)?;
    capacitated::register(m)?;
    clustering::register(m)?;
    coloring::register(m)?;
    components::register(m)?;
    cuts::register(m)?;
    cycles::register(m)?;
    decompositions::register(m)?;
    drawing::register(m)?;
    dynamic::register(m)?;
    flow::register(m)?;
    isomorphism::register(m)?;
    matching::register(m)?;
    metrics::register(m)?;
    paths::register(m)?;
    routing::register(m)?;
    scoring::register(m)?;
    shortestpaths::register(m)?;
    similarity::register(m)?;
    structure::register(m)?;
    subsets::register(m)?;
    tours::register(m)?;
    transforms::register(m)?;
    traversal::register(m)?;
    trees::register(m)?;
    derived::register(m)?;
    Ok(())
}
