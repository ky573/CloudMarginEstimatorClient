import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))

sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, 'src'))

project = 'Margin Estimator Tool'
copyright = '2025, Daniel Lopata'
author = 'Daniel Lopata'

extensions = [
    'sphinx.ext.autodoc',       # Core extension for auto API documentation
    'sphinx.ext.viewcode',      # Add links to view the source code
    'sphinx.ext.napoleon',      # Support for Google or NumPy style docstrings
    'sphinx.ext.autosummary',   # Generate summary tables for modules
]

# Configure autodoc
autodoc_default_options = {
    'members': True,
    'undoc-members': True,
    'show-inheritance': True,
    'member-order': 'bysource',
}

autosummary_generate = True

html_theme = 'sphinx_rtd_theme'

viewcode_follow_imported_members = True

autodoc_member_order = 'bysource'

autodoc_default_flags = ['members', 'undoc-members', 'private-members']