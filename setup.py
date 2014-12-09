#!/usr/bin/env python

# Copyright (c) 2009 - 2014, UChicago Argonne, LLC.
# See LICENSE file for details.


from setuptools import setup, find_packages
import os
import re
import sys

# pull in some definitions from the package's __init__.py file
sys.path.insert(0, os.path.join('src', ))
import moxy

requires = ['PySide>=1.2', 'PyEpics>=3.2', 'bcdaqwidgets>=0.1.1']
packages = find_packages()
verbose=1
long_description = open('README.rst', 'r').read()


setup (name             = moxy.__package_name__,        # moxy
       version          = moxy.__version__,
       license          = moxy.__license__,
       description      = moxy.__description__,
       long_description = long_description,
       author           = moxy.__author_name__,
       author_email     = moxy.__author_email__,
       url              = moxy.__url__,
       download_url     = moxy.__download_url__,
       keywords         = moxy.__keywords__,
       install_requires = requires,
       platforms        = 'any',
       package_dir      = {'': 'src'},
       #packages         = find_packages(),
       packages         = [moxy.__package_name__, ],
       package_data     = dict(moxy=['forms/*', ]),
       classifiers      = moxy.__classifiers__,
       entry_points={
          # create & install console_scripts in <python>/bin
          'console_scripts': ['moxy = moxy.main:main'],
          },
      )
