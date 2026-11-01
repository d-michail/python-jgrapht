//! Graph generators.
//!
//! Every generator returns a new graph with the integer vertices ``0..n``: a :class:`Graph` by
//! default, or an immutable :class:`SparseGraph` with ``sparse=True``.

use jgrapht::alg::flow::MinimumCostFlowProblem;
use jgrapht::generate::named;
use jgrapht::generate::netgen::{NetworkGenerator, NetworkGeneratorConfigBuilder};
use jgrapht::generate::{
    BarabasiAlbertForestGenerator, BarabasiAlbertGraphGenerator, Complete, CompleteBipartite,
    DirectedScaleFreeGraphGenerator, Empty, GeneralizedPetersen, GnmRandomBipartiteGraphGenerator,
    GnmRandomGraphGenerator, GnpRandomBipartiteGraphGenerator, GnpRandomGraphGenerator,
    GraphGenerator, Grid, Hypercube, KleinbergSmallWorldGraphGenerator, Linear,
    LinearizedChordDiagramGenerator, PlantedPartitionGraphGenerator, PruferTreeGenerator,
    RandomRegularGraphGenerator, Ring, ScaleFreeGraphGenerator, Star, WattsStrogatzGraphGenerator,
    WeightedBipartiteMatrixGenerator, WeightedMatrixGenerator, Wheel, Windmill, WindmillMode,
};
use jgrapht::{DefaultEdge, DiGraph, Graph as _, GraphExt as _, GraphType, UGraph};
use pyo3::IntoPyObjectExt;
use pyo3::prelude::*;
use pyo3::types::PyDict;
use rand::SeedableRng;
use rand::rngs::StdRng;
use std::borrow::Borrow;

use crate::error::{GraphError, graph_error};
use crate::graph::Graph;
use crate::sparse::SparseGraph;

pub(crate) type Edges = Vec<(usize, usize, Option<f64>)>;

/// Rust graphs the generators fill. Vertices are the integers handed out by the generator.
pub(crate) trait Target:
    jgrapht::GraphMut<Vertex = usize, Edge = DefaultEdge> + jgrapht::IncidenceGraph
{
}
impl<T> Target for T where
    T: jgrapht::GraphMut<Vertex = usize, Edge = DefaultEdge> + jgrapht::IncidenceGraph
{
}

fn rng(seed: Option<u64>) -> StdRng {
    match seed {
        Some(s) => StdRng::seed_from_u64(s),
        None => StdRng::from_os_rng(),
    }
}

/// The vertex count and edges (with weights when `weighted`) of a generated graph.
pub(crate) fn collect<G: Target>(g: &G, weighted: bool) -> PyResult<(usize, Edges)> {
    let mut vertices: Vec<usize> = g.vertices().map(|v| *v.borrow()).collect();
    vertices.sort_unstable();
    if vertices.iter().enumerate().any(|(i, v)| i != *v) {
        return Err(GraphError::new_err(
            "generator produced non-contiguous vertex ids",
        ));
    }
    let edges = g
        .edges()
        .map(|e| {
            let e = e.borrow();
            let (s, t) = g.edge_endpoints(e).expect("edge of the graph");
            (*s, *t, weighted.then(|| g.weight_of(e)))
        })
        .collect();
    Ok((vertices.len(), edges))
}

/// Turns a vertex count and edge list into a `Graph` or `SparseGraph` of the requested kind.
fn output(
    py: Python<'_>,
    directed: bool,
    n: usize,
    edges: Edges,
    sparse: bool,
) -> PyResult<Py<PyAny>> {
    if sparse {
        let weights: Option<Vec<f64>> = edges.iter().map(|(_, _, w)| *w).collect();
        let pairs = edges.iter().map(|(s, t, _)| (*s, *t)).collect();
        return Ok(Py::new(py, SparseGraph::create(n, pairs, directed, weights)?)?.into_any());
    }
    let vertices = (0..n)
        .map(|v| v.into_py_any(py))
        .collect::<PyResult<Vec<_>>>()?;
    Ok(Graph::from_parts(py, directed, vertices, edges)?.into_any())
}

