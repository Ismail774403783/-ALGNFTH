from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from setuptools import setup

setup(
    entry_points={
        'console_scripts': [
            'pyLoadCore = pyLoadCore:main',
            'pyLoadCli = pyLoadCli:main'
        ],
    },
)
