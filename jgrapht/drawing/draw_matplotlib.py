from ..algorithms.drawing import (
    circular_layout_2d,
    random_layout_2d,
    fruchterman_reingold_layout_2d,
    fruchterman_reingold_indexed_layout_2d,
)


def draw(g, positions=None, ax=None, **kwds):
    """Draw a graph using Matplotlib.

    Draws the graph as a simple representation with no vertex labels or edge labels
    and using the full Matplotlib figure area and no axis labels by default.
    See draw_jgrapht() for more full-featured drawing that allows title, axis labels etc.

    :param g: graph
    :type g: :py:class:`.Graph`
    :param positions: vertices positions
    :type positions: dict, optional
    :param kwargs: additional arguments to pass through
    :type kwargs: dict
    :param ax: draw the graph in the specified Matplotlib axes
    :type ax: Matplotlib Axes object, optional

    Examples
    --------
    >>> import matplotlib.pyplot as plt
    >>> g = jgrapht.create_graph(directed=False, weighted=True)
    >>> for i in range(0,5):g.add_vertex()
    >>> e1 = g.add_edge(0, 1)
    >>> e2 = g.add_edge(0, 2)
    >>> e3 = g.add_edge(0, 3)
    >>> e4 = g.add_edge(0, 4)
    >>> drawing.draw(g, positions=drawing.layout(g, name="random"))
    >>> plt.show()

    See Also
    --------
    draw_jgrapht()
    draw_jgrapht_vertices()
    draw_jgrapht_edges()
    draw_jgrapht_vertex_labels()
    draw_jgrapht_edge_labels()
    """
    try:
        import matplotlib.pyplot as plt
    except ImportError as e:
        raise ImportError("Matplotlib required for draw()") from e
    except RuntimeError:
        print("Matplotlib unable to open display")
        raise

    cf = plt.gcf() if ax is None else ax.get_figure()
    cf.set_facecolor("w")

    if ax is None:
        if cf._axstack() is None:
            ax = cf.add_axes((0, 0, 1, 1))
        else:
            ax = cf.gca()

    if positions is None:
        positions = layout(g)

    draw_jgrapht(g, positions=positions, ax=ax, **kwds)
    ax.set_axis_off()
    plt.draw_if_interactive()


def draw_jgrapht(
    g, positions=None, vertex_labels=None, edge_labels=None, axis=True, **kwargs
):
    """Draw the graph g using Matplotlib.

    Draw the graph with Matplotlib with options for vertex positions, labels, titles, and many
    other drawing features. See draw() for simple drawing without labels or axes.

    :param g: graph
    :type g: :py:class:`.Graph`
    :param positions: vertices positions
    :type positions: dict, optional
    :param axis: Draw the axes
    :type axis: bool, optional (default=True)
    :param vertex_labels: vertex labels
    :type vertex_labels: dict, optional (default=None)
    :param edge_labels: edge labels
    :type edge_labels: dict, optional (default=None)
    :param kwargs: additional arguments to pass through
    :type kwargs: dict

    Examples
    --------
    >>> import matplotlib.pyplot as plt
    >>> g = jgrapht.create_graph(directed=False)
    >>> for i in range(0,5):g.add_vertex()
    >>> e1 = g.add_edge(0, 1)
    >>> e2 = g.add_edge(0, 2)
    >>> e3 = g.add_edge(0, 3)
    >>> e4 = g.add_edge(0, 4)
    >>> drawing.draw_jgrapht(g, positions=drawing.layout(g, name="random"))
    >>> plt.show()

    See Also
    --------
    draw()
    draw_jgrapht_vertices()
    draw_jgrapht_edges()
    draw_jgrapht_vertex_labels()
    draw_jgrapht_edge_labels()
    """
    try:
        import matplotlib.pyplot as plt
    except ImportError as e:
        raise ImportError("Matplotlib required for draw()") from e
    except RuntimeError:
        print("Matplotlib unable to open display")
        raise
    if positions is None:
        positions = layout(g, name=kwargs.get('name'))

    draw_jgrapht_vertices(g, positions=positions, axis=axis, **kwargs)

    draw_jgrapht_edges(
        g,
        positions=positions,
        edge_labels=edge_labels,
        axis=axis,
        **kwargs,
    )

    if vertex_labels is not None:
        draw_jgrapht_vertex_labels(
            g, positions=positions, labels=vertex_labels, axis=axis, **kwargs
        )

    if edge_labels is not None:
        draw_jgrapht_edge_labels(
            g, positions=positions, labels=edge_labels, axis=axis, **kwargs
        )

    plt.draw_if_interactive()


