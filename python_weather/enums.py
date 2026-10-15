# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2021-2026 null8626

from enum import Enum

from .constants import KIND_EMOJIS, WIND_DIRECTION_EMOJIS


class BasicEnum(Enum):
  """An ordinary enum."""

  __slots__: tuple[str, ...] = ()

  def __repr__(self) -> str:
    """The enum's debug string representation."""
    return f'{self.__class__.__name__}.{self.name}'

  def __str__(self) -> str:
    """The enum's friendly name."""
    return self.name.replace('_', ' ').title()

  @property
  def _index(self) -> int:
    return next(filter(lambda kind: self is kind[1], enumerate(self.__class__)))[0]


class IndexedEnum(Enum):
  """An enum that carries an index value."""

  __slots__: tuple[str, ...] = ('index',)

  index: int
  """The index value."""

  def __lt__(self, other: 'IndexedEnum | float | int') -> bool:
    """Checks if the enum's index value is less than the other."""
    return float(self.index) < float(other)

  def __le__(self, other: 'IndexedEnum | float | int') -> bool:
    """Checks if the enum's index value is less than or equal to the other."""
    return float(self.index) <= float(other)

  def __eq__(self, other: object) -> bool:
    """Checks if the enum's index value is equal to the other."""
    if other_float := getattr(other, '__float__', None):
      return float(self.index) == other_float()

    return False  # pragma: nocover

  def __gt__(self, other: 'IndexedEnum | float | int') -> bool:
    """Checks if the enum's index value is greater than the other."""
    return float(self.index) > float(other)

  def __ge__(self, other: 'IndexedEnum | float | int') -> bool:
    """Checks if the enum's index value is greater than or equal to the other."""
    return float(self.index) >= float(other)

  def __hash__(self) -> int:
    """The enum's index value."""
    return self.index

  def __int__(self) -> int:
    """The enum's index value."""
    return self.index

  def __float__(self) -> float:
    """The floating point representation of the enum's index value."""
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
  """The wind direction's angle in degrees."""

  @staticmethod
  def _new(value: str, degrees: float) -> 'WindDirection':
    enum = WindDirection(value)
    enum.degrees = degrees

    return enum

  def __contains__(self, other: 'WindDirection | float | int') -> bool:
    """Checks if the other's angle is within the enum's wind direction."""
    members = list(self.__class__)

    return self is members[int(((float(other) % 360) + 11.25) // 22.5) % len(members)]

  def __int__(self) -> int:
    """The integer representation of the wind direction's angle."""
    return int(self.degrees)

  def __float__(self) -> float:
    """The wind direction's angle."""
    return self.degrees

  @property
  def emoji(self) -> str:
    """The wind direction's emoji representation."""
    return WIND_DIRECTION_EMOJIS[int(((self.degrees + 22.5) % 360) // 45)]


class Locale(Enum):
  """A supported locale."""

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
    """The locale's debug string representation."""
    return f'{__class__.__name__}.{self.name}'

  def __str__(self) -> str:
    """The locale's friendly name."""
    arr = self.name.title().split('_')

    return f'{" ".join(arr[:-1])} ({arr[-1]})' if len(arr) != 1 else arr[0]


class Kind(BasicEnum):
  """A weather forecast kind."""

  __slots__: tuple[str, ...] = ()

  SUNNY = 113
  PARTLY_CLOUDY = 116
  CLOUDY = 119
  OVERCAST = 122
  HAZE = 125
  DUST_HAZE = 128
  BLOWING_DUST = 131
  DUST_STORM = 134
  SANDSTORM = 137
  SEVERE_SANDSTORM = 140
  MIST = 143
  SMOKE = 146
  SMOKY_HAZE = 149
  SMOG = 152
  SEVERE_SMOG = 155
  SAHARAN_DUST = 158
  DUST = 161
  PATCHY_RAIN_NEARBY = 176
  PATCHY_SNOW_NEARBY = 179
  PATCHY_SLEET_NEARBY = 182
  PATCHY_FREEZING_DRIZZLE_NEARBY = 185
  THUNDERY_OUTBREAKS_IN_NEARBY = 200
  BLOWING_SNOW = 227
  BLIZZARD = 230
  FOG = 248
  FREEZING_FOG = 260
  PATCHY_LIGHT_DRIZZLE = 263
  LIGHT_DRIZZLE = 266
  FREEZING_DRIZZLE = 281
  HEAVY_FREEZING_DRIZZLE = 284
  PATCHY_LIGHT_RAIN = 293
  LIGHT_RAIN = 296
  MODERATE_RAIN_AT_TIMES = 299
  MODERATE_RAIN = 302
  HEAVY_RAIN_AT_TIMES = 305
  HEAVY_RAIN = 308
  LIGHT_FREEZING_RAIN = 311
  MODERATE_OR_HEAVY_FREEZING_RAIN = 314
  LIGHT_SLEET = 317
  MODERATE_OR_HEAVY_SLEET = 320
  PATCHY_LIGHT_SNOW = 323
  LIGHT_SNOW = 326
  PATCHY_MODERATE_SNOW = 329
  MODERATE_SNOW = 332
  PATCHY_HEAVY_SNOW = 335
  HEAVY_SNOW = 338
  ICE_PELLETS = 350
  LIGHT_RAIN_SHOWER = 353
  MODERATE_OR_HEAVY_RAIN_SHOWER = 356
  TORRENTIAL_RAIN_SHOWER = 359
  LIGHT_SLEET_SHOWERS = 362
  MODERATE_OR_HEAVY_SLEET_SHOWERS = 365
  LIGHT_SNOW_SHOWERS = 368
  MODERATE_OR_HEAVY_SNOW_SHOWERS = 371
  LIGHT_SHOWERS_OF_ICE_PELLETS = 374
  MODERATE_OR_HEAVY_SHOWERS_OF_ICE_PELLETS = 377
  PATCHY_LIGHT_RAIN_IN_AREA_WITH_THUNDER = 386
  MODERATE_OR_HEAVY_RAIN_IN_AREA_WITH_THUNDER = 389
  PATCHY_LIGHT_SNOW_IN_AREA_WITH_THUNDER = 392
  MODERATE_OR_HEAVY_SNOW_IN_AREA_WITH_THUNDER = 395

  @property
  def emoji(self) -> str:
    """The weather forecast kind's emoji representation."""
    return KIND_EMOJIS[self.value]


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
    """The moon phase's emoji representation."""
    return chr(0x1F311 + self._index)
