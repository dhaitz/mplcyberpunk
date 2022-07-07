# -*- coding: utf-8 -*-

from typing import Optional, Union, List
import numpy as np
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


def add_gradient_fill(ax: Optional[plt.Axes] = None, alpha_gradientglow: float = 1.0):
    """Add a gradient fill under each line,
       i.e. faintly color the area below the line."""

    if not ax:
        ax = plt.gca()

    lines = ax.get_lines()

    for line in lines:

        # don't add gradient fill for glow effect lines:
        if hasattr(line, 'is_glow_line') and line.is_glow_line:
            continue

        fill_color = line.get_color()
        zorder = line.get_zorder()
        alpha = line.get_alpha()
        alpha = 1.0 if alpha is None else alpha
        rgb = mcolors.colorConverter.to_rgb(fill_color)
        z = np.empty((100, 1, 4), dtype=float)
        z[:,:,:3] = rgb
        z[:,:,-1] = np.linspace(0, alpha, 100)[:,None]
        x, y = line.get_data(orig=False)
        x, y = np.array(x), np.array(y)  # enforce x,y as numpy arrays
        xmin, xmax = x.min(), x.max()
        ymin, ymax = y.min(), y.max()
        im = ax.imshow(z, aspect='auto',
                       extent=[xmin, xmax, ymin, ymax],
                       alpha=alpha_gradientglow,
                       origin='lower', zorder=zorder)
        xy = np.column_stack([x, y])
        xy = np.vstack([[xmin, ymin], xy, [xmax, ymin], [xmin, ymin]])
        clip_path = Polygon(xy, facecolor='none', edgecolor='none', closed=True)
        ax.add_patch(clip_path)
        im.set_clip_path(clip_path)
        ax.autoscale(True)


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