def draw_jgrapht_vertices(
    g,
    positions,
    vertex_list=None,
    axis=False,
    vertex_linewidths=1.0,
    vertex_title=None,
    vertex_size=450,
    vertex_color="green",
    vertex_cmap=None,
    vmin=None,
    vmax=None,
    vertex_shape="o",
    vertex_edge_color="face",
    alpha=1,
    ax=None,
    **kwargs
):
    """Draw only the vertices of the graph g.

    :param g: graph
    :type g: :py:class:`.Graph`
    :param positions: vertices positions
    :type positions: dict, optional
    :param vertex_list: Draw only the vertices in this list
    :type vertex_list: list, optional (default: vertex_list=None)
    :param axis: Draw the axes
    :type axis: bool, optional (default=False)
    :param vertex_linewidths: Line width of symbol border
    :type vertex_linewidths: float,(default:1.0)
    :param vertex_title: Label for graph legend
    :type vertex_title: list, optional  (default:None)
    :param vertex_size: Size of vertices
    :type vertex_size: scalar or array, optional (default=450)
    :param vertex_color: vertex color
    :type vertex_color: color or array of colors (default='green')
    :param vertex_cmap: Colormap for mapping intensities of vertices
    :type vertex_cmap: Matplotlib colormap, optional (default=None | example:vertex_cmap=plt.cm.Greens)
    :param vmin: Minimum for vertex colormap scaling
    :type vmin: float, optional (default=None)
    :param vmax: Maximum for vertex colormap scaling positions
    :type vmax: float, optional (default=None)
    :param vertex_shape: The shape of the vertex
    :type vertex_shape: string, optional (default='o')
    :param vertex_edge_color: color the edge of vertex
    :type vertex_edge_color: string, optional (default='face')
    :param alpha: The vertex transparency
    :type alpha: float, optional (default=1.0)
    :param ax: Draw the graph in the specified Matplotlib axes
    :type ax: Matplotlib Axes object, optional
    :param kwargs: Additional arguments to pass through
    :type kwargs: dict

    Examples
    --------
    >>> import matplotlib.pyplot as plt
    >>> g = jgrapht.create_graph(directed=False)
    >>> for i in range(0,5):g.add_vertex()
    >>> e1 = g.add_edge(0, 1)
    >>> e2 = g.add_edge(0, 2)
    >>> e3 = g.add_edge(0, 3)
    >>> e4 = g.add_edge(0, 4)
    >>> drawing.draw_jgrapht_vertices(g, positions=drawing.layout(g, name="random"))
    >>> plt.show()

    See Also
    --------
    draw()
    draw_jgrapht()
    draw_jgrapht_edges()
    draw_jgrapht_vertex_labels()
    draw_jgrapht_edge_labels()
    """
    try:
        import matplotlib.pyplot as plt
    except ImportError as e:
        raise ImportError("Matplotlib required for draw()") from e
    except RuntimeError:
        print("Matplotlib unable to open display")
        raise

    if ax is None:
        ax = plt.gca()

    # Hide axis values
    ax.get_yaxis().set_visible(False)
    ax.get_xaxis().set_visible(False)

    if axis is False:
        ax.set_axis_off()

    if vertex_list is not None:
        x, y = zip(*[positions[v] for v in vertex_list])
    else:
        x, y = zip(*positions.values())

    # Draw vertices
    ax.scatter(
        x,
        y,
        c=vertex_color,
        alpha=alpha,
        linewidth=vertex_linewidths,
        s=vertex_size,
        cmap=vertex_cmap,
        vmin=vmin,
        vmax=vmax,
        marker=vertex_shape,
        edgecolors=vertex_edge_color,
        zorder=2.5,
        label=vertex_title,
    )

    if vertex_title is not None:
        # Draw legend for the vertices
        handles, labels = ax.get_legend_handles_labels()
        unique = [
            (h, l)
            for i, (h, l) in enumerate(zip(handles, labels))
            if l not in labels[:i]
        ]
        ax.legend(
            *zip(*unique),
            loc="upper center",
            fancybox=True,
            framealpha=1,
            shadow=True,
            borderpad=0.3,
            markerscale=0.5,
            markerfirst=True,
            ncol=3,
            bbox_to_anchor=(0.5, 1.15),
        )


