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

from typing import Iterable, Optional, Tuple, List
from datetime import datetime, date, time

from .base import BaseForecast, CustomizableBase
from .enums import Phase, Locale, HeatIndex
from .constants import _Unit, LATLON_REGEX


class HourlyForecast(BaseForecast):
  """Represents a weather forecast of a specific hour."""

  __slots__: Tuple[str, ...] = ()

  def __init__(self, json: dict, unit: _Unit, locale: Locale):
    # for inheritance purposes
    if 'temp_C' not in json:
      json['temp_C'] = json.pop('tempC')
    if 'temp_F' not in json:
      json['temp_F'] = json.pop('tempF')

    super().__init__(json, unit, locale)

  def __repr__(self) -> str:
    return f'<{__class__.__name__} time={self.time!r} temperature={self.temperature!r} description={self.description!r} kind={self.kind!r}>'

  @property
  def dew_point(self) -> int:
    """The dew point in either celcius or fahrenheit."""

    return int(
      self._BaseForecast__inner[f'DewPoint{self._CustomizableBase__unit.temperature}']
    )

  @property
  def heat_index(self) -> HeatIndex:
    """The heat index in either celcius or fahrenheit."""

    celcius_index = int(self._BaseForecast__inner['HeatIndexC'])

    return HeatIndex._new(
      celcius_index,
      int(
        self._BaseForecast__inner[
          f'HeatIndex{self._CustomizableBase__unit.temperature}'
        ]
      ),
    )

  @property
  def wind_chill(self) -> int:
    """The wind chill value in either celcius or fahrenheit."""

    return int(
      self._BaseForecast__inner[f'WindChill{self._CustomizableBase__unit.temperature}']
    )

  @property
  def wind_gust(self) -> int:
    """The wind gust value in either kilometers/hour or miles/hour."""

    return int(
      self._BaseForecast__inner[f'WindGust{self._CustomizableBase__unit.velocity}']
    )

  @property
  def chances_of_fog(self) -> int:
    """Chances of a fog in percent."""

    return int(self._BaseForecast__inner['chanceoffog'])

  @property
  def chances_of_frost(self) -> int:
    """Chances of a frost in percent."""

    return int(self._BaseForecast__inner['chanceoffrost'])

  @property
  def chances_of_high_temperature(self) -> int:
    """Chances of a high temperature in percent."""

    return int(self._BaseForecast__inner['chanceofhightemp'])

  @property
  def chances_of_overcast(self) -> int:
    """Chances of an overcast in percent."""

    return int(self._BaseForecast__inner['chanceofovercast'])

  @property
  def chances_of_rain(self) -> int:
    """Chances of a rain in percent."""

    return int(self._BaseForecast__inner['chanceofrain'])

  @property
  def chances_of_remaining_dry(self) -> int:
    """Chances of remaining dry in percent."""

    return int(self._BaseForecast__inner['chanceofremdry'])

  @property
  def chances_of_snow(self) -> int:
    """Chances of a snow in percent."""

    return int(self._BaseForecast__inner['chanceofsnow'])

  @property
  def chances_of_sunshine(self) -> int:
    """Chances of a sunshine in percent."""

    return int(self._BaseForecast__inner['chanceofsunshine'])

  @property
  def chances_of_thunder(self) -> int:
    """Chances of a thunder in percent."""

    return int(self._BaseForecast__inner['chanceofthunder'])

  @property
  def chances_of_windy(self) -> int:
    """Chances of windy in percent."""

    return int(self._BaseForecast__inner['chanceofwindy'])

  @property
  def cloud_cover(self) -> int:
    """The cloud cover value in percent."""

    return int(self._BaseForecast__inner['cloudcover'])

  @property
  def time(self) -> time:
    """The local time in hours and minutes."""

    return (
      time()
      if len(self._BaseForecast__inner['time']) < 3
      else datetime.strptime(self._BaseForecast__inner['time'], '%H%M').time()
    )