/// Runs `gen` into a fresh graph of the requested type.
fn generate(
    py: Python<'_>,
    mut generator: impl GraphGenerator,
    directed: bool,
    ty: GraphType,
    sparse: bool,
) -> PyResult<Py<PyAny>> {
    let weighted = ty.weighted;
    let (n, edges) = if directed {
        let mut t = DiGraph::<usize>::with_graph_type(ty);
        generator.generate_indexed(&mut t).map_err(graph_error)?;
        collect(&t, weighted)?
    } else {
        let mut t = UGraph::<usize>::with_graph_type(ty);
        generator.generate_indexed(&mut t).map_err(graph_error)?;
        collect(&t, weighted)?
    };
    output(py, directed, n, edges, sparse)
}

fn simple() -> GraphType {
    GraphType::simple()
}

fn pseudo() -> GraphType {
    GraphType::pseudograph()
}

// ---------------------------------------------------------------- structured

/// The graph with ``n`` vertices and no edges.
#[pyfunction]
#[pyo3(signature = (n, directed=false, sparse=false))]
fn empty_graph(py: Python<'_>, n: usize, directed: bool, sparse: bool) -> PyResult<Py<PyAny>> {
    generate(py, Empty(n), directed, simple(), sparse)
}

/// The path on ``n`` vertices ``0 - 1 - ... - n-1`` (edges ``i -> i+1`` if directed).
#[pyfunction]
#[pyo3(signature = (n, directed=false, sparse=false))]
fn path_graph(py: Python<'_>, n: usize, directed: bool, sparse: bool) -> PyResult<Py<PyAny>> {
    generate(py, Linear(n), directed, simple(), sparse)
}

/// The cycle on ``n`` vertices.
#[pyfunction]
#[pyo3(signature = (n, directed=false, sparse=false))]
fn ring_graph(py: Python<'_>, n: usize, directed: bool, sparse: bool) -> PyResult<Py<PyAny>> {
    generate(py, Ring(n), directed, simple(), sparse)
}

/// The star on ``n`` vertices: vertex 0 is the centre. In a directed star the edges point from the
/// leaves to the centre.
#[pyfunction]
#[pyo3(signature = (n, directed=false, sparse=false))]
fn star_graph(py: Python<'_>, n: usize, directed: bool, sparse: bool) -> PyResult<Py<PyAny>> {
    generate(py, Star(n), directed, simple(), sparse)
}

/// The wheel on ``n`` vertices: a ring of ``n - 1`` rim vertices plus the hub, vertex ``n - 1``.
/// In a directed wheel the spokes point towards the hub if ``inward_spokes``.
#[pyfunction]
#[pyo3(signature = (n, directed=false, inward_spokes=false, sparse=false))]
fn wheel_graph(
    py: Python<'_>,
    n: usize,
    directed: bool,
    inward_spokes: bool,
    sparse: bool,
) -> PyResult<Py<PyAny>> {
    generate(py, Wheel { n, inward_spokes }, directed, simple(), sparse)
}

/// The complete graph on ``n`` vertices (every ordered pair if directed).
#[pyfunction]
#[pyo3(signature = (n, directed=false, sparse=false))]
fn complete_graph(py: Python<'_>, n: usize, directed: bool, sparse: bool) -> PyResult<Py<PyAny>> {
    generate(py, Complete(n), directed, simple(), sparse)
}

/// The complete bipartite graph ``K(n1, n2)``: vertices ``0..n1`` against ``n1..n1+n2``.
#[pyfunction]
#[pyo3(signature = (n1, n2, directed=false, sparse=false))]
fn complete_bipartite_graph(
    py: Python<'_>,
    n1: usize,
    n2: usize,
    directed: bool,
    sparse: bool,
) -> PyResult<Py<PyAny>> {
    generate(py, CompleteBipartite(n1, n2), directed, simple(), sparse)
}

/// The ``rows`` by ``cols`` grid (both at least 2).
#[pyfunction]
#[pyo3(signature = (rows, cols, directed=false, sparse=false))]
fn grid_graph(
    py: Python<'_>,
    rows: usize,
    cols: usize,
    directed: bool,
    sparse: bool,
) -> PyResult<Py<PyAny>> {
    generate(py, Grid { rows, cols }, directed, simple(), sparse)
}

