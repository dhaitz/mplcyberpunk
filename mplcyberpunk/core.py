# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt


def make_lines_glow(ax=None):
    """https://stackoverflow.com/a/54688412/3240855"""
    if not ax:
        ax = plt.gca()

    lines = ax.get_lines()

    for line in lines:

        data = line.get_data()

        n_lines = 10
        diff_linewidth = 1.05
        alpha_value = 0.3 / n_lines

        for n in range(1, n_lines + 1):
            line_copy, = ax.plot(*data)
            line_copy.update_from(line)

            line_copy.set_alpha(alpha_value)
            line_copy.set_linewidth(2 + (diff_linewidth * n))
            line_copy.glow_line = True


def add_underglow(ax=None):
    """https://stackoverflow.com/a/54688412/3240855"""
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
                        alpha=0.1)