def draw_jgrapht_edges(
    g,
    positions,
    edge_list=None,
    edge_labels=False,
    edge_title=None,
    edge_color="black",
    edge_cmap=None,
    edge_linewidth=1.3,
    line_style="solid",
    arrow_size=1,
    arrow_style="-|>",
    arrow_color="black",
    arrow_line="-",
    arrow_head=20,
    alpha=1,
    axis=False,
    connection_style=None,
    bbox=dict(boxstyle="round,pad=0.03", ec="white", fc="white"),
    ax=None,
    **kwargs
):
    """Draw the edges of the graph g.

    This draws only the edges of the graph g.

    :param g: graph
    :type g: :py:class:`.Graph`
    :param positions: vertices positions
    :type positions: dictionary, optional
    :param edge_list: Draw only specified edges
    :type edge_list: list, optional (default: edge_list=None)
    :param edge_color: Edge color
    :type edge_color: color or array of colors (default='black')
    :param edge_cmap: Colormap for mapping intensities of edges
    :type edge_cmap: list, optional (default:edge_cmap=None | example: edge_cmap =plt.cm.Greens(np.linspace(edge_vmin,edge_vmax,len(g.edges))))
    :param edge_linewidth: Line width of edges
    :type edge_linewidth: float, optional (default=1.3)
    :param line_style: Edge line style (solid|dashed|dotted|dashdot)
    :type line_style: string, optional (default='solid')
    :param arrow_size: size of arrow
    :type arrow_size: int, optional (default=1)
    :param arrow_style: choose the style of the arrowsheads.(Fancy|Simple|Wedge etc)
    :type arrow_style: str, optional (default='-|>')
    :param arrow_color: arrow color
    :type arrow_color: color or array of colors (default='black')
    :param arrow_line: Edge line style (solid|dashed|dotted|dashdot)
    :type arrow_line: string, optional (default='solid')
    :param arrow_head: size of arrowhead
    :type arrow_head: int, optional (default=20)
    :param alpha: edge transparency
    :type alpha: float, optional (default=1.0)
    :param axis: Draw the axes
    :type axis: bool, optional (default=False)
    :param edge_title: Label for graph legend
    :type edge_title: list, optional  (default:None)
    :param edge_labels: draw labels on the edges.
    :type edge_labels: bool, optional (default=False)
    :param connection_style: Pass the connection_style parameter to create curved arc of rounding radius rad
    :type connection_style: str, optional (default=None | example: connection_style="arc3,rad=-0.3")
    :param bbox: Matplotlib bbox,specify text box shape and colors.
    :type bbox: Matplotlib bbox
    :param ax: Draw the graph in the specified Matplotlib axes
    :type ax: Matplotlib Axes object, optional
    :param kwargs: additional arguments
    :type kwargs: dict

    Examples
    --------
    >>> import matplotlib.pyplot as plt
    >>> g = jgrapht.create_graph(directed=False)
    >>> for i in range(0,5):g.add_vertex()
    >>> e1 = g.add_edge(0, 1)
    >>> e2 = g.add_edge(0, 2)
    >>> e3 = g.add_edge(0, 3)
    >>> e4 = g.add_edge(0, 4)
    >>> drawing.draw_jgrapht_edges(g, positions=drawing.layout(g, name="random"))
    >>> plt.show()

    See Also
    --------
    draw()
    draw_jgrapht()
    draw_jgrapht_vertices()
    draw_jgrapht_vertex_labels()
    draw_jgrapht_edge_labels()
    -----
    """
    try:
        import matplotlib.pyplot as plt
        import numpy as np
        import matplotlib as mpl
        from matplotlib.patches import FancyArrowPatch
    except ImportError as e:
        raise ImportError("Matplotlib required for draw()") from e
    except RuntimeError:
        print("Matplotlib unable to open display")
        raise

    if len(g.edges) == 0:
        return

    if ax is None:
        ax = plt.gca()

    # Hide axis values
    ax.get_yaxis().set_visible(False)
    ax.get_xaxis().set_visible(False)

    if axis is False:
        ax.set_axis_off()

    if edge_cmap is not None:  # if the user wants color map for the edges
        plt.close()
        plt.rcParams["axes.prop_cycle"] = plt.cycler("color", edge_cmap)
        ax = plt.gca()
        edge_color = ""
        edge_cmap = None

    if edge_list is None:
        edge_list = g.edges

    # draw edges
    is_directed = g.type.directed
    for e in edge_list:
        v = g.edge_source(e)
        u = g.edge_target(e)
        x1, y1 = positions[v]
        x2, y2 = positions[u]

        if is_directed:
            a = FancyArrowPatch(
                (x1, y1),
                (x2, y2),
                arrowstyle=arrow_style,
                shrinkA=9.5,
                shrinkB=9.5,
                mutation_scale=arrow_head,
                alpha=alpha,
                ls=arrow_line,
                lw=arrow_size,
                connectionstyle=connection_style,
                color=arrow_color,
                label=edge_title,
            )
            ax.add_patch(a)
            ax.autoscale_view()
        else:
            ax.plot(
                (x1, x2),
                (y1, y2),
                edge_color,
                alpha=alpha,
                linewidth=edge_linewidth,
                linestyle=line_style,
                label=edge_title,
            )

    if edge_title is not None:  # legend title
        handles, labels = ax.get_legend_handles_labels()
        unique = [
            (h, l)
            for i, (h, l) in enumerate(zip(handles, labels))
            if l not in labels[:i]
        ]
        ax.legend(
            *zip(*unique),
            loc="upper center",
            fancybox=True,
            framealpha=1,
            shadow=True,
            borderpad=0.3,
            markerscale=0.5,
            markerfirst=True,
            ncol=3,
            bbox_to_anchor=(0.5, 1.15),
        )