/// The ``dimension``-dimensional hypercube on ``2 ** dimension`` vertices.
#[pyfunction]
#[pyo3(signature = (dimension, directed=false, sparse=false))]
fn hypercube_graph(
    py: Python<'_>,
    dimension: u32,
    directed: bool,
    sparse: bool,
) -> PyResult<Py<PyAny>> {
    generate(py, Hypercube(dimension), directed, simple(), sparse)
}

/// The generalized Petersen graph ``GP(n, k)`` on ``2n`` vertices (``GP(5, 2)`` is Petersen's).
#[pyfunction]
#[pyo3(signature = (n, k, sparse=false))]
fn generalized_petersen_graph(
    py: Python<'_>,
    n: usize,
    k: usize,
    sparse: bool,
) -> PyResult<Py<PyAny>> {
    generate(py, GeneralizedPetersen { n, k }, false, simple(), sparse)
}

/// ``m`` blades sharing vertex 0, each a complete graph on ``n`` vertices (a windmill) or, with
/// ``dutch``, a cycle on ``n`` vertices (a Dutch windmill).
#[pyfunction]
#[pyo3(signature = (m, n, dutch=false, sparse=false))]
fn windmill_graph(
    py: Python<'_>,
    m: usize,
    n: usize,
    dutch: bool,
    sparse: bool,
) -> PyResult<Py<PyAny>> {
    let mode = if dutch {
        WindmillMode::DutchWindmill
    } else {
        WindmillMode::Windmill
    };
    generate(py, Windmill { mode, m, n }, false, simple(), sparse)
}

fn square(weights: &[Vec<f64>]) -> PyResult<()> {
    if weights.iter().any(|row| row.len() != weights.len()) {
        return Err(GraphError::new_err("the weight matrix must be square"));
    }
    Ok(())
}

/// A complete weighted graph on ``0..n`` from an ``n x n`` weight matrix: the edge ``i -> j``
/// (``i < j`` for an undirected graph) gets weight ``weights[i][j]``.
#[pyfunction]
#[pyo3(signature = (weights, directed=false, sparse=false))]
fn graph_from_weight_matrix(
    py: Python<'_>,
    weights: Vec<Vec<f64>>,
    directed: bool,
    sparse: bool,
) -> PyResult<Py<PyAny>> {
    square(&weights)?;
    let n = weights.len();
    let ty = simple().weighted(true);
    let make = || {
        WeightedMatrixGenerator::<usize>::new()
            .vertices((0..n).collect())
            .weights(weights.clone())
    };
    let (count, edges) = if directed {
        let mut t = DiGraph::<usize>::with_graph_type(ty);
        make().generate_into(&mut t).map_err(graph_error)?;
        collect(&t, true)?
    } else {
        let mut t = UGraph::<usize>::with_graph_type(ty);
        make().generate_into(&mut t).map_err(graph_error)?;
        collect(&t, true)?
    };
    output(py, directed, count, edges, sparse)
}

/// A complete weighted bipartite graph from a ``n1 x n2`` weight matrix: vertices ``0..n1`` against
/// ``n1..n1+n2``, with edge ``(i, n1 + j)`` of weight ``weights[i][j]``.
#[pyfunction]
#[pyo3(signature = (weights, sparse=false))]
fn bipartite_graph_from_weight_matrix(
    py: Python<'_>,
    weights: Vec<Vec<f64>>,
    sparse: bool,
) -> PyResult<Py<PyAny>> {
    let n1 = weights.len();
    let n2 = weights.first().map_or(0, Vec::len);
    if weights.iter().any(|row| row.len() != n2) {
        return Err(GraphError::new_err("the weight matrix must be rectangular"));
    }
    let mut t = UGraph::<usize>::with_graph_type(simple().weighted(true));
    WeightedBipartiteMatrixGenerator::<usize>::new()
        .first((0..n1).collect())
        .second((n1..n1 + n2).collect())
        .weights(weights)
        .generate_into(&mut t)
        .map_err(graph_error)?;
    let (n, edges) = collect(&t, true)?;
    output(py, false, n, edges, sparse)
}

// ---------------------------------------------------------------- random

