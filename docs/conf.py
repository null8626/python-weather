import sys
import os
import re

sys.path.insert(0, os.path.abspath('..'))

project = 'python-weather'
copyright = '2021-2024, null8626'
author = 'null8626'

version = ''
with open('../python_weather/__init__.py') as f:
  version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

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