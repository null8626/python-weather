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

intersphinx_mapping = {
  'py': ('https://docs.python.org/3', None),
  'aio': ('https://docs.aiohttp.org/en/stable/', None)
}

html_js_files = ['script.js']
html_static_path = ['_static']
html_theme = 'furo'
html_title = 'python-weather'