# Configuration file for the Sphinx documentation builder.
# https://github.com/richdayandnight/Tutorial_SimpleTeacherAPI/blob/master/docs/source/conf.py
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys
sys.path.insert(0, os.path.abspath('/cpme_api/'))
sys.setrecursionlimit(1000)

project = 'COMET - Cloud Margin Estimator api Test tool'
copyright = '2023, cpME team, author Miroslav Paris'
author = 'Miroslav Paris'
release = '1.1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.ifconfig',
    'sphinx.ext.viewcode',
    'sphinx_rtd_size',
    'sphinx_copybutton'
   # 'rinoh.frontend.sphinx'
]

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
# html_static_path = ['_static']

html_show_sourcelink = False

html_show_sphinx = False
# https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-html_show_sphinx

sphinx_rtd_size_width = "90%"


rst_epilog = """
.. |psf| replace:: Python Software Foundation
"""


