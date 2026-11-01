//! Reading and writing graphs in the file formats of ``jgrapht-io``.
//!
//! * [`read_graph`] / [`parse_graph`] import a graph from a file or a string,
//! * [`write_graph`] / [`graph_to_string`] export one.
//!
//! The formats are chosen by name and configured with keyword options; unknown options are
//! rejected. Imported graphs are a [`Graph`] (or a [`SparseGraph`] with ``sparse=True``).

mod sniff;

use std::cell::{Cell, RefCell};
use std::collections::{HashMap, HashSet};
use std::fmt::Display;
use std::hash::Hash;
use std::path::PathBuf;
use std::rc::Rc;

use indexmap::IndexMap;
use jgrapht::{
    DefaultEdge, DiGraph, Graph as _, GraphExt as _, GraphMut, GraphType, IncidenceGraph, UGraph,
};
use jgrapht_io::csv::{
    CsvEventDrivenImporter, CsvExporter, CsvFormat, CsvImporter, CsvParameter, VisioExporter,
};
use jgrapht_io::dimacs::{
    DimacsEventDrivenImporter, DimacsExporter, DimacsFormat, DimacsImporter, DimacsParameter,
};
use jgrapht_io::dot::{DotExporter, DotImporter, DotSubgraph};
use jgrapht_io::gexf::{
    GexfAttributeCategory, GexfAttributeType, GexfEventDrivenImporter, GexfExporter, GexfImporter,
    GexfParameter,
};
use jgrapht_io::gml::{GmlExporter, GmlImporter, GmlParameter};
use jgrapht_io::graph6::{Graph6EventDrivenImporter, Graph6Exporter, Graph6Format, Graph6Importer};
use jgrapht_io::graphml::{
    AttributeCategory, GraphMlEventDrivenImporter, GraphMlExporter, GraphMlImporter,
    SimpleGraphMlEdgeListImporter,
};
use jgrapht_io::json::{JsonEventDrivenImporter, JsonExporter, JsonImporter};
use jgrapht_io::lemon::{LemonExporter, LemonParameter};
use jgrapht_io::matrix::{MatrixExporter, MatrixFormat};
use jgrapht_io::tsplib::TsplibImporter;
use jgrapht_io::{
    Attribute, AttributeMap, AttributeType, EventDrivenImporter, GraphExporter, GraphImporter,
    ImportEvent, IoError,
};
use pyo3::IntoPyObjectExt;
use pyo3::exceptions::PyOSError;
use pyo3::prelude::*;
use pyo3::types::{PyBool, PyBytes, PyDict, PyFloat, PyInt, PyList, PyString, PyTuple};

use crate::error::GraphError;
use crate::generators::{Edges, collect};
use crate::graph::Graph;
use crate::labels::{EdgeId, Labels, dispatch};
use crate::sparse::SparseGraph;

// ---------------------------------------------------------------- formats and options

#[derive(Clone, Copy, PartialEq, Eq, Debug)]
enum Fmt {
    Csv,
    Dimacs,
    Dot,
    Gexf,
    Gml,
    Graph6,
    GraphMl,
    Json,
    Lemon,
    Matrix,
    Tsplib,
    Visio,
}

const IMPORT_FORMATS: &[&str] = &[
    "csv", "dimacs", "dot", "gexf", "gml", "graph6", "graphml", "json", "tsplib",
];
const EXPORT_FORMATS: &[&str] = &[
    "csv", "dimacs", "dot", "gexf", "gml", "graph6", "graphml", "json", "lemon", "matrix", "visio",
];

fn parse_format(name: &str, import: bool) -> PyResult<Fmt> {
    let fmt = match name.to_ascii_lowercase().as_str() {
        "csv" => Fmt::Csv,
        "dimacs" => Fmt::Dimacs,
        "dot" | "gv" => Fmt::Dot,
        "gexf" => Fmt::Gexf,
        "gml" => Fmt::Gml,
        "graph6" | "g6" | "sparse6" | "digraph6" => Fmt::Graph6,
        "graphml" => Fmt::GraphMl,
        "json" => Fmt::Json,
        "lemon" | "lgf" => Fmt::Lemon,
        "matrix" => Fmt::Matrix,
        "tsplib" | "tsp" => Fmt::Tsplib,
        "visio" => Fmt::Visio,
        _ => {
            return Err(GraphError::new_err(format!(
                "unknown graph format {name:?}"
            )));
        }
    };
    let supported = match (fmt, import) {
        (Fmt::Lemon | Fmt::Matrix | Fmt::Visio, true) => false,
        (Fmt::Tsplib, false) => false,
        _ => true,
    };
    if supported {
        Ok(fmt)
    } else {
        let direction = if import { "import" } else { "export" };
        Err(GraphError::new_err(format!(
            "format {name:?} does not support {direction}"
        )))
    }
}

/// The keyword options of a call; each option is consumed by the format that understands it and
/// whatever is left over is an error.
struct Opts<'py> {
    items: HashMap<String, Bound<'py, PyAny>>,
}

impl<'py> Opts<'py> {
    fn new(kwargs: Option<&Bound<'py, PyDict>>) -> PyResult<Self> {
        let mut items = HashMap::new();
        if let Some(kwargs) = kwargs {
            for (k, v) in kwargs.iter() {
                if !v.is_none() {
                    items.insert(k.extract::<String>()?, v);
                }
            }
        }
        Ok(Opts { items })
    }

    fn take(&mut self, name: &str) -> Option<Bound<'py, PyAny>> {
        self.items.remove(name)
    }

    /// Like `take`, but only for the names in `allowed`.
    fn take_if(&mut self, allowed: &[&str], name: &str) -> Option<Bound<'py, PyAny>> {
        if allowed.contains(&name) {
            self.take(name)
        } else {
            None
        }
    }

    fn flag(&mut self, name: &str, default: bool) -> PyResult<bool> {
        match self.take(name) {
            None => Ok(default),
            Some(v) => v.extract::<bool>(),
        }
    }

    fn string(&mut self, name: &str) -> PyResult<Option<String>> {
        self.take(name).map(|v| v.extract::<String>()).transpose()
    }

    fn float(&mut self, name: &str, default: f64) -> PyResult<f64> {
        match self.take(name) {
            None => Ok(default),
            Some(v) => v.extract::<f64>(),
        }
    }

    fn choice<'a>(
        &mut self,
        name: &str,
        allowed: &[&'a str],
        default: &'a str,
    ) -> PyResult<&'a str> {
        match self.take(name) {
            None => Ok(default),
            Some(v) => {
                let value = v.extract::<String>()?;
                allowed
                    .iter()
                    .find(|a| **a == value)
                    .copied()
                    .ok_or_else(|| {
                        GraphError::new_err(format!(
                            "invalid value {value:?} for option {name:?}, expected one of {allowed:?}"
                        ))
                    })
            }
        }
    }

    fn delimiter(&mut self) -> PyResult<Option<char>> {
        match self.string("delimiter")? {
            None => Ok(None),
            Some(s) => {
                let mut chars = s.chars();
                match (chars.next(), chars.next()) {
                    (Some(c), None) => Ok(Some(c)),
                    _ => Err(GraphError::new_err(
                        "the delimiter must be a single character",
                    )),
                }
            }
        }
    }

    fn finish(self, format: &str) -> PyResult<()> {
        if self.items.is_empty() {
            return Ok(());
        }
        let mut names: Vec<_> = self.items.keys().cloned().collect();
        names.sort();
        Err(GraphError::new_err(format!(
            "unsupported option(s) for format {format:?}: {}",
            names.join(", ")
        )))
    }
}

fn io_error(error: IoError) -> PyErr {
    match error {
        IoError::Io(e) => PyOSError::new_err(e.to_string()),
        other => GraphError::new_err(other.to_string()),
    }
}

// ---------------------------------------------------------------- attribute values

fn attribute_to_py(py: Python<'_>, a: &Attribute) -> PyResult<Py<PyAny>> {
    let text = a.value();
    match a.attribute_type() {
        AttributeType::Null => Ok(py.None()),
        AttributeType::Boolean => match text.trim().to_ascii_lowercase().as_str() {
            "true" | "1" => true.into_py_any(py),
            "false" | "0" => false.into_py_any(py),
            _ => text.into_py_any(py),
        },
        AttributeType::Int | AttributeType::Long => match text.trim().parse::<i64>() {
            Ok(i) => i.into_py_any(py),
            Err(_) => text.into_py_any(py),
        },
        AttributeType::Float | AttributeType::Double => match text.trim().parse::<f64>() {
            Ok(f) => f.into_py_any(py),
            Err(_) => text.into_py_any(py),
        },
        _ => text.into_py_any(py),
    }
}

fn attributes_to_py<'py>(
    py: Python<'py>,
    map: &IndexMap<String, Attribute>,
) -> PyResult<Bound<'py, PyDict>> {
    let d = PyDict::new(py);
    for (k, v) in map {
        d.set_item(k, attribute_to_py(py, v)?)?;
    }
    Ok(d)
}

fn py_to_attribute(value: &Bound<'_, PyAny>) -> PyResult<Attribute> {
    if value.is_none() {
        Ok(Attribute::null())
    } else if value.is_instance_of::<PyBool>() {
        Ok(Attribute::from(value.extract::<bool>()?))
    } else if value.is_instance_of::<PyInt>() {
        let i = value.extract::<i64>()?;
        Ok(match i32::try_from(i) {
            Ok(small) => Attribute::from(small),
            Err(_) => Attribute::from(i),
        })
    } else if value.is_instance_of::<PyFloat>() {
        Ok(Attribute::from(value.extract::<f64>()?))
    } else {
        Ok(Attribute::from(value.str()?.to_string()))
    }
}

fn py_to_attribute_map(value: &Bound<'_, PyAny>) -> PyResult<AttributeMap> {
    let dict = value.cast::<PyDict>().map_err(|_| {
        GraphError::new_err("attributes must be given as a dict from names to values")
    })?;
    let mut map = AttributeMap::new();
    for (k, v) in dict.iter() {
        map.insert(k.extract::<String>()?, py_to_attribute(&v)?);
    }
    Ok(map)
}

// ---------------------------------------------------------------- import

/// An identifier of a vertex as it appears in the file.
#[derive(Clone, PartialEq, Eq, Hash, Debug)]
enum Key {
    Str(String),
    Int(i64),
}

