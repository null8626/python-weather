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

from typing import Iterable, Optional, Tuple
from datetime import datetime, date, time
from enum import auto

from .enums import Kind, Phase, WindDirection, Locale, UltraViolet
from .constants import VALID_UNITS, LATLON_REGEX, METRIC
from .base import BaseForecast, CustomizableBase
from .errors import Error

class Area:
  """Represents the location of the weather forecast."""
  
  __slots__ = ('__inner',)
  
  def __init__(self, json: dict):
    self.__inner = json
  
  def __repr__(self) -> str:
    """:class:`str`: The string representation of this object."""
    
    return f'<{self.__class__.__name__} name={self.name!r} country={self.country!r} region={self.region!r}>'
  
  @property
  def latitude(self) -> float:
    """:class:`float`: The :term:`latitude`."""
    
    return float(self.__inner['latitude'])
  
  @property
  def longitude(self) -> float:
    """:class:`float`: The :term:`longitude`."""
    
    return float(self.__inner['longitude'])
  
  @property
  def population(self) -> int:
    """:class:`float`: The location's population count."""
    
    return int(self.__inner['population'])
  
  @property
  def region(self) -> str:
    """:class:`str`: The location's region name."""
    
    return self.__inner['region'][0]['value']
  
  @property
  def name(self) -> str:
    """:class:`str`: The location's name."""
    
    return self.__inner['areaName'][0]['value']
  
  @property
  def country(self) -> str:
    """:class:`str`: The location's country name."""
    
    return self.__inner['country'][0]['value']

class Astronomy:
  """Represents the astronomical information of said weather forecast."""
  
  __slots__ = ('__inner',)
  
  def __init__(self, json: dict):
    self.__inner = json
  
  def __repr__(self) -> str:
    """:class:`str`: The string representation of this object."""
    
    return f'<{self.__class__.__name__} moon_phase="{self.moon_phase!r}" sun_rise={self.sun_rise!r} sun_set={self.sun_set!r}>'
  
  @property
  def moon_illumination(self) -> int:
    """:class:`int`: The percentage of the moon illuminated."""
    
    return int(self.__inner['moon_illumination'])
  
  @property
  def moon_phase(self) -> Phase:
    """:class:`Phase`: The moon's phase."""
    
    return Phase(self.__inner['moon_phase'])
  
  @property
  def moon_rise(self) -> Optional[time]:
    """Optional[:class:`time`]: The local time when the moon rises. This can be ``None``."""
    
    try:
      return datetime.strptime(self.__inner['moonrise'], '%I:%M %p').time()
    except ValueError:
      ...
  
  @property
  def moon_set(self) -> time:
    """Optional[:class:`time`]: The local time when the moon sets. This can be ``None``."""
    
    try:
      return datetime.strptime(self.__inner['moonset'], '%I:%M %p').time()
    except ValueError:
      ...
  
  @property
  def sun_rise(self) -> Optional[time]:
    """Optional[:class:`time`]:  The local time when the sun rises. This can be ``None``."""
    
    try:
      return datetime.strptime(self.__inner['sunrise'], '%I:%M %p').time()
    except ValueError:
      ...
  
  @property
  def sun_set(self) -> Optional[time]:
    """Optional[:class:`time`]: The local time when the sun sets. This can be ``None``."""
    
    try:
      return datetime.strptime(self.__inner['sunset'], '%I:%M %p').time()
    except ValueError:
      ...

class CurrentForecast(BaseForecast):
  """Represents a weather forecast of the current day."""
  
  __slots__ = ()
  
  def __repr__(self) -> str:
    """:class:`str`: The string representation of said object."""
    
    return f'<{self.__class__.__name__} temperature={self.temperature!r} description={self.description!r} kind="{self.kind!r}">'
  
  @property
  def local_time(self) -> datetime:
    """:class:`datetime`: The local time of this weather forecast."""
    
    return datetime.strptime(
      self._BaseForecast__inner['localObsDateTime'], '%Y-%m-%d %I:%M %p'
    )

