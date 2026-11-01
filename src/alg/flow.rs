//! Maximum flow, minimum cost flow and flow-based algorithms. Edge weights are the capacities.

use jgrapht::GraphExt as _;
use jgrapht::alg::flow::{
    BoykovKolmogorov, CapacityScalingMinimumCostFlow, Dinic, EdmondsKarp, MaximumFlowAlgorithm,
    MinimumCostFlowNetwork, PushRelabel,
};
use pyo3::prelude::*;
use pyo3::types::PyDict;
use std::collections::HashMap;

use crate::error::{GraphError, graph_error};
use crate::labels::{EdgeId, as_i32, dispatch, dispatch_directed, spec_value};

/// A maximum flow together with a minimum cut.
#[pyclass(module = "jgrapht", frozen)]
pub struct MaximumFlow {
    value: f64,
    flow: Py<PyDict>,
    source_partition: Vec<Py<PyAny>>,
}

#[pymethods]
impl MaximumFlow {
    /// The value of the flow, which equals the capacity of the minimum cut.
    #[getter]
    fn value(&self) -> f64 {
        self.value
    }

    /// ``{edge: flow}`` for every edge of the network.
    #[getter]
    fn flow(&self, py: Python<'_>) -> Py<PyDict> {
        self.flow.clone_ref(py)
    }

    /// The vertices on the source side of the minimum cut.
    #[getter]
    fn source_partition(&self, py: Python<'_>) -> Vec<Py<PyAny>> {
        self.source_partition
            .iter()
            .map(|v| v.clone_ref(py))
            .collect()
    }

    fn __repr__(&self) -> String {
        format!("MaximumFlow(value={:?})", self.value)
    }
}

/// Maximum flow from ``source`` to ``sink``, using edge weights as capacities.
/// ``algorithm`` is ``"dinic"`` (default), ``"edmonds_karp"``, ``"push_relabel"`` or
/// ``"boykov_kolmogorov"``.
#[pyfunction]
#[pyo3(signature = (graph, source, sink, algorithm="dinic"))]
fn maximum_flow(
    py: Python<'_>,
    graph: &Bound<'_, PyAny>,
    source: Bound<'_, PyAny>,
    sink: Bound<'_, PyAny>,
    algorithm: &str,
) -> PyResult<MaximumFlow> {
    dispatch!(graph, |g, lab| {
        let (s, t) = (lab.vertex_id(py, &source)?, lab.vertex_id(py, &sink)?);
        let result = match algorithm {
            "dinic" => Dinic::new(g).and_then(|mut a| a.maximum_flow(&s, &t)),
            "edmonds_karp" => EdmondsKarp::new(g).and_then(|mut a| a.maximum_flow(&s, &t)),
            "push_relabel" => PushRelabel::new(g).and_then(|mut a| a.maximum_flow(&s, &t)),
            "boykov_kolmogorov" => {
                BoykovKolmogorov::new(g).and_then(|mut a| a.maximum_flow(&s, &t))
            }
            other => return Err(GraphError::new_err(format!("unknown algorithm {other:?}"))),
        }
        .map_err(graph_error)?;
        let flow = lab.edge_dict(py, result.flow_map().iter().map(|(e, f)| (e.eid(), *f)))?;
        Ok(MaximumFlow {
            value: result.value(),
            flow: flow.unbind(),
            source_partition: lab.vertices(py, result.source_partition().iter().copied()),
        })
    })
}

/// A minimum cost flow: its total cost, the flow on every edge and the dual (potential) of every
/// vertex.
#[pyclass(module = "jgrapht", frozen)]
pub struct MinimumCostFlow {
    cost: f64,
    flow: Py<PyDict>,
    dual: Py<PyDict>,
}

#[pymethods]
impl MinimumCostFlow {
    /// The total cost of the flow.
    #[getter]
    fn cost(&self) -> f64 {
        self.cost
    }

    /// ``{edge: flow}`` for every edge.
    #[getter]
    fn flow(&self, py: Python<'_>) -> Py<PyDict> {
        self.flow.clone_ref(py)
    }

    /// ``{vertex: dual value}``.
    #[getter]
    fn dual(&self, py: Python<'_>) -> Py<PyDict> {
        self.dual.clone_ref(py)
    }

    fn __repr__(&self) -> String {
        format!("MinimumCostFlow(cost={:?})", self.cost)
    }
}

/// A minimum cost flow in a directed graph (capacity scaling).
///
/// ``supply`` gives each vertex's supply (positive) or demand (negative) as a dict (missing
/// vertices have 0), a callable or a constant; supplies must sum to zero. ``capacity`` is the
/// upper bound on each edge's flow (a dict, a callable or a constant) and ``lower_bound`` the
/// lower bound (default 0). ``cost`` is the cost per unit of flow on each edge; if omitted the
/// edge weights are used. Capacities, supplies and bounds must be integers.
#[pyfunction]
#[pyo3(signature = (graph, supply, capacity, cost=None, lower_bound=None))]
fn minimum_cost_flow(
    py: Python<'_>,
    graph: &Bound<'_, PyAny>,
    supply: Bound<'_, PyAny>,
    capacity: Bound<'_, PyAny>,
    cost: Option<Bound<'_, PyAny>>,
    lower_bound: Option<Bound<'_, PyAny>>,
) -> PyResult<MinimumCostFlow> {
    dispatch_directed!(graph, |g, lab| {
        let mut supplies: HashMap<usize, i32> = HashMap::new();
        for v in g.vertices_cloned() {
            let x = spec_value(&supply, lab.vertex_obj(py, v), 0.0)?;
            supplies.insert(v, as_i32(x, "supply")?);
        }
        let mut upper = HashMap::new();
        let mut lower = HashMap::new();
        let mut costs = HashMap::new();
        for e in g.edges_cloned() {
            let obj = || lab.edge_obj(py, e.eid());
            upper.insert(
                e.clone(),
                as_i32(spec_value(&capacity, obj(), f64::NAN)?, "capacity")?,
            );
            let lo = match &lower_bound {
                Some(spec) => spec_value(spec, obj(), 0.0)?,
                None => 0.0,
            };
            lower.insert(e.clone(), as_i32(lo, "lower bound")?);
            let c = match &cost {
                Some(spec) => spec_value(spec, obj(), 0.0)?,
                None => g.weight_of(&e),
            };
            costs.insert(e, c);
        }
        let problem = MinimumCostFlowNetwork::with_costs(
            g,
            |v| supplies[v],
            |e| upper[e],
            |e| lower[e],
            |e| costs[e],
        );
        let solution = CapacityScalingMinimumCostFlow::new()
            .solve(&problem)
            .map_err(graph_error)?;
        let flow = lab.edge_dict(
            py,
            solution.flow().flow_map.iter().map(|(e, f)| (e.eid(), *f)),
        )?;
        let dual = lab.vertex_dict(py, solution.dual_solution().iter().map(|(v, d)| (*v, *d)))?;
        Ok(MinimumCostFlow {
            cost: solution.flow().cost,
            flow: flow.unbind(),
            dual: dual.unbind(),
        })
    })
}

pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<MinimumCostFlow>()?;
    m.add_function(wrap_pyfunction!(minimum_cost_flow, m)?)?;
    m.add_class::<MaximumFlow>()?;
    m.add_function(wrap_pyfunction!(maximum_flow, m)?)?;
    Ok(())
}
