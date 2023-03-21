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

from enum import Enum, auto

from .enums import Direction, Kind, Locale, UltraViolet
from .constants import METRIC, VALID_FORMATS

class CustomizableBase:
  __slots__ = ('__unit', '__locale')
  
  def __init__(self, unit: auto, locale: Locale):
    self.unit = unit
    self.locale = locale
  
  @property
  def unit(self) -> auto:
    """:class:`auto`: The measuring unit used to display information in this object."""
    
    return self.__unit
  
  @unit.setter
  def unit(self, to: auto):
    """
    Sets the default measuring unit used to display information in this object.
    
    Parameters
    ----------
    to: :class:`auto`
      The new default measuring unit to be used to display information in this object. Must be either :attr:`METRIC` or :attr:`IMPERIAL`.

    Raises
    ------
    Error
      If the ``to`` argument is not either :attr:`METRIC` or :attr:`IMPERIAL`.
    """
    
    if to not in VALID_FORMATS:
      raise Error('Invalid measuring unit specified!')
    
    self.__unit = to
  
  @property
  def locale(self) -> Locale:
    """:class:`Locale`: The :term:`localization`/translation/language used to display information in this object."""
    
    return self.__locale
  
  @locale.setter
  def locale(self, to: Locale):
    """
    Sets the default :term:`localization`/translation/language used to display information in this object.
    
    Parameters
    ----------
    to: :class:`Locale`
      The new :term:`localization`/translation/language to be used to display information in this object.

    Raises
    ------
    Error
      If the ``to`` argument is not a part of the :class:`Locale` :class:`Enum`.
    """
    
    if not isinstance(to, Locale):
      raise Error(f'Expected {to!r} to be a Locale enum')
    
    self.__locale = to

class BaseForecast(CustomizableBase):
  __slots__ = ('__inner',)
  
  def __init__(self, json: dict, unit: auto, locale: Locale):
    self.__inner = json
    
    super().__init__(unit, locale)
  
  @property
  def ultra_violet(self) -> UltraViolet:
    """:class:`UltraViolet`: The UV (:term:`ultraviolet`) index."""
    
    return UltraViolet(int(self.__inner['uvIndex']))
  
  @property
  def feels_like(self) -> int:
    """:class:`int`: What it felt like, in Celcius or Fahrenheit."""
    
    return int(
      self.__inner[
        f'FeelsLike{"C" if self._CustomizableBase__unit == METRIC else "F"}']
    )
  
  @property
  def humidity(self) -> int:
    """:class:`int`: The humidity value in percent."""
    
    return int(self.__inner['humidity'])
  
  @property
  def temperature(self) -> int:
    """:class:`int`: The weather temperature in either Celcius or Fahrenheit."""
    
    return int(
      self.
      __inner[f'temp_{"C" if self._CustomizableBase__unit == METRIC else "F"}']
    )
  
  @property
  def precipitation(self) -> float:
    """:class:`float`: The precipitation in either Millimeters or Inches."""
    
    return float(
      self.__inner[
        f'precip{"MM" if self._CustomizableBase__unit == METRIC else "Inches"}']
    )
  
  @property
  def pressure(self) -> float:
    """:class:`float`: The pressure in either Pascal or Inches."""
    
    return float(
      self.__inner[
        f'pressure{"" if self._CustomizableBase__unit == METRIC else "Inches"}']
    )
  
  @property
  def visibility(self) -> int:
    """:class:`int`: The visibility distance in either Kilometers or Miles."""
    
    return int(
      self.__inner[
        f'visibility{"" if self._CustomizableBase__unit == METRIC else "Miles"}'
      ]
    )
  
  @property
  def wind_speed(self) -> int:
    """:class:`int`: The wind speeds in either Kilometers per hour or Miles per hour."""
    
    return int(
      self.__inner[
        f'windspeed{"Kmph" if self._CustomizableBase__unit == METRIC else "Miles"}'
      ]
    )
  
  @property
  def wind_direction(self) -> Direction:
    """:class:`Direction`: The wind direction."""
    
    return Direction(self.__inner['winddir16Point'])
  
  @property
  def description(self) -> str:
    """:class:`str`: The description regarding the forecast. This can be localized in different languages depending on the :term:`localization`/translation used."""
    
    return self.__inner['weatherDesc'][0]['value'] if self._CustomizableBase__locale == Locale.ENGLISH else self.__inner[f'lang_{self._CustomizableBase__locale.value}'][0]['value']
  
  @property
  def kind(self) -> Kind:
    """:class:`Kind`: The kind of the weather."""
    
    return Kind(int(self.__inner['weatherCode']))
