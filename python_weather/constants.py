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

from typing import Union, Tuple
import re


class _Unit:
  __slots__: Tuple[str, ...] = (
    'temperature',
    'velocity',
    'pressure',
    'precipitation',
    'visibility',
    'cm_divisor',
  )

  def __init__(
    self,
    temperature: str,
    velocity: str,
    pressure: str,
    precipitation: str,
    visibility: str,
    cm_divisor: Union[int, float],
  ):
    self.temperature = temperature
    self.velocity = velocity
    self.pressure = pressure
    self.precipitation = precipitation
    self.visibility = visibility
    self.cm_divisor = cm_divisor

  def __repr__(self) -> str:
    return f'<Unit [{self.temperature}, {self.velocity}]>'


METRIC = _Unit('C', 'Kmph', '', 'MM', '', 1)
IMPERIAL = _Unit('F', 'Miles', 'Inches', 'Inches', 'Miles', 2.54)

WIND_DIRECTION_EMOJIS = ('↓', '↙', '←', '↖', '↑', '↗', '→', '↘')
LATLON_REGEX = re.compile(r'^Lat (\-?[\d\.]+) and Lon (\-?[\d\.]+)$')
