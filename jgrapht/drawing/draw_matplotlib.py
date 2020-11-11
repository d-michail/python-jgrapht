from ..algorithms.drawing import (
    circular_layout_2d,
    random_layout_2d,
    fruchterman_reingold_layout_2d,
    fruchterman_reingold_indexed_layout_2d,
)


def draw(g, positions=None, ax=None, **kwds):
    """Draw a graph using Matplotlib.

    Draws the graph as a simple representation with no node labels or edge labels
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
    g,
    positions=None,
    node_labels=True,
    edge_labels=False,
    axis=True,
    **kwargs
):
    """Draw the graph g using Matplotlib.

    Draw the graph with Matplotlib with options for node positions, labeling, titles, and many
    other drawing features. See draw() for simple drawing without labels or axes.

    :param g: graph
    :type g: :py:class:`.Graph`
    :param positions: vertices positions
    :type positions: dict, optional
    :param axis: Draw the axes
    :type axis: bool, optional (default=True)
    :param node_labels: whether to draw node labels
    :type node_labels: bool, optional (default=False)
    :param positions: vertices positions
    :param edge_labels: whether to draw edge labels
    :type edge_labels: bool, optional (default=False)
    :param kwargs: additional arguments to pass through
    :type kwargs: optional keywords

    Examples
    --------
    >>> import matplotlib.pyplot as plt
    >>> g = jgrapht.create_graph(directed=False, weighted=True)
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
        positions = layout(g)

    draw_jgrapht_vertices(
        g, positions=positions, node_labels=node_labels, axis=axis, show=0, **kwargs
    )

    draw_jgrapht_edges(
        g,
        positions=positions,
        edge_labels=edge_labels,
        node_labels=node_labels,
        axis=axis,
        show=0,
        **kwargs,
    )

    if node_labels:
        draw_jgrapht_vertex_labels(g, positions=positions, axis=axis, **kwargs)

    if edge_labels:
        draw_jgrapht_edge_labels(g, positions=positions, axis=axis, **kwargs)

    plt.draw_if_interactive()


