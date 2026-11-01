//! Cliques, independent sets and vertex covers.

use jgrapht::alg::centers::GonHeuristic;
use jgrapht::alg::centers::greedy_k_center;
use jgrapht::alg::densest::{GoldbergMaximumDensitySubgraph, greedy_densest_subgraph};
use jgrapht::alg::holes;
use jgrapht::alg::interfaces::CentersLocationAlgorithm;
use std::collections::HashMap;

use jgrapht::GraphExt as _;
use jgrapht::alg::clique::{
    BronKerboschCliqueFinder, ChordalGraphMaxCliqueFinder, CliqueMinimalSeparatorDecomposition,
    DegeneracyBronKerboschCliqueFinder, PivotBronKerboschCliqueFinder,
};
use jgrapht::alg::cover::{
    EdgeBasedTwoApproxVertexCover, bar_yehuda_even_vertex_cover, bipartite_vertex_cover,
    clarkson_vertex_cover, is_vertex_cover as rust_is_vertex_cover,
};
use jgrapht::alg::cycle::{BergeGraphInspector, MinimalVertexSeparatorFinder};
use jgrapht::alg::independent_set::ChordalGraphIndependentSetFinder;
use jgrapht::alg::interfaces::{MaximalCliqueEnumerationAlgorithm, VertexCoverAlgorithm};
use jgrapht::alg::metrics::{naive_count_triangles, number_of_triangles as rust_triangles};
use jgrapht::alg::{clique, cover};
use pyo3::prelude::*;

use crate::error::{GraphError, graph_error};
use crate::graph::Graph;
use crate::labels::{dispatch, dispatch_undirected, spec_value};

/// All maximal cliques, as lists of vertices. ``algorithm`` is ``"default"``,
/// ``"bron_kerbosch"``, ``"pivot"`` (Bron-Kerbosch with pivoting) or ``"degeneracy"``
/// (Bron-Kerbosch over a degeneracy ordering); they all find the same cliques.
#[pyfunction]
#[pyo3(signature = (graph, algorithm="default"))]
fn maximal_cliques(
    py: Python<'_>,
    graph: &Bound<'_, PyAny>,
    algorithm: &str,
) -> PyResult<Vec<Vec<Py<PyAny>>>> {
    dispatch!(graph, |g, lab| {
        let cliques: Vec<Vec<usize>> = match algorithm {
            "default" => clique::maximal_cliques(g),
            "bron_kerbosch" => sorted(BronKerboschCliqueFinder::new(g).cliques()),
            "pivot" => sorted(PivotBronKerboschCliqueFinder::new(g).cliques()),
            "degeneracy" => sorted(DegeneracyBronKerboschCliqueFinder::new(g).cliques()),
            other => return Err(GraphError::new_err(format!("unknown algorithm {other:?}"))),
        };
        Ok(cliques.into_iter().map(|c| lab.vertices(py, c)).collect())
    })
}

fn sorted(cliques: jgrapht::Result<&[std::collections::HashSet<usize>]>) -> Vec<Vec<usize>> {
    cliques
        .expect("clique enumeration without a timeout cannot fail")
        .iter()
        .map(|c| {
            let mut v: Vec<usize> = c.iter().copied().collect();
            v.sort_unstable();
            v
        })
        .collect()
}

/// Whether ``vertices`` are pairwise adjacent.
#[pyfunction]
fn is_clique(
    py: Python<'_>,
    graph: &Bound<'_, PyAny>,
    vertices: Vec<Bound<'_, PyAny>>,
) -> PyResult<bool> {
    dispatch!(graph, |g, lab| {
        let vs: Vec<usize> = vertices
            .iter()
            .map(|v| lab.vertex_id(py, v))
            .collect::<PyResult<_>>()?;
        Ok(clique::is_clique(g, &vs))
    })
}

/// Whether no two of ``vertices`` are adjacent.
#[pyfunction]
fn is_independent_set(
    py: Python<'_>,
    graph: &Bound<'_, PyAny>,
    vertices: Vec<Bound<'_, PyAny>>,
) -> PyResult<bool> {
    dispatch!(graph, |g, lab| {
        let vs: Vec<usize> = vertices
            .iter()
            .map(|v| lab.vertex_id(py, v))
            .collect::<PyResult<_>>()?;
        Ok(clique::is_independent_set(g, &vs))
    })
}

