"""
The MIT License (MIT)

Copyright (c) 2021-2025 null8626

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from .enums import HeatIndex, Kind, Locale, Phase, UltraViolet, WindDirection
from .constants import METRIC, IMPERIAL
from .errors import Error, RequestError
from .version import VERSION
from .client import Client


__title__ = 'python-weather'
__author__ = 'null8626'
__license__ = 'MIT'
__copyright__ = 'Copyright (c) 2021-2025 null8626'
__version__ = VERSION
__all__ = (
  'METRIC',
  'IMPERIAL',
  'Client',
  'Error',
  'RequestError',
  'HeatIndex',
  'Kind',
  'Locale',
  'Phase',
  'UltraViolet',
  'VERSION',
  'WindDirection',
)
