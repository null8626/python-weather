import sys
import os
import re


sys.path.insert(0, os.path.join(os.getcwd(), '..', 'python_weather'))
sys.path.insert(0, os.path.abspath('..'))

from version import VERSION


project = 'python-weather'
author = 'null8626'

copyright = ''
with open('../LICENSE', 'r') as f:
  copyright = re.search(r'[\d\-]+ null8626', f.read()).group()

version = VERSION
extensions = ['sphinx.ext.autodoc', 'sphinx.ext.intersphinx', 'sphinx_reredirects']

intersphinx_mapping = {
  'py': ('https://docs.python.org/3', None),
  'aio': ('https://docs.aiohttp.org/en/stable/', None),
}

redirects = {
  'github-donate': 'https://github.com/sponsors/null8626',
  'ko-fi-donate': 'https://ko-fi.com/null8626',
  'repository': 'https://github.com/null8626/python-weather',
  'forecast/index': 'weather.html',
}

html_css_files = [
  'style.css',
  'https://fonts.googleapis.com/css2?family=Inter:wght@100..900&family=Roboto+Mono&display=swap',
]
html_js_files = ['script.js']
html_static_path = ['_static']
html_theme = 'furo'
html_title = project