def draw_jgrapht_vertex_labels(
    g,
    positions,
    labels=None,
    vertex_fontsize=12,
    vertex_font_color="black",
    vertex_font_weight="normal",
    vertex_font_family="sans-serif",
    horizontalalignment="center",
    verticalalignment="center",
    alpha=1,
    axis=False,
    bbox=dict(boxstyle="round,pad=0.03", ec="white", fc="white"),
    ax=None,
    **kwargs
):
    """Draw only the vertex labels on the graph g.

    If no labels are provided then this method uses the string representation of the vertices. 
    If the parameter labels is a dictionary, then only labels for the contained vertices are drawn.
    If labels is a list then labels for all vertices must be provided.

    :param g: graph
    :type g: :py:class:`.Graph`
    :param positions: vertices positions
    :type positions: dict
    :param labels: vertices labels
    :type labels: dict or list, optional
    :param vertex_fontsize: Font size for text labels
    :type vertex_fontsize: int, optional (default=12)
    :param vertex_font_color: Font color string
    :type vertex_font_color: string, optional (default='black')
    :param vertex_font_weight: Font weight ( 'normal' | 'bold' | 'heavy' | 'light' | 'ultralight')
    :type vertex_font_weight: string, optional (default='normal')
    :param vertex_font_family: Font family ('cursive', 'fantasy', 'monospace', 'sans', 'sans serif', 'sans-serif', 'serif')
    :type vertex_font_family: string, optional (default='sans-serif')
    :param verticalalignment: Vertical alignment (default='center')
    :type verticalalignment: {'center', 'top', 'bottom', 'baseline', 'center_baseline'}
    :param horizontalalignment: Horizontal alignment (default='center')
    :type horizontalalignment: {'center', 'right', 'left'}
    :param alpha: label transparency
    :type alpha: float, optional (default=1.0)
    :param axis: Draw the axes
    :type axis: bool, optional (default=False)
    :param ax: Draw the graph in the specified Matplotlib axes
    :type ax: Matplotlib Axes object, optional
    :param bbox: Matplotlib bbox,specify text box shape and colors.
    :param kwargs: additional arguments
    :type kwargs: dict

    Examples
    --------
    >>> import matplotlib.pyplot as plt
    >>> g = jgrapht.create_graph(directed=False, weighted=True)
    >>> for i in range(0,5):g.add_vertex()
    >>> e1 = g.add_edge(0, 1)
    >>> e2 = g.add_edge(0, 2)
    >>> e3 = g.add_edge(0, 3)
    >>> e4 = g.add_edge(0, 4)
    >>> drawing.draw_jgrapht_vertex_labels(g, positions=drawing.layout(g, name="random"))
    >>> plt.show()

    See Also
    --------
    draw()
    draw_jgrapht()
    draw_jgrapht_vertices()
    draw_jgrapht_edges()
    draw_jgrapht_edge_labels()
    """
    try:
        import matplotlib.pyplot as plt
    except ImportError as e:
        raise ImportError("Matplotlib required for draw()") from e
    except RuntimeError:
        print("Matplotlib unable to open display")
        raise

    if ax is None:
        ax = plt.gca()

    # Hide axis values
    ax.get_yaxis().set_visible(False)
    ax.get_xaxis().set_visible(False)

    if not axis:
        ax.set_axis_off()

    if labels is None:
        labels = {}
        for v in g.vertices:
            labels.update({v: str(v)})

    try:
        vertices_and_labels = labels.items()
    except (AttributeError, KeyError):
        vertices_and_labels = zip(g.vertices, labels)        

    # Draw the labels
    for v, label in vertices_and_labels:
        x, y = positions[v]
        ax.text(
            x,
            y,
            label,
            fontsize=vertex_fontsize,
            horizontalalignment=horizontalalignment,
            verticalalignment=verticalalignment,
            alpha=alpha,
            color=vertex_font_color,
            weight=vertex_font_weight,
            family=vertex_font_family,
            transform=ax.transData,
        )
        ax.plot(x, y)