/// Numbers the vertices of a file in order of first appearance.
#[derive(Default)]
struct Names {
    index: HashMap<Key, usize>,
    keys: Vec<Key>,
}

impl Names {
    fn id(&mut self, key: Key) -> usize {
        if let Some(&i) = self.index.get(&key) {
            return i;
        }
        let i = self.keys.len();
        self.index.insert(key.clone(), i);
        self.keys.push(key);
        i
    }
}

/// Attributes met during an import.
#[derive(Default)]
struct Collected {
    graph: IndexMap<String, Attribute>,
    vertices: HashMap<usize, IndexMap<String, Attribute>>,
    edges: HashMap<u64, IndexMap<String, Attribute>>,
}

type Shared<T> = Rc<RefCell<T>>;

struct ImportOpts {
    weighted: bool,
    csv_format: CsvFormat,
    delimiter: Option<char>,
    matrix_node_id: bool,
    matrix_zero: bool,
    default_weight: f64,
    weight_attribute: Option<String>,
    schema_validation: Option<bool>,
    vertices_name: Option<String>,
    edges_name: Option<String>,
}

impl ImportOpts {
    fn parse(fmt: Fmt, weighted: bool, o: &mut Opts<'_>) -> PyResult<Self> {
        let mut opts = ImportOpts {
            weighted,
            csv_format: CsvFormat::default(),
            delimiter: None,
            matrix_node_id: false,
            matrix_zero: false,
            default_weight: 1.0,
            weight_attribute: None,
            schema_validation: None,
            vertices_name: None,
            edges_name: None,
        };
        match fmt {
            Fmt::Csv => {
                opts.csv_format = csv_format(o.choice(
                    "variant",
                    &["edge_list", "adjacency_list", "matrix"],
                    "adjacency_list",
                )?);
                opts.delimiter = o.delimiter()?;
                opts.matrix_node_id = o.flag("matrix_node_id", false)?;
                opts.matrix_zero = o.flag("matrix_zero_when_no_edge", false)?;
            }
            Fmt::Dimacs => opts.default_weight = o.float("default_weight", 1.0)?,
            Fmt::GraphMl => {
                opts.weight_attribute = o.string("edge_weight_attribute")?;
                opts.schema_validation = o
                    .take("schema_validation")
                    .map(|v| v.extract())
                    .transpose()?;
            }
            Fmt::Gexf => {
                opts.schema_validation = o
                    .take("schema_validation")
                    .map(|v| v.extract())
                    .transpose()?;
            }
            Fmt::Json => {
                opts.vertices_name = o.string("vertices_name")?;
                opts.edges_name = o.string("edges_name")?;
            }
            _ => {}
        }
        Ok(opts)
    }
}

fn csv_format(name: &str) -> CsvFormat {
    match name {
        "edge_list" => CsvFormat::EdgeList,
        "matrix" => CsvFormat::Matrix,
        _ => CsvFormat::AdjacencyList,
    }
}

/// Wires the attribute consumers of an importer to `col`.
macro_rules! collect_attributes {
    ($imp:ident, $col:expr, vertex) => {{
        let c = $col.clone();
        $imp.set_vertex_attribute_consumer(move |v, k, a| {
            c.borrow_mut()
                .vertices
                .entry(*v)
                .or_default()
                .insert(k.to_owned(), a.clone());
            Ok(())
        });
    }};
    ($imp:ident, $col:expr, edge) => {{
        let c = $col.clone();
        $imp.set_edge_attribute_consumer(move |e, k, a| {
            c.borrow_mut()
                .edges
                .entry(e.0)
                .or_default()
                .insert(k.to_owned(), a.clone());
            Ok(())
        });
    }};
    ($imp:ident, $col:expr, graph) => {{
        let c = $col.clone();
        $imp.set_graph_attribute_consumer(move |k, a| {
            c.borrow_mut().graph.insert(k.to_owned(), a.clone());
            Ok(())
        });
    }};
}

fn str_factory(names: &Shared<Names>) -> impl FnMut(&str) -> usize + 'static + use<> {
    let names = names.clone();
    move |id| names.borrow_mut().id(Key::Str(id.to_owned()))
}

fn num_factory(names: &Shared<Names>) -> impl FnMut(usize) -> usize + 'static + use<> {
    let names = names.clone();
    move |id| names.borrow_mut().id(Key::Int(id as i64))
}

/// Runs the importer of `fmt` on `input`, adding to `g`.
fn import_into<G>(
    g: &mut G,
    fmt: Fmt,
    o: &ImportOpts,
    input: &[u8],
    names: &Shared<Names>,
    col: &Shared<Collected>,
    tsplib: &mut Option<jgrapht_io::tsplib::TsplibMetadata<usize>>,
) -> Result<(), IoError>
where
    G: GraphMut<Vertex = usize, Edge = DefaultEdge> + IncidenceGraph,
{
    match fmt {
        Fmt::Csv => {
            let mut imp = CsvImporter::<usize>::new(o.csv_format);
            if let Some(d) = o.delimiter {
                imp.set_delimiter(d)?;
            }
            imp.set_parameter(CsvParameter::EdgeWeights, o.weighted);
            imp.set_parameter(CsvParameter::MatrixNodeId, o.matrix_node_id);
            imp.set_parameter(CsvParameter::MatrixZeroWhenNoEdge, o.matrix_zero);
            imp.set_vertex_factory(str_factory(names));
            imp.import_graph(g, input)
        }
        Fmt::Dimacs => {
            let mut imp = DimacsImporter::<usize>::with_default_weight(o.default_weight);
            imp.set_vertex_factory(num_factory(names));
            imp.import_graph(g, input)
        }
        Fmt::Dot => {
            let mut imp = DotImporter::<usize, DefaultEdge>::new();
            imp.set_vertex_factory(str_factory(names));
            collect_attributes!(imp, col, vertex);
            collect_attributes!(imp, col, edge);
            collect_attributes!(imp, col, graph);
            imp.import_graph(g, input)
        }
        Fmt::Gexf => {
            let mut imp = GexfImporter::<usize, DefaultEdge>::new();
            if let Some(v) = o.schema_validation {
                imp.set_schema_validation(v);
            }
            imp.set_vertex_factory(str_factory(names));
            collect_attributes!(imp, col, vertex);
            collect_attributes!(imp, col, edge);
            imp.import_graph(g, input)
        }
        Fmt::Gml => {
            let mut imp = GmlImporter::<usize, DefaultEdge>::new();
            let n = names.clone();
            imp.set_vertex_factory(move |id| n.borrow_mut().id(Key::Int(id)));
            collect_attributes!(imp, col, vertex);
            collect_attributes!(imp, col, edge);
            imp.import_graph(g, input)
        }
        Fmt::Graph6 => {
            let mut imp = Graph6Importer::<usize>::new();
            imp.set_vertex_factory(num_factory(names));
            imp.import_graph(g, input)
        }
        Fmt::GraphMl => {
            let mut imp = GraphMlImporter::<usize, DefaultEdge>::new();
            if let Some(v) = o.schema_validation {
                imp.set_schema_validation(v);
            }
            imp.set_vertex_factory(str_factory(names));
            if let Some(w) = &o.weight_attribute {
                imp.set_edge_weight_attribute_name(w.clone());
            }
            collect_attributes!(imp, col, vertex);
            collect_attributes!(imp, col, edge);
            collect_attributes!(imp, col, graph);
            imp.import_graph(g, input)
        }
        Fmt::Json => {
            let mut imp = JsonImporter::<usize, DefaultEdge>::new();
            if let Some(n) = &o.vertices_name {
                imp.set_vertices_collection_name(n.clone());
            }
            if let Some(n) = &o.edges_name {
                imp.set_edges_collection_name(n.clone());
            }
            let (n, c) = (names.clone(), col.clone());
            imp.set_vertex_with_attributes_factory(move |id, attributes| {
                let v = n.borrow_mut().id(Key::Str(id.to_owned()));
                let mut c = c.borrow_mut();
                let slot = c.vertices.entry(v).or_default();
                for (k, a) in attributes {
                    slot.insert(k.clone(), a.clone());
                }
                v
            });
            let (next, c) = (Rc::new(Cell::new(0u64)), col.clone());
            imp.set_edge_with_attributes_factory(move |attributes| {
                let id = next.get();
                next.set(id + 1);
                if !attributes.is_empty() {
                    c.borrow_mut().edges.insert(id, attributes.clone());
                }
                DefaultEdge(id)
            });
            imp.import_graph(g, input)
        }
        Fmt::Tsplib => {
            let mut imp = TsplibImporter::<usize>::new();
            imp.import_graph(g, input)?;
            *tsplib = imp.metadata().cloned();
            Ok(())
        }
        Fmt::Lemon | Fmt::Matrix | Fmt::Visio => unreachable!("export-only format"),
    }
}

struct Imported {
    n: usize,
    edges: Edges,
    names: Vec<Key>,
    collected: Collected,
    /// the position of each edge (by the importer's edge identifier) in `edges`
    edge_index: HashMap<u64, usize>,
    tsplib: Option<jgrapht_io::tsplib::TsplibMetadata<usize>>,
}

fn run_import(fmt: Fmt, o: &ImportOpts, input: &[u8], directed: bool) -> PyResult<Imported> {
    let names: Shared<Names> = Rc::default();
    let col: Shared<Collected> = Rc::default();
    let mut tsplib = None;
    let mut ty = GraphType::pseudograph();
    ty.weighted = o.weighted || fmt == Fmt::Tsplib;
    let weighted = ty.weighted;

    macro_rules! go {
        ($graph:expr) => {{
            let mut g = $graph.with_vertex_factory(|i| i as usize);
            import_into(&mut g, fmt, o, input, &names, &col, &mut tsplib).map_err(io_error)?;
            let (n, edges) = collect(&g, weighted)?;
            let edge_index = g
                .edges()
                .enumerate()
                .map(|(i, e)| (std::borrow::Borrow::<DefaultEdge>::borrow(&e).0, i))
                .collect();
            (n, edges, edge_index)
        }};
    }
    let (n, edges, edge_index): (usize, Edges, HashMap<u64, usize>) = if directed {
        go!(DiGraph::<usize>::with_graph_type(ty))
    } else {
        go!(UGraph::<usize>::with_graph_type(ty))
    };

    let mut keys = std::mem::take(&mut names.borrow_mut().keys);
    if fmt == Fmt::Tsplib {
        keys = (0..n as i64).map(Key::Int).collect();
    }
    if keys.len() != n {
        return Err(GraphError::new_err(
            "the file defines inconsistent vertices",
        ));
    }
    let collected = std::mem::take(&mut *col.borrow_mut());
    let mut edges = edges;
    if fmt == Fmt::Dot && weighted {
        // the DOT importer reports attributes but does not set weights: use the `weight` attribute
        for (id, attrs) in &collected.edges {
            if let (Some(i), Some(w)) = (edge_index.get(id), attrs.get("weight"))
                && let Ok(w) = w.value().trim().parse::<f64>()
            {
                edges[*i].2 = Some(w);
            }
        }
    }
    Ok(Imported {
        n,
        edges,
        names: keys,
        collected,
        edge_index,
        tsplib,
    })
}

