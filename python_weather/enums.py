# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2021-2026 null8626

from enum import Enum

from .constants import KIND_EMOJIS, WIND_DIRECTION_EMOJIS


class BasicEnum(Enum):
  __slots__: tuple[str, ...] = ()

  def __repr__(self) -> str:
    return f'{self.__class__.__name__}.{self.name}'

  def __str__(self) -> str:
    return self.name.replace('_', ' ').title()

  @property
  def _index(self) -> int:
    return next(filter(lambda kind: self is kind[1], enumerate(self.__class__)))[0]


class IndexedEnum(Enum):
  __slots__: tuple[str, ...] = ('index',)

  index: int
  """The index value."""

  def __lt__(self, other: 'IndexedEnum | float | int') -> bool:
    return float(self.index) < float(other)

  def __le__(self, other: 'IndexedEnum | float | int') -> bool:
    return float(self.index) <= float(other)

  def __eq__(self, other: object) -> bool:
    if other_float := getattr(other, '__float__', None):
      return float(self.index) == other_float()

    return False  # pragma: nocover

  def __gt__(self, other: 'IndexedEnum | float | int') -> bool:
    return float(self.index) > float(other)

  def __ge__(self, other: 'IndexedEnum | float | int') -> bool:
    return float(self.index) >= float(other)

  def __hash__(self) -> int:
    return self.index

  def __int__(self) -> int:
    return self.index

  def __float__(self) -> float:
    return float(self.index)


class HeatIndex(IndexedEnum):
  """A heat index."""

  __slots__: tuple[str, ...] = ()

  CAUTION = None
  EXTREME_CAUTION = None
  DANGER = None
  EXTREME_DANGER = None

  @staticmethod
  def _new(celcius_index: int, true_index: int) -> 'HeatIndex':
    enum = HeatIndex(celcius_index)
    enum.index = true_index

    return enum

  @classmethod
  def _missing_(cls, value: object) -> 'HeatIndex | None':
    if isinstance(value, int):
      if value <= 32:
        return cls.CAUTION
      elif value <= 39:
        return cls.EXTREME_CAUTION
      elif value <= 51:
        return cls.DANGER
      else:
        return cls.EXTREME_DANGER


class UltraViolet(BasicEnum, IndexedEnum):
  """An ultra-violet (UV) index."""

  __slots__: tuple[str, ...] = ()

  LOW = None
  MODERATE = None
  HIGH = None
  VERY_HIGH = None
  EXTREME = None

  @staticmethod
  def _new(index: int) -> 'UltraViolet':
    enum = UltraViolet(index)
    enum.index = index

    return enum

  @classmethod
  def _missing_(cls, value: object) -> 'UltraViolet | None':
    if isinstance(value, int):
      if value <= 2:
        return cls.LOW
      elif value <= 5:
        return cls.MODERATE
      elif value <= 7:
        return cls.HIGH
      elif value <= 10:
        return cls.VERY_HIGH
      else:
        return cls.EXTREME


class WindDirection(BasicEnum):
  """A wind direction."""

  __slots__: tuple[str, ...] = ('degrees',)

  NORTH = 'N'
  NORTH_NORTHEAST = 'NNE'
  NORTHEAST = 'NE'
  EAST_NORTHEAST = 'ENE'
  EAST = 'E'
  EAST_SOUTHEAST = 'ESE'
  SOUTHEAST = 'SE'
  SOUTH_SOUTHEAST = 'SSE'
  SOUTH = 'S'
  SOUTH_SOUTHWEST = 'SSW'
  SOUTHWEST = 'SW'
  WEST_SOUTHWEST = 'WSW'
  WEST = 'W'
  WEST_NORTHWEST = 'WNW'
  NORTHWEST = 'NW'
  NORTH_NORTHWEST = 'NNW'

  degrees: float
  """The wind direction's value in degrees."""

  @staticmethod
  def _new(value: str, degrees: float) -> 'WindDirection':
    enum = WindDirection(value)
    enum.degrees = degrees

    return enum

  def __contains__(self, other: 'WindDirection | float | int') -> bool:
    members = list(self.__class__)

    return self is members[int(((float(other) % 360) + 11.25) // 22.5) % len(members)]

  def __int__(self) -> int:
    return int(self.degrees)

  def __float__(self) -> float:
    return self.degrees

  @property
  def emoji(self) -> str:
    """Emoji representation."""

    return WIND_DIRECTION_EMOJIS[int(((self.degrees + 22.5) % 360) // 45)]


class Locale(Enum):
  """Supported locales/languages."""

  __slots__: tuple[str, ...] = ()

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
    return f'{__class__.__name__}.{self.name}'

  def __str__(self) -> str:
    arr = self.name.title().split('_')

    return f'{" ".join(arr[:-1])} ({arr[-1]})' if len(arr) != 1 else arr[0]


class Kind(BasicEnum):
  """A weather forecast kind."""

  __slots__: tuple[str, ...] = ()

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
  def _missing_(cls, value: object) -> 'Kind | None':
    if value in (248, 260):
      return cls.FOG
    elif value in (263, 353):
      return cls.LIGHT_SHOWERS
    elif value in (362, 365, 374):
      return cls.LIGHT_SLEET_SHOWERS
    elif value in (185, 281, 284, 311, 314, 317, 350, 377):
      return cls.LIGHT_SLEET
    elif value == 386:
      return cls.THUNDERY_SHOWERS
    elif value == 320:
      return cls.LIGHT_SNOW
    elif value in (329, 332, 338):
      return cls.HEAVY_SNOW
    elif value in (293, 296):
      return cls.LIGHT_RAIN
    elif value in (305, 356):
      return cls.HEAVY_SHOWERS
    elif value in (308, 359):
      return cls.HEAVY_RAIN
    elif value in (326, 368):
      return cls.LIGHT_SNOW_SHOWERS
    elif value in (371, 395):
      return cls.HEAVY_SNOW_SHOWERS

  @property
  def emoji(self) -> str:
    """Emoji representation."""

    return KIND_EMOJIS[self._index]


class Phase(BasicEnum):
  """A moon phase."""

  __slots__: tuple[str, ...] = ()

  NEW_MOON = 'New Moon'
  WAXING_CRESCENT = 'Waxing Crescent'
  FIRST_QUARTER = 'First Quarter'
  WAXING_GIBBOUS = 'Waxing Gibbous'
  FULL_MOON = 'Full Moon'
  WANING_GIBBOUS = 'Waning Gibbous'
  LAST_QUARTER = 'Last Quarter'
  WANING_CRESCENT = 'Waning Crescent'

  @property
  def emoji(self) -> str:
    """Emoji representation."""

    return chr(0x1F311 + self._index)
