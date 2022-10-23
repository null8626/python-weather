from setuptools import setup

readme = None

with open('README.md', 'r', encoding='utf-8') as f:
  readme = f.read()

setup(
  name='python-weather',
  packages=['python_weather'],
  version='0.4.3',
  license='MIT',
  description='A free and asynchronous Weather API Wrapper.',
  long_description=readme,
  long_description_content_type='text/markdown',
  author='null8626',
  url='https://github.com/null8626/python-weather',
  download_url='https://github.com/null8626/python-weather/archive/0.4.3.tar.gz',
  keywords=['Weather', 'API', 'Weather API', 'API Wrapper', 'Weather CLI', 'CLI'],
  install_requires=['aiohttp'],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10'
  ],
  python_requires='>=3.7',
)