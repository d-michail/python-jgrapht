#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# JGraphT documentation build configuration file.

import os
import sys

from sphinx_gallery.sorting import ExplicitOrder

on_rtd = os.environ.get('READTHEDOCS') == 'True'

if not on_rtd:
    sys.path.insert(0, os.path.abspath('..'))

import jgrapht

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.mathjax',
    'sphinx.ext.todo',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx_gallery.gen_gallery',
]

templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'

project = jgrapht.__title__
copyright = jgrapht.__copyright__
author = jgrapht.__author__

version = jgrapht.__version__
release = jgrapht.__version__
backend_version = jgrapht.__backend_version__

rst_prolog = """
.. |BackendVersion| replace:: {backend_version}
.. |Project| replace:: {project}
.. |Bindings| replace:: Python bindings of {project}
""".format(backend_version=backend_version, project=project)

language = 'en'
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
pygments_style = 'sphinx'
todo_include_todos = False

if on_rtd:
    html_theme = 'default'
else:
    html_theme = 'sphinx_rtd_theme'

html_theme_options = {
    'canonical_url': '',
    'logo_only': False,
    'prev_next_buttons_location': 'bottom',
    'style_external_links': False,
    'style_nav_header_background': 'white',
    'collapse_navigation': True,
    'sticky_navigation': True,
    'navigation_depth': 4,
    'includehidden': True,
    'titles_only': False,
}

html_static_path = ['_static']

html_sidebars = {
    '**': [
        'relations.html',
        'searchbox.html',
    ]
}

htmlhelp_basename = 'jgraphtdoc'

latex_elements = {'papersize': 'a4paper', 'pointsize': '11pt'}
latex_documents = [
    (master_doc, 'jgrapht.tex', 'JGraphT Documentation',
     'Dimitrios Michail', 'manual'),
]
man_pages = [
    (master_doc, 'jgrapht', 'JGraphT Documentation', [author], 1)
]
texinfo_documents = [
    (master_doc, 'jgrapht', 'JGraphT Documentation',
     author, 'jgrapht', 'Python bindings for the jgrapht graph library.',
     'Miscellaneous'),
]

#
# Sphinx gallery configuration
#
sphinx_gallery_conf = {
    'examples_dirs': '../examples',
    'gallery_dirs': 'auto_examples',
    'download_all_examples': False,
}