def draw_jgrapht_edge_labels(
    g,
    positions,
    labels=None,
    draw_edge_weights=False,
    edge_weight_format="{:.2f}",
    horizontalalignment="center",
    verticalalignment="center",
    edge_fontsize=12,
    edge_font_color="black",
    edge_font_weight="normal",
    edge_font_family="sans-serif",
    alpha=1,
    axis=False,
    bbox=dict(boxstyle="round,pad=0.03", ec="white", fc="white"),
    ax=None,
    **kwargs
):
    """Draw only the edge labels on the graph g.

    If no labels are provided then this method uses the string representation of the edges or the 
    weight if explicitly requested by the parameters. 
    If the parameter labels is a dictionary, then only labels for the contained edges are drawn.
    If labels is a list then labels for all edges must be provided.

    :param g: graph
    :type g: :py:class:`.Graph`
    :param positions: vertices positions
    :type positions: dict
    :param labels: edge labels
    :type labels: dict, optional
    :param draw_edge_weights: whether to use edge weights as edge labels
    :type draw_edge_weights: bool, optional (default=False)
    :param edge_weight_format: format for the edge weights
    :type edge_weight_format: str, optional (default=2 decimal points)
    :param edge_fontsize: Font size for text labels
    :type edge_fontsize: int, optional (default=12)
    :param edge_font_color: Font color string
    :type edge_font_color: str, optional (default='black')
    :param edge_font_weight: Font weight ( 'normal' | 'bold' | 'heavy' | 'light' | 'ultralight')
    :type edge_font_weight: str, optional (default='normal')
    :param edge_font_family: Font family ('cursive', 'fantasy', 'monospace', 'sans', 'sans serif', 'sans-serif', 'serif')
    :type edge_font_family: str, optional (default='sans-serif')
    :param verticalalignment: Vertical alignment (default='center')
    :type verticalalignment: {'center', 'top', 'bottom', 'baseline', 'center_baseline'}
    :param horizontalalignment: Horizontal alignment (default='center')
    :type horizontalalignment: {'center', 'right', 'left'}
    :param alpha: label transparency
    :type alpha: float, optional (default=1.0)
    :param bbox: Matplotlib bbox, specify text box shape and colors.
    :type bbox: Matplotlib bbox
    :param ax: Draw the graph in the specified Matplotlib axes
    :type ax: Matplotlib Axes object, optional
    :param axis: Draw the axes
    :type axis: bool, optional (default=False)
    :param kwargs: See draw_jgrapht
    :type kwargs: dict

    Examples
    --------
    >>> import matplotlib.pyplot as plt
    >>> g = jgrapht.create_graph(directed=False, weighted=True)
    >>> for i in range(0,5):g.add_vertex()
    >>> e1 = g.add_edge(0, 1)
    >>> e2 = g.add_edge(0, 2)
    >>> e3 = g.add_edge(0, 3)
    >>> e4 = g.add_edge(0, 4)
    >>> drawing.draw_jgrapht_edge_labels(g, position=drawing.layout(g, name="random"))
    >>> plt.show()
    See Also
    --------
    draw()
    draw_jgrapht()
    draw_jgrapht_vertices()
    draw_jgrapht_edges()
    draw_jgrapht_vertex_labels()
    --------
    """
    try:
        import matplotlib.pyplot as plt
    except ImportError as e:
        raise ImportError("Matplotlib required for draw()") from e
    except RuntimeError:
        print("Matplotlib unable to open display")
        raise

    if len(g.edges) == 0:
        return

    if ax is None:
        ax = plt.gca()

    # Hide axis values
    ax.get_yaxis().set_visible(False)
    ax.get_xaxis().set_visible(False)

    if not axis:
        ax.set_axis_off()

    if labels is None:
        labels = {}
        if draw_edge_weights:
            for e in g.edges:
                weight = edge_weight_format.format(g.get_edge_weight(e))
                labels.update({e: weight})
        else:
            for e in g.edges:
                labels.update({e: str(e)})

    try:
        edges_and_labels = labels.items()
    except (AttributeError, KeyError):
        edges_and_labels = zip(g.edges, labels)

    # Draw the labels
    for e, label in edges_and_labels:
        v = g.edge_source(e)
        u = g.edge_target(e)
        x1, y1 = positions[v]
        x2, y2 = positions[u]

        ax.text(
            (x1 + x2) / 2,
            (y1 + y2) / 2,
            label,
            fontsize=edge_fontsize,
            horizontalalignment=horizontalalignment,
            verticalalignment=verticalalignment,
            alpha=alpha,
            color=edge_font_color,
            weight=edge_font_weight,
            family=edge_font_family,
            transform=ax.transData,
            bbox=bbox,
            zorder=2,
        )
        ax.plot((x1 + x2) / 2, (y1 + y2) / 2)


