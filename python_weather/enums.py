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

from .errors import Error
from typing import Union, Self
from enum import Enum, auto

class UltraViolet(Enum):
  """Represents a :term:`UV index`."""
  
  __slots__ = ()
  
  LOW = auto()
  MODERATE = auto()
  HIGH = auto()
  VERY_HIGH = auto()
  EXTREME = auto()
  
  @classmethod
  def _missing_(self, index: int) -> Self:
    if index <= 2:
      return self.LOW
    elif index <= 5:
      return self.MODERATE
    elif index <= 7:
      return self.HIGH
    elif index <= 10:
      return self.VERY_HIGH
    else:
      return self.EXTREME
  
  def __str__(self) -> str:
    """:class:`str`: The stylized name for this :class:`Enum`."""
    
    return self.name.replace('_', ' ').title()

class Direction(Enum):
  """Represents a wind direction."""
  
  __slots__ = ()
  
  NORTH = "N"
  NORTH_NORTHEAST = "NNE"
  NORTHEAST = "NE"
  EAST_NORTHEAST = "ENE"
  EAST = "E"
  EAST_SOUTHEAST = "ESE"
  SOUTHEAST = "SE"
  SOUTH_SOUTHEAST = "SSE"
  SOUTH = "S"
  SOUTH_SOUTHWEST = "SSW"
  SOUTHWEST = "SW"
  WEST_SOUTHWEST = "WSW"
  WEST = "W"
  WEST_NORTHWEST = "WNW"
  NORTHWEST = "NW"
  NORTH_NORTHWEST = "NNW"
  
  def __str__(self) -> str:
    """:class:`str`: The stylized name for this :class:`Enum`."""
    
    return self.name.replace('_', ' ').title()
  
  def __contains__(self, degrees: Union[float, int]) -> bool:
    """
    Checks if the degrees value is a part of this wind direction.
    
    Parameters
    ----------
    degrees: Union[:class:`float`, :class:`int`]
      The degrees value. Must be between 0 and 360.
    
    Raises
    ------
    Error
      Invalid ``degrees`` argument.
    
    Returns
    -------
    :class:`bool`
      The boolean.
    """
    
    if not ((isinstance(degrees, int) or isinstance(degrees, float)) and
            0 <= degrees <= 360):
      raise Error('Invalid degrees value.')
    elif self is self.NORTH:
      return degrees > 348.75 or degrees <= 11.25
    elif self is self.NORTH_NORTHEAST:
      return 11.25 < degrees <= 33.75
    elif self is self.NORTHEAST:
      return 33.75 < degrees <= 56.25
    elif self is self.EAST_NORTHEAST:
      return 56.25 < degrees <= 78.75
    elif self is self.EAST:
      return 78.75 < degrees <= 101.25
    elif self is self.EAST_SOUTHEAST:
      return 101.25 < degrees <= 123.75
    elif self is self.SOUTHEAST:
      return 123.75 < degrees <= 146.25
    elif self is self.SOUTH_SOUTHEAST:
      return 146.25 < degrees <= 168.75
    elif self is self.SOUTH:
      return 168.75 < degrees <= 191.25
    elif self is self.SOUTH_SOUTHWEST:
      return 191.25 < degrees <= 213.75
    elif self is self.SOUTHWEST:
      return 213.75 < degrees <= 236.25
    elif self is self.WEST_SOUTHWEST:
      return 236.25 < degrees <= 258.75
    elif self is self.WEST:
      return 258.75 < degrees <= 281.25
    elif self is self.WEST_NORTHWEST:
      return 281.25 < degrees <= 303.75
    elif self is self.NORTHWEST:
      return 303.75 < degrees <= 326.25
    else:
      return 326.25 < degrees <= 348.75

