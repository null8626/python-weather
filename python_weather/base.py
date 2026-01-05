# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2021-2026 null8626

from .enums import WindDirection, Kind, Locale, UltraViolet
from .constants import _Unit
from .errors import Error


class CustomizableBase:
  __slots__: tuple[str, ...] = '_unit', '_locale'

  _unit: _Unit
  _locale: Locale

  def __init__(self, unit: _Unit, locale: Locale):
    self.unit = unit
    self.locale = locale

  @property
  def unit(self) -> _Unit:
    """The measuring unit used."""

    return self._unit

  @unit.setter
  def unit(self, to: _Unit) -> None:
    """
    Sets the default measuring unit used.

    :param to: The new default measuring unit to be used.

    :exception Error: ``to`` is not either :data:`~.constants.METRIC` or :data:`~.constants.IMPERIAL`.
    """

    if not isinstance(to, _Unit):
      raise Error('Invalid measuring unit specified!')

    self._unit = to

  @property
  def locale(self) -> Locale:
    """The localization used."""

    return self._locale

  @locale.setter
  def locale(self, to: Locale) -> None:
    """
    Sets the default localization used.

    :param to: The new :class:`.Locale` to be used.
    :type to: :class:`.Locale`

    :exception Error: ``to`` is not a part of the :class:`.Locale` enum.
    """

    if not isinstance(to, Locale):
      raise Error(f'Expected {to!r} to be a Locale enum')

    self._locale = to


class BaseForecast:
  __slots__: tuple[str, ...] = (
    'cloud_cover',
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

  cloud_cover: int
  """The cloud cover value in percent."""

  ultraviolet: UltraViolet
  """The ultra-violet index."""

  humidity: int
  """The humidity value in percent."""

  wind_direction: WindDirection
  """The wind direction."""

  kind: Kind
  """The kind of the forecast."""

  feels_like: int
  """What it felt like in either celcius or fahrenheit."""

  temperature: int
  """The temperature in either celcius or fahrenheit."""

  precipitation: float
  """The precipitation in either millimeters or inches."""

  pressure: float
  """The pressure in either pascal or inches."""

  visibility: int
  """The visibility distance in either kilometers or miles."""

  wind_speed: int
  """The wind speeds in either kilometers/hour or miles/hour."""

  description: str
  """The description regarding the forecast depending on the localization used."""

  def __init__(self, json: dict, unit: _Unit, locale: Locale):
    description = (
      json['weatherDesc'][0]['value']
      if locale is Locale.ENGLISH
      else json[f'lang_{locale.value}'][0]['value']
    )

    self.cloud_cover = int(json['cloudcover'])
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
