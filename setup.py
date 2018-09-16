# !/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os
import re

from setuptools import find_packages, setup

# Package meta-data.
NAME = 'cards'
DESCRIPTION = 'Project task tracking / todo list.'
URL = 'https://github.com/okken/cards'
EMAIL = 'brian@pythontesting.net'
AUTHOR = 'Brian Okken'
REQUIRES_PYTHON = '>=3.6.0'

REQUIRED = ['click', 'tabulate',  # for CLI
            'tinydb',             # for DB
            "dataclasses; python_version<'3.7'",  # cli <-> db data type
            ]

# The rest you shouldn't have to touch too much :)
# ------------------------------------------------

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
with io.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = '\n' + f.read()


def read(*parts):
    with io.open(os.path.join(here, *parts), 'r') as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name=NAME,
    version=find_version('src', 'cards', '__init__.py'),
    description=DESCRIPTION,
    long_description=long_description,
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    entry_points={
        'console_scripts': ['cards=cards.cli:cards_cli'],
    },
    install_requires=REQUIRED,
    include_package_data=True,
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
)
