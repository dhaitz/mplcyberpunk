# mplcyberpunk


[![Latest PyPI version](https://img.shields.io/pypi/v/mplcyberpunk.svg)](https://pypi.python.org/pypi/mplcyberpunk) [![Build Status](https://travis-ci.com/dhaitz/mplcyberpunk.svg?branch=master)](https://travis-ci.com/dhaitz/mplcyberpunk)

A Python package on top of `matplotlib` to create 'cyberpunk' style plots with 3 additional lines of code.

![](img/demo.png)

## Installation

    pip install mplcyberpunk
    
## Usage

After importing the package, the _cyberpunk_ stylesheet (dark background etc.) is available via `plt.style.use`.
The line glow and 'underglow' effects are added via calling `add_glow_effects`: 

```python
    import matplotlib.pyplot as plt
    import mplcyberpunk
    
    plt.style.use("cyberpunk")
    
    plt.plot([1, 3, 9, 5, 2, 1, 1], marker='o')
    plt.plot([4, 5, 5, 7, 9, 8, 6], marker='o')
    
    mplcyberpunk.add_glow_effects()
    
    plt.show()
```
    
Result: 

![](img/demo.png)

This effect is currently only implemented for lines.

The individual steps are described [here](https://matplotlib.org/matplotblog/posts/matplotlib-cyberpunk-style/) in more detail.
    
    
    
Instead of `add_glow_effects`, you can add the line glow and underglow effects separately:

    mplcyberpunk.make_lines_glow()
    mplcyberpunk.add_underglow()

    
You can also add the effect to a specific axis object explicitly:

    fig, ax = plt.subplots()
    ...
    mplcyberpunk.make_lines_glow(ax)
       
![](img/sin.png)

The default colormap is [cool](https://user-images.githubusercontent.com/5802753/78286625-3e6e2d80-7521-11ea-978a-96ec42f5d6ca.png).

## Requirements
Depends only on `matplotlib`.


## Authors

*mplcyberpunk* was written by [Dominik Haitz](https://dhaitz.github.io).
