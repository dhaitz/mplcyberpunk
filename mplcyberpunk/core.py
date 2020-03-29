# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt


def add_glow_effects(ax=None):
    """Add a glow effect to the lines in an axis object and an 'underglow' effect below the line."""
    make_lines_glow(ax=ax)
    add_underglow(ax=ax)


def make_lines_glow(ax=None, n_glow_lines=10, diff_linewidth=1.05, alpha_line=0.3):
    """Add a glow effect to the lines in an axis object.

    Each existing line is redrawn several times with increasing width and low alpha to create the glow effect.
    The line properties are copied as seen in this solution: https://stackoverflow.com/a/54688412/3240855
    """
    if not ax:
        ax = plt.gca()

    lines = ax.get_lines()

    alpha_value = alpha_line / n_glow_lines

    for line in lines:

        data = line.get_data()
        linewidth = line.get_linewidth()

        for n in range(1, n_glow_lines + 1):
            line_copy, = ax.plot(*data)
            line_copy.update_from(line)

            line_copy.set_alpha(alpha_value)
            line_copy.set_linewidth(linewidth + (diff_linewidth * n))
            line_copy.glow_line = True  # mark the glow lines, to disregard them in the underglow function.


def add_underglow(ax=None, alpha_underglow=0.1):
    """Add an 'underglow' effect, i.e. faintly color the area below the line.

    The line properties are copied as seen in this solution: https://stackoverflow.com/a/54688412/3240855
    """
    if not ax:
        ax = plt.gca()

    lines = ax.get_lines()

    for line in lines:

        if hasattr(line, 'glow_line') and line.glow_line:
            continue

        x, y = line.get_data()
        color = line.get_c()

        ax.fill_between(x=x,
                        y1=y,
                        y2=[0] * len(y),
                        color=color,
                        alpha=alpha_underglow)