fn key_to_py(py: Python<'_>, key: &Key) -> PyResult<Py<PyAny>> {
    match key {
        Key::Str(s) => s.into_py_any(py),
        Key::Int(i) => i.into_py_any(py),
    }
}

fn tsplib_to_py<'py>(
    py: Python<'py>,
    meta: &jgrapht_io::tsplib::TsplibMetadata<usize>,
    vertices: &[Py<PyAny>],
) -> PyResult<Bound<'py, PyDict>> {
    let d = PyDict::new(py);
    d.set_item("name", &meta.name)?;
    d.set_item("comment", &meta.comment)?;
    d.set_item("comments", &meta.comments)?;
    d.set_item("type", &meta.problem_type)?;
    d.set_item("edge_weight_type", &meta.edge_weight_type)?;
    d.set_item("dimension", meta.dimension)?;
    d.set_item("capacity", meta.capacity)?;
    d.set_item("edge_weight_format", &meta.edge_weight_format)?;
    d.set_item("edge_data_format", &meta.edge_data_format)?;
    d.set_item("node_coord_type", &meta.node_coord_type)?;
    d.set_item("display_data_type", &meta.display_data_type)?;
    let coordinates = PyDict::new(py);
    let numbers = PyDict::new(py);
    for (v, node) in &meta.nodes {
        coordinates.set_item(&vertices[*v], PyTuple::new(py, &node.coordinates)?)?;
        numbers.set_item(&vertices[*v], node.number)?;
    }
    d.set_item("coordinates", coordinates)?;
    d.set_item("node_numbers", numbers)?;
    let tour = meta.tour.as_ref().map(|t| {
        t.iter()
            .map(|v| vertices[*v].clone_ref(py))
            .collect::<Vec<_>>()
    });
    d.set_item("tour", tour)?;
    d.set_item(
        "distinct_node_locations",
        meta.has_distinct_node_locations(),
    )?;
    d.set_item(
        "distinct_neighbor_distances",
        meta.has_distinct_neighbor_distances(),
    )?;
    Ok(d)
}

/// Bytes of a file name or of an object with a ``read`` method.
fn read_source(source: &Bound<'_, PyAny>) -> PyResult<Vec<u8>> {
    if let Ok(read) = source.getattr("read") {
        let data = read.call0()?;
        return bytes_of(&data);
    }
    let path: PathBuf = source.extract().map_err(|_| {
        pyo3::exceptions::PyTypeError::new_err(
            "expected a file name or a file-like object with a read() method",
        )
    })?;
    Ok(std::fs::read(path)?)
}

fn bytes_of(data: &Bound<'_, PyAny>) -> PyResult<Vec<u8>> {
    if let Ok(s) = data.cast::<PyString>() {
        Ok(s.to_str()?.as_bytes().to_vec())
    } else if let Ok(b) = data.cast::<PyBytes>() {
        Ok(b.as_bytes().to_vec())
    } else {
        Err(pyo3::exceptions::PyTypeError::new_err(
            "expected str or bytes",
        ))
    }
}

fn import_graph_impl(
    py: Python<'_>,
    input: Vec<u8>,
    format: &str,
    kwargs: Option<&Bound<'_, PyDict>>,
) -> PyResult<Py<PyAny>> {
    let fmt = parse_format(format, true)?;
    let mut o = Opts::new(kwargs)?;
    let directed = o.take("directed");
    let weighted = o.flag("weighted", false)?;
    let sparse = o.flag("sparse", false)?;
    if o.take("attributes").is_some() {
        return Err(GraphError::new_err(
            "the attributes option no longer exists: the attributes of a file are stored in the \
             graph, in vertex_attrs, edge_attrs and graph_attrs",
        ));
    }
    let factory = o.take("vertex_factory");
    let into = o.take("into");
    let params = ImportOpts::parse(fmt, weighted, &mut o)?;
    o.finish(format)?;
    let mut weighted = weighted;
    let mut directed = directed;
    if let Some(target) = &into {
        if sparse {
            return Err(GraphError::new_err(
                "into cannot be combined with sparse=True",
            ));
        }
        let target = target.cast::<Graph>().map_err(|_| {
            GraphError::new_err("into must be a Graph (a SparseGraph cannot be modified)")
        })?;
        let (target_directed, target_weighted, _, _) = target.try_borrow()?.flags();
        match &directed {
            Some(d) if d.extract::<bool>()? != target_directed => {
                return Err(GraphError::new_err(
                    "the direction requested does not match the graph given as into",
                ));
            }
            _ => directed = Some(PyBool::new(py, target_directed).to_owned().into_any()),
        }
        if weighted && !target_weighted {
            return Err(GraphError::new_err(
                "weighted=True but the graph given as into is not weighted",
            ));
        }
        weighted = target_weighted;
    }
    let params = ImportOpts {
        weighted: params.weighted || weighted,
        ..params
    };
    if sparse && factory.is_some() {
        return Err(GraphError::new_err(
            "vertex_factory cannot be combined with sparse=True, whose vertices are 0..n-1",
        ));
    }
    let directed = match directed {
        Some(d) => d.extract::<bool>()?,
        None => sniff::directed(fmt, &String::from_utf8_lossy(&input)),
    };

    let imported = py.detach(|| run_import(fmt, &params, &input, directed))?;

    let originals = imported
        .names
        .iter()
        .map(|k| key_to_py(py, k))
        .collect::<PyResult<Vec<_>>>()?;
    let vertices: Vec<Py<PyAny>> = if sparse {
        (0..imported.n)
            .map(|i| i.into_py_any(py))
            .collect::<PyResult<_>>()?
    } else if let Some(factory) = &factory {
        let mapped = originals
            .iter()
            .map(|k| factory.call1((k.bind(py),)).map(Bound::unbind))
            .collect::<PyResult<Vec<_>>>()?;
        let distinct = PyList::new(py, &mapped)?;
        let set = pyo3::types::PySet::new(py, distinct.iter())?;
        if set.len() != mapped.len() {
            return Err(GraphError::new_err(
                "vertex_factory mapped distinct vertices to equal objects",
            ));
        }
        mapped
    } else {
        originals.iter().map(|k| k.clone_ref(py)).collect()
    };

    let mut edge_keys: Option<Vec<Py<PyAny>>> = None;
    let graph: Py<PyAny> = if let Some(target) = &into {
        let target = target.cast::<Graph>()?;
        let mut g = target.try_borrow_mut()?;
        for v in &vertices {
            g.add_vertex(py, v.bind(py).clone())?;
        }
        let mut keys = Vec::with_capacity(imported.edges.len());
        for (s, t, w) in &imported.edges {
            let added = g.add_edge(
                py,
                vertices[*s].bind(py).clone(),
                vertices[*t].bind(py).clone(),
                None,
                *w,
            )?;
            match added {
                Some(edge) => keys.push(edge),
                None => {
                    return Err(GraphError::new_err(
                        "the graph given as into rejected an edge of the file (a self-loop or a \
                         parallel edge it does not allow)",
                    ));
                }
            }
        }
        edge_keys = Some(keys);
        target.clone().into_any().unbind()
    } else if sparse {
        let weights: Option<Vec<f64>> =
            if imported.edges.iter().all(|e| e.2.is_some()) && (weighted || fmt == Fmt::Tsplib) {
                imported.edges.iter().map(|e| e.2).collect()
            } else {
                None
            };
        let pairs = imported.edges.iter().map(|(s, t, _)| (*s, *t)).collect();
        Py::new(
            py,
            SparseGraph::create(imported.n, pairs, directed, weights)?,
        )?
        .into_any()
    } else {
        let g = Graph::from_parts_weighted(
            py,
            directed,
            weighted || fmt == Fmt::Tsplib,
            vertices.iter().map(|v| v.clone_ref(py)).collect(),
            imported.edges.clone(),
        )?;
        // `weighted` graphs stay weighted even without edges
        g.into_any()
    };

    // store what the file says about the graph, its vertices and its edges
    let target = graph.bind(py);
    let graph_attrs = target.getattr("graph_attrs")?;
    let vertex_attrs = target.getattr("vertex_attrs")?;
    let edge_attrs = target.getattr("edge_attrs")?;
    let collected = attributes_to_py(py, &imported.collected.graph)?;
    graph_attrs.call_method1("update", (collected,))?;
    let mut ordered: Vec<_> = imported.collected.vertices.iter().collect();
    ordered.sort_by_key(|(v, _)| **v);
    for (v, map) in ordered {
        if !map.is_empty() {
            let d = attributes_to_py(py, map)?;
            vertex_attrs
                .get_item(&vertices[*v])?
                .call_method1("update", (d,))?;
        }
    }
    let mut ordered: Vec<_> = imported
        .collected
        .edges
        .iter()
        .filter_map(|(id, map)| imported.edge_index.get(id).map(|i| (*i, map)))
        .collect();
    ordered.sort_by_key(|(i, _)| *i);
    // an edge weight that was read is the weight of the edge, not also an attribute
    let weight_name = params.weight_attribute.as_deref().unwrap_or("weight");
    let weights_read = params.weighted || fmt == Fmt::Tsplib;
    for (i, map) in ordered {
        if !map.is_empty() {
            let d = attributes_to_py(py, map)?;
            if weights_read && d.contains(weight_name)? {
                d.del_item(weight_name)?;
            }
            if d.is_empty() {
                continue;
            }
            let edge = match &edge_keys {
                Some(keys) => keys[i].bind(py).clone(),
                None => i.into_pyobject(py)?.into_any(),
            };
            edge_attrs.get_item(edge)?.call_method1("update", (d,))?;
        }
    }
    if sparse || factory.is_some() {
        // the identifiers of the file, when the vertices are not the identifiers themselves
        graph_attrs.set_item("vertex_ids", PyList::new(py, &originals)?)?;
    }
    if let Some(meta) = &imported.tsplib {
        graph_attrs.set_item("tsplib", tsplib_to_py(py, meta, &vertices)?)?;
    }
    Ok(graph)
}

