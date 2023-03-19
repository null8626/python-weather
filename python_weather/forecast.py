"""
The MIT License (MIT)

Copyright (c) 2021-2023 null (https://github.com/null8626)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the 'Software'), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from datetime import datetime, date, time, timedelta, timezone
from typing import Generator, Optional, Tuple
from enum import auto

from .constants import (VALID_FORMATS, TIME_REGEX, LOCAL_DATETIME_REGEX,
                        UTC_DATETIME_REGEX, DATE_REGEX, LATLON_REGEX, METRIC)

from .errors import Error
from .enums import WeatherType, MoonPhase, WindDirection

def _convert_to_24h(hour, ampm):
  res = (0 if ampm == 'A' else 12) + int(hour)

  if res == 24:
    return 12
  elif res == 0 or res == 12:
    return 0
  else:
    return res

class NearestArea:
  __slots__ = ('__inner',)

  def __init__(self, json: dict):
    self.__inner = json

  def __repr__(self) -> str:
    """
    Returns:
      str: The string representation of said object.
    """

    return f'<NearestArea name={self.name!r} country={self.country!r} region={self.region!r}>'

  @property
  def latitude(self) -> float:
    """
    Returns:
      float: The latitude.
    """

    return float(self.__inner['latitude'])

  @property
  def longitude(self) -> float:
    """
    Returns:
      float: The longitude.
    """

    return float(self.__inner['longitude'])

  @property
  def region(self) -> str:
    """
    Returns:
      str: The region location.
    """

    return self.__inner['region'][0]['value']

  @property
  def name(self) -> str:
    """
    Returns:
      str: The area name.
    """

    return self.__inner['areaName'][0]['value']

  @property
  def country(self) -> str:
    """
    Returns:
      str: The country name.
    """

    return self.__inner['country'][0]['value']

class Astronomy:
  __slots__ = ('__inner',)

  def __init__(self, json: dict):
    self.__inner = json

  def __repr__(self) -> str:
    """
    Returns:
      str: The string representation of said object.
    """

    return f'<Astronomy moon_phase="{self.moon_phase!r}" sun_rise={self.sun_rise!r} sun_set={self.sun_set!r}>'

  @property
  def moon_illumination(self) -> int:
    """
    Returns:
      int: The illumination value of the moon.
    """

    return int(self.__inner['moon_illumination'])

  @property
  def moon_phase(self) -> MoonPhase:
    """
    Returns:
      MoonPhase: The moon phase.
    """

    return MoonPhase(self.__inner['moon_phase'])

  @property
  def moon_rise(self) -> Optional[time]:
    """
    Returns:
      time: The time when the moon rises. This can be `None`.
    """

    try:
      h12, m, ampm = TIME_REGEX.findall(self.__inner['moonrise'])[0]
      h24 = _convert_to_24h(h12, ampm)

      return time(h24, int(m))
    except:
      pass

  @property
  def moon_set(self) -> Optional[time]:
    """
    Returns:
      time: The time when the moon sets. This can be `None`.
    """

    try:
      h12, m, ampm = TIME_REGEX.findall(self.__inner['moonset'])[0]
      h24 = _convert_to_24h(h12, ampm)

      return time(h24, int(m))
    except:
      pass

  @property
  def sun_rise(self) -> Optional[time]:
    """
    Returns:
      time: The time when the sun rises. This can be `None`.
    """

    try:
      h12, m, ampm = TIME_REGEX.findall(self.__inner['sunrise'])[0]
      h24 = _convert_to_24h(h12, ampm)

      return time(h24, int(m))
    except:
      pass

  @property
  def sun_set(self) -> Optional[time]:
    """
    Returns:
      time: The time when the sun sets. This can be `None`.
    """

    try:
      h12, m, ampm = TIME_REGEX.findall(self.__inner['sunset'])[0]
      h24 = _convert_to_24h(h12, ampm)

      return time(h24, int(m))
    except:
      pass

# to minimize boilerplate code
class ModifiableFormat:
  __slots__ = ('__format',)

  def __init__(self, format: str):
    self.__format = format

  @property
  def format(self) -> str:
    """
    Returns:
      str: The format used here. This can be METRIC or IMPERIAL.
    """

    return self.__format

  @format.setter
  def format(self, to: auto):
    """
    Sets the format. This must be either METRIC or IMPERIAL.

    Args:
      to (str): The new format to be used. This must be either METRIC or IMPERIAL.

    Raises:
      Error: Invalid format type.
    """

    if to not in VALID_FORMATS:
      raise Error('Invalid format specified!')

    self.__format = to

class BaseForecast(ModifiableFormat):
  __slots__ = ('__inner',)

  def __init__(self, json: dict, format: str):
    self.__inner = json

    super().__init__(format)

  @property
  def uv_index(self) -> int:
    """
    Returns:
      int: The UV (ultraviolet) index value.
    """

    return int(self.__inner['uvIndex'])

  @property
  def feels_like(self) -> int:
    """
    Returns:
      int: What it felt like, in Celcius or Fahrenheit.
    """

    return int(self.__inner[f'FeelsLike{"C" if self._ModifiableFormat__format == METRIC else "F"}'])

  @property
  def humidity(self) -> int:
    """
    Returns:
      int: The humidity value in percent.
    """

    return int(self.__inner['humidity'])

  @property
  def temperature(self) -> int:
    """
    Returns:
      int: The weather temperature in either Celcius or Fahrenheit
    """

    return int(self.__inner[f'temp_{"C" if self._ModifiableFormat__format == METRIC else "F"}'])

  @property
  def precipitation(self) -> float:
    """
    Returns:
      float: The precipitation value in either Millimeters or Inches.
    """

    key = f'precip{"MM" if self._ModifiableFormat__format == METRIC else "Inches"}'
    return float(self.__inner[key])

  @property
  def pressure(self) -> float:
    """
    Returns:
      float: The pressure value in either Pascal or Inches.
    """

    key = f'pressure{"" if self._ModifiableFormat__format == METRIC else "Inches"}'
    return float(self.__inner[key])

  @property
  def visibility(self) -> int:
    """
    Returns:
      int: The visibility distance in either Kilometers or Miles.
    """

    key = f'visibility{"" if self._ModifiableFormat__format == METRIC else "Miles"}'
    return int(self.__inner[key])

  @property
  def wind_speed(self) -> int:
    """
    Returns:
      int: The wind speeds value in kmh or mph.
    """

    key = f'windspeed{"Kmph" if self._ModifiableFormat__format == METRIC else "Miles"}'
    return int(self.__inner[key])

  @property
  def wind_direction(self) -> WindDirection:
    """
    Returns:
      WindDirection: The wind direction value.
    """

    return WindDirection(self.__inner['winddir16Point'])

  @property
  def description(self) -> str:
    """
    Returns:
      str: The description regarding the forecast. This can be localized in different languages.
    """

    for k in self.__inner.keys():
      if k.startswith('lang_'):
        return self.__inner[k][0][value]

    return self.__inner['weatherDesc'][0]['value']

  @property
  def type(self) -> WeatherType:
    """
    Returns:
      WeatherType: The forecast type.
    """

    return WeatherType._new(int(
        self.__inner['weatherCode']))  # inspired by Rust <3

class CurrentForecast(BaseForecast):
  __slots__ = ()

  def __init__(self, json: dict, format: str):
    super().__init__(json, format)

  def __repr__(self) -> str:
    """
    Returns:
      str: The string representation of said object.
    """

    return f'<CurrentForecast temperature={self.temperature!r} description={self.description!r} type="{self.type!r}">'

  @property
  def local_timezone(self) -> timezone:
    """
    Returns:
      timezone: The local timezone (unnamed).
    """

    h_local, m_local, ampm_local = LOCAL_DATETIME_REGEX.findall(
        self._BaseForecast__inner['localObsDateTime'])[0]
    h_utc, m_utc, ampm_utc = UTC_DATETIME_REGEX.findall(
        self._BaseForecast__inner['observation_time'])[0]

    h_local_24h = _convert_to_24h(h_local, ampm_local)
    h_utc_24h = _convert_to_24h(h_utc, ampm_utc)

    return timezone(
        timedelta(hours=h_local_24h - h_utc_24h,
                  minutes=int(m_local) - int(m_utc)))

  @property
  def local_time(self) -> datetime:
    """
    Returns:
      datetime: The local time.
    """

    return datetime.strptime(self._BaseForecast__inner['localObsDateTime'],
                             '%Y-%m-%d %I:%M %p').astimezone(
                                 self.local_timezone)

  @property
  def utc_time(self) -> datetime:
    """
    Returns:
      datetime: The time in UTC.
    """

    return self.local_time.astimezone(timezone.utc)

class HourlyForecast(BaseForecast):

  def __init__(self, json: dict, format: str):
    # for inheritance purposes
    json['temp_C'] = json.pop('tempC')
    json['temp_F'] = json.pop('tempF')

    super().__init__(json, format)

  def __repr__(self) -> str:
    """
    Returns:
      str: The string representation of said object.
    """

    return f'<HourlyForecast time={self.time!r} temperature={self.temperature!r} description={self.description!r} type={self.type!r}>'

  @property
  def dew_point(self) -> int:
    """
    Returns:
      int: The dew point in either Celcius or Fahrenheit
    """

    return int(
        self._BaseForecast__inner[f'DewPoint{"C" if self._ModifiableFormat__format == METRIC else "F"}'])

  @property
  def heat_index(self) -> int:
    """
    Returns:
      int: The heat index in either Celcius or Fahrenheit
    """

    return int(
        self._BaseForecast__inner[f'HeatIndex{"C" if self._ModifiableFormat__format == METRIC else "F"}'])

  @property
  def wind_chill(self) -> int:
    """
    Returns:
      int: The wind chill value in either Celcius or Fahrenheit
    """

    return int(
        self._BaseForecast__inner[f'WindChill{"C" if self._ModifiableFormat__format == METRIC else "F"}'])

  @property
  def wind_gust(self) -> int:
    """
    Returns:
      int: The wind gust value in kmh or mph.
    """

    key = f'WindGust{"Kmph" if self._ModifiableFormat__format == METRIC else "Miles"}'
    return int(self._BaseForecast__inner[key])

  @property
  def chance_of_fog(self) -> int:
    """
    Returns:
      int: Chances of a fog in percent.
    """

    return int(self._BaseForecast__inner['chanceoffog'])

  @property
  def chance_of_frost(self) -> int:
    """
    Returns:
      int: Chances of a frost in percent.
    """

    return int(self._BaseForecast__inner['chanceoffrost'])

  @property
  def chance_of_hightemp(self) -> int:
    """
    Returns:
      int: Chances of a high temperature in percent.
    """

    return int(self._BaseForecast__inner['chanceofhightemp'])

  @property
  def chance_of_overcast(self) -> int:
    """
    Returns:
      int: Chances of an overcast in percent.
    """

    return int(self._BaseForecast__inner['chanceofovercast'])

  @property
  def chance_of_rain(self) -> int:
    """
    Returns:
      int: Chances of a rain in percent.
    """

    return int(self._BaseForecast__inner['chanceofrain'])

  @property
  def chance_of_rewdry(self) -> int:
    """
    Returns:
      int: Chances of a rew dry in percent.
    """

    return int(self._BaseForecast__inner['chanceofrewdry'])

  @property
  def chance_of_snow(self) -> int:
    """
    Returns:
      int: Chances of a snow in percent.
    """

    return int(self._BaseForecast__inner['chanceofsnow'])

  @property
  def chance_of_sunshine(self) -> int:
    """
    Returns:
      int: Chances of a sunshine in percent.
    """

    return int(self._BaseForecast__inner['chanceofsunshine'])

  @property
  def chance_of_thunder(self) -> int:
    """
    Returns:
      int: Chances of a thunder in percent.
    """

    return int(self._BaseForecast__inner['chanceofthunder'])

  @property
  def chance_of_windy(self) -> int:
    """
    Returns:
      int: Chances of windy in percent.
    """

    return int(self._BaseForecast__inner['chanceofwindy'])

  @property
  def cloud_cover(self) -> int:
    """
    Returns:
      int: Cloud cover value in percent.
    """

    return int(self._BaseForecast__inner['cloudcover'])

  @property
  def time(self) -> time:
    """
    Returns:
      time: The time in hours and minutes.
    """

    try:
      t = self._BaseForecast__inner['time']

      return time(int(t[:-2]), int(t[2:]))
    except ValueError:
      return time()

class DailyForecast(ModifiableFormat):
  __slots__ = ('__inner',)

  def __init__(self, json: dict, format: str):
    self.__inner = json

    super().__init__(format)

  def __repr__(self) -> str:
    """
    Returns:
      str: The string representation of said object.
    """

    return f'<DailyForecast date={self.date!r} astronomy={self.astronomy!r} temperature={self.temperature!r}>'

  @property
  def astronomy(self) -> Astronomy:
    """
    Returns:
      Astronomy: The astronomy information.
    """

    return Astronomy(self.__inner['astronomy'][0])

  @property
  def date(self) -> date:
    """
    Returns:
      date: The date for this forecast.
    """

    h, m, d = DATE_REGEX.findall(self.__inner['date'])[0]
    return date(int(h), int(m), int(d))

  @property
  def lowest_temperature(self) -> int:
    """
    Returns:
      int: The lowest temperature. In Celcius or Fahrenheit.
    """

    return int(self.__inner[f'mintemp{"C" if self._ModifiableFormat__format == METRIC else "F"}'])

  @property
  def highest_temperature(self) -> int:
    """
    Returns:
      int: The highest temperature. In Celcius or Fahrenheit.
    """

    return int(self.__inner[f'maxtemp{"C" if self._ModifiableFormat__format == METRIC else "F"}'])

  @property
  def temperature(self) -> int:
    """
    Returns:
      int: The average temperature. In Celcius or Fahrenheit.
    """

    return int(self.__inner[f'avgtemp{"C" if self._ModifiableFormat__format == METRIC else "F"}'])

  @property
  def sun_shines(self) -> float:
    """
    Returns:
      float: The amount of hours the sun shines.
    """

    return float(self.__inner['sunHour'])

  @property
  def snow_width(self) -> float:
    """
    Returns:
      float: Total snow width in either centimeters or inches.
    """

    width = float(self.__inner['totalSnow_cm'])
    return width if self._ModifiableFormat__format == METRIC else width / 2.54

  @property
  def uv_index(self) -> int:
    """
    Returns:
      int: The UV (ultraviolet) index value.
    """

    return int(self.__inner['uvIndex'])

  @property
  def hourly(self) -> Generator[HourlyForecast, None, None]:
    """
    Yields:
      Generator[HourlyForecast, None, None]: The hourly forecast for this day.
    """

    return (HourlyForecast(elem, self._ModifiableFormat__format)
            for elem in self.__inner['hourly'])

class Weather(ModifiableFormat):
  __slots__ = ('__inner',)

  def __init__(self, json: dict, format: str):
    self.__inner = json

    super().__init__(format)

  def __repr__(self) -> str:
    """
    Returns:
      str: The string representation of said object.
    """

    return f'<Weather current={self.current!r} location={self.location!r}>'

  @property
  def current(self) -> CurrentForecast:
    """
    Returns:
      CurrentForecast: The forecast for the current day.
    """

    return CurrentForecast(self.__inner['current_condition'][0],
                           self._ModifiableFormat__format)

  @property
  def nearest_area(self) -> NearestArea:
    """
    Returns:
      NearestArea: The nearest area.
    """

    return NearestArea(self.__inner['nearest_area'][0])

  @property
  def forecasts(self) -> Generator[DailyForecast, None, None]:
    """
    Yields:
      Generator[DailyForecast, None, None]: Daily forecasts.
    """

    return (DailyForecast(elem, self._ModifiableFormat__format)
            for elem in self.__inner['weather'])

  @property
  def location(self) -> Optional[Tuple[float, float]]:
    """
    Returns:
      Optional[Tuple[float, float]]: A tuple of Latitude and Longitude. This can be `None`.
    """

    try:
      for req in filter(lambda x: x['type'] == 'LatLon',
                        self.__inner['request']):
        lat, lon = LATLON_REGEX.findall(req['query'])[0]

        return float(lat), float(lon)
    except:
      pass
