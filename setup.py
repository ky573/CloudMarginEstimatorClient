# coding: utf-8
"""
    Cloud Prisma Margin Estimator API

    Cloud Prisma Margin Estimator (CPME) calculates margin for an uploaded portfolio according to Eurex PRISMA methodology.
    The application is available to both members and non-members of Eurex Clearing.

    OpenAPI spec version: 3.0

    To install the library, run the following
    $ pip install .

    prerequisite: setuptools
    http://pypi.python.org/pypi/setuptools
"""
from os import path
from setuptools import setup, find_packages

NAME = "cpme-api-client"
VERSION = "1.0.0"
here = path.abspath(path.dirname(__file__))

# get the dependencies and installs
with open("requirements.txt", encoding="utf-8") as f:
    requires = [x.strip() for x in f if x.strip()]

# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    readme = f.read()


setup(
    name=NAME,
    version=VERSION,
    description="Cloud Prisma Margin Estimator API",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Miroslav Paris",
    author_email="miroslav.paris@deutsche-boerse.com",
    install_requires=requires,
    url="https://github.deutsche-boerse.de/dev/DAVe-MarginEstimator-PythonAPIClient",
    keywords="margining, risk, estimator, marginestimator, risk-it",
    python_requires=">=3.8",
    packages=find_packages(),
    include_package_data=True,
    setup_requires=['setuptools>=59.0'],
    classifiers=[
        "Development Status :: 1 - Beta",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
)
