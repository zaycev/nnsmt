#!/usr/bin/env python
# coding: utf-8
# Author: Vova Zaytsev <zaytsev@usc.edu>

from distutils.core import setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize("alignment.pyx")
)