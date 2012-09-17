#!/usr/bin/env python
 
from distutils.core import setup
from distutils.extension import Extension

setup(name="ArtoolKit",
    ext_modules=[
        Extension("artoolkit", ["artoolkitmodule.cpp"],
        libraries = ["boost_python"])
    ])