class Locale(Enum):
  """Represents the list of supported :term:`locales`/languages by this library."""
  
  __slots__ = ()
  
  AFRIKAANS = 'af'
  AMHARIC = 'am'
  ARABIC = 'ar'
  ARMENIAN = 'hy'
  AZERBAIJANI = 'az'
  BANGLA = 'bn'
  BASQUE = 'eu'
  BELARUSIAN = 'be'
  BOSNIAN = 'bs'
  BULGARIAN = 'bg'
  CATALAN = 'ca'
  CHINESE_SIMPLIFIED = 'zh'
  CHINESE_SIMPLIFIED_CHINA = 'zh-cn'
  CHINESE_TRADITIONAL_TAIWAN = 'zh-tw'
  CROATIAN = 'hr'
  CZECH = 'cs'
  DANISH = 'da'
  DUTCH = 'nl'
  ENGLISH = 'en'
  ESPERANTO = 'eo'
  ESTONIAN = 'et'
  FINNISH = 'fi'
  FRENCH = 'fr'
  FRISIAN = 'fy'
  GALICIAN = 'gl'
  GEORGIAN = 'ka'
  GERMAN = 'de'
  GREEK = 'el'
  HINDI = 'hi'
  HIRI_MOTU = 'ho'
  HUNGARIAN = 'hu'
  ICELANDIC = 'is'
  INDONESIAN = 'id'
  INTERLINGUA = 'ia'
  IRISH = 'ga'
  ITALIAN = 'it'
  JAPANESE = 'ja'
  JAVANESE = 'jv'
  KAZAKH = 'kk'
  KISWAHILI = 'sw'
  KOREAN = 'ko'
  KYRGYZ = 'ky'
  LATVIAN = 'lv'
  LITHUANIAN = 'lt'
  MACEDONIAN = 'mk'
  MALAGASY = 'mg'
  MALAYALAM = 'ml'
  MARATHI = 'mr'
  NORWEGIAN_BOKMAL = 'nb'
  NORWEGIAN_NYNORSK = 'nn'
  OCCITAN = 'oc'
  PERSIAN = 'fa'
  POLISH = 'pl'
  PORTUGUESE = 'pt'
  PORTUGUESE_BRAZIL = 'pt-br'
  ROMANIAN = 'ro'
  RUSSIAN = 'ru'
  SERBIAN = 'sr'
  SERBIAN_LATIN = 'sr-lat'
  SLOVAK = 'sk'
  SLOVENIAN = 'sl'
  SPANISH = 'es'
  SWEDISH = 'sv'
  TAMIL = 'ta'
  TELUGU = 'te'
  THAI = 'th'
  TURKISH = 'tr'
  UKRAINIAN = 'uk'
  UZBEK = 'uz'
  VIETNAMESE = 'vi'
  WELSH = 'cy'
  ZULU = 'zu'
  
  def __str__(self) -> str:
    """:class:`str`: The stylized name for this :class:`Enum`."""
    
    arr = self.name.title().split('_')
    return f'{arr[:-1].join(" ")} ({arr[-1]})' if len(arr) != 1 else arr[0]