/// A maximum clique of a chordal undirected graph in linear time, or ``None`` if the graph is
/// not chordal.
#[pyfunction]
fn chordal_maximum_clique(
    py: Python<'_>,
    graph: &Bound<'_, PyAny>,
) -> PyResult<Option<Vec<Py<PyAny>>>> {
    dispatch_undirected!(graph, |g, lab| {
        Ok(ChordalGraphMaxCliqueFinder::new(g)
            .clique()
            .map(|c| lab.vertices(py, sort_set(c))))
    })
}

/// A maximum independent set of a chordal undirected graph in linear time, or ``None`` if the
/// graph is not chordal.
#[pyfunction]
fn chordal_maximum_independent_set(
    py: Python<'_>,
    graph: &Bound<'_, PyAny>,
) -> PyResult<Option<Vec<Py<PyAny>>>> {
    dispatch_undirected!(graph, |g, lab| {
        Ok(ChordalGraphIndependentSetFinder::new(g)
            .independent_set()
            .map(|c| lab.vertices(py, sort_set(c))))
    })
}

fn sort_set(set: std::collections::HashSet<usize>) -> Vec<usize> {
    let mut v: Vec<usize> = set.into_iter().collect();
    v.sort_unstable();
    v
}

/// The minimal vertex separators of a chordal undirected graph as ``{separator: multiplicity}``
/// where each separator is a tuple of vertices; ``None`` if the graph is not chordal.
#[pyfunction]
fn chordal_minimal_separators<'py>(
    py: Python<'py>,
    graph: &Bound<'py, PyAny>,
) -> PyResult<Option<Bound<'py, pyo3::types::PyDict>>> {
    dispatch_undirected!(graph, |g, lab| {
        let mut finder = MinimalVertexSeparatorFinder::new(g);
        let Some(separators) = finder.minimal_separators_with_multiplicities() else {
            return Ok(None);
        };
        let out = pyo3::types::PyDict::new(py);
        for (sep, count) in separators {
            let key = pyo3::types::PyTuple::new(py, lab.vertices(py, sep.iter().copied()))?;
            out.set_item(key, *count)?;
        }
        Ok(Some(out))
    })
}

/// The clique minimal separator decomposition of an undirected graph.
#[pyclass(module = "jgrapht", frozen)]
pub struct CliqueSeparatorDecomposition {
    atoms: Vec<Vec<Py<PyAny>>>,
    separators: Vec<Vec<Py<PyAny>>>,
    generators: Vec<Py<PyAny>>,
    meo: Vec<Py<PyAny>>,
    fill_edges: Vec<(Py<PyAny>, Py<PyAny>)>,
    chordal: bool,
    triangulation: Py<Graph>,
}

#[pymethods]
impl CliqueSeparatorDecomposition {
    /// The atoms: the maximal subgraphs without a clique separator, as vertex lists.
    #[getter]
    fn atoms(&self, py: Python<'_>) -> Vec<Vec<Py<PyAny>>> {
        self.atoms
            .iter()
            .map(|a| a.iter().map(|v| v.clone_ref(py)).collect())
            .collect()
    }

    /// The clique minimal separators, as vertex lists.
    #[getter]
    fn separators(&self, py: Python<'_>) -> Vec<Vec<Py<PyAny>>> {
        self.separators
            .iter()
            .map(|a| a.iter().map(|v| v.clone_ref(py)).collect())
            .collect()
    }

    /// The generators of the minimal elimination ordering.
    #[getter]
    fn generators(&self, py: Python<'_>) -> Vec<Py<PyAny>> {
        self.generators.iter().map(|v| v.clone_ref(py)).collect()
    }

    /// The minimal elimination ordering.
    #[getter]
    fn minimal_elimination_ordering(&self, py: Python<'_>) -> Vec<Py<PyAny>> {
        self.meo.iter().map(|v| v.clone_ref(py)).collect()
    }

    /// The edges added by the minimal triangulation.
    #[getter]
    fn fill_edges(&self, py: Python<'_>) -> Vec<(Py<PyAny>, Py<PyAny>)> {
        self.fill_edges
            .iter()
            .map(|(a, b)| (a.clone_ref(py), b.clone_ref(py)))
            .collect()
    }

