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

from enum import auto
from typing import Tuple

from .errors import Error
from .enums import WindDirection, Kind, Locale, UltraViolet
from .constants import _Unit


class CustomizableBase:
  __slots__: Tuple[str, ...] = ('__unit', '__locale')

  def __init__(self, unit: _Unit, locale: Locale):
    self.unit = unit
    self.locale = locale

  @property
  def unit(self) -> auto:
    """The measuring unit used to display information in this object."""

    return self.__unit

  @unit.setter
  def unit(self, to: _Unit) -> None:
    """
    Sets the default measuring unit used to display information in this object.

    :param to: The new default measuring unit to be used to display information in this object. Must be either ``METRIC`` or ``IMPERIAL``.
    :exception Error: If the ``to`` argument is not either ``METRIC`` or ``IMPERIAL``.
    """

    if not isinstance(to, _Unit):
      raise Error('Invalid measuring unit specified!')

    self.__unit = to

  @property
  def locale(self) -> Locale:
    """The localization used to display information in this object."""

    return self.__locale

  @locale.setter
  def locale(self, to: Locale) -> None:
    """
    Sets the default localization used to display information in this object.

    :param to: The new :class:`~python_weather.enums.Locale` to be used to display information in this object.
    :type to: Locale
    :exception Error: If the ``to`` argument is not a part of the :class:`~python_weather.enums.Locale` enum.
    """

    if not isinstance(to, Locale):
      raise Error(f'Expected {to!r} to be a Locale enum')

    self.__locale = to


class BaseForecast:
  __slots__: Tuple[str, ...] = (
    'ultraviolet',
    'humidity',
    'wind_direction',
    'kind',
    'feels_like',
    'temperature',
    'precipitation',
    'pressure',
    'visibility',
    'wind_speed',
    'description',
  )

  ultraviolet: UltraViolet
  """The ultra-violet (UV) index."""

  humidity: int
  """The humidity value in percent."""

  wind_direction: WindDirection
  """The wind direction."""

  kind: Kind
  """The kind of the forecast."""

  feels_like: int
  """What it felt like, in celcius or fahrenheit."""

  temperature: int
  """The temperature in either celcius or Fahrenheit."""

  precipitation: float
  """The precipitation in either millimeters or inches."""

  pressure: float
  """The pressure in either pascal or inches."""

  visibility: int
  """The visibility distance in either kilometers or miles."""

  wind_speed: int
  """The wind speeds in either kilometers/hour or miles/hour."""

  description: str
  """The description regarding the forecast. This can be localized in different languages depending on the localization used."""

  def __init__(self, json: dict, unit: _Unit, locale: Locale):
    description = (
      json['weatherDesc'][0]['value']
      if locale is Locale.ENGLISH
      else json[f'lang_{locale.value}'][0]['value']
    )

    self.ultraviolet = UltraViolet._new(int(json['uvIndex']))
    self.humidity = int(json['humidity'])
    self.wind_direction = WindDirection._new(
      json['winddir16Point'], int(json['winddirDegree'])
    )
    self.kind = Kind(int(json['weatherCode']))
    self.feels_like = int(json[f'FeelsLike{unit.temperature}'])
    self.temperature = int(json[f'temp_{unit.temperature}'])
    self.precipitation = float(json[f'precip{unit.precipitation}'])
    self.pressure = float(json[f'pressure{unit.pressure}'])
    self.visibility = int(json[f'visibility{unit.visibility}'])
    self.wind_speed = int(json[f'windspeed{unit.velocity}'])
    self.description = description.strip()
