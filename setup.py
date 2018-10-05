#!/usr/bin/env python

import setuptools
from distutils.core import setup

setup(
    name='apistar-dynamic',
    version='0.1.0',
    description='API Star Dynamic model and handler generator.',
    author='Ben Fitzhardinge',
    author_email='ben@fitzhardinge.net',
    url='https://github.com/bendog/apistar-dynamic',
    python_requires='>3.5.0',
    packages=['apistar_dynamic'],
    install_requires=[
        'psycopg2',
        "apistar>0.5.0,<0.6.0",
        "apistar-jwt>=0.4.2"
    ]
)