class DailyForecast(CustomizableBase):
  __slots__: Tuple[str, ...] = ('__inner', '__astronomy')

  def __init__(self, json: dict, unit: _Unit, locale: Locale):
    self.__astronomy = json.pop('astronomy')[0]
    self.__inner = json

    super().__init__(unit, locale)

  def __repr__(self) -> str:
    return f'<{__class__.__name__} date={self.date!r} temperature={self.temperature!r}>'

  def __iter__(self) -> Iterable[HourlyForecast]:
    return self.hourly_forecasts

  def __list__(self) -> List[HourlyForecast]:
    return list(iter(self))

  @property
  def moon_illumination(self) -> int:
    """The percentage of the moon illuminated."""

    return int(self.__astronomy['moon_illumination'])

  @property
  def moon_phase(self) -> Phase:
    """The moon's phase."""

    return Phase(self.__astronomy['moon_phase'])

  @property
  def moonrise(self) -> Optional[time]:
    """The local time when the moon rises. This can be ``None``."""

    try:
      return datetime.strptime(self.__astronomy['moonrise'], '%I:%M %p').time()
    except ValueError:
      ...

  @property
  def moonset(self) -> Optional[time]:
    """The local time when the moon sets. This can be ``None``."""

    try:
      return datetime.strptime(self.__astronomy['moonset'], '%I:%M %p').time()
    except ValueError:
      ...

  @property
  def sunrise(self) -> Optional[time]:
    """The local time when the sun rises. This can be ``None``."""

    try:
      return datetime.strptime(self.__astronomy['sunrise'], '%I:%M %p').time()
    except ValueError:
      ...

  @property
  def sunset(self) -> Optional[time]:
    """The local time when the sun sets. This can be ``None``."""

    try:
      return datetime.strptime(self.__astronomy['sunset'], '%I:%M %p').time()
    except ValueError:
      ...

  @property
  def date(self) -> date:
    """The local date of this forecast."""

    return datetime.strptime(self.__inner['date'], '%Y-%m-%d').date()

  @property
  def lowest_temperature(self) -> int:
    """The lowest temperature in either celcius or fahrenheit."""

    return int(self.__inner[f'mintemp{self._CustomizableBase__unit.temperature}'])

  @property
  def highest_temperature(self) -> int:
    """The highest temperature in either celcius or fahrenheit."""

    return int(self.__inner[f'maxtemp{self._CustomizableBase__unit.temperature}'])

  @property
  def temperature(self) -> int:
    """The average temperature in either celcius or fahrenheit."""

    return int(self.__inner[f'avgtemp{self._CustomizableBase__unit.temperature}'])

  @property
  def sunlight(self) -> float:
    """Hours of sunlight."""

    return float(self.__inner['sunHour'])

  @property
  def snowfall(self) -> float:
    """Total snowfall in either centimeters or inches."""

    return float(self.__inner['totalSnow_cm']) / self._CustomizableBase__unit.cm_divisor

  @property
  def hourly_forecasts(self) -> Iterable[HourlyForecast]:
    """The hourly forecasts of this day."""

    return (
      HourlyForecast(elem, self._CustomizableBase__unit, self._CustomizableBase__locale)
      for elem in self.__inner['hourly']
    )


class Forecast(BaseForecast):
  """Represents today's weather forecast, alongside daily and hourly weather forecasts."""

  __slots__: Tuple[str, ...] = ('__inner', '__nearest')

  def __init__(self, json: dict, unit: _Unit, locale: Locale):
    current = json['current_condition'][0]
    self.__nearest = json.pop('nearest_area')[0]
    self.__inner = json

    super().__init__(current, unit, locale)

  def __repr__(self) -> str:
    return f'<{__class__.__name__} location={self.location!r} datetime={self.datetime!r} temperature={self.temperature!r}>'

  def __iter__(self) -> Iterable[DailyForecast]:
    return self.daily_forecasts

  def __list__(self) -> List[DailyForecast]:
    return list(iter(self))

  @property
  def local_population(self) -> int:
    """The local population count."""

    return int(self.__nearest['population'])

  @property
  def region(self) -> str:
    """The local region's name."""

    return self.__nearest['region'][0]['value']

  @property
  def location(self) -> str:
    """The location's name."""

    return self.__nearest['areaName'][0]['value']

  @property
  def country(self) -> str:
    """The local country's name."""

    return self.__nearest['country'][0]['value']

  @property
  def datetime(self) -> datetime:
    """The local date and time of this weather forecast."""

    return datetime.strptime(
      self._BaseForecast__inner['localObsDateTime'], '%Y-%m-%d %I:%M %p'
    )

  @property
  def daily_forecasts(self) -> Iterable[DailyForecast]:
    """Daily weather forecasts in this location."""

    return (
      DailyForecast(elem, self._CustomizableBase__unit, self._CustomizableBase__locale)
      for elem in self.__inner['weather']
    )

  @property
  def coordinates(self) -> Tuple[float, float]:
    """A tuple of this forecast's latitude and longitude."""

    try:
      req = next(filter(lambda x: x['type'] == 'LatLon', self.__inner['request']))
      match = LATLON_REGEX.match(req['query'])

      return float(match[1]), float(match[2])
    except:
      return float(self.__nearest['latitude']), float(self.__nearest['longitude'])
