from os import path
from setuptools import setup

name = "COMET"
here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    readme = f.read()

# get the dependencies and installs
with open("requirements.txt", encoding="utf-8") as f:
    requires = [x.strip() for x in f if x.strip()]

setup(
    name=name,
    version='2.0.0',
    description="CoMet helps to test/query cpME API",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.deutsche-boerse.de/dev/DAVe-MarginEstimator-Tests",
    python_requires=">=3.8, <3.11",
    install_requires=requires,
    author="Miroslav Paris",
    entry_points={
        "console_scripts":
            ["comet = comet.cli:main", "model_gen = model_gen.cli:main"]
    },
    setup_requires=['wheel'],
    keywords="dave, margining, risk, estimator, marginestimator, test, risk-it",
    classifiers=[
        "Development Status :: 1 - Beta",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
