#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('README.md') as readme_file:
    readme = readme_file.read()

setup(
    name = "gcodelib",
    version = "0.0.1",
    author = "Phil Underwood",
    author_email = "beardydoc@gmail.com",
    license = "GPL3",
    url = "http://github.com/furbrain/gcodelib",
    packages = ["gcodelib"],
    requires = ["attrs"],
    test_suite = "tests",
    )
    