/// An Erdős-Rényi ``G(n, p)`` random graph: each possible edge is present with probability ``p``.
/// ``loops`` also considers self-loops.
#[pyfunction]
#[pyo3(signature = (n, p, directed=false, loops=false, seed=None, sparse=false))]
fn gnp_random_graph(
    py: Python<'_>,
    n: usize,
    p: f64,
    directed: bool,
    loops: bool,
    seed: Option<u64>,
    sparse: bool,
) -> PyResult<Py<PyAny>> {
    let g = GnpRandomGraphGenerator::new(n, p, rng(seed), loops).map_err(graph_error)?;
    generate(
        py,
        g,
        directed,
        if loops { pseudo() } else { simple() },
        sparse,
    )
}

/// An Erdős-Rényi ``G(n, m)`` random graph with exactly ``m`` edges, optionally with self-loops
/// and parallel edges.
#[pyfunction]
#[pyo3(signature = (n, m, directed=false, loops=false, multiple_edges=false, seed=None, sparse=false))]
#[allow(clippy::too_many_arguments)]
fn gnm_random_graph(
    py: Python<'_>,
    n: usize,
    m: usize,
    directed: bool,
    loops: bool,
    multiple_edges: bool,
    seed: Option<u64>,
    sparse: bool,
) -> PyResult<Py<PyAny>> {
    let g = GnmRandomGraphGenerator::new(n, m, rng(seed), loops, multiple_edges)
        .map_err(graph_error)?;
    let mut ty = simple();
    ty.self_loops = loops;
    ty.multiple_edges = multiple_edges;
    generate(py, g, directed, ty, sparse)
}

/// A Barabási-Albert preferential-attachment graph: start from ``m0`` vertices and add vertices up
/// to ``n``, each joined to ``m`` existing ones with probability proportional to their degree.
#[pyfunction]
#[pyo3(signature = (m0, m, n, seed=None, sparse=false))]
fn barabasi_albert_graph(
    py: Python<'_>,
    m0: usize,
    m: usize,
    n: usize,
    seed: Option<u64>,
    sparse: bool,
) -> PyResult<Py<PyAny>> {
    let g = BarabasiAlbertGraphGenerator::new(m0, m, n, rng(seed)).map_err(graph_error)?;
    generate(py, g, false, simple(), sparse)
}

/// A Barabási-Albert forest: ``t`` initial trees grown to ``n`` vertices by preferential attachment.
#[pyfunction]
#[pyo3(signature = (t, n, seed=None, sparse=false))]
fn barabasi_albert_forest(
    py: Python<'_>,
    t: usize,
    n: usize,
    seed: Option<u64>,
    sparse: bool,
) -> PyResult<Py<PyAny>> {
    let g = BarabasiAlbertForestGenerator::new(t, n, rng(seed)).map_err(graph_error)?;
    generate(py, g, false, simple(), sparse)
}

/// A scale-free random graph on ``n`` vertices.
#[pyfunction]
#[pyo3(signature = (n, seed=None, sparse=false))]
fn scale_free_graph(
    py: Python<'_>,
    n: i64,
    seed: Option<u64>,
    sparse: bool,
) -> PyResult<Py<PyAny>> {
    let g = ScaleFreeGraphGenerator::new(n, rng(seed)).map_err(graph_error)?;
    generate(py, g, false, simple(), sparse)
}

/// A directed scale-free graph (Bollobás, Borgs, Chayes, Riordan) grown until it has
/// ``target_edges`` edges or ``target_nodes`` vertices (give at least one; the other is ``-1``).
#[pyfunction]
#[pyo3(signature = (alpha, gamma, delta_in, delta_out, target_edges=-1, target_nodes=-1, multiple_edges=true, self_loops=true, seed=None, sparse=false))]
#[allow(clippy::too_many_arguments)]
fn directed_scale_free_graph(
    py: Python<'_>,
    alpha: f32,
    gamma: f32,
    delta_in: f32,
    delta_out: f32,
    target_edges: i64,
    target_nodes: i64,
    multiple_edges: bool,
    self_loops: bool,
    seed: Option<u64>,
    sparse: bool,
) -> PyResult<Py<PyAny>> {
    let mut g = DirectedScaleFreeGraphGenerator::new(
        alpha,
        gamma,
        delta_in,
        delta_out,
        target_edges,
        target_nodes,
        rng(seed),
    )
    .map_err(graph_error)?;
    g.set_allowing_multiple_edges(multiple_edges);
    g.set_allowing_self_loops(self_loops);
    generate(py, g, true, pseudo(), sparse)
}

