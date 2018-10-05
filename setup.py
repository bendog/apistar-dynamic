#!/usr/bin/env python

import setuptools
from distutils.core import setup

setup(
    name='apistar-dynamic',
    version='1.0.0',
    description='Omnisyan Database Class shared resource',
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
