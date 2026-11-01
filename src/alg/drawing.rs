//! Two-dimensional graph layouts.

use std::collections::{HashMap, HashSet};

use jgrapht::alg::drawing::fr::FrLayoutAlgorithm2D;
use jgrapht::alg::drawing::layouts::{
    CircularLayoutAlgorithm2D, LayoutAlgorithm2D, RandomLayoutAlgorithm2D,
    RescaleLayoutAlgorithm2D, TwoLayeredBipartiteLayout2D,
};
use jgrapht::alg::drawing::model::{Box2D, LayoutModel2D, MapLayoutModel2D, Point2D};
use jgrapht::alg::drawing::{
    circular_layout as rust_circular, fruchterman_reingold as rust_fr, random_layout as rust_random,
};
use pyo3::prelude::*;
use pyo3::types::PyDict;
use rand::SeedableRng;
use rand::rngs::StdRng;

use crate::error::{GraphError, graph_error};
use crate::labels::dispatch;

fn rng(seed: Option<u64>) -> StdRng {
    match seed {
        Some(s) => StdRng::seed_from_u64(s),
        None => StdRng::from_os_rng(),
    }
}

/// Places the vertices evenly on a circle of the given ``radius``; returns ``{vertex: (x, y)}``.
#[pyfunction]
#[pyo3(signature = (graph, radius=1.0))]
fn circular_layout<'py>(
    py: Python<'py>,
    graph: &Bound<'py, PyAny>,
    radius: f64,
) -> PyResult<Bound<'py, PyDict>> {
    dispatch!(graph, |g, lab| lab
        .vertex_dict(py, rust_circular(g, radius)))
}

/// Places the vertices uniformly at random in a ``width`` by ``height`` box.
#[pyfunction]
#[pyo3(signature = (graph, width=1.0, height=1.0, seed=None))]
fn random_layout<'py>(
    py: Python<'py>,
    graph: &Bound<'py, PyAny>,
    width: f64,
    height: f64,
    seed: Option<u64>,
) -> PyResult<Bound<'py, PyDict>> {
    dispatch!(graph, |g, lab| lab
        .vertex_dict(py, rust_random(g, width, height, &mut rng(seed))))
}

/// Force-directed Fruchterman-Reingold layout in a ``width`` by ``height`` box.
#[pyfunction]
#[pyo3(signature = (graph, width=1.0, height=1.0, iterations=100, seed=None))]
fn fruchterman_reingold_layout<'py>(
    py: Python<'py>,
    graph: &Bound<'py, PyAny>,
    width: f64,
    height: f64,
    iterations: usize,
    seed: Option<u64>,
) -> PyResult<Bound<'py, PyDict>> {
    dispatch!(graph, |g, lab| {
        lab.vertex_dict(py, rust_fr(g, width, height, iterations, &mut rng(seed)))
    })
}

fn area_box(area: (f64, f64, f64, f64)) -> Box2D {
    Box2D::at(area.0, area.1, area.2, area.3)
}

fn to_positions<'py>(
    py: Python<'py>,
    lab: &crate::labels::Labels<'_>,
    model: &MapLayoutModel2D<usize>,
) -> PyResult<Bound<'py, PyDict>> {
    lab.vertex_dict(
        py,
        model.collect().into_iter().map(|(v, p)| (v, (p.x, p.y))),
    )
}