    /// Whether the graph is chordal (the triangulation added no edge).
    #[getter]
    fn is_chordal(&self) -> bool {
        self.chordal
    }

    /// The minimal triangulation as a :class:`Graph`.
    #[getter]
    fn minimal_triangulation(&self, py: Python<'_>) -> Py<Graph> {
        self.triangulation.clone_ref(py)
    }
}

/// Decomposes an undirected graph by its clique minimal separators.
#[pyfunction]
fn clique_minimal_separator_decomposition(
    py: Python<'_>,
    graph: &Bound<'_, PyAny>,
) -> PyResult<CliqueSeparatorDecomposition> {
    dispatch_undirected!(graph, |g, lab| {
        let mut d = CliqueMinimalSeparatorDecomposition::new(g).map_err(graph_error)?;
        let chordal = d.is_chordal();
        let fill: Vec<(usize, usize)> = d.fill_edges().to_vec();
        let meo = d.meo().to_vec();
        let generators = d.generators().to_vec();
        let tri = d.minimal_triangulation().clone();
        let order: Vec<usize> = tri.vertices_cloned().collect();
        let index: HashMap<usize, usize> = order.iter().enumerate().map(|(i, v)| (*v, i)).collect();
        let tri_edges = tri
            .edges_cloned()
            .map(|e| {
                let (a, b) = tri.edge_endpoints(&e).expect("edge of the triangulation");
                (index[a], index[b], None)
            })
            .collect();
        let triangulation = Graph::from_parts(py, false, lab.vertices(py, order), tri_edges)?;
        let to_lists = |sets: &[jgrapht::util::HashableSet<usize>]| -> Vec<Vec<Py<PyAny>>> {
            sets.iter()
                .map(|s| lab.vertices(py, sort_set(s.0.clone())))
                .collect()
        };
        let atoms = to_lists(d.atoms());
        let separators = to_lists(d.separators());
        Ok(CliqueSeparatorDecomposition {
            atoms,
            separators,
            generators: lab.vertices(py, generators),
            meo: lab.vertices(py, meo),
            fill_edges: fill
                .into_iter()
                .map(|(a, b)| (lab.vertex_obj(py, a), lab.vertex_obj(py, b)))
                .collect(),
            chordal,
            triangulation,
        })
    })
}

/// A certificate that an undirected graph is not Berge (perfect): ``("odd_hole", vertices)`` or
/// ``("odd_antihole", vertices)``, or ``None`` if the graph is a Berge graph. The vertex list is
/// a closed walk: its first vertex is repeated at the end.
#[pyfunction]
fn berge_certificate(
    py: Python<'_>,
    graph: &Bound<'_, PyAny>,
) -> PyResult<Option<(&'static str, Vec<Py<PyAny>>)>> {
    dispatch_undirected!(graph, |g, lab| {
        let mut inspector = BergeGraphInspector::new();
        if inspector
            .is_berge_with_certificate(g, true)
            .map_err(graph_error)?
        {
            return Ok(None);
        }
        Ok(inspector.certificate().map(|c| {
            (
                if c.is_hole() {
                    "odd_hole"
                } else {
                    "odd_antihole"
                },
                lab.vertices(py, c.vertex_list().iter().copied()),
            )
        }))
    })
}

/// The number of triangles in the graph (edge direction ignored).
#[pyfunction]
fn number_of_triangles(graph: &Bound<'_, PyAny>) -> PyResult<u64> {
    dispatch!(graph, |g, _lab| Ok(rust_triangles(g)))
}

/// The number of triangles whose three vertices all lie in ``vertices``.
#[pyfunction]
fn count_triangles_among(
    py: Python<'_>,
    graph: &Bound<'_, PyAny>,
    vertices: Vec<Bound<'_, PyAny>>,
) -> PyResult<u64> {
    dispatch!(graph, |g, lab| {
        let vs: Vec<usize> = vertices
            .iter()
            .map(|v| lab.vertex_id(py, v))
            .collect::<PyResult<_>>()?;
        Ok(naive_count_triangles(g, &vs))
    })
}

