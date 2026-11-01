"""Drawing helpers for graphs, built on matplotlib.

The functions draw vertices, edges and labels onto a matplotlib ``Axes`` at the positions given by
a layout, for example :func:`jgrapht.circular_layout` or :func:`jgrapht.fruchterman_reingold_layout`.
They work with :class:`~jgrapht.Graph`, :class:`~jgrapht.SparseGraph` and read-only wrappers.

matplotlib is not a dependency of the package. Install it with ``pip install matplotlib`` (or
``pip install jgrapht[plot]``); using these functions without it raises :class:`ImportError`.
"""

import math

from ._jgrapht_rs import fruchterman_reingold_layout

__all__ = [
    "draw",
    "draw_vertices",
    "draw_edges",
    "draw_vertex_labels",
    "draw_edge_labels",
]

_VERTEX_COLOR = "#1f78b4"
_EDGE_COLOR = "#555555"


def _matplotlib():
    try:
        import matplotlib  # noqa: F401
    except ImportError as exc:
        raise ImportError(
            "jgrapht.drawing needs matplotlib; install it with 'pip install matplotlib'"
        ) from exc
    import matplotlib

    return matplotlib


def _axes(ax):
    if ax is not None:
        return ax
    _matplotlib()
    import matplotlib.pyplot as plt

    return plt.gca()


def _positions(graph, pos):
    """The layout to draw with: ``pos`` itself, or a Fruchterman-Reingold layout."""
    if pos is None:
        return fruchterman_reingold_layout(graph, seed=0)
    missing = [v for v in graph.vertices() if v not in pos]
    if missing:
        raise ValueError(f"no position for vertex {missing[0]!r}")
    return pos


def _per_item(spec, items, default):
    """A list with one entry per item from a constant, a dict ``item -> value``, or a function."""
    if isinstance(spec, dict):
        return [spec.get(item, default) for item in items]
    if callable(spec):
        return [spec(item) for item in items]
    return spec