def layout(g, name=None, area=(0, 0, 10, 10), **kwargs):
    """Compute the positions of vertices for a particular layout.

    :param g: the graph to draw
    :type g: :py:class:`.Graph`
    :param name: circular|random|fruchterman_reingold|fruchterman_reingold_indexed
    :type name: str
    :param area: the two dimensional area as a tuple (minx, miny, width, height)
    :type area: tuple
    :param kwargs: additional arguments passed through
    :type kwargs: dict
    :returns: vertex positions
    :rtype: dict

    Examples
    --------
    >>> import matplotlib.pyplot as plt
    >>> g = jgrapht.create_graph(directed=False, weighted=True)
    >>> for i in range(0,5):g.add_vertex()
    >>> e1 = g.add_edge(0, 1)
    >>> e2 = g.add_edge(0, 2)
    >>> e3 = g.add_edge(0, 3)
    >>> e4 = g.add_edge(0, 4)
    >>> position = drawing.layout(g, seed=10, name="random")
    >>> drawing.draw_jgrapht(g, position=position)
    >>> plt.show()
    """
    if name == "random":
        alg = random_layout_2d
        args = {"seed": kwargs.get("seed")}
    elif name == "fruchterman_reingold":
        alg = fruchterman_reingold_layout_2d
        args = {
            "iterations": kwargs.get("iterations", 100),
            "normalization_factor": kwargs.get("normalization_factor", 0.5),
            "seed": kwargs.get("seed"),
        }
    elif name == "fruchterman_reingold_indexed":
        alg = fruchterman_reingold_indexed_layout_2d
        args = {
            "iterations": kwargs.get("iterations", 100),
            "normalization_factor": kwargs.get("normalization_factor", 0.5),
            "seed": kwargs.get("seed"),
            "theta": kwargs.get("theta", 0.5),
            "tolerance": kwargs.get("tolerance"),
        }
    else:
        alg = circular_layout_2d
        args = {
            "radius": kwargs.get("radius", 5),
            "vertex_comparator_cb": kwargs.get("vertex_comparator_cb", None),
        }

    result = alg(g, area, **args)
    positions = {}
    for i, vertex in enumerate(g.vertices):
        x, y = result.get_vertex_location(i)
        positions[vertex] = (x, y)

    return positions