/// Reads a graph from a file.
///
/// ``source`` is a file name or an open file (anything with a ``read`` method, in text or binary
/// mode). ``format`` is one of :func:`import_formats`. The remaining keyword options are:
///
/// * ``directed`` -- whether to build a directed graph. By default this is taken from the
///   document where the format declares it (DOT, GraphML, GEXF, GML, DIMACS, digraph6) and is
///   ``False`` otherwise.
/// * ``weighted`` -- read edge weights (default ``False``, so the result is unweighted).
///   TSPLIB graphs are always weighted.
/// * ``sparse`` -- return a :class:`SparseGraph` instead of a :class:`Graph`; its vertices are
///   the numbers ``0..n-1`` in order of appearance in the file.
/// * ``vertex_factory`` -- a function applied to the identifier of each vertex in the file
///   (a ``str``, or an ``int`` for DIMACS, GML and graph6) to obtain the vertex object, for
///   example ``int``. Without it the identifiers themselves are the vertices.
/// * ``into`` -- add to an existing :class:`Graph` instead of building a new one, and return it.
///
/// The attributes found in the file are stored in the graph: ``graph.vertex_attrs[v]`` and
/// ``graph.edge_attrs[e]`` are the attribute dicts of a vertex and an edge, and ``graph.graph_attrs``
/// those of the graph. Their values are ``bool``, ``int``, ``float`` or ``str`` according to the
/// declared type. When the vertices are not the identifiers of the file (``sparse=True`` or a
/// ``vertex_factory``), ``graph.graph_attrs["vertex_ids"]`` lists the identifiers, indexed by vertex
/// number. For TSPLIB files ``graph.graph_attrs["tsplib"]`` holds the specification, the coordinates
/// and the tour. Edge weights are read with ``weighted=True``; the attribute that holds the weight
/// (``weight``, or ``edge_weight_attribute`` for GraphML) is then the weight of the edge, and is not
/// stored as an attribute.
///
/// Format specific options: ``variant`` (``"edge_list"``, ``"adjacency_list"`` or ``"matrix"``),
/// ``delimiter``, ``matrix_node_id`` and ``matrix_zero_when_no_edge`` for ``csv``;
/// ``default_weight`` for ``dimacs``; ``edge_weight_attribute`` for ``graphml``;
/// ``vertices_name`` and ``edges_name`` for ``json``; ``schema_validation`` (default ``True``) for
/// ``graphml`` and ``gexf``, which the Rust parser accepts but does not act on yet. Unknown options
/// raise :class:`GraphError`.
#[pyfunction]
#[pyo3(signature = (source, format, **options))]
fn read_graph(
    py: Python<'_>,
    source: &Bound<'_, PyAny>,
    format: &str,
    options: Option<&Bound<'_, PyDict>>,
) -> PyResult<Py<PyAny>> {
    import_graph_impl(py, read_source(source)?, format, options)
}

/// Parses a graph from a string (or ``bytes``); see :func:`read_graph` for the options.
#[pyfunction]
#[pyo3(signature = (text, format, **options))]
fn parse_graph(
    py: Python<'_>,
    text: &Bound<'_, PyAny>,
    format: &str,
    options: Option<&Bound<'_, PyDict>>,
) -> PyResult<Py<PyAny>> {
    import_graph_impl(py, bytes_of(text)?, format, options)
}

/// The names of the formats :func:`read_graph` and :func:`parse_graph` understand.
#[pyfunction]
fn import_formats() -> Vec<&'static str> {
    IMPORT_FORMATS.to_vec()
}

/// The names of the formats :func:`write_graph` and :func:`graph_to_string` can produce.
#[pyfunction]
fn export_formats() -> Vec<&'static str> {
    EXPORT_FORMATS.to_vec()
}

// ---------------------------------------------------------------- export

/// The identifiers and attributes requested for an export, evaluated up front so that Python
/// callbacks run (and fail) before the exporter starts.
#[derive(Default)]
struct Common {
    vertex_ids: Option<Rc<HashMap<usize, String>>>,
    edge_ids: Option<Rc<HashMap<u64, String>>>,
    vertex_attrs: Option<Rc<HashMap<usize, AttributeMap>>>,
    edge_attrs: Option<Rc<HashMap<u64, AttributeMap>>>,
    graph_attrs: Option<AttributeMap>,
    graph_id: Option<String>,
}

/// ``spec`` applied to `obj`: a callable is called, a dict is indexed (missing keys give `None`).
fn lookup<'py>(spec: &Bound<'py, PyAny>, obj: Py<PyAny>) -> PyResult<Option<Bound<'py, PyAny>>> {
    let py = spec.py();
    if let Ok(d) = spec.cast::<PyDict>() {
        return Ok(d.get_item(obj.bind(py))?);
    }
    if spec.is_callable() {
        let v = spec.call1((obj,))?;
        return Ok(if v.is_none() { None } else { Some(v) });
    }
    Err(pyo3::exceptions::PyTypeError::new_err(
        "expected a function or a dict",
    ))
}

/// The identifier and attribute options (`vertex_id`, `edge_id`, `vertex_attributes`,
/// `edge_attributes`, `graph_attributes`, `graph_id`) a format understands.
fn common_options(fmt: Fmt) -> &'static [&'static str] {
    match fmt {
        Fmt::Csv | Fmt::Dimacs | Fmt::Lemon | Fmt::Matrix | Fmt::Visio => &["vertex_id"],
        Fmt::Dot => &[
            "vertex_id",
            "vertex_attributes",
            "edge_attributes",
            "graph_attributes",
            "graph_id",
        ],
        Fmt::Gexf => &[
            "vertex_id",
            "edge_id",
            "vertex_attributes",
            "edge_attributes",
        ],
        Fmt::Gml => &["edge_id", "vertex_attributes", "edge_attributes"],
        Fmt::GraphMl => &[
            "vertex_id",
            "edge_id",
            "vertex_attributes",
            "edge_attributes",
            "graph_attributes",
        ],
        Fmt::Json => &[
            "vertex_id",
            "edge_id",
            "vertex_attributes",
            "edge_attributes",
        ],
        Fmt::Graph6 | Fmt::Tsplib => &[],
    }
}

fn common<G>(
    py: Python<'_>,
    g: &G,
    lab: &Labels<'_>,
    fmt: Fmt,
    o: &mut Opts<'_>,
) -> PyResult<Common>
where
    G: jgrapht::Graph<Vertex = usize>,
    G::Edge: EdgeId,
{
    let mut c = Common::default();
    let allowed = common_options(fmt);
    if let Some(spec) = o.take_if(allowed, "vertex_id") {
        let mut ids = HashMap::new();
        let mut seen = HashSet::new();
        for v in g.vertices_cloned() {
            let obj = lab.vertex_obj(py, v);
            let id = spec.call1((obj,))?.str()?.to_string();
            if !seen.insert(id.clone()) {
                return Err(GraphError::new_err(format!(
                    "vertex_id gave the identifier {id:?} to more than one vertex"
                )));
            }
            ids.insert(v, id);
        }
        c.vertex_ids = Some(Rc::new(ids));
    }
    if let Some(spec) = o.take_if(allowed, "edge_id") {
        let mut ids = HashMap::new();
        for e in g.edges_cloned() {
            let obj = lab.edge_obj(py, e.eid());
            ids.insert(e.eid(), spec.call1((obj,))?.str()?.to_string());
        }
        c.edge_ids = Some(Rc::new(ids));
    }
    if let Some(spec) = o.take_if(allowed, "vertex_attributes") {
        let mut attrs = HashMap::new();
        for v in g.vertices_cloned() {
            if let Some(map) = lookup(&spec, lab.vertex_obj(py, v))? {
                attrs.insert(v, py_to_attribute_map(&map)?);
            }
        }
        c.vertex_attrs = Some(Rc::new(attrs));
    }
    if let Some(spec) = o.take_if(allowed, "edge_attributes") {
        let mut attrs = HashMap::new();
        for e in g.edges_cloned() {
            if let Some(map) = lookup(&spec, lab.edge_obj(py, e.eid()))? {
                attrs.insert(e.eid(), py_to_attribute_map(&map)?);
            }
        }
        c.edge_attrs = Some(Rc::new(attrs));
    }
    if let Some(spec) = o.take_if(allowed, "graph_attributes") {
        c.graph_attrs = Some(py_to_attribute_map(&spec)?);
    }
    if allowed.contains(&"graph_id") {
        c.graph_id = o.string("graph_id")?;
    }
    // without an explicit option, the attributes stored in the graph are written
    let stored = lab.attrs();
    if allowed.contains(&"vertex_attributes") && c.vertex_attrs.is_none() {
        let mut attrs = HashMap::new();
        for v in g.vertices_cloned() {
            if let Some(d) = stored
                .existing(py, false, v as u64)
                .filter(|d| !d.bind(py).is_empty())
            {
                attrs.insert(v, py_to_attribute_map(d.bind(py).as_any())?);
            }
        }
        if !attrs.is_empty() {
            c.vertex_attrs = Some(Rc::new(attrs));
        }
    }
    if allowed.contains(&"edge_attributes") && c.edge_attrs.is_none() {
        let mut attrs = HashMap::new();
        for e in g.edges_cloned() {
            if let Some(d) = stored
                .existing(py, true, e.eid())
                .filter(|d| !d.bind(py).is_empty())
            {
                attrs.insert(e.eid(), py_to_attribute_map(d.bind(py).as_any())?);
            }
        }
        if !attrs.is_empty() {
            c.edge_attrs = Some(Rc::new(attrs));
        }
    }
    if allowed.contains(&"graph_attributes") && c.graph_attrs.is_none() {
        let dict = stored.graph_dict(py);
        let own = PyDict::new(py);
        for (k, v) in dict.bind(py).iter() {
            // what the importers add about the file itself is not an attribute to write back
            if !matches!(k.extract::<String>().as_deref(), Ok("vertex_ids" | "tsplib")) {
                own.set_item(k, v)?;
            }
        }
        if !own.is_empty() {
            c.graph_attrs = Some(py_to_attribute_map(own.as_any())?);
        }
    }
    Ok(c)
}

