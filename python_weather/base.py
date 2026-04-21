# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2021-2026 null8626

from .enums import WindDirection, Kind, Locale, UltraViolet
from .constants import _Unit


class BaseForecast:

  """A base weather forecast."""

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
