"""mplcyberpunk - A new Python package"""

import matplotlib as mpl
import importlib.metadata
import importlib.resources

from .core import (
    add_glow_effects,
    make_lines_glow,
    add_underglow,
    make_scatter_glow,
    add_gradient_fill,
    add_bar_gradient,
)

__version__ = importlib.metadata.version("mplcyberpunk")
__author__ = "Dominik Haitz <dominik.haitz@gmx.de>"
__all__ = []

# register the included stylesheet in the mpl style library
with importlib.resources.path("mplcyberpunk", "data") as data_path:
    cyberpunk_stylesheets = mpl.style.core.read_style_directory(data_path)
    mpl.style.core.update_nested_dict(mpl.style.library, cyberpunk_stylesheets)
