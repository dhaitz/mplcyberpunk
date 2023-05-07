# Sample Test passing with and pytest

import pandas as pd
import matplotlib.pyplot as plt
import mplcyberpunk
import random
import numpy as np

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


def test_step_and_normal_plot():

    plt.style.use("cyberpunk")

    plt.step([1,2,3], [6,7,8])
    plt.plot([1,2,3], [9,0,1])

    mplcyberpunk.add_glow_effects()

    plt.savefig("test_step.png")


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


def test_make_specific_line_glow():

    plt.style.use("cyberpunk")

    values = {c: [random.randint(0, 10) for _ in range(7)] for c in 'ABCDEFG'}
    df = pd.DataFrame(values)

    marker = 'x'
    linestyle='--'
    df.plot(marker=marker, linestyle=linestyle)

    lines = plt.gca().lines[::2]
    mplcyberpunk.make_lines_glow(lines=lines)

    # check number of lines
    n_original_lines = 7
    n_glowing_original_lines = 4
    n_lines_per_glow = 10
    expected_num_total_lines = n_original_lines + n_glowing_original_lines * n_lines_per_glow

    new_lines = plt.gca().lines
    assert len(new_lines) == expected_num_total_lines


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


def test_plotting_gradient():
    plt.style.use("cyberpunk")
    fig, axes = plt.subplots(nrows=3, ncols=5)
    axes = iter(np.array(axes).flatten())

    x = np.linspace(0,7,20)
    y = np.sin(x)
    choices = ['min','max','top','bottom','zero']
    for choice, ax in zip(choices, axes):
        ax.set_ylim((-1.8, 1.8))
        ax.plot(x,y,marker='o',markersize=3)
        mplcyberpunk.add_gradient_fill(ax, 0.6, choice)
        ax.legend([choice])

    for off,ax in zip((-3/2, -1/2, 1/2, 3/2), axes):
        ax.set_ylim((-3, 3))
        ax.plot(x,y+off,marker='o',markersize=3)
        mplcyberpunk.add_gradient_fill(ax, (0.1, 0.6), 'zero')
        ax.legend(['zero '+str(off)])

    x = np.linspace(-2,2,20)
    choices = ['min', 'top']
    for choice, ax in zip(choices, axes):
        ax.set_yscale('log')
        ax.plot(x,np.exp(-x**2),marker='o',markersize=3)
        mplcyberpunk.add_gradient_fill(ax, (0., 1.), choice, 200)
        ax.legend(['log '+ choice])
    for choice, ax in zip(choices, axes):
        ax.plot(x,-x**2,marker='o',markersize=3)
        mplcyberpunk.add_gradient_fill(ax, (0., 1.), choice)
        ax.legend([choice + '\nreference'])

    for scale, ax in zip(['symlog', 'logit'], axes):
        ax.set_yscale(scale)
        x = np.linspace(-50,50,20) if scale=='symlog' else np.linspace(0,1,20)
        ax.plot(x,x,marker='o',markersize=3)
        # it seems like imshow() fails silently for 'logit'
        # ax.imshow(np.random.random((6, 1, 4)))
        mplcyberpunk.add_gradient_fill(ax)
        ax.legend([scale])

    fig.set_size_inches(16, 10)
    fig.savefig("test_gradient_fill.png")


def test_gradient_step():
    plt.style.use("cyberpunk")
    fig, axes = plt.subplots(nrows=1, ncols=3)
    axes = iter(np.array(axes).flatten())

    x = np.linspace(0,7,20)
    y = np.sin(x) + 1
    choices = ['pre', 'post', 'mid']
    for choice, ax in zip(choices, axes):
        ax.step(x, y, where=choice, marker='o', markersize=3)
        mplcyberpunk.add_gradient_fill(ax, 0.6, 'bottom')
        ax.legend([choice])

    fig.set_size_inches(8, 5)
    fig.savefig("test_gradient_step.png")


def test_gradient_bars():
    plt.style.use('cyberpunk')
    fig, ax = plt.subplots()

    categories = ['A', 'B', 'C', 'D', 'E']
    values = [25, 67, 19, 45, 10]
    colors = ["C0", "C1", "C2", "C3", "C4"]

    bars = ax.bar(categories, values, color=colors, zorder=2)

    mplcyberpunk.add_bar_gradient(bars=bars, ax=ax)

    fig.savefig('test_gradient_bars.png')
