# -*- coding: utf-8 -*-

from typing import Optional, Union, List, Tuple
import numpy as np
import matplotlib as mpl
from matplotlib.path import Path
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.patches import Polygon


def add_glow_effects(ax: Optional[plt.Axes] = None, gradient_fill: bool = False) -> None:
    """Add a glow effect to the lines in an axis object and an 'underglow' effect below the line."""
    make_lines_glow(ax=ax)

    if gradient_fill:
        add_gradient_fill(ax=ax)
    else:
        add_underglow(ax=ax)


def make_lines_glow(
    ax: Optional[plt.Axes] = None,
    n_glow_lines: int = 10,
    diff_linewidth: float = 1.05,
    alpha_line: float = 0.3,
    lines: Union[Line2D, List[Line2D]] = None,
) -> None:
    """Add a glow effect to the lines in an axis object.

    Each existing line is redrawn several times with increasing width and low alpha to create the glow effect.
    """
    if not ax:
        ax = plt.gca()

    lines = ax.get_lines() if lines is None else lines
    lines = [lines] if isinstance(lines, Line2D) else lines

    alpha_value = alpha_line / n_glow_lines

    for line in lines:

        data = line.get_data(orig=False)
        linewidth = line.get_linewidth()

        try:
            step_type = line.get_drawstyle().split('-')[1]
        except:
            step_type = None

        for n in range(1, n_glow_lines + 1):
            if step_type:
                glow_line, = ax.step(*data)
            else:
                glow_line, = ax.plot(*data)
            glow_line.update_from(line)  # line properties are copied as seen in this solution: https://stackoverflow.com/a/54688412/3240855

            glow_line.set_alpha(alpha_value)
            glow_line.set_linewidth(linewidth + (diff_linewidth * n))
            glow_line.is_glow_line = True  # mark the glow lines, to disregard them in the underglow function.


def add_underglow(ax: Optional[plt.Axes] = None, alpha_underglow: float = 0.1) -> None:
    """Add an 'underglow' effect, i.e. faintly color the area below the line."""
    if not ax:
        ax = plt.gca()

    # because ax.fill_between changes axis limits, save current xy-limits to restore them later:
    xlims, ylims = ax.get_xlim(), ax.get_ylim()

    lines = ax.get_lines()

    for line in lines:

        # don't add underglow for glow effect lines:
        if hasattr(line, 'is_glow_line') and line.is_glow_line:
            continue

        # parameters to be used from original line:
        x, y = line.get_data(orig=False)
        color = line.get_c()
        transform = line.get_transform()

        try:
            step_type = line.get_drawstyle().split('-')[1]
        except:
            step_type = None

        ax.fill_between(x=x,
                        y1=y,
                        y2=[0] * len(y),
                        color=color,
                        step=step_type,
                        alpha=alpha_underglow,
                        transform=transform)

    ax.set(xlim=xlims, ylim=ylims)