/// A Watts-Strogatz small-world graph: a ring lattice of ``n`` vertices each joined to its ``k``
/// nearest neighbours, every edge rewired with probability ``p`` (or, with ``add_instead_of_rewire``,
/// a new edge added).
#[pyfunction]
#[pyo3(signature = (n, k, p, add_instead_of_rewire=false, seed=None, sparse=false))]
fn watts_strogatz_graph(
    py: Python<'_>,
    n: usize,
    k: usize,
    p: f64,
    add_instead_of_rewire: bool,
    seed: Option<u64>,
    sparse: bool,
) -> PyResult<Py<PyAny>> {
    let g = WattsStrogatzGraphGenerator::new(n, k, p, add_instead_of_rewire, rng(seed))
        .map_err(graph_error)?;
    generate(py, g, false, simple(), sparse)
}

/// A uniformly random labelled tree on ``n`` vertices (via a random Prüfer sequence), or the tree
/// of a given Prüfer ``sequence`` (``n`` is then ignored).
#[pyfunction]
#[pyo3(signature = (n, sequence=None, seed=None, sparse=false))]
fn prufer_tree(
    py: Python<'_>,
    n: usize,
    sequence: Option<Vec<usize>>,
    seed: Option<u64>,
    sparse: bool,
) -> PyResult<Py<PyAny>> {
    match sequence {
        Some(s) => generate(
            py,
            PruferTreeGenerator::<StdRng>::from_sequence(&s).map_err(graph_error)?,
            false,
            simple(),
            sparse,
        ),
        None => generate(
            py,
            PruferTreeGenerator::new(n, rng(seed)).map_err(graph_error)?,
            false,
            simple(),
            sparse,
        ),
    }
}

/// A random ``d``-regular graph on ``n`` vertices (``n * d`` must be even).
#[pyfunction]
#[pyo3(signature = (n, d, seed=None, sparse=false))]
fn random_regular_graph(
    py: Python<'_>,
    n: usize,
    d: usize,
    seed: Option<u64>,
    sparse: bool,
) -> PyResult<Py<PyAny>> {
    let g = RandomRegularGraphGenerator::new(n, d, rng(seed)).map_err(graph_error)?;
    generate(py, g, false, simple(), sparse)
}

/// A planted-partition graph: ``l`` groups of ``k`` vertices, edges inside a group with
/// probability ``p`` and between groups with probability ``q``.
#[pyfunction]
#[pyo3(signature = (l, k, p, q, self_loops=false, seed=None, sparse=false))]
#[allow(clippy::too_many_arguments)]
fn planted_partition_graph(
    py: Python<'_>,
    l: usize,
    k: usize,
    p: f64,
    q: f64,
    self_loops: bool,
    seed: Option<u64>,
    sparse: bool,
) -> PyResult<Py<PyAny>> {
    let g = PlantedPartitionGraphGenerator::new(l, k, p, q, rng(seed), self_loops)
        .map_err(graph_error)?;
    generate(
        py,
        g,
        false,
        if self_loops { pseudo() } else { simple() },
        sparse,
    )
}

/// A Kleinberg small-world graph on an ``n x n`` lattice with local range ``p``, ``q`` long-range
/// contacts per vertex and clustering exponent ``r``.
#[pyfunction]
#[pyo3(signature = (n, p, q, r, seed=None, sparse=false))]
fn kleinberg_small_world_graph(
    py: Python<'_>,
    n: i64,
    p: i64,
    q: i64,
    r: i64,
    seed: Option<u64>,
    sparse: bool,
) -> PyResult<Py<PyAny>> {
    let g = KleinbergSmallWorldGraphGenerator::new(n, p, q, r, rng(seed)).map_err(graph_error)?;
    generate(py, g, true, pseudo(), sparse)
}

