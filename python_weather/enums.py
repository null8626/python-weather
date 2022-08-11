from enum import Enum

class WeatherType(Enum):
  Sunny = 113
  PartlyCloudy = 116
  Cloudy = 119
  VeryCloudy = 122
  Fog = 143
  LightShowers = 176
  Mist = 260
  LightRain = 296
  LightSnow = 320
  HeavySnow = 338
  HeavyShowers = 356
  HeavyRain = 359
  LightSnowShowers = 368
  LightSleetShowers = 374
  LightSleet = 377
  ThunderyShowers = 386
  ThunderyHeavyRain = 389
  ThunderySnowShowers = 392
  HeavySnowShowers = 395

  def _new(num: int):
    # handle dups

    if num == 182:
      num = 185
    elif num == 248 or num == 143:
      num = 260
    elif num == 263 or num == 353:
      num = 176
    elif num == 185 or num == 281 or num == 284 or num == 311 or num == 314 or num == 317 or num == 350:
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
        str: The name.
    """

    if self is self.Sunny:
      return "Sunny"
    elif self is self.PartlyCloudy:
      return "Partly Cloudy"
    elif self is self.Cloudy:
      return "Cloudy"
    elif self is self.VeryCloudy:
      return "Very Cloudy"
    elif self is self.Fog:
      return "Fog"
    elif self is self.LightShowers:
      return "Light Showers"
    elif self is self.LightRain:
      return "Light Rain"
    elif self is self.LightSnow:
      return "Light Snow"
    elif self is self.HeavySnow:
      return "Heavy Snow"
    elif self is self.HeavyShowers:
      return "Heavy Showers"
    elif self is self.HeavyRain:
      return "Heavy Rain"
    elif self is self.LightSnowShowers:
      return "Light Snow Showers"
    elif self is self.LightSleetShowers:
      return "Light Sleet Showers"
    elif self is self.LightSleet:
      return "Light Sleet"
    elif self is self.ThunderyShowers:
      return "Thundery Showers"
    elif self is self.ThunderyHeavyRain:
      return "Thundery Heavy Rain"
    elif self is self.ThunderySnowShowers:
      return "Thundery Snow Showers"
    elif self is self.HeavySnowShowers:
      return "Heavy Snow Showers"
    else:
      return "Unknown"

  def __repr__(self) -> str:
    """
    Returns:
        str: The emoji representing it.
    """    

    if self is self.Cloudy:
      return "☁️"
    elif self is self.Fog:
      return "🌫"
    elif self is self.HeavyRain:
      return "🌧"
    elif self is self.HeavyShowers:
      return "🌧"
    elif self is self.HeavySnow:
      return "❄️"
    elif self is self.HeavySnowShowers:
      return "❄️"
    elif self is self.LightRain:
      return "🌦"
    elif self is self.LightShowers:
      return "🌦"
    elif self is self.LightSleet:
      return "🌧"
    elif self is self.LightSleetShowers:
      return "🌧"
    elif self is self.LightSnow:
      return "🌨"
    elif self is self.LightSnowShowers:
      return "🌨"
    elif self is self.PartlyCloudy:
      return "⛅️"
    elif self is self.Sunny:
      return "☀️"
    elif self is self.ThunderyHeavyRain:
      return "🌩"
    elif self is self.ThunderyShowers:
      return "⛈"
    elif self is self.ThunderySnowShowers:
      return "⛈"
    elif self is self.VeryCloudy:
      return "☁️"
    else:
      return "✨"

class MoonPhase(Enum):
  NewMoon = "New Moon"
  WaxingCrescent = "Waxing Crescent"
  FirstQuarter = "First Quarter"
  WaxingGibbous = "Waxing Gibbous"
  FullMoon = "Full Moon"
  WaningGibbous = "Waning Gibbous"
  LastQuarter = "Last Quarter"
  WaningCrescent = "Waning Crescent"

  def __str__(self) -> str:
    """
    Returns:
        str: An alias for the enum's value
    """

    return self.value

  def __repr__(self) -> str:
    """
    Returns:
        str: The emoji representation of the moon phase.
    """    

    if self is self.NewMoon:
      return "🌑"
    elif self is self.WaxingCrescent:
      return "🌒"
    elif self is self.FirstQuarter:
      return "🌓"
    elif self is self.WaxingGibbous:
      return "🌔"
    elif self is self.FullMoon:
      return "🌕"
    elif self is self.WaningGibbous:
      return "🌖"
    elif self is self.LastQuarter:
      return "🌗"
    else:
      return "🌘"