impl Common {
    /// Adds each edge's weight to its attributes under the name ``weight``.
    fn add_weights<G: jgrapht::Graph>(&mut self, g: &G)
    where
        G::Edge: EdgeId,
    {
        let mut attrs = self
            .edge_attrs
            .take()
            .map(|m| (*m).clone())
            .unwrap_or_default();
        for e in g.edges_cloned() {
            attrs
                .entry(e.eid())
                .or_default()
                .insert("weight".to_owned(), Attribute::from(g.weight_of(&e)));
        }
        self.edge_attrs = Some(Rc::new(attrs));
    }

    fn vertex_id_fn(&self) -> Option<impl FnMut(&usize) -> String + 'static + use<>> {
        let ids = self.vertex_ids.clone()?;
        Some(move |v: &usize| ids.get(v).cloned().unwrap_or_default())
    }

    fn edge_id_fn<E: EdgeId + 'static>(&self) -> Option<impl FnMut(&E) -> String + 'static> {
        let ids = self.edge_ids.clone()?;
        Some(move |e: &E| ids.get(&e.eid()).cloned().unwrap_or_default())
    }

    fn vertex_attr_fn(&self) -> Option<impl Fn(&usize) -> AttributeMap + 'static + use<>> {
        let attrs = self.vertex_attrs.clone()?;
        Some(move |v: &usize| attrs.get(v).cloned().unwrap_or_default())
    }

    fn edge_attr_fn<E: EdgeId + 'static>(&self) -> Option<impl Fn(&E) -> AttributeMap + 'static> {
        let attrs = self.edge_attrs.clone()?;
        Some(move |e: &E| attrs.get(&e.eid()).cloned().unwrap_or_default())
    }

    fn graph_attr_fn(&self) -> Option<impl Fn() -> AttributeMap + 'static + use<>> {
        let attrs = self.graph_attrs.clone()?;
        Some(move || attrs.clone())
    }

    fn graph_id_fn(&self) -> Option<impl FnMut() -> String + 'static + use<>> {
        let id = self.graph_id.clone()?;
        Some(move || id.clone())
    }

    /// The names used by the attributes in `maps`, with a type that fits all their values.
    fn types<'a>(maps: impl Iterator<Item = &'a AttributeMap>) -> IndexMap<String, AttributeType> {
        let mut types: IndexMap<String, AttributeType> = IndexMap::new();
        for map in maps {
            for (k, a) in map {
                let t = a.attribute_type();
                let t = if t == AttributeType::Null {
                    AttributeType::String
                } else {
                    t
                };
                match types.get(k).copied() {
                    None => {
                        types.insert(k.clone(), t);
                    }
                    Some(old) if old == t => {}
                    Some(old) => {
                        let numeric = |t: AttributeType| {
                            matches!(
                                t,
                                AttributeType::Int
                                    | AttributeType::Long
                                    | AttributeType::Float
                                    | AttributeType::Double
                            )
                        };
                        let merged = if numeric(old) && numeric(t) {
                            AttributeType::Double
                        } else {
                            AttributeType::String
                        };
                        types.insert(k.clone(), merged);
                    }
                }
            }
        }
        types
    }

    fn vertex_types(&self) -> IndexMap<String, AttributeType> {
        Self::types(self.vertex_attrs.iter().flat_map(|m| m.values()))
    }

    fn edge_types(&self) -> IndexMap<String, AttributeType> {
        Self::types(self.edge_attrs.iter().flat_map(|m| m.values()))
    }
}

fn gexf_type(t: AttributeType) -> GexfAttributeType {
    match t {
        AttributeType::Boolean => GexfAttributeType::Boolean,
        AttributeType::Int => GexfAttributeType::Integer,
        AttributeType::Long => GexfAttributeType::Long,
        AttributeType::Float => GexfAttributeType::Float,
        AttributeType::Double => GexfAttributeType::Double,
        _ => GexfAttributeType::String,
    }
}

/// Declared attribute types: a dict from attribute name to a type name, or to a pair
/// `(type name, default value)`.
type Declared = IndexMap<String, (String, Option<String>)>;

fn declared_types(o: &mut Opts<'_>, option: &str) -> PyResult<Declared> {
    let mut out = Declared::new();
    let Some(spec) = o.take(option) else {
        return Ok(out);
    };
    let dict = spec
        .cast::<PyDict>()
        .map_err(|_| GraphError::new_err(format!("{option} must be a dict from names to types")))?;
    for (name, value) in dict.iter() {
        let name = name.extract::<String>()?;
        let entry = if let Ok(kind) = value.extract::<String>() {
            (kind, None)
        } else if let Ok((kind, default)) = value.extract::<(String, Bound<'_, PyAny>)>() {
            (kind, Some(default.str()?.to_string()))
        } else {
            return Err(GraphError::new_err(format!(
                "{option}[{name:?}] must be a type name or a pair (type name, default)"
            )));
        };
        out.insert(name, entry);
    }
    Ok(out)
}

/// The attribute types to register: those inferred from the values (except `skip`ped names),
/// overridden and extended by the declared ones.
fn merge_types<T>(
    inferred: IndexMap<String, AttributeType>,
    skip: &[String],
    declared: Declared,
    parse: impl Fn(&str) -> PyResult<T>,
    convert: impl Fn(AttributeType) -> T,
) -> PyResult<Vec<(String, T, Option<String>)>> {
    let mut out: IndexMap<String, (T, Option<String>)> = inferred
        .into_iter()
        .filter(|(name, _)| !skip.contains(name))
        .map(|(name, t)| (name, (convert(t), None)))
        .collect();
    for (name, (kind, default)) in declared {
        out.insert(name, (parse(&kind)?, default));
    }
    Ok(out.into_iter().map(|(n, (t, d))| (n, t, d)).collect())
}

fn parse_attribute_type(name: &str) -> PyResult<AttributeType> {
    name.parse::<AttributeType>().map_err(|_| {
        GraphError::new_err(format!(
            "unknown attribute type {name:?}, expected one of null, boolean, int, long, float, \
             double, string, html, unknown, identifier"
        ))
    })
}

fn parse_gexf_type(name: &str) -> PyResult<GexfAttributeType> {
    Ok(match name.to_ascii_lowercase().as_str() {
        "boolean" => GexfAttributeType::Boolean,
        "int" | "integer" => GexfAttributeType::Integer,
        "long" => GexfAttributeType::Long,
        "float" => GexfAttributeType::Float,
        "double" => GexfAttributeType::Double,
        "string" => GexfAttributeType::String,
        "liststring" => GexfAttributeType::ListString,
        "anyuri" => GexfAttributeType::AnyUri,
        _ => {
            return Err(GraphError::new_err(format!(
                "unknown GEXF attribute type {name:?}, expected one of boolean, integer, long, \
                 float, double, string, liststring, anyuri"
            )));
        }
    })
}

/// The ``subgraphs`` option of the DOT exporter: a dict from subgraph name to a dict with the
/// optional keys ``vertices``, ``edges``, ``graph_attributes`` and ``cluster_attributes``.
fn dot_subgraphs<G>(
    py: Python<'_>,
    lab: &Labels<'_>,
    spec: &Bound<'_, PyAny>,
) -> PyResult<IndexMap<String, DotSubgraph<usize, G::Edge>>>
where
    G: jgrapht::Graph<Vertex = usize>,
    G::Edge: EdgeId,
{
    let bad = || {
        GraphError::new_err(
            "subgraphs must be a dict from names to dicts with the keys vertices, edges, \
             graph_attributes and cluster_attributes",
        )
    };
    let dict = spec.cast::<PyDict>().map_err(|_| bad())?;
    let mut out = IndexMap::new();
    for (name, body) in dict.iter() {
        let name = name.extract::<String>()?;
        let body = body.cast::<PyDict>().map_err(|_| bad())?;
        let mut sub = DotSubgraph::new(Vec::new(), Vec::new());
        for (key, value) in body.iter() {
            match key.extract::<String>()?.as_str() {
                "vertices" => {
                    for v in value.try_iter()? {
                        sub.vertices.push(lab.vertex_id(py, &v?)?);
                    }
                }
                "edges" => {
                    for e in value.try_iter()? {
                        sub.edges.push(G::Edge::from_eid(lab.edge_id(py, &e?)?));
                    }
                }
                "graph_attributes" => sub.graph_attributes = py_to_attribute_map(&value)?,
                "cluster_attributes" => sub.cluster_attributes = py_to_attribute_map(&value)?,
                other => {
                    return Err(GraphError::new_err(format!(
                        "unknown key {other:?} in subgraph {name:?}"
                    )));
                }
            }
        }
        out.insert(name, sub);
    }
    Ok(out)
}

fn export_error(error: IoError) -> PyErr {
    io_error(error)
}

