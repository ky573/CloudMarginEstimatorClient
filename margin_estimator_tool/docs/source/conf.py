# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Margin Estimator Tool'
copyright = '2025, Daniel Lopata'
author = 'Daniel Lopata'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

import os
import sys

for x in os.walk('../../src'):
  sys.path.insert(0, x[0])

extensions = [
    'sphinx.ext.autodoc',      # Extracts docstrings for documentation
    'sphinx.ext.napoleon',     # Parses Google-style and NumPy-style docstrings
    'sphinx.ext.intersphinx',  # Links to other project's documentation
]

html_theme = "sphinx_rtd_theme"
