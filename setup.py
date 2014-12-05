#!/usr/bin/env python
# -*- coding: utf8 -*-
from setuptools import setup, find_packages
import os


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()


if __name__ == '__main__':
    setup(
        name='ymp',
        version='1.0.0a',
        long_description=read('README.md'),
        packages=find_packages(),
        install_requires=[
            'soundcloud'
        #    'pygrooveshark'
        ],
        #dependency_links=[
        #    'git+https://github.com/koehlma/pygrooveshark.git'
        #],
        entry_points={
            'console_scripts': [
                'ymp = ymp.__main__:main'
            ]
        }
    )