/// Serializes `g` in `fmt`.
fn export<G>(
    py: Python<'_>,
    g: &G,
    lab: &Labels<'_>,
    fmt: Fmt,
    o: &mut Opts<'_>,
) -> PyResult<Vec<u8>>
where
    G: IncidenceGraph<Vertex = usize>,
    G::Edge: EdgeId + Clone + Eq + Hash + Display + 'static,
{
    let mut c = common(py, g, lab, fmt, o)?;
    let mut out = Vec::new();
    match fmt {
        Fmt::Csv => {
            let kind = csv_format(o.choice(
                "variant",
                &["edge_list", "adjacency_list", "matrix"],
                "adjacency_list",
            )?);
            let delimiter = o.delimiter()?;
            let weights = o.flag("edge_weights", false)?;
            let node_id = o.flag("matrix_node_id", false)?;
            let zero = o.flag("matrix_zero_when_no_edge", false)?;
            let mut ex = match c.vertex_id_fn() {
                Some(f) => CsvExporter::<usize, G::Edge>::with_vertex_id_provider(
                    f,
                    kind,
                    delimiter.unwrap_or(','),
                )
                .map_err(export_error)?,
                None => {
                    let mut ex = CsvExporter::<usize, G::Edge>::new(kind);
                    if let Some(d) = delimiter {
                        ex.set_delimiter(d).map_err(export_error)?;
                    }
                    ex
                }
            };
            ex.set_parameter(CsvParameter::EdgeWeights, weights);
            ex.set_parameter(CsvParameter::MatrixNodeId, node_id);
            ex.set_parameter(CsvParameter::MatrixZeroWhenNoEdge, zero);
            ex.export_graph(g, &mut out).map_err(export_error)?;
        }
        Fmt::Visio => {
            let mut ex = match c.vertex_id_fn() {
                Some(f) => VisioExporter::<usize, G::Edge>::with_vertex_id_provider(f),
                None => VisioExporter::<usize, G::Edge>::new(),
            };
            ex.export_graph(g, &mut out).map_err(export_error)?;
        }
        Fmt::Dimacs => {
            let kind = match o.choice(
                "variant",
                &["max_clique", "coloring", "shortest_path"],
                "max_clique",
            )? {
                "coloring" => DimacsFormat::Coloring,
                "shortest_path" => DimacsFormat::ShortestPath,
                _ => DimacsFormat::MaxClique,
            };
            let weights = o.flag("edge_weights", false)?;
            let mut ex = match c.vertex_id_fn() {
                Some(f) => DimacsExporter::<usize, G::Edge>::with_vertex_id_provider(f),
                None => DimacsExporter::<usize, G::Edge>::new(),
            };
            ex.set_format(kind);
            ex.set_parameter(DimacsParameter::ExportEdgeWeights, weights);
            ex.export_graph(g, &mut out).map_err(export_error)?;
        }
        Fmt::Dot => {
            if o.flag("edge_weights", false)? {
                c.add_weights(g);
            }
            let mut ex = match c.vertex_id_fn() {
                Some(f) => DotExporter::<usize, G::Edge>::with_vertex_id_provider(f),
                None => DotExporter::<usize, G::Edge>::new(),
            };
            if let Some(spec) = o.take("subgraphs") {
                let subgraphs = Rc::new(dot_subgraphs::<G>(py, lab, &spec)?);
                ex.set_subgraph_provider(move || (*subgraphs).clone());
            }
            if let Some(f) = c.graph_id_fn() {
                ex.set_graph_id_provider(f);
            }
            if let Some(f) = c.graph_attr_fn() {
                ex.set_graph_attribute_provider(f);
            }
            if let Some(f) = c.vertex_attr_fn() {
                ex.set_vertex_attribute_provider(f);
            }
            if let Some(f) = c.edge_attr_fn::<G::Edge>() {
                ex.set_edge_attribute_provider(f);
            }
            ex.export_graph(g, &mut out).map_err(export_error)?;
        }
        Fmt::Gexf => {
            let mut ex = GexfExporter::<usize, G::Edge>::new();
            if let Some(f) = c.vertex_id_fn() {
                ex.set_vertex_id_provider(f);
            }
            if let Some(f) = c.edge_id_fn::<G::Edge>() {
                ex.set_edge_id_provider(f);
            }
            ex.set_parameter(
                GexfParameter::ExportEdgeWeights,
                o.flag("edge_weights", false)?,
            );
            ex.set_parameter(
                GexfParameter::ExportEdgeLabels,
                o.flag("edge_labels", false)?,
            );
            ex.set_parameter(GexfParameter::ExportEdgeTypes, o.flag("edge_types", false)?);
            ex.set_parameter(GexfParameter::ExportMeta, o.flag("meta", true)?);
            if let Some(s) = o.string("creator")? {
                ex.set_creator(s);
            }
            if let Some(s) = o.string("keywords")? {
                ex.set_keywords(s);
            }
            if let Some(s) = o.string("description")? {
                ex.set_description(s);
            }
            let reserved_node = ["id".to_owned(), "label".to_owned()];
            let reserved_edge: Vec<String> = ["id", "type", "label", "source", "target", "weight"]
                .map(str::to_owned)
                .to_vec();
            let declared_nodes = declared_types(o, "vertex_attribute_types")?;
            let declared_edges = declared_types(o, "edge_attribute_types")?;
            if let Some(f) = c.vertex_attr_fn() {
                ex.set_vertex_attribute_provider(f);
            }
            if let Some(f) = c.edge_attr_fn::<G::Edge>() {
                ex.set_edge_attribute_provider(f);
            }
            for (name, t, default) in merge_types(
                c.vertex_types(),
                &reserved_node,
                declared_nodes,
                parse_gexf_type,
                gexf_type,
            )? {
                ex.register_attribute(name, GexfAttributeCategory::Node, t, default, None)
                    .map_err(export_error)?;
            }
            for (name, t, default) in merge_types(
                c.edge_types(),
                &reserved_edge,
                declared_edges,
                parse_gexf_type,
                gexf_type,
            )? {
                ex.register_attribute(name, GexfAttributeCategory::Edge, t, default, None)
                    .map_err(export_error)?;
            }
            ex.export_graph(g, &mut out).map_err(export_error)?;
        }
        Fmt::Gml => {
            let mut ex = GmlExporter::<usize, G::Edge>::new();
            if let Some(spec) = o.take("vertex_graphics") {
                let mut graphics = HashMap::new();
                for v in g.vertices_cloned() {
                    if let Some(map) = lookup(&spec, lab.vertex_obj(py, v))? {
                        graphics.insert(v, py_to_attribute_map(&map)?);
                    }
                }
                ex.set_parameter(GmlParameter::ExportCustomVertexGraphicsAttributes, true);
                ex.set_vertex_graphics_attribute_provider(move |v| {
                    graphics.get(v).cloned().unwrap_or_default()
                });
            }
            ex.set_parameter(
                GmlParameter::ExportEdgeWeights,
                o.flag("edge_weights", false)?,
            );
            ex.set_parameter(
                GmlParameter::ExportEdgeLabels,
                o.flag("edge_labels", false)?,
            );
            ex.set_parameter(
                GmlParameter::ExportVertexLabels,
                o.flag("vertex_labels", false)?,
            );
            ex.set_parameter(
                GmlParameter::EscapeStringsAsJava,
                o.flag("escape_strings", false)?,
            );
            ex.set_parameter(
                GmlParameter::ExportCustomVertexAttributes,
                c.vertex_attrs.is_some(),
            );
            ex.set_parameter(
                GmlParameter::ExportCustomEdgeAttributes,
                c.edge_attrs.is_some(),
            );
            if let Some(f) = c.vertex_attr_fn() {
                ex.set_vertex_attribute_provider(f);
            }
            if let Some(f) = c.edge_attr_fn::<G::Edge>() {
                ex.set_edge_attribute_provider(f);
            }
            if let Some(f) = c.edge_id_fn::<G::Edge>() {
                ex.set_edge_id_provider(f);
            }
            ex.export_graph(g, &mut out).map_err(export_error)?;
        }
        Fmt::Graph6 => {
            let kind = match o.choice(
                "variant",
                &["graph6", "sparse6", "digraph6"],
                if g.graph_type().directed {
                    "digraph6"
                } else {
                    "graph6"
                },
            )? {
                "sparse6" => Graph6Format::Sparse6,
                "digraph6" => Graph6Format::Digraph6,
                _ => Graph6Format::Graph6,
            };
            let mut ex = Graph6Exporter::new(kind);
            ex.export_graph(g, &mut out).map_err(export_error)?;
        }
        Fmt::GraphMl => {
            let mut ex = match c.vertex_id_fn() {
                Some(f) => GraphMlExporter::<usize, G::Edge>::with_vertex_id_provider(f),
                None => GraphMlExporter::<usize, G::Edge>::new(),
            };
            ex.set_export_edge_weights(o.flag("edge_weights", false)?);
            ex.set_export_vertex_labels(o.flag("vertex_labels", false)?);
            ex.set_export_edge_labels(o.flag("edge_labels", false)?);
            if let Some(f) = c.edge_id_fn::<G::Edge>() {
                ex.set_edge_id_provider(f);
            }
            if let Some(f) = c.graph_attr_fn() {
                ex.set_graph_attribute_provider(f);
            }
            if let Some(f) = c.vertex_attr_fn() {
                ex.set_vertex_attribute_provider(f);
            }
            if let Some(f) = c.edge_attr_fn::<G::Edge>() {
                ex.set_edge_attribute_provider(f);
            }
            let vertex_label = o.string("vertex_label_attribute")?;
            let edge_label = o.string("edge_label_attribute")?;
            let weight = o.string("edge_weight_attribute")?;
            if let Some(n) = &vertex_label {
                ex.set_vertex_label_attribute_name(n.clone())
                    .map_err(export_error)?;
            }
            if let Some(n) = &edge_label {
                ex.set_edge_label_attribute_name(n.clone())
                    .map_err(export_error)?;
            }
            if let Some(n) = &weight {
                ex.set_edge_weight_attribute_name(n.clone())
                    .map_err(export_error)?;
            }
            let reserved: Vec<String> = vec![
                vertex_label.unwrap_or_else(|| "label".into()),
                edge_label.unwrap_or_else(|| "label".into()),
                weight.unwrap_or_else(|| "weight".into()),
            ];
            let declared_nodes = declared_types(o, "vertex_attribute_types")?;
            let declared_edges = declared_types(o, "edge_attribute_types")?;
            let declared_graph = declared_types(o, "graph_attribute_types")?;
            let graph_types = Common::types(c.graph_attrs.iter());
            for (category, inferred, declared) in [
                (AttributeCategory::Node, c.vertex_types(), declared_nodes),
                (AttributeCategory::Edge, c.edge_types(), declared_edges),
                (AttributeCategory::Graph, graph_types, declared_graph),
            ] {
                let skip: &[String] = if category == AttributeCategory::Graph {
                    &[]
                } else {
                    &reserved
                };
                for (name, t, default) in
                    merge_types(inferred, skip, declared, parse_attribute_type, |t| t)?
                {
                    ex.register_attribute(name, category, t, default)
                        .map_err(export_error)?;
                }
            }
            ex.export_graph(g, &mut out).map_err(export_error)?;
        }
        Fmt::Json => {
            if o.flag("edge_weights", false)? {
                c.add_weights(g);
            }
            let mut ex = match c.vertex_id_fn() {
                Some(f) => JsonExporter::<usize, G::Edge>::with_vertex_id_provider(f),
                None => JsonExporter::<usize, G::Edge>::new(),
            };
            if let Some(s) = o.string("vertices_name")? {
                ex.set_vertices_collection_name(s);
            }
            if let Some(s) = o.string("edges_name")? {
                ex.set_edges_collection_name(s);
            }
            if let Some(f) = c.edge_id_fn::<G::Edge>() {
                ex.set_edge_id_provider(f);
            }
            if let Some(f) = c.vertex_attr_fn() {
                ex.set_vertex_attribute_provider(f);
            }
            if let Some(f) = c.edge_attr_fn::<G::Edge>() {
                ex.set_edge_attribute_provider(f);
            }
            ex.export_graph(g, &mut out).map_err(export_error)?;
        }
        Fmt::Lemon => {
            let mut ex = match c.vertex_id_fn() {
                Some(f) => LemonExporter::<usize, G::Edge>::with_vertex_id_provider(f),
                None => LemonExporter::<usize, G::Edge>::new(),
            };
            ex.set_parameter(
                LemonParameter::ExportEdgeWeights,
                o.flag("edge_weights", false)?,
            );
            ex.set_parameter(
                LemonParameter::EscapeStringsAsJava,
                o.flag("escape_strings", false)?,
            );
            ex.export_graph(g, &mut out).map_err(export_error)?;
        }
        Fmt::Matrix => {
            let kind = match o.choice(
                "variant",
                &["adjacency", "laplacian", "normalized_laplacian"],
                "adjacency",
            )? {
                "laplacian" => MatrixFormat::SparseLaplacian,
                "normalized_laplacian" => MatrixFormat::SparseNormalizedLaplacian,
                _ => MatrixFormat::SparseAdjacency,
            };
            let mut ex = match c.vertex_id_fn() {
                Some(f) => MatrixExporter::<usize, G::Edge>::with_vertex_id_provider(kind, f),
                None => MatrixExporter::<usize, G::Edge>::new(kind),
            };
            ex.export_graph(g, &mut out).map_err(export_error)?;
        }
        Fmt::Tsplib => unreachable!("import-only format"),
    }
    Ok(out)
}

