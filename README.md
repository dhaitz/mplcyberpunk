# mplcyberpunk


[![Latest PyPI version](https://img.shields.io/pypi/v/mplcyberpunk.svg)](https://pypi.python.org/pypi/mplcyberpunk)

[![Latest Travis CI build status](https://travis-ci.org/dhaitz/mplcyberpunk.png)](https://travis-ci.org/dhaitz/mplcyberpunk)

[![Documentation Status](https://readthedocs.org/projects/mplcyberpunk/badge/?version=stable)](http://mplcyberpunk.pypa.io/en/stable/?badge=stable)

A Python package on top of `matplotlib` to create a 'cyberpunk' style

![](img/demo.png)

## Installation

    pip install mplcyberpunk
    
## Usage

After importing the package, the _cyberpunk_ stylesheet (dark background etc.) is available via `plt.style.use`.
The line glow and 'underglow' effects are added via calling the respective functions: 

    import matplotlib.pyplot as plt
    import mplcyberpunk
    
    plt.style.use("cyberpunk")
    
    plt.plot([1, 3, 9, 5, 2, 1, 1], marker='o')
    plt.plot([4, 5, 5, 7, 9, 8, 6], marker='o')
    
    mplcyberpunk.make_lines_glow()
    mplcyberpunk.add_underglow()
    
    plt.show()
    
Result: 

![](img/demo.png)
    

This effect is currently only implemented for lines.


## Stuff
testpypi:

:   twine upload --repository-url <https://test.pypi.org/legacy/>
    dist/\*

travis:

:   check



## Requirements
Depends only on `matplotlib`.


## Authors

*mplcyberpunk* was written by [Dominik Haitz](https://dhaitz.github.io).
