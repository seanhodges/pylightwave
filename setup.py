# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='pylightwave',
    version='0.1.0',
    description='Basic library and commandline tools for interacting with the Lightwave API',
    long_description=readme,
    author='Sean Hodges',
    author_email='seanhodges84@gmail.com',
    url='https://github.com/seanhodges/pylightwave',
    license=license,
    packages=find_packages()
)