def draw_circular(
    g, area=(0, 0, 10, 10), radius=5, vertex_comparator_cb=None, axis=True, **kwargs
):
    """Draw the graph g with a circular layout

    :param g: graph
    :type g: :py:class:`.Graph`
    :param area: the two dimensional area as a tuple (minx, miny, width, height)
    :type area: tuple
    :param axis: whether to draw the axes
    :type axis: bool, optional (default=True)
    :param radius: radius of the circle
    :type radius: double
    :param vertex_comparator_cb: a vertex comparator. Should be a function which accepts two vertices
           v1, v2 and returns -1, 0, 1 depending of whether v1 < v2, v1 == v2, or v1 > v2 in the ordering
    :type vertex_comparator_cb: function
    :param kwargs: additional arguments passed through
    :type kwargs: dict
    :returns: vertex positions
    :rtype: dict

    Examples
    --------
    >>> import matplotlib.pyplot as plt
    >>> g = jgrapht.create_graph(directed=False, weighted=True)
    >>> for i in range(0,5):g.add_vertex()
    >>> e1 = g.add_edge(0, 1)
    >>> e2 = g.add_edge(0, 2)
    >>> e3 = g.add_edge(0, 3)
    >>> e4 = g.add_edge(0, 4)
    >>> drawing.draw_circular(g)
    >>> plt.show()
    """
    draw_jgrapht(
        g,
        positions=layout(
            g,
            area=area,
            name="circular",
            radius=radius,
            vertex_comparator_cb=vertex_comparator_cb,
        ),
        axis=axis,
        **kwargs,
    )


def draw_random(g, area=(0, 0, 10, 10), seed=None, axis=True, **kwargs):
    """Draw the graph g with a random layout.

    :param g: graph
    :type g: :py:class:`.Graph`
    :param area: the two dimensional area as a tuple (minx, miny, width, height)
    :type area: tuple
    :param seed: seed for the random number generator. If None the system time is used
    :type seed: integer
    :param axis: whether to draw the axes
    :type axis: bool, optional (default=True)
    :param kwargs: additional arguments passed through
    :type kwargs: dict
    :returns: vertex positions
    :rtype: dict

    Examples
    --------
    >>> import matplotlib.pyplot as plt
    >>> g = jgrapht.create_graph(directed=False, weighted=True)
    >>> for i in range(0,5):g.add_vertex()
    >>> e1 = g.add_edge(0, 1)
    >>> e2 = g.add_edge(0, 2)
    >>> e3 = g.add_edge(0, 3)
    >>> e4 = g.add_edge(0, 4)
    >>> drawing.draw_random(g)
    >>> plt.show()
    """
    draw_jgrapht(
        g,
        positions=layout(g, area=area, name="random", seed=seed),
        axis=axis,
        **kwargs,
    )


def draw_fruchterman_reingold(
    g,
    area=(0, 0, 10, 10),
    iterations=100,
    normalization_factor=0.5,
    seed=None,
    theta=0.5,
    tolerance=None,
    indexed=False,
    axis=True,
    **kwargs
):
    """Draw the graph g with a Fruchterman-Reingold layout.

    :param g: graph
    :type g: :py:class:`.Graph`
    :param area: the two dimensional area as a tuple (minx, miny, width, height)
    :type area: tuple
    :param iterations: number of iterations
    :type iterations: int
    :param normalization_factor: normalization factor when calculating optimal distance
    :type normalization_factor: double
    :param seed: seed for the random number generator. If None the system time is used
    :type seed: integer
    :param theta: parameter for approximation using the Barnes-Hut technique
    :type theta: double
    :param indexed: whether to use the Barnes-Hut approximation
    :type indexed: bool, optional (default=False)
    :param axis: whether to draw the axes
    :type axis: bool, optional (default=True)
    :param tolerance: tolerance used when comparing floating point values
    :param kwargs: additional arguments passed through
    :type kwargs: dict
    :returns: vertex positions
    :rtype: dict

    Examples
    --------
    >>> import matplotlib.pyplot as plt
    >>> g = jgrapht.create_graph(directed=False, weighted=True)
    >>> for i in range(0,5):g.add_vertex()
    >>> e1 = g.add_edge(0, 1)
    >>> e2 = g.add_edge(0, 2)
    >>> e3 = g.add_edge(0, 3)
    >>> e4 = g.add_edge(0, 4)
    >>> drawing.draw_fruchterman_reingold(g)
    >>> plt.show()
    """
    extra_args = {
        "area": area,
        "name": "fruchterman_reingold",
        "iterations": iterations,
        "normalization_factor": normalization_factor,
        "seed": seed,
    }
    if indexed:
        extra_args.update(
            {
                "name": "fruchterman_reingold_indexed",
                "theta": theta,
                "tolerance": tolerance,
            }
        )

    draw_jgrapht(
        g,
        positions=layout(g, **extra_args),
        axis=axis,
        **kwargs,
    )
