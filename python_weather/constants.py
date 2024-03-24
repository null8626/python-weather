from typing import Union
from re import compile


class _Unit:
  __slots__ = (
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

WIND_DIRECTION_EMOJIS = ['↓', '↙', '←', '↖', '↑', '↗', '→', '↘']
LATLON_REGEX = compile(r'^Lat (\-?[\d\.]+) and Lon (\-?[\d\.]+)$')
