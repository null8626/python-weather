project = 'python-weather'
copyright = '2021-2024, null8626'
author = 'null8626'
release = '1.1.2'

extensions = []

extensions = [
  'sphinx.ext.autodoc',
  'sphinx.ext.intersphinx',
  'sphinxcontrib_trio'
]

exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = 'basic'
html_static_path = ['_static']
