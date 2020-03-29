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

