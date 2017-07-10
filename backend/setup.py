# -*- coding: utf-8 -*-
"""
    locali
    ~~~~~~~
    locali's backend
"""

from setuptools import setup, find_packages


def get_long_description():
    with open('README.md') as f:
        result = f.read()
    return result


setup(
    name='locali',
    version='0.0.1',
    url='https://github.com/paralelstudios/locali',
    author='Michael Pérez',
    author_email='mpuhrez@paralelstudios.com',
    description="MATCHME's backend",
    long_description=get_long_description(),
    packages=find_packages(),
    include_package_data=True,
    platforms='any',
)