class Kind(Enum):
  """Represents a weather forecast kind."""
  
  __slots__ = ()
  
  SUNNY = 113
  PARTLY_CLOUDY = 116
  CLOUDY = 119
  VERY_CLOUDY = 122
  FOG = 143
  LIGHT_SHOWERS = 176
  LIGHT_SLEET_SHOWERS = 179
  LIGHT_SLEET = 182
  THUNDERY_SHOWERS = 200
  LIGHT_SNOW = 227
  HEAVY_SNOW = 230
  LIGHT_RAIN = 266
  HEAVY_SHOWERS = 299
  HEAVY_RAIN = 302
  LIGHT_SNOW_SHOWERS = 323
  HEAVY_SNOW_SHOWERS = 335
  THUNDERY_HEAVY_RAIN = 389
  THUNDERY_SNOW_SHOWERS = 392
  
  @classmethod
  def _missing_(self, value: int) -> Self:
    if value == 248 or value == 260:
      return self.FOG
    elif value == 263 or value == 353:
      return self.LIGHT_SHOWERS
    elif value == 362 or value == 365 or value == 374:
      return self.LIGHT_SLEET_SHOWERS
    elif value == 185 or value == 281 or value == 284 or value == 311 or value == 314 or value == 317 or value == 350 or value == 377:
      return self.LIGHT_SLEET
    elif value == 386:
      return self.THUNDERY_SHOWERS
    elif value == 320:
      return self.LIGHT_SNOW
    elif value == 329 or value == 332 or value == 338:
      return self.HEAVY_SNOW
    elif value == 293 or value == 296:
      return self.LIGHT_RAIN
    elif value == 305 or value == 356:
      return self.HEAVY_SHOWERS
    elif value == 308 or value == 359:
      return self.HEAVY_RAIN
    elif value == 326 or value == 368:
      return self.LIGHT_SNOW_SHOWERS
    elif value == 371 or value == 395:
      return self.HEAVY_SNOW_SHOWERS
  
  def __str__(self) -> str:
    """:class:`str`: The stylized name for this :class:`Enum`."""
    
    return self.name.replace('_', ' ').title()
  
  @property
  def emoji(self) -> str:
    """:class:`str`: The emoji representing this :class:`Enum`."""
    
    if self is self.CLOUDY:
      return '☁️'
    elif self is self.FOG:
      return '🌫'
    elif self is self.HEAVY_RAIN:
      return '🌧'
    elif self is self.HEAVY_SHOWERS:
      return '🌧'
    elif self is self.HEAVY_SNOW:
      return '❄️'
    elif self is self.HEAVY_SNOW_SHOWERS:
      return '❄️'
    elif self is self.LIGHT_RAIN:
      return '🌦'
    elif self is self.LIGHT_SHOWERS:
      return '🌦'
    elif self is self.LIGHT_SLEET:
      return '🌧'
    elif self is self.LIGHT_SLEET_SHOWERS:
      return '🌧'
    elif self is self.LIGHT_SNOW:
      return '🌨'
    elif self is self.LIGHT_SNOW_SHOWERS:
      return '🌨'
    elif self is self.PARTLY_CLOUDY:
      return '⛅️'
    elif self is self.SUNNY:
      return '☀️'
    elif self is self.THUNDERY_HEAVY_RAIN:
      return '🌩'
    elif self is self.THUNDERY_SHOWERS:
      return '⛈'
    elif self is self.THUNDERY_SNOW_SHOWERS:
      return '⛈'
    elif self is self.VERY_CLOUDY:
      return '☁️'
    else:
      return '✨'

class Phase(Enum):
  """Represents a moon phase."""
  
  __slots__ = ()
  
  NEW_MOON = 'New Moon'
  WAXING_CRESCENT = 'Waxing Crescent'
  FIRST_QUARTER = 'First Quarter'
  Waxing_GIBBOUS = 'Waxing Gibbous'
  FULL_MOON = 'Full Moon'
  WANING_GIBBOUS = 'Waning Gibbous'
  LAST_QUARTER = 'Last Quarter'
  WANING_CRESCENT = 'Waning Crescent'
  
  def __str__(self) -> str:
    """:class:`str`: The stylized name for this :class:`Enum`."""
    
    return self.value
  
  @property
  def emoji(self) -> str:
    """:class:`str`: The stylized name for this :class:`Enum`."""
    
    if self is self.NEW_MOON:
      return '🌑'
    elif self is self.WAXING_CRESCENT:
      return '🌒'
    elif self is self.FIRST_QUARTER:
      return '🌓'
    elif self is self.Waxing_GIBBOUS:
      return '🌔'
    elif self is self.FULL_MOON:
      return '🌕'
    elif self is self.WANING_GIBBOUS:
      return '🌖'
    elif self is self.LAST_QUARTER:
      return '🌗'
    else:
      return '🌘'