/// Lays the graph out inside ``area = (x, y, width, height)`` and returns ``{vertex: (x, y)}``.
///
/// ``algorithm`` is one of
///
/// * ``"circular"`` (default): evenly on a circle (``radius``, default fits the area),
/// * ``"random"``: uniformly at random (``seed``),
/// * ``"fruchterman_reingold"``: force-directed (``iterations``, ``normalization_factor``,
///   ``seed``; with ``theta`` in ``[0, 1]`` repulsion is approximated with a quadtree
///   (Barnes-Hut), much faster on large graphs),
/// * ``"bipartite"``: two layers for a bipartite graph (``first_partition`` lists the vertices
///   of the first layer, otherwise a bipartition is computed; ``vertical`` selects the layer
///   direction; ``order`` is ``"plain"``, ``"median"`` or ``"barycenter"`` to reduce crossings).
///
/// ``initial_positions`` (a ``{vertex: (x, y)}`` dict) seeds the force-directed layout.
#[pyfunction]
#[pyo3(signature = (
    graph, algorithm="circular", area=(0.0, 0.0, 1.0, 1.0), seed=None, radius=None, iterations=100,
    normalization_factor=0.5, theta=None, first_partition=None, vertical=true, order="plain",
    initial_positions=None,
))]
#[allow(clippy::too_many_arguments)]
fn layout_2d<'py>(
    py: Python<'py>,
    graph: &Bound<'py, PyAny>,
    algorithm: &str,
    area: (f64, f64, f64, f64),
    seed: Option<u64>,
    radius: Option<f64>,
    iterations: usize,
    normalization_factor: f64,
    theta: Option<f64>,
    first_partition: Option<Vec<Bound<'py, PyAny>>>,
    vertical: bool,
    order: &str,
    initial_positions: Option<Bound<'py, PyDict>>,
) -> PyResult<Bound<'py, PyDict>> {
    dispatch!(graph, |g, lab| {
        let mut model = MapLayoutModel2D::<usize>::new(area_box(area));
        match algorithm {
            "circular" => {
                let mut a = match radius {
                    Some(r) => CircularLayoutAlgorithm2D::new(r).map_err(graph_error)?,
                    None => CircularLayoutAlgorithm2D::default(),
                };
                a.layout(g, &mut model).map_err(graph_error)?;
            }
            "random" => {
                let seed = seed.unwrap_or_else(|| u64::from(rand::random::<u32>()));
                RandomLayoutAlgorithm2D::with_seed(seed as i64)
                    .layout(g, &mut model)
                    .map_err(graph_error)?;
            }
            "fruchterman_reingold" => {
                let r = rng(seed);
                let mut a = match theta {
                    Some(t) => FrLayoutAlgorithm2D::indexed(iterations, t, normalization_factor, r)
                        .map_err(graph_error)?,
                    None => FrLayoutAlgorithm2D::new(iterations, normalization_factor, r),
                };
                if let Some(init) = &initial_positions {
                    let mut map: HashMap<usize, Point2D> = HashMap::new();
                    for (v, p) in init.iter() {
                        let (x, y): (f64, f64) = p.extract()?;
                        map.insert(lab.vertex_id(py, &v)?, Point2D::of(x, y));
                    }
                    a.initializer = Some(Box::new(move |v| map.get(v).copied()));
                }
                a.layout(g, &mut model).map_err(graph_error)?;
            }
            "bipartite" => {
                let mut a = match order {
                    "plain" => TwoLayeredBipartiteLayout2D::new(),
                    "median" => TwoLayeredBipartiteLayout2D::median_greedy(),
                    "barycenter" => TwoLayeredBipartiteLayout2D::barycenter_greedy(),
                    other => return Err(GraphError::new_err(format!("unknown order {other:?}"))),
                }
                .with_vertical(vertical);
                if let Some(first) = &first_partition {
                    let ids: HashSet<usize> = first
                        .iter()
                        .map(|v| lab.vertex_id(py, v))
                        .collect::<PyResult<_>>()?;
                    a = a.with_first_partition(ids);
                }
                a.layout(g, &mut model).map_err(graph_error)?;
            }
            other => return Err(GraphError::new_err(format!("unknown algorithm {other:?}"))),
        }
        to_positions(py, &lab, &model)
    })
}

/// Recentres a layout on the middle of ``area`` and scales it so that its largest extent from
/// the centre is ``scale``. ``positions`` is a ``{vertex: (x, y)}`` dict covering every vertex.
#[pyfunction]
#[pyo3(signature = (graph, positions, scale=1.0, area=(0.0, 0.0, 1.0, 1.0)))]
fn rescale_layout<'py>(
    py: Python<'py>,
    graph: &Bound<'py, PyAny>,
    positions: &Bound<'py, PyDict>,
    scale: f64,
    area: (f64, f64, f64, f64),
) -> PyResult<Bound<'py, PyDict>> {
    dispatch!(graph, |g, lab| {
        let mut model = MapLayoutModel2D::<usize>::new(area_box(area));
        for (v, p) in positions.iter() {
            let (x, y): (f64, f64) = p.extract()?;
            model.put(lab.vertex_id(py, &v)?, Point2D::of(x, y));
        }
        RescaleLayoutAlgorithm2D::new(scale)
            .and_then(|mut a| a.layout(g, &mut model))
            .map_err(graph_error)?;
        to_positions(py, &lab, &model)
    })
}

pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(layout_2d, m)?)?;
    m.add_function(wrap_pyfunction!(rescale_layout, m)?)?;
    m.add_function(wrap_pyfunction!(circular_layout, m)?)?;
    m.add_function(wrap_pyfunction!(random_layout, m)?)?;
    m.add_function(wrap_pyfunction!(fruchterman_reingold_layout, m)?)?;
    Ok(())
}