fn export_bytes(
    py: Python<'_>,
    graph: &Bound<'_, PyAny>,
    format: &str,
    kwargs: Option<&Bound<'_, PyDict>>,
) -> PyResult<Vec<u8>> {
    let fmt = parse_format(format, false)?;
    let mut o = Opts::new(kwargs)?;
    let bytes = dispatch!(graph, |g, lab| export(py, g, &lab, fmt, &mut o))?;
    o.finish(format)?;
    Ok(bytes)
}

/// Writes a graph to a file.
///
/// ``target`` is a file name or an open file (anything with a ``write`` method). ``format`` is
/// one of :func:`export_formats`; see :func:`graph_to_string` for the options.
#[pyfunction]
#[pyo3(signature = (graph, target, format, **options))]
fn write_graph(
    py: Python<'_>,
    graph: &Bound<'_, PyAny>,
    target: &Bound<'_, PyAny>,
    format: &str,
    options: Option<&Bound<'_, PyDict>>,
) -> PyResult<()> {
    let bytes = export_bytes(py, graph, format, options)?;
    let text = String::from_utf8(bytes)
        .map_err(|e| GraphError::new_err(format!("exporter produced invalid UTF-8: {e}")))?;
    if let Ok(write) = target.getattr("write") {
        if write.call1((&text,)).is_err() {
            write.call1((PyBytes::new(py, text.as_bytes()),))?;
        }
        return Ok(());
    }
    let path: PathBuf = target.extract().map_err(|_| {
        pyo3::exceptions::PyTypeError::new_err(
            "expected a file name or a file-like object with a write() method",
        )
    })?;
    std::fs::write(path, text)?;
    Ok(())
}

/// Serializes a graph to a string.
///
/// ``format`` is one of :func:`export_formats`. The vertices are numbered ``1, 2, ...`` (in the
/// order of ``graph.vertices()``) unless ``vertex_id`` is given: a function from a vertex to its
/// identifier string, for example ``str``. Identifiers must be distinct. (The GML and graph6
/// formats number the vertices themselves.) Further options common to several formats:
///
/// * ``edge_id`` -- a function from an edge to its identifier string (formats with edge ids).
/// * ``vertex_attributes`` / ``edge_attributes`` -- a dict from vertex (edge) to a dict from
///   attribute names to values, or a function returning such a dict (or ``None``). Values are
///   ``bool``, ``int``, ``float``, ``str`` or ``None``; any other value is written as its ``str``.
///   Supported by DOT, GEXF, GML, GraphML and JSON. Without the option, the attributes stored in
///   the graph (``graph.vertex_attrs`` and ``graph.edge_attrs``) are written.
/// * ``graph_attributes`` -- a dict of graph attributes (DOT, GraphML); without the option,
///   ``graph.graph_attrs`` is written. ``graph_id`` -- a name for the graph (DOT).
/// * ``edge_weights`` -- write the edge weights (CSV, DIMACS, DOT and JSON as an edge attribute
///   ``weight``, GEXF, GML, GraphML, LEMON).
/// * ``vertex_labels`` / ``edge_labels`` -- write the attribute ``"label"`` as the label of
///   the vertices (edges) (GML, GraphML; ``edge_labels`` also GEXF).
///
/// Format specific options: ``variant`` (CSV: ``"edge_list"``, ``"adjacency_list"`` (default) or
/// ``"matrix"``; DIMACS: ``"max_clique"`` (default), ``"coloring"`` or ``"shortest_path"``;
/// matrix: ``"adjacency"`` (default), ``"laplacian"`` or ``"normalized_laplacian"``);
/// ``delimiter``, ``matrix_node_id`` and ``matrix_zero_when_no_edge`` (CSV); ``variant``
/// (graph6: ``"graph6"``, ``"sparse6"`` or ``"digraph6"``, by default digraph6 for directed
/// graphs); ``edge_types``, ``meta``, ``creator``, ``keywords`` and ``description`` (GEXF);
/// ``escape_strings`` (GML, LEMON); ``vertices_name`` and ``edges_name`` (JSON). Unknown options
/// raise :class:`GraphError`.
///
/// Notes: the CSV ``"adjacency_list"`` variant of an undirected graph lists every edge from both
/// of its ends (so reading it back gives parallel edges); use ``"edge_list"`` to round-trip
/// undirected graphs. A :class:`SparseGraph` counts as a multigraph, so graph6 (which is for
/// simple graphs) refuses it; use ``variant="sparse6"``.
#[pyfunction]
#[pyo3(signature = (graph, format, **options))]
fn graph_to_string(
    py: Python<'_>,
    graph: &Bound<'_, PyAny>,
    format: &str,
    options: Option<&Bound<'_, PyDict>>,
) -> PyResult<String> {
    let bytes = export_bytes(py, graph, format, options)?;
    String::from_utf8(bytes)
        .map_err(|e| GraphError::new_err(format!("exporter produced invalid UTF-8: {e}")))
}

/// The metadata of the TSPLIB instance `input`, as `TsplibImporter::import_tour` needs it.
fn tsplib_reference(input: &[u8]) -> PyResult<jgrapht_io::tsplib::TsplibMetadata<usize>> {
    let mut ty = GraphType::pseudograph();
    ty.weighted = true;
    let mut g = UGraph::<usize>::with_graph_type(ty).with_vertex_factory(|i| i as usize);
    let mut importer = TsplibImporter::<usize>::new();
    importer.import_graph(&mut g, input).map_err(io_error)?;
    importer
        .metadata()
        .cloned()
        .ok_or_else(|| GraphError::new_err("the TSPLIB instance has no metadata"))
}

fn tsplib_tour(tour: &[u8], instance: &[u8]) -> PyResult<Option<Vec<usize>>> {
    let reference = tsplib_reference(instance)?;
    let mut importer = TsplibImporter::<usize>::new();
    importer.import_tour(&reference, tour).map_err(io_error)
}

/// Reads the tour of a TSPLIB tour file.
///
/// ``tour`` is the tour file and ``instance`` the instance file whose nodes it refers to (both a
/// file name or an open file). Returns the vertices of the tour in order, as the vertices of the
/// graph :func:`read_graph` builds from the same instance (the numbers ``0..n-1`` in the order of
/// the file), or ``None`` if the file has no ``TOUR_SECTION``. A node number that the instance
/// does not define raises :class:`GraphError`.
#[pyfunction]
fn read_tsplib_tour(
    tour: &Bound<'_, PyAny>,
    instance: &Bound<'_, PyAny>,
) -> PyResult<Option<Vec<usize>>> {
    tsplib_tour(&read_source(tour)?, &read_source(instance)?)
}

/// Like :func:`read_tsplib_tour`, with the contents of the tour and instance files given as
/// strings (or ``bytes``).
#[pyfunction]
fn parse_tsplib_tour(
    tour: &Bound<'_, PyAny>,
    instance: &Bound<'_, PyAny>,
) -> PyResult<Option<Vec<usize>>> {
    tsplib_tour(&bytes_of(tour)?, &bytes_of(instance)?)
}

/// The TSPLIB ``GEO`` distance (an integer number of kilometres) between two nodes whose
/// coordinates are given as ``(latitude, longitude)`` in TSPLIB's ``DDD.MM`` degrees-and-minutes
/// notation.
#[pyfunction]
fn tsplib_geographic_distance(a: Vec<f64>, b: Vec<f64>) -> PyResult<i32> {
    let node = |number, coordinates| jgrapht_io::tsplib::TsplibNode {
        number,
        coordinates,
    };
    TsplibImporter::<usize>::geographical_distance_2d(&node(1, a), &node(2, b)).map_err(io_error)
}

// ---------------------------------------------------------------- event-driven import

const EVENT_FORMATS: &[&str] = &[
    "csv",
    "dimacs",
    "gexf",
    "graph6",
    "graphml",
    "graphml_edge_list",
    "json",
];

