"""
The MIT License (MIT)

Copyright (c) 2021-2024 null (https://github.com/null8626)

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
from typing import Union

from .errors import Error

class BasicEnum(Enum):
  __slots__ = ()
  
  def __repr__(self) -> str:
    """:class:`str`: The string representation of this :class:`Enum`."""
    
    return f'{self.__class__.__name__}.{self.name}'
  
  def __str__(self) -> str:
    """:class:`str`: The stylized name for this :class:`Enum`."""
    
    return self.name.replace('_', ' ').title()

class Ultraviolet(Enum):
  """Represents a :term:`UV index`."""
  
  __slots__ = ('__index',)
  
  LOW = 13
  MODERATE = auto()
  HIGH = auto()
  VERY_HIGH = auto()
  EXTREME = auto()
  
  def _new(index: int):
    enum = Ultraviolet(index)
    enum.__index = index
    
    return enum
  
  @classmethod
  def _missing_(self, index: int):
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
  
  def __repr__(self) -> str:
    """:class:`str`: The string representation of this :class:`Enum`."""
    
    return f'<{self.__class__.__name__}.{self.name} index={self.__index}>'
  
  def __str__(self) -> str:
    """:class:`str`: The stylized name for this :class:`Enum`."""
    
    return self.name.replace('_', ' ').title()
  
  def __lt__(self, other: Union["Ultraviolet", int, float]) -> bool:
    """
    Checks if this :class:`Enum`'s ultraviolet index is less than the other ultraviolet index.
    
    Parameters
    ----------
    other: Union[:class:`Ultraviolet`, :class:`int`, :class:`float`]
      The other ultraviolet index to compare. Besides :class:`int` and :class:`float`, this also works for any type that can be compared with an :class:`int`.
    
    Raises
    ------
    TypeError
      If the ``other`` argument's type is incompatible.
    
    Returns
    -------
    :class:`bool`
    """
    
    if isinstance(other, self.__class__):
      return self.__index < other.index
    else:
      return self.__index < other
  
  def __eq__(self, other: Union["Ultraviolet", int, float]) -> bool:
    """
    Checks if this :class:`Enum`'s ultraviolet index is equal to the other ultraviolet index.
    
    Parameters
    ----------
    other: Union[:class:`Ultraviolet`, :class:`int`, :class:`float`]
      The other ultraviolet index to compare. Besides :class:`int` and :class:`float`, this also works for any type that can be compared with an :class:`int`.
    
    Raises
    ------
    TypeError
      If the ``other`` argument's type is incompatible.
    
    Returns
    -------
    :class:`bool`
    """
    
    if isinstance(other, self.__class__):
      return self.__index == other.index
    else:
      return self.__index == other
  
  def __gt__(self, other: Union["Ultraviolet", int, float]) -> bool:
    """
    Checks if this :class:`Enum`'s ultraviolet index is greater than the other ultraviolet index.
    
    Parameters
    ----------
    other: Union[:class:`Ultraviolet`, :class:`int`, :class:`float`]
      The other ultraviolet index to compare. Besides :class:`int` and :class:`float`, this also works for any type that can be compared with an :class:`int`.
    
    Raises
    ------
    TypeError
      If the ``other`` argument's type is incompatible.
    
    Returns
    -------
    :class:`bool`
    """
    
    if isinstance(other, self.__class__):
      return self.__index > other.index
    else:
      return self.__index > other
  
  def __hash__(self) -> int:
    """:class:`int`: A hashed version of this :class:`Enum`."""
    
    return self.__index
  
  def __int__(self) -> int:
    """:class:`int`: The ultraviolet index."""
    
    return self.__index
  
  @property
  def index(self) -> int:
    """:class:`int`: The ultraviolet index."""
    
    return self.__index

class WindDirection(Enum):
  """Represents a wind direction."""
  
  __slots__ = ('__degrees',)
  
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
  
  def _new(value: str, degrees: float):
    enum = WindDirection(value)
    enum.__degrees = degrees
    
    return enum
  
  def __repr__(self) -> str:
    """:class:`str`: The string representation of this :class:`Enum`."""
    
    return f'<{self.__class__.__name__}.{self.name} degrees={self.__degrees!r}>'
  
  def __str__(self) -> str:
    """:class:`str`: The stylized name for this :class:`Enum`."""
    
    return self.name.replace('_', ' ').title()
  
  def __contains__(self, other: Union["WindDirection", float, int]) -> bool:
    """
    Checks if the other degrees value is a part of this :class:`Enum`'s wind direction category.
    
    Parameters
    ----------
    other: Union[:class:`WindDirection`, :class:`int`, :class:`float`]
      The other degrees value to compare. Besides :class:`int` and :class:`float`, this also works for any type that can be compared with a :class:`float`.
    
    Raises
    ------
    TypeError
      If the ``other`` argument's type is incompatible.
    
    Returns
    -------
    :class:`bool`
    """
    
    if isinstance(other, self.__class__):
      other = other.degrees
    
    if self is self.NORTH:
      return other > 348.75 or other <= 11.25
    elif self is self.NORTH_NORTHEAST:
      return 11.25 < other <= 33.75
    elif self is self.NORTHEAST:
      return 33.75 < other <= 56.25
    elif self is self.EAST_NORTHEAST:
      return 56.25 < other <= 78.75
    elif self is self.EAST:
      return 78.75 < other <= 101.25
    elif self is self.EAST_SOUTHEAST:
      return 101.25 < other <= 123.75
    elif self is self.SOUTHEAST:
      return 123.75 < other <= 146.25
    elif self is self.SOUTH_SOUTHEAST:
      return 146.25 < other <= 168.75
    elif self is self.SOUTH:
      return 168.75 < other <= 191.25
    elif self is self.SOUTH_SOUTHWEST:
      return 191.25 < other <= 213.75
    elif self is self.SOUTHWEST:
      return 213.75 < other <= 236.25
    elif self is self.WEST_SOUTHWEST:
      return 236.25 < other <= 258.75
    elif self is self.WEST:
      return 258.75 < other <= 281.25
    elif self is self.WEST_NORTHWEST:
      return 281.25 < other <= 303.75
    elif self is self.NORTHWEST:
      return 303.75 < other <= 326.25
    else:
      return 326.25 < other <= 348.75
  
  @property
  def degrees(self) -> int:
    """:class:`int`: The wind direction's value in degrees."""
    
    return self.__degrees

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
  
  def __repr__(self) -> str:
    """:class:`str`: The string representation of this :class:`Enum`."""
    
    return f'{self.__class__.__name__}.{self.name}'
  
  def __str__(self) -> str:
    """:class:`str`: The stylized name for this :class:`Enum`."""
    
    arr = self.name.title().split('_')
    return f'{arr[:-1].join(" ")} ({arr[-1]})' if len(arr) != 1 else arr[0]

class Kind(BasicEnum):
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
  def _missing_(self, value: int):
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

class Phase(BasicEnum):
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