/// A random graph from the linearized chord diagram model with ``n`` vertices and ``m`` edges per
/// vertex (a multigraph with loops).
#[pyfunction]
#[pyo3(signature = (n, m, seed=None, sparse=false))]
fn linearized_chord_diagram_graph(
    py: Python<'_>,
    n: usize,
    m: usize,
    seed: Option<u64>,
    sparse: bool,
) -> PyResult<Py<PyAny>> {
    let g = LinearizedChordDiagramGenerator::new(n, m, rng(seed)).map_err(graph_error)?;
    generate(py, g, false, pseudo(), sparse)
}

/// A random bipartite graph with ``n1 + n2`` vertices and exactly ``m`` edges.
#[pyfunction]
#[pyo3(signature = (n1, n2, m, seed=None, sparse=false))]
fn gnm_random_bipartite_graph(
    py: Python<'_>,
    n1: usize,
    n2: usize,
    m: usize,
    seed: Option<u64>,
    sparse: bool,
) -> PyResult<Py<PyAny>> {
    generate(
        py,
        GnmRandomBipartiteGraphGenerator::new(n1, n2, m, rng(seed)),
        false,
        simple(),
        sparse,
    )
}

/// A random bipartite graph with ``n1 + n2`` vertices, each possible edge present with
/// probability ``p``.
#[pyfunction]
#[pyo3(signature = (n1, n2, p, seed=None, sparse=false))]
fn gnp_random_bipartite_graph(
    py: Python<'_>,
    n1: usize,
    n2: usize,
    p: f64,
    seed: Option<u64>,
    sparse: bool,
) -> PyResult<Py<PyAny>> {
    let g = GnpRandomBipartiteGraphGenerator::new(n1, n2, p, rng(seed)).map_err(graph_error)?;
    generate(py, g, false, simple(), sparse)
}

// ---------------------------------------------------------------- named graphs

macro_rules! named_table {
    ($($name:ident),+ $(,)?) => {
        const NAMES: &[&str] = &[$(stringify!($name)),+];

        fn named_structure(name: &str) -> Option<UGraph<usize>> {
            match name {
                $(stringify!($name) => Some(named::build(named::$name())),)+
                _ => None,
            }
        }
    };
}

named_table!(
    bidiakis_cube,
    blanusa_first_snark,
    blanusa_second_snark,
    brinkmann,
    bucky_ball,
    bull,
    butterfly,
    chvatal,
    claw,
    clebsch,
    coxeter,
    desargues,
    diamond,
    dodecahedron,
    double_star_snark,
    doyle,
    durer,
    ellingham_horton54,
    ellingham_horton78,
    errera,
    folkman,
    franklin,
    frucht,
    goldner_harary,
    gosset,
    grotzsch,
    heawood,
    herschel,
    hoffman,
    kittell,
    klein3_regular,
    klein7_regular,
    krackhardt_kite,
    mobius_kantor,
    moser_spindle,
    nauru,
    pappus,
    petersen,
    poussin,
    schlafli,
    thomsen,
    tietze,
    tutte,
    zachary_karate_club,
);

/// The names accepted by :func:`named_graph`.
#[pyfunction]
fn named_graph_names() -> Vec<&'static str> {
    NAMES.to_vec()
}

/// A famous small graph by name, for example ``"petersen"``, ``"heawood"``, ``"frucht"`` or
/// ``"zachary_karate_club"``; see :func:`named_graph_names` for all of them.
#[pyfunction]
#[pyo3(signature = (name, sparse=false))]
fn named_graph(py: Python<'_>, name: &str, sparse: bool) -> PyResult<Py<PyAny>> {
    let g = named_structure(name)
        .ok_or_else(|| GraphError::new_err(format!("unknown named graph {name:?}")))?;
    let (n, edges) = collect(&g, false)?;
    output(py, false, n, edges, sparse)
}

// ---------------------------------------------------------------- network problems

fn seeded(seed: u64) -> u64 {
    seed
}

