# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2021-2026 null8626

import re
from dataclasses import dataclass


@dataclass(frozen=True, repr=False, slots=True)
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
TIME_REGEX = re.compile(r'^(\d{2}):(\d{2}) ([AP])M$')

KIND_EMOJIS = {
  113: '☀️',
  116: '⛅',
  119: '☁️',
  122: '☁️',
  125: '🌫️',
  128: '🌫️',
  131: '💨',
  134: '💨',
  137: '💨',
  140: '💨',
  143: '🌫️',
  146: '🌫️',
  149: '🌫️',
  152: '🌫️',
  155: '🌫️',
  158: '💨',
  161: '💨',
  176: '🌦️',
  179: '🌨️',
  182: '🌨️',
  185: '🌧️',
  200: '⛈️',
  227: '💨',
  230: '🌨️',
  248: '🌫️',
  260: '🌫️',
  263: '🌦️',
  266: '🌦️',
  281: '🌧️',
  284: '🌧️',
  293: '🌦️',
  296: '🌦️',
  299: '🌧️',
  302: '🌧️',
  305: '🌧️',
  308: '🌧️',
  311: '🌧️',
  314: '🌧️',
  317: '🌨️',
  320: '🌨️',
  323: '🌨️',
  326: '🌨️',
  329: '🌨️',
  332: '🌨️',
  335: '🌨️',
  338: '🌨️',
  350: '🌨️',
  353: '🌦️',
  356: '🌧️',
  359: '🌧️',
  362: '🌨️',
  365: '🌨️',
  368: '🌨️',
  371: '🌨️',
  374: '🌨️',
  377: '🌨️',
  386: '⛈️',
  389: '🌩️',
  392: '⛈️',
  395: '🌩️',
}
WIND_DIRECTION_EMOJIS = '↑', '↖', '←', '↙', '↓', '↘', '→', '↗'