/// A maximum clique (exact; exponential in the worst case).
#[pyfunction]
fn maximum_clique(py: Python<'_>, graph: &Bound<'_, PyAny>) -> PyResult<Vec<Py<PyAny>>> {
    dispatch!(graph, |g, lab| Ok(
        lab.vertices(py, clique::maximum_clique(g))
    ))
}

/// A maximal independent set built greedily.
#[pyfunction]
fn greedy_independent_set(py: Python<'_>, graph: &Bound<'_, PyAny>) -> PyResult<Vec<Py<PyAny>>> {
    dispatch!(graph, |g, lab| Ok(
        lab.vertices(py, clique::greedy_independent_set(g))
    ))
}

/// A maximum independent set (exact; exponential in the worst case, for small graphs).
#[pyfunction]
fn maximum_independent_set(py: Python<'_>, graph: &Bound<'_, PyAny>) -> PyResult<Vec<Py<PyAny>>> {
    dispatch!(graph, |g, lab| Ok(
        lab.vertices(py, clique::maximum_independent_set(g))
    ))
}

/// A vertex cover as ``(weight, vertices)``.
///
/// ``algorithm`` is ``"greedy"`` (default), ``"two_approximation"``, ``"bar_yehuda_even"`` or
/// ``"clarkson"`` (the last two weighted 2-approximations), or, for undirected graphs,
/// ``"edge_based_two_approximation"`` and ``"bipartite"`` (exact, for bipartite graphs).
/// ``weights`` gives the vertex weights as a dict (missing vertices weigh 1), a callable or a
/// constant; only the weighted algorithms use it.
#[pyfunction]
#[pyo3(signature = (graph, algorithm="greedy", weights=None))]
fn vertex_cover(
    py: Python<'_>,
    graph: &Bound<'_, PyAny>,
    algorithm: &str,
    weights: Option<Bound<'_, PyAny>>,
) -> PyResult<(f64, Vec<Py<PyAny>>)> {
    let unknown = |a: &str| GraphError::new_err(format!("unknown algorithm {a:?}"));
    match algorithm {
        "edge_based_two_approximation" | "bipartite" => dispatch_undirected!(graph, |g, lab| {
            let c = if algorithm == "bipartite" {
                bipartite_vertex_cover(g)
            } else {
                EdgeBasedTwoApproxVertexCover::new(g).and_then(|a| a.vertex_cover())
            }
            .map_err(graph_error)?;
            Ok((c.weight, lab.vertices(py, c.vertices)))
        }),
        "greedy" | "two_approximation" | "bar_yehuda_even" | "clarkson" => {
            dispatch!(graph, |g, lab| {
                let mut w: HashMap<usize, f64> = HashMap::new();
                if let Some(spec) = &weights {
                    for v in g.vertices_cloned() {
                        w.insert(v, spec_value(spec, lab.vertex_obj(py, v), 1.0)?);
                    }
                }
                let weight = |v: &usize| w.get(v).copied().unwrap_or(1.0);
                let c = match algorithm {
                    "greedy" => cover::greedy_vertex_cover(g),
                    "two_approximation" => cover::two_approximation_vertex_cover(g),
                    "bar_yehuda_even" => bar_yehuda_even_vertex_cover(g, weight),
                    _ => clarkson_vertex_cover(g, weight),
                };
                Ok((c.weight, lab.vertices(py, c.vertices)))
            })
        }
        other => Err(unknown(other)),
    }
}

/// Whether ``vertices`` cover every edge of the graph.
#[pyfunction]
fn is_vertex_cover(
    py: Python<'_>,
    graph: &Bound<'_, PyAny>,
    vertices: Vec<Bound<'_, PyAny>>,
) -> PyResult<bool> {
    dispatch!(graph, |g, lab| {
        let vs: Vec<usize> = vertices
            .iter()
            .map(|v| lab.vertex_id(py, v))
            .collect::<PyResult<_>>()?;
        Ok(rust_is_vertex_cover(g, &vs))
    })
}

