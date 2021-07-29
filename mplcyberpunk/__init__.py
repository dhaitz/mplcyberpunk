"""mplcyberpunk - A new Python package"""

import matplotlib as mpl
import pkg_resources

from .core import add_glow_effects, make_lines_glow, add_underglow, make_scatter_glow

__version__ = pkg_resources.require("mplcyberpunk")[0].version
__author__ = 'Dominik Haitz <dominik.haitz@gmx.de>'
__all__ = []

# register the included stylesheet in the mpl style library
data_path = pkg_resources.resource_filename('mplcyberpunk', 'data/')
cyberpunk_stylesheets = mpl.style.core.read_style_directory(data_path)
mpl.style.core.update_nested_dict(mpl.style.library, cyberpunk_stylesheets)
