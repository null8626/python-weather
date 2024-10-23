"""
The MIT License (MIT)

Copyright (c) 2021-2024 null8626

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

from typing import Tuple


class Error(Exception):
  """A ``python_weather`` error class. Extends :py:class:`Exception`."""

  __slots__: Tuple[str, ...] = ()


class RequestError(Error):
  """Thrown upon HTTP request failure. Extends :class:`.Error`."""

  __slots__: Tuple[str, ...] = ('source',)

  source: Exception
  """The :py:class:`Exception` instance causing this exception."""

  def __init__(self, source: Exception):
    self.source = source

    super().__init__()

  def __repr__(self) -> str:
    return f'<{__class__.__name__} source={self.source!r}>'
