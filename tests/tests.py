# Sample Test passing with and pytest

import pandas as pd
import matplotlib.pyplot as plt
import mplcyberpunk
import random


def test_plotting_working():
    plt.style.use("cyberpunk")

    values = {c: [random.randint(0, 10) for _ in range(7)] for c in 'ABCDEF'}
    df = pd.DataFrame(values)

    df.plot(marker='o')
    mplcyberpunk.add_glow_effects()

    plt.savefig("test.png")


def test_plotting_working_individual_functions():
    plt.style.use("cyberpunk")

    values = {c: [random.randint(0, 10) for _ in range(7)] for c in 'ABCDEF'}
    df = pd.DataFrame(values)

    df.plot(marker='o')
    mplcyberpunk.make_lines_glow()
    mplcyberpunk.add_underglow()

    plt.savefig("test_individual.png")


def test_linestyle_attributes_copied():

    plt.style.use("cyberpunk")

    values = {c: [random.randint(0, 10) for _ in range(7)] for c in 'A'}
    df = pd.DataFrame(values)

    marker = 'x'
    linestyle='--'
    df.plot(marker=marker, linestyle=linestyle)

    n_glow_lines = 10
    mplcyberpunk.make_lines_glow(n_glow_lines=n_glow_lines)

    # check number of lines
    lines = plt.gca().lines
    assert len(lines) == 1 + n_glow_lines

    # check line styling attributes
    for line in lines:
        assert line.get_marker() == marker
        assert line.get_linestyle() == linestyle



def test_axis_limits_unchanged_by_underglow():
    plt.style.use("cyberpunk")

    values = {c: [random.randint(20, 30) for _ in range(7)] for c in 'ABCDEF'}
    df = pd.DataFrame(values)

    df.plot(marker='o')

    ax = plt.gca()
    xlims, ylims = ax.get_xlim(), ax.get_ylim()

    mplcyberpunk.add_underglow(ax)

    assert xlims == ax.get_xlim()
    assert ylims == ax.get_ylim()