/// A random maximum flow instance (the NETGEN generator): returns ``(graph, sources, sinks)``
/// where ``graph`` is a directed weighted graph whose edge weights are the capacities.
#[pyfunction]
#[pyo3(signature = (nodes, arcs, supply, min_capacity=1, max_capacity=1, sources=1, sinks=1, percent_capacitated=100, seed=0, sparse=false))]
#[allow(clippy::too_many_arguments)]
fn maximum_flow_network(
    py: Python<'_>,
    nodes: i32,
    arcs: i32,
    supply: i32,
    min_capacity: i32,
    max_capacity: i32,
    sources: i32,
    sinks: i32,
    percent_capacitated: i32,
    seed: u64,
    sparse: bool,
) -> PyResult<(Py<PyAny>, Vec<usize>, Vec<usize>)> {
    let config = NetworkGeneratorConfigBuilder::new()
        .with_maximum_flow_problem_params_full(
            nodes,
            arcs,
            supply,
            min_capacity,
            max_capacity,
            sources,
            sinks,
            percent_capacitated,
        )
        .build()
        .map_err(graph_error)?;
    let mut g = DiGraph::<usize>::simple()
        .weighted()
        .with_vertex_factory(|i| i as usize);
    let problem = NetworkGenerator::<usize, DefaultEdge>::new(config, seeded(seed))
        .generate_max_flow_problem(&mut g)
        .map_err(graph_error)?;
    let (n, mut edges) = collect(&g, true)?;
    for (slot, e) in edges.iter_mut().zip(g.edges()) {
        slot.2 = Some(problem.capacities[e]);
    }
    let (mut s, mut t): (Vec<usize>, Vec<usize>) = (
        problem.sources.iter().copied().collect(),
        problem.sinks.iter().copied().collect(),
    );
    s.sort_unstable();
    t.sort_unstable();
    Ok((output(py, true, n, edges, sparse)?, s, t))
}

/// A random bipartite matching (assignment) instance: returns ``(graph, left, right)`` where
/// ``graph`` is a directed weighted graph from ``left`` to ``right`` whose edge weights are the
/// costs. ``nodes`` must be even.
#[pyfunction]
#[pyo3(signature = (nodes, arcs, min_cost=1, max_cost=1, percent_with_inf_cost=0, seed=0, sparse=false))]
fn bipartite_matching_network(
    py: Python<'_>,
    nodes: i32,
    arcs: i32,
    min_cost: i32,
    max_cost: i32,
    percent_with_inf_cost: i32,
    seed: u64,
    sparse: bool,
) -> PyResult<(Py<PyAny>, Vec<usize>, Vec<usize>)> {
    let config = NetworkGeneratorConfigBuilder::new()
        .with_bipartite_matching_problem_params_full(
            nodes,
            arcs,
            min_cost,
            max_cost,
            percent_with_inf_cost,
        )
        .build()
        .map_err(graph_error)?;
    let mut g = DiGraph::<usize>::simple()
        .weighted()
        .with_vertex_factory(|i| i as usize);
    let problem = NetworkGenerator::<usize, DefaultEdge>::new(config, seeded(seed))
        .generate_bipartite_matching_problem(&mut g)
        .map_err(graph_error)?;
    let (n, mut edges) = collect(&g, true)?;
    for (slot, e) in edges.iter_mut().zip(g.edges()) {
        slot.2 = Some(problem.costs[e]);
    }
    let (mut l, mut r): (Vec<usize>, Vec<usize>) = (
        problem.partition1.iter().copied().collect(),
        problem.partition2.iter().copied().collect(),
    );
    l.sort_unstable();
    r.sort_unstable();
    Ok((output(py, true, n, edges, sparse)?, l, r))
}