/// ``k`` centers minimising the largest distance from a vertex to its nearest center (greedy
/// 2-approximation), as ``(centers, radius)``. ``weighted`` uses edge weights as distances.
#[pyfunction]
#[pyo3(signature = (graph, k, weighted=false))]
fn k_center(
    py: Python<'_>,
    graph: &Bound<'_, PyAny>,
    k: usize,
    weighted: bool,
) -> PyResult<(Vec<Py<PyAny>>, f64)> {
    dispatch!(graph, |g, lab| {
        let (centers, radius) = greedy_k_center(g, k, weighted).map_err(graph_error)?;
        Ok((lab.vertices(py, centers), radius))
    })
}

/// A dense subgraph as ``(vertices, density)`` with density = total edge weight / number of
/// vertices.
///
/// ``algorithm`` is ``"greedy"`` (default; peeling, a 1/2-approximation) or ``"goldberg"``
/// (exact, via repeated minimum cuts; ``epsilon`` is the precision of the search). For
/// ``"goldberg"`` ``node_weights`` (a dict, a callable or a constant; missing vertices weigh 1)
/// changes the density to ``(total edge weight + total node weight) / number of vertices``, or,
/// with ``per_edge_weight``, to ``total edge weight / total node weight``.
#[pyfunction]
#[pyo3(signature = (graph, algorithm="greedy", epsilon=1e-6, node_weights=None, per_edge_weight=false))]
fn densest_subgraph(
    py: Python<'_>,
    graph: &Bound<'_, PyAny>,
    algorithm: &str,
    epsilon: f64,
    node_weights: Option<Bound<'_, PyAny>>,
    per_edge_weight: bool,
) -> PyResult<(Vec<Py<PyAny>>, f64)> {
    dispatch!(graph, |g, lab| match algorithm {
        "greedy" => {
            let (vs, density) = greedy_densest_subgraph(g);
            Ok((lab.vertices(py, vs), density))
        }
        "goldberg" => {
            // the algorithm needs two vertex values outside the graph for its flow network
            let top = g.vertices_cloned().max().map_or(0, |m| m + 1);
            let (s, t) = (top, top + 1);
            let mut w: HashMap<usize, f64> = HashMap::new();
            if let Some(spec) = &node_weights {
                for v in g.vertices_cloned() {
                    w.insert(v, spec_value(spec, lab.vertex_obj(py, v), 1.0)?);
                }
            }
            let mut a = match (&node_weights, per_edge_weight) {
                (None, _) => GoldbergMaximumDensitySubgraph::new(g, s, t, epsilon),
                (Some(_), false) => {
                    GoldbergMaximumDensitySubgraph::with_node_weights(g, s, t, epsilon, move |v| {
                        w[v]
                    })
                }
                (Some(_), true) => {
                    GoldbergMaximumDensitySubgraph::with_node_weight_per_edge_weight(
                        g,
                        s,
                        t,
                        epsilon,
                        move |v| w[v],
                    )
                }
            }
            .map_err(graph_error)?;
            let sub = a.densest_subgraph().map_err(graph_error)?;
            let density = a.density().map_err(graph_error)?;
            let mut vs: Vec<usize> = sub.vertices_cloned().collect();
            vs.sort_unstable();
            Ok((lab.vertices(py, vs), density))
        }
        other => Err(GraphError::new_err(format!("unknown algorithm {other:?}"))),
    })
}

/// ``k`` centers by Gon's farthest-point heuristic, a 2-approximation for a *complete*
/// undirected graph whose edge weights are metric distances: returns
/// ``(centers, assignment, radius)`` with ``assignment`` mapping each non-center vertex to its
/// center. ``initial_centers`` optionally seeds the choice; otherwise ``seed`` picks randomly.
#[pyfunction]
#[pyo3(signature = (graph, k, seed=None, initial_centers=None))]
#[allow(clippy::type_complexity)]
fn gon_k_center<'py>(
    py: Python<'py>,
    graph: &Bound<'py, PyAny>,
    k: usize,
    seed: Option<u64>,
    initial_centers: Option<Vec<Bound<'py, PyAny>>>,
) -> PyResult<(Vec<Py<PyAny>>, Bound<'py, pyo3::types::PyDict>, f64)> {
    dispatch_undirected!(graph, |g, lab| {
        let solution = match initial_centers {
            Some(cs) => {
                let ids: std::collections::HashSet<usize> = cs
                    .iter()
                    .map(|v| lab.vertex_id(py, v))
                    .collect::<PyResult<_>>()?;
                GonHeuristic::with_initial_centers(ids).centers(g, k)
            }
            None => {
                use rand::SeedableRng;
                let rng = match seed {
                    Some(s) => rand::rngs::StdRng::seed_from_u64(s),
                    None => rand::rngs::StdRng::from_os_rng(),
                };
                GonHeuristic::with_rng(rng).centers(g, k)
            }
        }
        .map_err(graph_error)?;
        let assignment = lab.vertex_dict(
            py,
            solution
                .assignment()
                .iter()
                .map(|(v, c)| (*v, lab.vertex_obj(py, *c))),
        )?;
        Ok((
            lab.vertices(py, solution.centers().iter().copied()),
            assignment,
            solution.covering_radius(),
        ))
    })
}

