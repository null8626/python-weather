from setuptools import setup
setup(
  name='python-weather',
  packages=['python_weather'],
  version='0.3.8',
  license='MIT',
  description='A free and asynchronous Weather API Wrapper.',
  long_description=open('README.md', 'r', encoding='utf-8').read(),
  long_description_content_type='text/markdown',
  author='null8626',
  author_email='vierofernando9@gmail.com',
  url='https://github.com/null8626/python-weather',
  download_url='https://github.com/null8626/python-weather/archive/0.3.8.tar.gz',
  keywords=['Weather', 'API', 'Weather API', 'API Wrapper', 'Weather CLI', 'CLI'],
  install_requires=[
    'aiohttp>3.8.1',
    'xmltodict'
  ],
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
