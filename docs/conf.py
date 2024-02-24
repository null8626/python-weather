import sys
import os

sys.path.insert(0, os.path.abspath('..'))

project = 'python-weather'
copyright = '2021-2024, null8626'
author = 'null8626'
release = '1.1.2'

extensions = [
  'sphinx.ext.autodoc',
  'sphinx.ext.intersphinx'
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = 'furo'
#html_static_path = ['_static']