def add_gradient_fill(
    ax: Optional[plt.Axes] = None,
    alpha_gradientglow: Union[float, Tuple[float,float]] = 1.0,
    gradient_start: str = 'min',
    N_sampling_points: int = 50,
) -> None:
    """
    Add a gradient fill under each line, faintly coloring the area below/above the line.
    PARAMETERS:
    - ax
        The matplolib axes, defaults to the global figure
    - alpha_gradientglow
        If float, the gradient is from 0 to alpha_gradientglow
        If tuple[float, float], the gradient is from alpha_gradientglow[0] to alpha_gradientglow[1]
    - gradient_start
        Sets the point where the gradient is minimal
        For aesthetic reasons, one may want the gradient to either start at:
            - 'min':  The minimum of each curve (default): this fills below the curve
            - 'max': The maximum of each curve: this fills above the curve
            - 'bottom': The bottom of the figure: this fills below the curve
            - 'top': The top of the figure: this fills below the curve
            - 'zero': this fills both above and below the curve
    - N_sampling_points
        Number of sampling points. Higher may look better at the cost of performance
    """

    choices = ['min','max','top','bottom','zero']
    if not gradient_start in choices:
        raise ValueError(f'key must be one of {choices}')
    if type(alpha_gradientglow) == float:
        alpha_gradientglow = (0., alpha_gradientglow)
    if not (type(alpha_gradientglow) == tuple and type(alpha_gradientglow[0]) == type(alpha_gradientglow[0]) == float):
        raise ValueError(f'alpha_gradientglow must be a float or a tuple of two floats but is {alpha_gradientglow}')
    if not ax:
        ax = plt.gca()

    # because ax.imshow changes axis limits, save current xy-limits to restore them later:
    xlims, ylims = ax.get_xlim(), ax.get_ylim()

    for line in ax.get_lines():

        # don't add gradient fill for glow effect lines:
        if hasattr(line, 'is_glow_line') and line.is_glow_line:
            continue

        fill_color = line.get_color()
        zorder = line.get_zorder()
        alpha = line.get_alpha()
        alpha = 1.0 if alpha is None else alpha
        rgb = mcolors.colorConverter.to_rgb(fill_color)
        z = np.empty((N_sampling_points, 1, 4), dtype=float)
        z[:,:,:3] = rgb

        # find the visual extend of the gradient
        x, y = line.get_data(orig=False)
        x, y = np.array(x), np.array(y)  # enforce x,y as numpy arrays
        xmin, xmax = x.min(), x.max()
        ymin, ymax = y.min(), y.max()
        Ay = {'min':ymin,'max':ymax,'top':ylims[1],'bottom':ylims[0],'zero':0}[gradient_start]
        extent = [xmin, xmax, min(ymin,Ay), max(ymax,Ay)]

        # alpha will be linearly interpolated on scaler(y)
        # {"linear","symlog","logit",...} are currentlty treated the same
        if ax.get_yscale() == 'log':
            if gradient_start == 'zero' : raise ValueError("key cannot be 'zero' on log plots")
            scaler = np.log
        else:
            scaler = lambda x: x

        a, b = alpha_gradientglow
        ya, yb = extent[2], extent[3]
        moment = lambda y : (scaler(y)-scaler(ya)) / (scaler(yb)-scaler(ya))
        ys = np.linspace(ya, yb, N_sampling_points)

        if gradient_start in ('min', 'bottom'):
            k = moment(ys)
        elif gradient_start in ('top', 'max'):
            k = 1 - moment(ys)
        elif gradient_start in ('zero',):
            abs_ys = np.abs(ys)
            k = abs_ys / np.max(abs_ys)

        alphas = k*b + (1-k)*a
        z[:,:,-1] = alphas[:,None]

        im = ax.imshow(z,
                       aspect='auto',
                       extent=extent,
                       alpha=alpha,
                       interpolation='bilinear',
                       origin='lower',
                       zorder=zorder)

        # xy = np.column_stack([x, y])
        # xy = np.vstack([[xmin, Ay], xy, [xmax, Ay], [xmin, Ay]])
        # clip_path = Polygon(xy, facecolor='none', edgecolor='none', closed=True)
        # ax.add_patch(clip_path)
        # im.set_clip_path(clip_path)

        path = line.get_path()
        extras = Path([[xmax,Ay],[xmin, Ay]], np.full(2, Path.MOVETO))
        extras.codes[:] = Path.LINETO
        path = path.make_compound_path(path, extras)
        im.set_clip_path(path, line._transform)

    ax.set(xlim=xlims, ylim=ylims)


def make_scatter_glow(
    ax: Optional[plt.Axes] = None,
    n_glow_lines: int = 10,
    diff_dotwidth: float = 1.2,
    alpha: float = 0.3,
) -> None:
    """Add glow effect to dots in scatter plot.

    Each plot is redrawn 10 times with increasing width to create glow effect."""
    if not ax:
        ax = plt.gca()

    scatterpoints = ax.collections[-1]
    x, y = scatterpoints.get_offsets().data.T
    dot_color = scatterpoints.get_array()
    dot_size = scatterpoints.get_sizes()

    alpha = alpha/n_glow_lines

    for i in range(1, n_glow_lines):
        plt.scatter(x, y, s=dot_size*(diff_dotwidth**i), c=dot_color, alpha=alpha)


def add_bar_gradient(
    bars: mpl.container.BarContainer,
    ax: Optional[plt.Axes] = None,
    horizontal: bool = False,
) -> None:
    """Replace each bar with a rectangle filled with a color gradient going transparent"""

    if not ax:
        ax = plt.gca()

    X = [[0, 1],[0, 1]] if horizontal else [[1, 1],[0, 0]]

    # freeze axis limits before calling imshow
    ax.axis()
    ax.autoscale(False)

    for bar in bars:

        # get properties of existing bar
        x, y = bar.get_xy()
        width, height = bar.get_width(), bar.get_height()
        zorder = bar.zorder
        color = bar.get_facecolor()

        cmap = mcolors.LinearSegmentedColormap.from_list('gradient_cmap', [(color[0], color[1], color[2], 0), color])

        ax.imshow(
            X=X,  # pseudo-image
            extent=[x, x+width, y, y+height],
            cmap=cmap,
            zorder=zorder,
            interpolation='bicubic',
            aspect='auto',  # to prevent mpl from auto-scaling axes equally
        )

        bar.remove()
