//! Vertex coloring.

use std::collections::HashMap;

use jgrapht::alg::color::{
    self, BrownBacktrackColoring, ChordalGraphColoring, ColorRefinementAlgorithm,
    RandomGreedyColoring,
};
use jgrapht::alg::interfaces::VertexColoringAlgorithm;
use pyo3::prelude::*;
use pyo3::types::PyDict;
use rand::SeedableRng;
use rand::rngs::StdRng;

use crate::error::{GraphError, graph_error};
use crate::labels::{dispatch, dispatch_undirected};

/// Vertex coloring as ``(number_of_colors, {vertex: color})`` with colors ``0..k``.
///
/// ``algorithm`` is ``"greedy"`` (default), ``"largest_degree_first"``,
/// ``"smallest_degree_last"``, ``"saturation_degree"``, ``"random_greedy"`` (seedable),
/// ``"brown_backtrack"`` (exact, exponential: finds the chromatic number),
/// ``"color_refinement"`` (the coarsest stable coloring, not necessarily proper) or, for
/// undirected chordal graphs, ``"chordal"`` (optimal).
#[pyfunction]
#[pyo3(signature = (graph, algorithm="greedy", seed=None))]
fn coloring<'py>(
    py: Python<'py>,
    graph: &Bound<'py, PyAny>,
    algorithm: &str,
    seed: Option<u64>,
) -> PyResult<(usize, Bound<'py, PyDict>)> {
    if algorithm == "chordal" {
        return dispatch_undirected!(graph, |g, lab| {
            let c = ChordalGraphColoring::new(g)
                .coloring()
                .ok_or_else(|| GraphError::new_err("graph is not chordal"))?;
            Ok((c.count, lab.vertex_dict(py, c.colors)?))
        });
    }
    dispatch!(graph, |g, lab| {
        let c = match algorithm {
            "greedy" => color::greedy_coloring(g),
            "largest_degree_first" => color::largest_degree_first_coloring(g),
            "smallest_degree_last" => color::smallest_degree_last_coloring(g),
            "saturation_degree" => color::saturation_degree_coloring(g),
            "random_greedy" => {
                let rng = match seed {
                    Some(s) => StdRng::seed_from_u64(s),
                    None => StdRng::from_os_rng(),
                };
                RandomGreedyColoring::new(g, rng)
                    .coloring()
                    .map_err(graph_error)?
            }
            "brown_backtrack" => BrownBacktrackColoring::new(g)
                .coloring()
                .map_err(graph_error)?,
            "color_refinement" => ColorRefinementAlgorithm::new(g)
                .coloring()
                .map_err(graph_error)?,
            other => return Err(GraphError::new_err(format!("unknown algorithm {other:?}"))),
        };
        Ok((c.count, lab.vertex_dict(py, c.colors)?))
    })
}

/// Whether ``colors`` (a ``{vertex: color}`` dict covering every vertex) is a proper coloring:
/// no edge joins two vertices of the same color.
#[pyfunction]
fn is_proper_coloring(
    py: Python<'_>,
    graph: &Bound<'_, PyAny>,
    colors: &Bound<'_, PyDict>,
) -> PyResult<bool> {
    dispatch!(graph, |g, lab| {
        let mut map: HashMap<usize, usize> = HashMap::new();
        for (v, c) in colors.iter() {
            map.insert(lab.vertex_id(py, &v)?, c.extract()?);
        }
        Ok(color::is_proper_coloring(g, &map))
    })
}

pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(coloring, m)?)?;
    m.add_function(wrap_pyfunction!(is_proper_coloring, m)?)?;
    Ok(())
}
