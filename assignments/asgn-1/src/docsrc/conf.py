##############
# READ OR DIE# ============>     pip install sphinx==4.0 -U
############## ============>     conda install pandoc # or you might instead just use `apt install pandoc`, depending on your environment
# if you install sphinx==3, it will not work. if you install sphinx==5 it will not work in the intended way.

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


import os
import sys

sys.path.insert(0, os.path.abspath(__file__ + "/../.."))
sys.path.insert(0, os.path.abspath(__file__ + "/../../rcognita"))
sys.path.insert(0, os.path.abspath(__file__ + "/../../rcognita"))

# -- Project information -----------------------------------------------------
try:
    from rcognita import __version__
except ModuleNotFoundError as e:
    print(f"This docs generating script is running from {sys.executable}. "
          f"Make sure that the respective environment has rcognita's dependencies installed.")
    raise e

project = "rcognita"
copyright = "2021, AIDA Lab"
author = "AIDA Lab"

# The full version, including alpha/beta/rc tags
release = __version__

html_logo = "logo.png"

html_show_sourcelink = False

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ["sphinx.ext.autodoc", "sphinx.ext.autosummary", "sphinx.ext.napoleon"]

autosummary_generate = True

"""
autodoc_mock_imports = [
    'rcognita.ROS_harnesses'
    'rcognita.utilities',
    'rcognita.t',
    'rcognita.w_plotting',
]
"""

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]