def _is_number(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def _map_numbers(colors, cmap, vmin, vmax):
    """Maps a list of numbers to RGBA colors with a colormap; other lists are returned as they are."""
    if not colors or not all(_is_number(c) for c in colors):
        return colors
    _matplotlib()
    import matplotlib.cm as cm
    from matplotlib.colors import Normalize

    return cm.ScalarMappable(norm=Normalize(vmin, vmax), cmap=cmap).to_rgba(colors)


def _label_text(spec, item, default):
    if spec is None or spec is True:
        return default
    if isinstance(spec, dict):
        return spec.get(item)
    if callable(spec):
        return spec(item)
    return default


def draw_vertices(
    graph,
    pos=None,
    ax=None,
    *,
    vertices=None,
    vertex_size=300,
    vertex_color=_VERTEX_COLOR,
    vertex_shape="o",
    border_color="none",
    border_width=1.0,
    cmap=None,
    vmin=None,
    vmax=None,
    alpha=None,
):
    """Draws the vertices of ``graph`` as markers.

    :param graph: a :class:`~jgrapht.Graph` or :class:`~jgrapht.SparseGraph`.
    :param pos: a dict from vertex to ``(x, y)``, such as the result of a layout function. By
        default a Fruchterman-Reingold layout with a fixed seed.
    :param ax: the matplotlib ``Axes`` to draw on, by default the current one.
    :param vertices: the vertices to draw, by default all of them.
    :param vertex_size: the marker area in points squared.
    :param vertex_color: a color, a list of colors, a dict from vertex to color, a function of the
        vertex, or numbers that ``cmap`` maps to colors.
    :param vertex_shape: the matplotlib marker, for example ``"o"`` (circle) or ``"s"`` (square).
    :param border_color: the color of the marker outline.
    :param border_width: the width of the marker outline.
    :param cmap: a matplotlib colormap for numeric colors.
    :param vmin: the lower bound of the colormap.
    :param vmax: the upper bound of the colormap.
    :param alpha: the transparency, between 0 and 1.
    :returns: the matplotlib ``PathCollection``.
    """
    ax = _axes(ax)
    pos = _positions(graph, pos)
    vs = list(graph.vertices() if vertices is None else vertices)
    colors = _per_item(vertex_color, vs, _VERTEX_COLOR)
    return ax.scatter(
        [pos[v][0] for v in vs],
        [pos[v][1] for v in vs],
        s=vertex_size,
        c=colors,
        marker=vertex_shape,
        edgecolors=border_color,
        linewidths=border_width,
        cmap=cmap,
        vmin=vmin,
        vmax=vmax,
        alpha=alpha,
        zorder=2,
    )


def draw_edges(
    graph,
    pos=None,
    ax=None,
    *,
    edges=None,
    edge_color=_EDGE_COLOR,
    edge_cmap=None,
    edge_vmin=None,
    edge_vmax=None,
    edge_width=1.0,
    edge_style="solid",
    arrows=None,
    arrow_size=12,
    vertex_size=300,
    alpha=None,
):
    """Draws the edges of ``graph`` as straight lines, or as arrows if the graph is directed.

    A self-loop is drawn as a ring around its vertex. When a directed graph has edges in both
    directions between two vertices, they are drawn as two curves.

    :param graph: a :class:`~jgrapht.Graph` or :class:`~jgrapht.SparseGraph`.
    :param pos: a dict from vertex to ``(x, y)``, by default a Fruchterman-Reingold layout.
    :param ax: the matplotlib ``Axes`` to draw on, by default the current one.
    :param edges: the edges to draw, by default all of them.
    :param edge_color: a color, a list of colors, a dict from edge to color, or a function of the
        edge. If the colors are numbers, ``edge_cmap`` maps them to colors.
    :param edge_cmap: a matplotlib colormap for numeric edge colors, by default ``viridis``.
    :param edge_vmin: the number that gets the lowest color of the colormap, by default the smallest.
    :param edge_vmax: the number that gets the highest color of the colormap, by default the largest.
    :param edge_width: the line width in points.
    :param edge_style: the line style: ``"solid"``, ``"dashed"``, ``"dotted"`` or ``"dashdot"``.
    :param arrows: whether to draw arrow heads, by default ``True`` for a directed graph.
    :param arrow_size: the size of the arrow heads.
    :param vertex_size: the ``vertex_size`` the vertices were drawn with, so that the edges stop at
        the marker border.
    :param alpha: the transparency, between 0 and 1.
    :returns: the list of matplotlib artists that were added.
    """
    _matplotlib()
    from matplotlib.collections import LineCollection
    from matplotlib.patches import FancyArrowPatch

    ax = _axes(ax)
    pos = _positions(graph, pos)
    es = list(graph.edges() if edges is None else edges)
    if arrows is None:
        arrows = graph.directed
    colors = _per_item(edge_color, es, _EDGE_COLOR)
    if not isinstance(colors, list):
        colors = [colors] * len(es)
    colors = list(_map_numbers(colors, edge_cmap, edge_vmin, edge_vmax))

    ends = [(graph.edge_source(e), graph.edge_target(e)) for e in es]
    radius = math.sqrt(vertex_size) / 2.0
    artists = []
    segments, segment_colors, loops = [], [], []
    present = set(ends)
    for (u, v), color in zip(ends, colors):
        if u == v:
            loops.append((u, color))
        elif not arrows:
            segments.append((tuple(pos[u]), tuple(pos[v])))
            segment_colors.append(color)
        else:
            curved = (v, u) in present
            patch = FancyArrowPatch(
                tuple(pos[u]),
                tuple(pos[v]),
                arrowstyle="-|>",
                mutation_scale=arrow_size,
                shrinkA=radius,
                shrinkB=radius,
                connectionstyle="arc3,rad=0.2" if curved else "arc3,rad=0",
                color=color,
                linewidth=edge_width,
                linestyle=edge_style,
                alpha=alpha,
                zorder=1,
            )
            ax.add_patch(patch)
            artists.append(patch)
    if segments:
        collection = LineCollection(
            segments,
            colors=segment_colors,
            linewidths=edge_width,
            linestyles=edge_style,
            alpha=alpha,
            zorder=1,
        )
        ax.add_collection(collection)
        artists.append(collection)
    if loops:
        rings = ax.scatter(
            [pos[u][0] for u, _ in loops],
            [pos[u][1] for u, _ in loops],
            s=vertex_size * 2.5,
            facecolors="none",
            edgecolors=[c for _, c in loops],
            linewidths=edge_width,
            alpha=alpha,
            zorder=1,
        )
        artists.append(rings)
    ax.autoscale_view()
    return artists


def draw_vertex_labels(
    graph,
    pos=None,
    ax=None,
    *,
    labels=None,
    vertices=None,
    font_size=10,
    font_color="black",
):
    """Writes a label at each vertex.

    :param graph: a :class:`~jgrapht.Graph` or :class:`~jgrapht.SparseGraph`.
    :param pos: a dict from vertex to ``(x, y)``, by default a Fruchterman-Reingold layout.
    :param ax: the matplotlib ``Axes`` to draw on, by default the current one.
    :param labels: a dict from vertex to text (vertices missing from it get no label), or a
        function of the vertex. By default the label is ``str(vertex)``.
    :param vertices: the vertices to label, by default all of them.
    :param font_size: the font size in points.
    :param font_color: the text color.
    :returns: a dict from vertex to the matplotlib ``Text``.
    """
    ax = _axes(ax)
    pos = _positions(graph, pos)
    out = {}
    for v in graph.vertices() if vertices is None else vertices:
        text = _label_text(labels, v, str(v))
        if text is None:
            continue
        out[v] = ax.text(
            pos[v][0],
            pos[v][1],
            str(text),
            ha="center",
            va="center",
            fontsize=font_size,
            color=font_color,
            zorder=3,
        )
    return out


def draw_edge_labels(
    graph,
    pos=None,
    ax=None,
    *,
    labels=None,
    edges=None,
    label_position=0.5,
    font_size=8,
    font_color="black",
):
    """Writes a label on each edge.

    :param graph: a :class:`~jgrapht.Graph` or :class:`~jgrapht.SparseGraph`.
    :param pos: a dict from vertex to ``(x, y)``, by default a Fruchterman-Reingold layout.
    :param ax: the matplotlib ``Axes`` to draw on, by default the current one.
    :param labels: a dict from edge to text (edges missing from it get no label), or a function of
        the edge. By default the label is the edge weight if the graph is weighted, else
        ``str(edge)``.
    :param edges: the edges to label, by default all of them.
    :param label_position: where the label sits along the edge, from 0 (source) to 1 (target).
    :param font_size: the font size in points.
    :param font_color: the text color.
    :returns: a dict from edge to the matplotlib ``Text``.
    """
    ax = _axes(ax)
    pos = _positions(graph, pos)
    out = {}
    for e in graph.edges() if edges is None else edges:
        default = graph.edge_weight(e) if graph.weighted else e
        text = _label_text(labels, e, default)
        if text is None:
            continue
        u, v = graph.edge_source(e), graph.edge_target(e)
        (x1, y1), (x2, y2) = pos[u], pos[v]
        t = label_position
        # the label of a self-loop sits above its vertex, clear of the vertex label
        offset = (0, 3 * font_size) if u == v else (0, 0)
        out[e] = ax.annotate(
            str(text),
            (x1 + t * (x2 - x1), y1 + t * (y2 - y1)),
            xytext=offset,
            textcoords="offset points",
            ha="center",
            va="center",
            fontsize=font_size,
            color=font_color,
            bbox={"boxstyle": "round,pad=0.15", "fc": "white", "ec": "none", "alpha": 0.8},
            zorder=3,
        )
    return out


def draw(
    graph,
    pos=None,
    ax=None,
    *,
    labels=True,
    edge_labels=False,
    vertex_size=300,
    vertex_color=_VERTEX_COLOR,
    edge_color=_EDGE_COLOR,
    edge_width=1.0,
    arrows=None,
    font_size=10,
    font_color="black",
):
    """Draws ``graph``: its edges, its vertices and, optionally, labels.

    This is a shortcut for :func:`draw_edges`, :func:`draw_vertices`, :func:`draw_vertex_labels`
    and :func:`draw_edge_labels`; use those for finer control.

    :param graph: a :class:`~jgrapht.Graph` or :class:`~jgrapht.SparseGraph`.
    :param pos: a dict from vertex to ``(x, y)``, such as the result of a layout function. By
        default a Fruchterman-Reingold layout with a fixed seed.
    :param ax: the matplotlib ``Axes`` to draw on, by default the current one.
    :param labels: ``True`` to label vertices with ``str(vertex)``, ``False`` for no labels, or a
        dict or function giving the text.
    :param edge_labels: ``False`` for no edge labels, ``True`` to label edges with their weight
        (or ``str(edge)`` if unweighted), or a dict or function giving the text.
    :param vertex_size: the marker area in points squared.
    :param vertex_color: a color, a list of colors, a dict from vertex to color, or a function.
    :param edge_color: a color, a list of colors, a dict from edge to color, or a function.
    :param edge_width: the line width in points.
    :param arrows: whether to draw arrow heads, by default ``True`` for a directed graph.
    :param font_size: the label font size in points.
    :param font_color: the label color.
    :returns: the matplotlib ``Axes`` that was drawn on.
    """
    ax = _axes(ax)
    pos = _positions(graph, pos)
    draw_edges(
        graph,
        pos,
        ax,
        edge_color=edge_color,
        edge_width=edge_width,
        arrows=arrows,
        vertex_size=vertex_size,
    )
    draw_vertices(graph, pos, ax, vertex_size=vertex_size, vertex_color=vertex_color)
    if labels is not False:
        draw_vertex_labels(
            graph, pos, ax, labels=labels, font_size=font_size, font_color=font_color
        )
    if edge_labels is not False:
        draw_edge_labels(graph, pos, ax, labels=edge_labels, font_size=font_size * 0.8)
    ax.margins(0.1)
    ax.set_axis_off()
    return ax