/// A random minimum cost flow instance (NETGEN): returns ``(graph, supply, capacity, cost)``
/// where ``graph`` is directed and ``supply`` is ``{vertex: supply}`` (negative for sinks),
/// ``capacity`` and ``cost`` are ``{edge: value}`` dicts. Feed them to :func:`minimum_cost_flow`.
#[pyfunction]
#[pyo3(signature = (
    nodes, arcs, sources, sinks, total_supply, transship_sources=0, transship_sinks=0,
    min_capacity=1, max_capacity=1, min_cost=1, max_cost=1, percent_capacitated=100,
    percent_with_inf_cost=0, seed=0, sparse=false,
))]
#[allow(clippy::too_many_arguments, clippy::type_complexity)]
fn minimum_cost_flow_network<'py>(
    py: Python<'py>,
    nodes: i32,
    arcs: i32,
    sources: i32,
    sinks: i32,
    total_supply: i32,
    transship_sources: i32,
    transship_sinks: i32,
    min_capacity: i32,
    max_capacity: i32,
    min_cost: i32,
    max_cost: i32,
    percent_capacitated: i32,
    percent_with_inf_cost: i32,
    seed: u64,
    sparse: bool,
) -> PyResult<(
    Py<PyAny>,
    Bound<'py, PyDict>,
    Bound<'py, PyDict>,
    Bound<'py, PyDict>,
)> {
    let config = NetworkGeneratorConfigBuilder::new()
        .with_params(
            nodes,
            arcs,
            sources,
            sinks,
            transship_sources,
            transship_sinks,
            total_supply,
            min_capacity,
            max_capacity,
            min_cost,
            max_cost,
            percent_capacitated,
            percent_with_inf_cost,
        )
        .build()
        .map_err(graph_error)?;
    let mut g = DiGraph::<usize>::simple().with_vertex_factory(|i| i as usize);
    let (supply, capacity, cost) = {
        let problem = NetworkGenerator::<usize, DefaultEdge>::new(config, seeded(seed))
            .generate_minimum_cost_flow_problem(&mut g)
            .map_err(graph_error)?;
        let graph = problem.graph();
        let supply = PyDict::new(py);
        for v in graph.vertices() {
            supply.set_item(*v, problem.node_supply(v))?;
        }
        let (capacity, cost) = (PyDict::new(py), PyDict::new(py));
        for (i, e) in graph.edges().enumerate() {
            capacity.set_item(i, problem.arc_capacity_upper_bound(e))?;
            cost.set_item(i, problem.arc_cost(e))?;
        }
        (supply, capacity, cost)
    };
    let (n, edges) = collect(&g, false)?;
    Ok((output(py, true, n, edges, sparse)?, supply, capacity, cost))
}

pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    for f in [
        wrap_pyfunction!(empty_graph, m)?,
        wrap_pyfunction!(path_graph, m)?,
        wrap_pyfunction!(ring_graph, m)?,
        wrap_pyfunction!(star_graph, m)?,
        wrap_pyfunction!(wheel_graph, m)?,
        wrap_pyfunction!(complete_graph, m)?,
        wrap_pyfunction!(complete_bipartite_graph, m)?,
        wrap_pyfunction!(grid_graph, m)?,
        wrap_pyfunction!(hypercube_graph, m)?,
        wrap_pyfunction!(generalized_petersen_graph, m)?,
        wrap_pyfunction!(windmill_graph, m)?,
        wrap_pyfunction!(graph_from_weight_matrix, m)?,
        wrap_pyfunction!(bipartite_graph_from_weight_matrix, m)?,
        wrap_pyfunction!(gnp_random_graph, m)?,
        wrap_pyfunction!(gnm_random_graph, m)?,
        wrap_pyfunction!(barabasi_albert_graph, m)?,
        wrap_pyfunction!(barabasi_albert_forest, m)?,
        wrap_pyfunction!(scale_free_graph, m)?,
        wrap_pyfunction!(directed_scale_free_graph, m)?,
        wrap_pyfunction!(watts_strogatz_graph, m)?,
        wrap_pyfunction!(prufer_tree, m)?,
        wrap_pyfunction!(random_regular_graph, m)?,
        wrap_pyfunction!(planted_partition_graph, m)?,
        wrap_pyfunction!(kleinberg_small_world_graph, m)?,
        wrap_pyfunction!(linearized_chord_diagram_graph, m)?,
        wrap_pyfunction!(gnm_random_bipartite_graph, m)?,
        wrap_pyfunction!(gnp_random_bipartite_graph, m)?,
        wrap_pyfunction!(named_graph_names, m)?,
        wrap_pyfunction!(named_graph, m)?,
        wrap_pyfunction!(maximum_flow_network, m)?,
        wrap_pyfunction!(bipartite_matching_network, m)?,
        wrap_pyfunction!(minimum_cost_flow_network, m)?,
    ] {
        m.add_function(f)?;
    }
    Ok(())
}
