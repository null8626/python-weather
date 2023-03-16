from enum import Enum
from re import sub

class WindDirection(Enum):
  NORTH = "N"
  NORTH_NORTH_EAST = "NNE"
  NORTH_EAST = "NE"
  EAST_NORTH_EAST = "ENE"
  EAST = "E"
  EAST_SOUTH_EAST = "ESE"
  SOUTH_EAST = "SE"
  SOUTH_SOUTH_EAST = "SSE"
  SOUTH = "S"
  SOUTH_SOUTH_WEST = "SSW"
  SOUTH_WEST = "SW"
  WEST_SOUTH_WEST = "WSW"
  WEST = "W"
  WEST_NORTH_WEST = "WNW"
  NORTH_WEST = "NW"
  NORTH_NORTH_WEST = "NNW"
  
  def __str__(self) -> str:
    """
    Returns:
      str: The stylized name.
    """
    
    if len(self.value) == 3:
      return sub(r'^(\w+_\w+)_', r'\1', self.name).replace('_', ' ').title()
    elif len(self.value) == 2:
      return self.name.replace('_', '').title()
    else:
      return self.name.title()

class Locale(Enum):
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

class WeatherType(Enum):
  SUNNY = 113
  PARTLY_CLOUDY = 116
  CLOUDY = 119
  VERY_CLOUDY = 122
  FOG = 143
  LIGHT_SHOWERS = 176
  MIST = 260
  LIGHT_RAIN = 296
  LIGHT_SNOW = 320
  HEAVY_SNOW = 338
  HEAVY_SHOWERS = 356
  HEAVY_RAIN = 359
  LIGHT_SNOW_SHOWERS = 368
  LIGHT_SLEET_SHOWERS = 374
  LIGHT_SLEET = 377
  THUNDERY_SHOWERS = 386
  THUNDERY_HEAVY_RAIN = 389
  THUNDERY_SNOW_SHOWERS = 392
  HEAVY_SNOW_SHOWERS = 395

  def _new(num: int):
    # handle dups

    if num == 182:
      num = 185
    elif num == 248 or num == 143:
      num = 260
    elif num == 263 or num == 353:
      num = 176
    elif (
      num == 185
      or num == 281
      or num == 284
      or num == 311
      or num == 314
      or num == 317
      or num == 350
    ):
      num = 377
    elif num == 179 or num == 362 or num == 365:
      num = 374
    elif num == 266 or num == 293:
      num = 296
    elif num == 302 or num == 358:
      num = 359
    elif num == 299 or num == 305:
      num = 356
    elif num == 323 or num == 326:
      num = 368
    elif num == 227:
      num = 320
    elif num == 230 or num == 329 or num == 332:
      num = 338
    elif num == 335 or num == 371:
      num = 395
    elif num == 200:
      num = 386

    return WeatherType(num)

  def __str__(self) -> str:
    """
    Returns:
      str: The stylized name.
    """

    return self.name.replace('_', ' ').title()

  def __repr__(self) -> str:
    """
    Returns:
      str: The emoji representing it.
    """

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

class MoonPhase(Enum):
  NEW_MOON = 'New Moon'
  WAXING_CRESCENT = 'Waxing Crescent'
  FIRST_QUARTER = 'First Quarter'
  Waxing_GIBBOUS = 'Waxing Gibbous'
  FULL_MOON = 'Full Moon'
  WANING_GIBBOUS = 'Waning Gibbous'
  LAST_QUARTER = 'Last Quarter'
  WANING_CRESCENT = 'Waning Crescent'

  def __str__(self) -> str:
    """
    Returns:
      str: The stylized name.
    """

    return self.value

  def __repr__(self) -> str:
    """
    Returns:
      str: The emoji representation of the moon phase.
    """

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