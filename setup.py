#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=6.0',
    'PyDispatcher>=2.0.5'
]

test_requirements = [
    'nose',
]

setup(
    name='pygear',
    version='0.1.0',
    description="PyGear is a collection of useful functions and snippets that you need or could use every day.",
    long_description=readme + '\n\n' + history,
    author="Amir Khakshour",
    author_email='khakshour.amir@gmail.com',
    url='https://github.com/amir-khakshour/pygear',
    packages=[
        'pygear',
    ],
    package_dir={'pygear':
                 'pygear'},
    entry_points={
        'console_scripts': [
            'pygear=pygear.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="GNU General Public License v3",
    zip_safe=False,
    keywords='pygear',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='nose.collector',
    tests_require=test_requirements
)
