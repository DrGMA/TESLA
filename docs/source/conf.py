#!/usr/bin/env python

# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html




# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
import os
import sys
import sphinx_rtd_theme
sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(0, os.path.abspath('./../../')) # needed to show docstrings via `automodules`

#import mock
#MOCK_MODULES = ['numpy', 'scipy', 'matplotlib', 'mpl_toolkits', 'obspy', 'pandas', 'yaml']
#for mod_name in MOCK_MODULES:
#    sys.modules[mod_name] = mock.Mock()




# -- Project information -----------------------------------------------------

project   = 'TESLA'
copyright = '2023, Guido Maria Adinolfi'
author    = 'Guido Maria Adinolfi'

# The short X.Y version.
release = version = '0.0.1'  # Is set by calling `setup.py docs`

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".


numfig = True

# -- General configuration ---------------------------------------------------

# Read the Docs will set master doc to index instead (or whatever it is you have 
# specified in your settings). Try adding this to your conf.py:
#for latex
#master_doc = 'index_latex'
#for html
master_doc = 'index'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinx.ext.autodoc', 
              'sphinx.ext.coverage', 
              'sphinx.ext.napoleon', 
              'sphinx_rtd_theme']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

latex_engine = 'xelatex'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []




# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'  # alabaster, pyramid, haiku, scrolls, classic, nature, sphinx_rtd_theme
# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
html_logo        = "_static/logo.png"



latex_logo        = "_static/logo.png"
latex_elements = {
    'makeindex': r'''\renewcommand{\sphinxlogo}{\sphinxincludegraphics[width=2.0\textwidth]{logo.png}\par\vspace{50pt}}
'''
}



# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
html_theme_options = {
    'logo_only'             : False,
    #'canonical_url'         : 'https://tesla.readthedocs.io/en/latest/index.html',
    'display_version'       : True,
    'prev_next_buttons_location': 'bottom',
    'style_external_links'      :  False,
    'vcs_pageview_mode'         :  '',
    #'style_nav_header_background': 'white',    
    # Toc options
    'collapse_navigation': False,
    'sticky_navigation':   True,
    'navigation_depth':    4,
    'includehidden':       True,
    'titles_only':         False
}
#html_theme_options ={
#    "light_logo": "logo.png",
#    "dark_logo": "logo.png"
#}