class HourlyForecast(BaseForecast):
  """Represents a weather forecast of a specific hour."""
  
  __slots__ = ()
  
  def __init__(self, json: dict, unit: auto, locale: Locale):
    # for inheritance purposes
    json['temp_C'] = json.pop('tempC')
    json['temp_F'] = json.pop('tempF')
    
    super().__init__(json, unit, locale)
  
  def __repr__(self) -> str:
    """:class:`str`: The string representation of this object."""
    
    return f'<{self.__class__.__name__} time={self.time!r} temperature={self.temperature!r} description={self.description!r} kind={self.kind!r}>'
  
  @property
  def dew_point(self) -> int:
    """:class:`int`: The dew point in either Celcius or Fahrenheit."""
    
    return int(
      self._BaseForecast__inner[
        f'DewPoint{"C" if self._CustomizableBase__unit == METRIC else "F"}']
    )
  
  @property
  def heat_index(self) -> int:
    """:class:`int`: The heat index in either Celcius or Fahrenheit."""
    
    return int(
      self._BaseForecast__inner[
        f'HeatIndex{"C" if self._CustomizableBase__unit == METRIC else "F"}']
    )
  
  @property
  def wind_chill(self) -> int:
    """:class:`int`: The wind chill value in either Celcius or Fahrenheit."""
    
    return int(
      self._BaseForecast__inner[
        f'WindChill{"C" if self._CustomizableBase__unit == METRIC else "F"}']
    )
  
  @property
  def wind_gust(self) -> int:
    """:class:`int`: The wind gust value in either Kilometers per hour or Miles per hour."""
    
    key = f'WindGust{"Kmph" if self._CustomizableBase__unit == METRIC else "Miles"}'
    return int(self._BaseForecast__inner[key])
  
  @property
  def chances_of_fog(self) -> int:
    """:class:`int`: Chances of a fog in percent."""
    
    return int(self._BaseForecast__inner['chanceoffog'])
  
  @property
  def chances_of_frost(self) -> int:
    """:class:`int`: Chances of a frost in percent."""
    
    return int(self._BaseForecast__inner['chanceoffrost'])
  
  @property
  def chances_of_hightemp(self) -> int:
    """:class:`int`: Chances of a high temperature in percent."""
    
    return int(self._BaseForecast__inner['chanceofhightemp'])
  
  @property
  def chances_of_overcast(self) -> int:
    """:class:`int`: Chances of an overcast in percent."""
    
    return int(self._BaseForecast__inner['chanceofovercast'])
  
  @property
  def chances_of_rain(self) -> int:
    """:class:`int`: Chances of a rain in percent."""
    
    return int(self._BaseForecast__inner['chanceofrain'])
  
  @property
  def chances_of_remdry(self) -> int:
    """:class:`int`: Chances of a rem dry in percent."""
    
    return int(self._BaseForecast__inner['chanceofremdry'])
  
  @property
  def chances_of_snow(self) -> int:
    """:class:`int`: Chances of a snow in percent."""
    
    return int(self._BaseForecast__inner['chanceofsnow'])
  
  @property
  def chances_of_sunshine(self) -> int:
    """:class:`int`: Chances of a sunshine in percent."""
    
    return int(self._BaseForecast__inner['chanceofsunshine'])
  
  @property
  def chances_of_thunder(self) -> int:
    """:class:`int`: Chances of a thunder in percent."""
    
    return int(self._BaseForecast__inner['chanceofthunder'])
  
  @property
  def chances_of_windy(self) -> int:
    """:class:`int`: Chances of windy in percent."""
    
    return int(self._BaseForecast__inner['chanceofwindy'])
  
  @property
  def cloud_cover(self) -> int:
    """:class:`int`: The Cloud cover value in percent."""
    
    return int(self._BaseForecast__inner['cloudcover'])
  
  @property
  def local_time(self) -> time:
    """:class:`time`: The local time in hours and minutes."""
    
    try:
      t = self._BaseForecast__inner['time']
      
      return time(int(t[:-2]), int(t[2:]))
    except ValueError:
      return time()

