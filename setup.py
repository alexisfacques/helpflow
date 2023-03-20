"""Install the helpflow package via setuptools."""
import os

# From development tooling.
from setuptools import setup, find_packages


def fread(filename: str) -> str:
    """
    Read a local file given its filename.

    :param filename: the local filename to read.
    """
    return open(os.path.join(os.path.dirname(__file__), filename)).read()


setup(
    name='helpflow',
    version=fread('VERSION'),
    description=('A Python helper library for creating Lambda-based AppFlow custom connectors.'),
    author_email='alfa@midfieldr.io',
    packages=find_packages(),
    install_requires=fread('requirements.txt').splitlines()
)
