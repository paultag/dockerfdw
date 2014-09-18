#!/usr/bin/env python

from setuptools import setup
from dockerfdw import __version__

long_description = "Docker FDW"

setup(
    name="dockerfdw",
    version=__version__,
    packages=['dockerfdw',],
    author="Paul Tagliamonte",
    author_email="paultag@debian.org",
    long_description=long_description,
    description='does some stuff with things & stuff',
    license="Expat",
    url="",
    platforms=['any']
)