def draw_jgrapht_vertices(
    g,
    positions,
    axis=False,
    node_linewidths=1.0,
    node_title=None,
    node_size=450,
    node_color="green",
    node_cmap=None,
    vmin=None,
    vmax=None,
    node_shape="o",
    node_edge_color="face",
    node_list=None,
    alpha=1,
    node_labels=False,
    ax=None,
    **kwargs
):
    """Draw the nodes of the graph g.

    This method draws only the nodes of the graph g.

    :param g: graph
    :type g: :py:class:`.Graph`
    :param positions: vertices positions
    :type positions: dict, optional
    :param axis: Draw the axes
    :type axis: bool, optional (default=False)
    :param node_linewidths: Line width of symbol border
    :type node_linewidths: float,(default:1.0)
    :param node_title: Label for graph legend
    :type node_title: list, optional  (default:None)
    :param node_size: Size of nodes
    :type node_size: scalar or array, optional (default=500)
    :param node_color: Node color
    :type node_color: color or array of colors (default='green')
    :param node_cmap: Colormap for mapping intensities of nodes
    :type node_cmap: Matplotlib colormap, optional (default=None | example:node_cmap=plt.cm.Greens)
    :param vmin: Minimum for node colormap scaling
    :type vmin: float, optional (default=None)
    :param vmax: Maximum for node colormap scaling positions
    :type vmax: float, optional (default=None)
    :param node_shape: The shape of the node
    :type node_shape: string, optional (default='o')
    :param node_edge_color: color the edge of node
    :type node_edge_color: string, optional (default='face')
    :param node_list: Draw only the nodes in this list
    :type node_list: list, optional (default: node_list=None)
    :param node_labels: whether to draw node labels
    :type node_labels: bool, optional (default=False)
    :param alpha: The node transparency
    :type alpha: float, optional (default=1.0)
    :param ax: Draw the graph in the specified Matplotlib axes
    :type ax: Matplotlib Axes object, optional
    :param kwargs: Additional arguments to pass through
    :type kwargs: optional keywords

    Examples
    --------
    >>> import matplotlib.pyplot as plt
    >>> g = jgrapht.create_graph(directed=False, weighted=True)
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

    if node_list is not None:
        x, y = zip(*[positions[v] for v in node_list])
    else:
        x, y = zip(*positions.values())

    # Draw nodes
    ax.scatter(
        x,
        y,
        c=node_color,
        alpha=alpha,
        linewidth=node_linewidths,
        s=node_size,
        cmap=node_cmap,
        vmin=vmin,
        vmax=vmax,
        marker=node_shape,
        edgecolors=node_edge_color,
        zorder=2.5,
        label=node_title,
    )

    if node_title is not None:
        # Draw Legend graph for the nodes
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

    show = kwargs.get("show")  # check if the user called only the function of nodes
    if show is None and node_labels is True:
        draw_jgrapht_vertex_labels(g, positions, axis=axis, **kwargs)


def draw_jgrapht_edges(
    g,
    positions,
    edge_list=None,
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
    edge_title=None,
    edge_labels=False,
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
    >>> g = jgrapht.create_graph(directed=False, weighted=True)
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

    show = kwargs.get("show")  # check if the user called only the function of edges

    if edge_cmap is not None:  # if the user wants color map for the edges
        plt.close()
        plt.rcParams["axes.prop_cycle"] = plt.cycler("color", edge_cmap)
        ax = plt.gca()
        if show is None:  # if  the user called only this function
            draw_jgrapht_edges(
                g,
                positions=positions,
                edge_labels=edge_labels,
                edge_cmap=None,
                edge_color="",
                edge_linewidth=edge_linewidth,
                line_style=line_style,
                arrow_size=arrow_size,
                arrows_tyle=arrow_style,
                arrow_color=arrow_color,
                edge_list=edge_list,
                alpha=alpha,
                axis=axis,
                edge_title=edge_title,
                connection_style=connection_style,
                bbox=bbox,
                ax=ax,
                arrow_head=arrow_head,
                arrow_line=arrow_line,
                **kwargs,
            )
        else:
            kwargs.pop("show")  # delete from kwargs the parameter show
            draw_jgrapht(
                g,
                positions=positions,
                edge_cmap=None,
                edge_color="",
                edge_linewidth=edge_linewidth,
                edge_list=edge_list,
                line_style=line_style,
                arrow_size=arrow_size,
                arrow_style=arrow_style,
                arrow_color=arrow_color,
                alpha=alpha,
                axis=axis,
                ax=ax,
                edge_title=edge_title,
                connection_style=connection_style,
                edge_labels=edge_labels,
                bbox=bbox,
                arrow_head=arrow_head,
                arrow_line=arrow_line,
                **kwargs,
            )
        return

    if edge_list is None: 
        edge_list = g.edges

    for e in edge_list:
        v = g.edge_source(e)
        u = g.edge_target(e)
        x1, y1 = positions[v]
        x2, y2 = positions[u]

        if g.type.directed:  # Draw  arrows
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
            # Draw  edges
            ax.plot(
                (x1, x2),
                (y1, y2),
                edge_color,
                alpha=alpha,
                linewidth=edge_linewidth,
                linestyle=line_style,
                label=edge_title,
            )

    if edge_title is not None:  # legend title for the specific edges
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

    if show is None and edge_labels:
        draw_jgrapht_edge_labels(g, positions, axis=axis, **kwargs)


def draw_jgrapht_vertex_labels(
    g,
    positions,
    labels=None,
    node_fontsize=12,
    node_font_color="black",
    node_font_weight="normal",
    node_font_family="sans-serif",
    horizontalalignment="center",
    verticalalignment="center",
    alpha=1,
    axis=False,
    bbox=dict(boxstyle="round,pad=0.03", ec="white", fc="white"),
    ax=None,
    **kwargs
):
    """Draw node labels on the graph g.

    This method draws only the nodes labels of the graph g.

    :param g: graph
    :type g: :py:class:`.Graph`            
    :param positions: vertices positions
    :type positions: dict
    :param labels: vertices labels
    :type labels: dict, optional
    :param node_fontsize: Font size for text labels
    :type node_fontsize: int, optional (default=12)
    :param node_font_color: Font color string
    :type node_font_color: string, optional (default='black')
    :param node_font_weight: Font weight ( 'normal' | 'bold' | 'heavy' | 'light' | 'ultralight')
    :type node_font_weight: string, optional (default='normal')
    :param node_font_family: Font family ('cursive', 'fantasy', 'monospace', 'sans', 'sans serif', 'sans-serif', 'serif')
    :type node_font_family: string, optional (default='sans-serif')
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

    # Draw the labels
    for v, label in labels.items():
        x, y = positions[v]
        ax.text(
            x,
            y,
            label,
            fontsize=node_fontsize,
            horizontalalignment=horizontalalignment,
            verticalalignment=verticalalignment,
            alpha=alpha,
            color=node_font_color,
            weight=node_font_weight,
            family=node_font_family,
            transform=ax.transData,
        )
        ax.plot(x, y)


def draw_jgrapht_edge_labels(
    g,
    positions,
    labels=None,
    draw_edge_weights=False,
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
    """Draw edge labels on the graph g.

    This method draws only the edge labels of the graph g.

    :param g: graph
    :type g: :py:class:`.Graph`        
    :param positions: vertices positions
    :type positions: dict
    :param labels: edge labels
    :type labels: dict, optional
    :param draw_edge_weights: whether to use edge weights as edge labels
    :type draw_edge_weights: bool, optional (default=False)
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
                labels.update({e: g.get_edge_weight(e)})
        else:
            for e in g.edges:
                labels.update({e: str(e)})

    # Draw the labels
    for e, label in labels.items():
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