/// Python values for the vertices and edges of import events.
trait EventValue {
    fn to_py(&self, py: Python<'_>) -> PyResult<Py<PyAny>>;
}

impl EventValue for String {
    fn to_py(&self, py: Python<'_>) -> PyResult<Py<PyAny>> {
        self.into_py_any(py)
    }
}

impl EventValue for usize {
    fn to_py(&self, py: Python<'_>) -> PyResult<Py<PyAny>> {
        self.into_py_any(py)
    }
}

impl<A: EventValue, B: EventValue> EventValue for (A, B) {
    fn to_py(&self, py: Python<'_>) -> PyResult<Py<PyAny>> {
        Ok(PyTuple::new(py, [self.0.to_py(py)?, self.1.to_py(py)?])?
            .into_any()
            .unbind())
    }
}

impl<A: EventValue, B: EventValue> EventValue for (A, B, Option<f64>) {
    fn to_py(&self, py: Python<'_>) -> PyResult<Py<PyAny>> {
        Ok(PyTuple::new(
            py,
            [
                self.0.to_py(py)?,
                self.1.to_py(py)?,
                self.2.into_py_any(py)?,
            ],
        )?
        .into_any()
        .unbind())
    }
}

impl<A: EventValue, B: EventValue> EventValue for (A, B, f64) {
    fn to_py(&self, py: Python<'_>) -> PyResult<Py<PyAny>> {
        Ok(PyTuple::new(
            py,
            [
                self.0.to_py(py)?,
                self.1.to_py(py)?,
                self.2.into_py_any(py)?,
            ],
        )?
        .into_any()
        .unbind())
    }
}

fn event_to_py<V: EventValue, E: EventValue>(
    py: Python<'_>,
    event: ImportEvent<V, E>,
) -> PyResult<Py<PyAny>> {
    let name = |n: &str| n.into_py_any(py);
    let items: Vec<Py<PyAny>> = match event {
        ImportEvent::Start => vec![name("start")?],
        ImportEvent::End => vec![name("end")?],
        ImportEvent::VertexCount(n) => vec![name("vertex_count")?, n.into_py_any(py)?],
        ImportEvent::EdgeCount(n) => vec![name("edge_count")?, n.into_py_any(py)?],
        ImportEvent::Vertex(v) => vec![name("vertex")?, v.to_py(py)?],
        ImportEvent::VertexWithAttributes(v, attrs) => vec![
            name("vertex_with_attributes")?,
            v.to_py(py)?,
            attributes_to_py(py, &attrs)?.into_any().unbind(),
        ],
        ImportEvent::Edge(e) => vec![name("edge")?, e.to_py(py)?],
        ImportEvent::EdgeWithAttributes(e, attrs) => vec![
            name("edge_with_attributes")?,
            e.to_py(py)?,
            attributes_to_py(py, &attrs)?.into_any().unbind(),
        ],
        ImportEvent::GraphAttribute(key, a) => {
            vec![
                name("graph_attribute")?,
                key.into_py_any(py)?,
                attribute_to_py(py, &a)?,
            ]
        }
        ImportEvent::VertexAttribute(v, key, a) => vec![
            name("vertex_attribute")?,
            v.to_py(py)?,
            key.into_py_any(py)?,
            attribute_to_py(py, &a)?,
        ],
        ImportEvent::EdgeAttribute(e, key, a) => vec![
            name("edge_attribute")?,
            e.to_py(py)?,
            key.into_py_any(py)?,
            attribute_to_py(py, &a)?,
        ],
        _ => return Err(GraphError::new_err("unsupported import event")),
    };
    Ok(PyTuple::new(py, items)?.into_any().unbind())
}

/// Runs `importer` on `input`; every event goes to `callback`, or is collected and returned.
fn run_events<I>(
    py: Python<'_>,
    importer: &mut I,
    input: &[u8],
    callback: Option<&Bound<'_, PyAny>>,
) -> PyResult<Vec<Py<PyAny>>>
where
    I: EventDrivenImporter,
    I::Vertex: EventValue,
    I::Edge: EventValue,
{
    let failure: RefCell<Option<PyErr>> = RefCell::new(None);
    let mut collected = Vec::new();
    let result = importer.import_events(input, |event| {
        let delivered = event_to_py(py, event).and_then(|e| match callback {
            Some(callback) => callback.call1((e,)).map(|_| ()),
            None => {
                collected.push(e);
                Ok(())
            }
        });
        delivered.map_err(|e| {
            *failure.borrow_mut() = Some(e);
            IoError::Import("the event callback raised an exception".into())
        })
    });
    if let Some(error) = failure.into_inner() {
        return Err(error);
    }
    result.map_err(io_error)?;
    Ok(collected)
}

fn events_impl(
    py: Python<'_>,
    input: Vec<u8>,
    format: &str,
    callback: Option<&Bound<'_, PyAny>>,
    kwargs: Option<&Bound<'_, PyDict>>,
) -> PyResult<Option<Vec<Py<PyAny>>>> {
    let mut o = Opts::new(kwargs)?;
    let events = match format.to_ascii_lowercase().as_str() {
        "csv" => {
            let kind = csv_format(o.choice(
                "variant",
                &["edge_list", "adjacency_list", "matrix"],
                "adjacency_list",
            )?);
            let mut imp = CsvEventDrivenImporter::new(kind);
            if let Some(d) = o.delimiter()? {
                imp.set_delimiter(d).map_err(io_error)?;
            }
            imp.set_parameter(CsvParameter::EdgeWeights, o.flag("weighted", false)?);
            imp.set_parameter(CsvParameter::MatrixNodeId, o.flag("matrix_node_id", false)?);
            imp.set_parameter(
                CsvParameter::MatrixZeroWhenNoEdge,
                o.flag("matrix_zero_when_no_edge", false)?,
            );
            o.finish(format)?;
            run_events(py, &mut imp, &input, callback)?
        }
        "dimacs" => {
            let mut imp = DimacsEventDrivenImporter::new()
                .zero_based_numbering(o.flag("zero_based_numbering", false)?)
                .renumber_vertices(o.flag("renumber_vertices", false)?);
            o.finish(format)?;
            run_events(py, &mut imp, &input, callback)?
        }
        "gexf" => {
            let mut imp = GexfEventDrivenImporter::new();
            imp.set_schema_validation(o.flag("schema_validation", true)?);
            o.finish(format)?;
            run_events(py, &mut imp, &input, callback)?
        }
        "graph6" => {
            let mut imp = Graph6EventDrivenImporter::new();
            o.finish(format)?;
            run_events(py, &mut imp, &input, callback)?
        }
        "graphml" => {
            let mut imp = GraphMlEventDrivenImporter::new();
            imp.set_schema_validation(o.flag("schema_validation", true)?);
            if let Some(n) = o.string("edge_weight_attribute")? {
                imp.set_edge_weight_attribute_name(n);
            }
            o.finish(format)?;
            run_events(py, &mut imp, &input, callback)?
        }
        "graphml_edge_list" => {
            let mut imp = SimpleGraphMlEdgeListImporter::new();
            imp.set_schema_validation(o.flag("schema_validation", true)?);
            if let Some(n) = o.string("edge_weight_attribute")? {
                imp.set_edge_weight_attribute_name(n);
            }
            o.finish(format)?;
            run_events(py, &mut imp, &input, callback)?
        }
        "json" => {
            let mut imp = JsonEventDrivenImporter::new();
            if let Some(n) = o.string("vertices_name")? {
                imp.set_vertices_collection_name(n);
            }
            if let Some(n) = o.string("edges_name")? {
                imp.set_edges_collection_name(n);
            }
            o.finish(format)?;
            run_events(py, &mut imp, &input, callback)?
        }
        _ => {
            return Err(GraphError::new_err(format!(
                "format {format:?} has no event-driven importer, expected one of {EVENT_FORMATS:?}"
            )));
        }
    };
    Ok(if callback.is_some() {
        None
    } else {
        Some(events)
    })
}

/// Reads a file as a stream of events, without building a graph.
///
/// ``source`` is a file name or an open file, ``format`` one of :func:`event_formats`. Each
/// event is a tuple whose first item is its name:
///
/// * ``("start",)`` and ``("end",)`` around the document;
/// * ``("vertex_count", n)`` and ``("edge_count", m)`` where the format declares them;
/// * ``("vertex", v)`` and ``("vertex_with_attributes", v, attributes)``;
/// * ``("edge", (source, target, weight))`` and ``("edge_with_attributes", edge, attributes)``,
///   where ``weight`` is ``None`` if the edge has none (graph6 edges are ``(source, target)``);
/// * ``("graph_attribute", name, value)``, ``("vertex_attribute", v, name, value)`` and
///   ``("edge_attribute", edge, name, value)``.
///
/// Vertices are strings, except for DIMACS, graph6 and ``graphml_edge_list`` where they are
/// integers. If ``callback`` is given it is called with every event as it is read, an exception
/// it raises stops the import and propagates, and the result is ``None``; otherwise the events are
/// returned as a list. The format specific options are those of :func:`read_graph`, plus
/// ``zero_based_numbering`` and ``renumber_vertices`` for DIMACS; for CSV, ``weighted`` makes the
/// importer read the weights.
#[pyfunction]
#[pyo3(signature = (source, format, callback=None, **options))]
fn read_events(
    py: Python<'_>,
    source: &Bound<'_, PyAny>,
    format: &str,
    callback: Option<&Bound<'_, PyAny>>,
    options: Option<&Bound<'_, PyDict>>,
) -> PyResult<Option<Vec<Py<PyAny>>>> {
    events_impl(py, read_source(source)?, format, callback, options)
}

/// Like :func:`read_events`, for a document given as a string (or ``bytes``).
#[pyfunction]
#[pyo3(signature = (text, format, callback=None, **options))]
fn parse_events(
    py: Python<'_>,
    text: &Bound<'_, PyAny>,
    format: &str,
    callback: Option<&Bound<'_, PyAny>>,
    options: Option<&Bound<'_, PyDict>>,
) -> PyResult<Option<Vec<Py<PyAny>>>> {
    events_impl(py, bytes_of(text)?, format, callback, options)
}

/// The names of the formats :func:`read_events` and :func:`parse_events` understand.
#[pyfunction]
fn event_formats() -> Vec<&'static str> {
    EVENT_FORMATS.to_vec()
}

pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    for f in [
        wrap_pyfunction!(read_graph, m)?,
        wrap_pyfunction!(parse_graph, m)?,
        wrap_pyfunction!(write_graph, m)?,
        wrap_pyfunction!(graph_to_string, m)?,
        wrap_pyfunction!(import_formats, m)?,
        wrap_pyfunction!(export_formats, m)?,
        wrap_pyfunction!(read_events, m)?,
        wrap_pyfunction!(parse_events, m)?,
        wrap_pyfunction!(event_formats, m)?,
        wrap_pyfunction!(read_tsplib_tour, m)?,
        wrap_pyfunction!(parse_tsplib_tour, m)?,
        wrap_pyfunction!(tsplib_geographic_distance, m)?,
    ] {
        m.add_function(f)?;
    }
    Ok(())
}
