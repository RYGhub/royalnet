# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))

import pkg_resources

# -- Project information -----------------------------------------------------

project = 'royalnet_telethon'
# noinspection PyShadowingBuiltins
copyright = '2021, Stefano Pigozzi'
author = 'Stefano Pigozzi'

# The full version, including alpha/beta/rc tags
release = pkg_resources.get_distribution("royalnet_telethon").version


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    'sphinx.ext.todo',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['Thumbs.db', '.DS_Store']

# Print warnings on the page
keep_warnings = True

# Display more warnings than usual
nitpicky = True

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']


# -- Intersphinx options -----------------------------------------------------

intersphinx_mapping = {
    "python": ("https://docs.python.org/3.8", None),
    "royalnet": ("https://royalnet-6.readthedocs.io/en/latest", None)
}


# -- Setup function ----------------------------------------------------------
def setup(app):
    app.add_css_file('royalblue.css')


# -- Substitutions -----------------------------------------------------------


rst_prolog = """

"""

# -- Automodule settings -----------------------------------------------------

autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    'special-members': '__init__',
    'undoc-members': True,
}

# -- Automodule settings -----------------------------------------------------

todo_include_todos = True
