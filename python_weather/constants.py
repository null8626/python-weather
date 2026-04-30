# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2021-2026 null8626

from dataclasses import dataclass
import re


@dataclass(repr=False, slots=True)
class _Unit:
  """A supported measurement unit."""

  temperature: str
  velocity: str
  pressure: str
  precipitation: str
  visibility: str
  cm_divisor: float | int

  def __repr__(self) -> str:
    """The unit's debug string representation."""
    return f'<Unit [{self.temperature}, {self.velocity}]>'


METRIC = _Unit('C', 'Kmph', '', 'MM', '', 1)
IMPERIAL = _Unit('F', 'Miles', 'Inches', 'Inches', 'Miles', 2.54)

LATLON_REGEX = re.compile(r'^Lat (\-?[\d\.]+) and Lon (\-?[\d\.]+)$')

KIND_EMOJIS = (
  '☀️',
  '⛅️',
  '☁️',
  '☁️',
  '🌫',
  '🌦',
  '🌧',
  '🌧',
  '⛈',
  '🌨',
  '❄️',
  '🌦',
  '🌧',
  '🌧',
  '🌨',
  '❄️',
  '🌩',
  '⛈',
)
WIND_DIRECTION_EMOJIS = '↑', '↖', '←', '↙', '↓', '↘', '→', '↗'
