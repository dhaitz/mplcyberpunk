#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup


setup(
    name="mplcyberpunk",
    url="https://github.com/dhaitz/mplcyberpunk",
    license='MIT',

    author="Dominik Haitz",
    author_email="dominik.haitz@gmx.de",

    description="Add-on for Matplotlib to produce 'Cyberpunk' style plots",

    long_description="Add-on for Matplotlib to produce 'Cyberpunk' style plots. See https://github.com/dhaitz/mplcyberpunk",

    packages=["mplcyberpunk"],
    package_data={
      'mplcyberpunk': ['data/*.mplstyle'],
   },
    install_requires=['matplotlib'],

    # Derive version from git. If HEAD is at the tag, the version will be the tag itself.
    setup_requires=['setuptools-scm'],
    use_scm_version=True,

    classifiers=[
        'Framework :: Matplotlib', 
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    zip_safe=False,
)