/// Whether the graph is perfect (neither it nor its complement has an odd hole).
#[pyfunction]
fn is_perfect(graph: &Bound<'_, PyAny>) -> PyResult<bool> {
    dispatch!(graph, |g, _lab| Ok(holes::is_perfect(g)))
}

/// Whether the graph is weakly chordal (no hole or antihole of length > 4).
#[pyfunction]
fn is_weakly_chordal(graph: &Bound<'_, PyAny>) -> PyResult<bool> {
    dispatch!(graph, |g, _lab| Ok(holes::is_weakly_chordal(g)))
}

/// The vertices of a hole or antihole of length > 4 if the graph is not weakly chordal, else
/// ``None``.
#[pyfunction]
fn weak_chordality_certificate(
    py: Python<'_>,
    graph: &Bound<'_, PyAny>,
) -> PyResult<Option<Vec<Py<PyAny>>>> {
    dispatch!(graph, |g, lab| {
        Ok(holes::find_weak_chordality_certificate(g).map(|vs| lab.vertices(py, vs)))
    })
}

/// The vertices of an odd hole or odd antihole if there is one (so the graph is not perfect),
/// else ``None``.
#[pyfunction]
fn odd_hole_or_antihole(
    py: Python<'_>,
    graph: &Bound<'_, PyAny>,
) -> PyResult<Option<Vec<Py<PyAny>>>> {
    dispatch!(graph, |g, lab| {
        Ok(holes::find_odd_hole_or_antihole(g).map(|vs| lab.vertices(py, vs)))
    })
}

pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<CliqueSeparatorDecomposition>()?;
    for f in [
        wrap_pyfunction!(is_clique, m)?,
        wrap_pyfunction!(is_independent_set, m)?,
        wrap_pyfunction!(chordal_maximum_clique, m)?,
        wrap_pyfunction!(chordal_maximum_independent_set, m)?,
        wrap_pyfunction!(chordal_minimal_separators, m)?,
        wrap_pyfunction!(clique_minimal_separator_decomposition, m)?,
        wrap_pyfunction!(berge_certificate, m)?,
        wrap_pyfunction!(number_of_triangles, m)?,
        wrap_pyfunction!(count_triangles_among, m)?,
        wrap_pyfunction!(is_vertex_cover, m)?,
    ] {
        m.add_function(f)?;
    }
    m.add_function(wrap_pyfunction!(k_center, m)?)?;
    m.add_function(wrap_pyfunction!(densest_subgraph, m)?)?;
    m.add_function(wrap_pyfunction!(gon_k_center, m)?)?;
    m.add_function(wrap_pyfunction!(is_perfect, m)?)?;
    m.add_function(wrap_pyfunction!(is_weakly_chordal, m)?)?;
    m.add_function(wrap_pyfunction!(weak_chordality_certificate, m)?)?;
    m.add_function(wrap_pyfunction!(odd_hole_or_antihole, m)?)?;
    m.add_function(wrap_pyfunction!(maximal_cliques, m)?)?;
    m.add_function(wrap_pyfunction!(maximum_clique, m)?)?;
    m.add_function(wrap_pyfunction!(greedy_independent_set, m)?)?;
    m.add_function(wrap_pyfunction!(maximum_independent_set, m)?)?;
    m.add_function(wrap_pyfunction!(vertex_cover, m)?)?;
    Ok(())
}
