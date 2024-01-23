# coding: utf-8
"""
    Cloud Prisma Margin Estimator API

    Cloud Prisma Margin Estimator (CPME) calculates margin for an uploaded portfolio according to Eurex PRISMA methodology.
    The application is available to both members and non-members of Eurex Clearing.

    OpenAPI spec version: 3.0
"""
from os import path
from setuptools import setup, find_packages
from cpme_api import __version__

NAME = "cpme-api-client"
VERSION = __version__
here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    readme = f.read()
# To install the library, run the following
#
# python . install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = ["urllib3 >= 1.15", "certifi", "requests", "pprintjson"]

setup(
    name=NAME,
    version=VERSION,
    description="Cloud Prisma Margin Estimator API",
    long_description=readme,
    author_email="Miroslav Paris",
    url="https://github.deutsche-boerse.de/dev/DAVe-MarginEstimator-PythonAPIClient",
    keywords="dave, margining, risk, estimator, marginestimator, test, risk-it",
    install_requires=REQUIRES,
    python_requires=">=3.8, <3.11",
    packages=find_packages(),
    include_package_data=True,
    setup_requires=['wheel']
)