class DailyForecast(CustomizableBase):
  __slots__ = ('__inner',)
  
  def __init__(self, json: dict, unit: auto, locale: Locale):
    self.__inner = json
    
    super().__init__(unit, locale)
  
  def __repr__(self) -> str:
    """:class:`str`: The string representation of this object."""
    
    return f'<{self.__class__.__name__} date={self.date!r} astronomy={self.astronomy!r} temperature={self.temperature!r}>'
  
  @property
  def astronomy(self) -> Astronomy:
    """:class:`Astronomy`: The astronomical information of said weather forecast."""
    
    return Astronomy(self.__inner['astronomy'][0])
  
  @property
  def local_date(self) -> date:
    """:class:`date`: The local date of this forecast."""
    
    return datetime.strptime(self.__inner['date'], '%Y-%m-%d').date()
  
  @property
  def lowest_temperature(self) -> int:
    """:class:`int`: The lowest temperature in either Celcius or Fahrenheit."""
    
    return int(
      self.__inner[
        f'mintemp{"C" if self._CustomizableBase__unit == METRIC else "F"}']
    )
  
  @property
  def highest_temperature(self) -> int:
    """:class:`int`: The highest temperature in either Celcius or Fahrenheit."""
    
    return int(
      self.__inner[
        f'maxtemp{"C" if self._CustomizableBase__unit == METRIC else "F"}']
    )
  
  @property
  def temperature(self) -> int:
    """:class:`int`: The average temperature in either Celcius or Fahrenheit."""
    
    return int(
      self.__inner[
        f'avgtemp{"C" if self._CustomizableBase__unit == METRIC else "F"}']
    )
  
  @property
  def sun_shines(self) -> float:
    """:class:`float`: Hours of sunlight."""
    
    return float(self.__inner['sunHour'])
  
  @property
  def snow_width(self) -> float:
    """:class:`float`: Total snowfall in either Centimeters or Inches."""
    
    width = float(self.__inner['totalSnow_cm'])
    return width if self._CustomizableBase__unit == METRIC else width / 2.54
  
  @property
  def ultra_violet(self) -> UltraViolet:
    """:class:`UltraViolet`: The UV (:term:`ultraviolet`) index."""
    
    return UltraViolet(int(self.__inner['uvIndex']))
  
  @property
  def hourly(self) -> Iterable[HourlyForecast]:
    """Iterable[:class:`HourlyForecast`]: The hourly forecasts of this day."""
    
    return (
      HourlyForecast(
        elem, self._CustomizableBase__unit, self._CustomizableBase__locale
      ) for elem in self.__inner['hourly']
    )

class Weather(CustomizableBase):
  """Represents an entire weather forecast."""
  
  __slots__ = ('__inner',)
  
  def __init__(self, json: dict, unit: auto, locale: Locale):
    self.__inner = json
    
    super().__init__(unit, locale)
  
  def __repr__(self) -> str:
    """:class:`str`: The string representation of this object."""
    
    return f'<{self.__class__.__name__} current={self.current!r} location={self.location!r}>'
  
  @property
  def current(self) -> CurrentForecast:
    """:class:`CurrentForecast`: The forecast of the current day."""
    
    return CurrentForecast(
      self.__inner['current_condition'][0], self._CustomizableBase__unit,
      self._CustomizableBase__locale
    )
  
  @property
  def nearest_area(self) -> Area:
    """:class:`Area`: The information of the nearest area of the current weather forecast."""
    
    return Area(self.__inner['nearest_area'][0])
  
  @property
  def forecasts(self) -> Iterable[DailyForecast]:
    """Iterable[:class:`DailyForecast`]: Daily forecasts of the current weather forecast."""
    
    return (
      DailyForecast(
        elem, self._CustomizableBase__unit, self._CustomizableBase__locale
      ) for elem in self.__inner['weather']
    )
  
  @property
  def location(self) -> Optional[Tuple[float, float]]:
    """Optional[Tuple[:class:`float`, :class:`float`]]: A tuple of both :term:`latitude` and :term:`longitude`. This can be ``None``."""
    
    try:
      for req in filter(
        lambda x: x['type'] == 'LatLon', self.__inner['request']
      ):
        lat, lon = LATLON_REGEX.findall(req['query'])[0]
        
        return float(lat), float(lon)
    except:
      ...
