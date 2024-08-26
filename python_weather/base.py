from enum import auto

from .errors import Error
from .enums import WindDirection, Kind, Locale, UltraViolet
from .constants import _Unit


class CustomizableBase:
  __slots__ = ('__unit', '__locale')

  def __init__(self, unit: _Unit, locale: Locale):
    self.unit = unit
    self.locale = locale

  @property
  def unit(self) -> auto:
    """The measuring unit used to display information in this object."""

    return self.__unit

  @unit.setter
  def unit(self, to: _Unit):
    """
    Sets the default measuring unit used to display information in this object.

    :param to: The new default measuring unit to be used to display information in this object. Must be either ``METRIC`` or ``IMPERIAL``.
    :exception Error: If the ``to`` argument is not either ``METRIC`` or ``IMPERIAL``.
    """

    if not isinstance(to, _Unit):
      raise Error('Invalid measuring unit specified!')

    self.__unit = to

  @property
  def locale(self) -> Locale:
    """The localization used to display information in this object."""

    return self.__locale

  @locale.setter
  def locale(self, to: Locale):
    """
    Sets the default localization used to display information in this object.

    :param to: The new :class:`Locale` to be used to display information in this object.
    :type to: Locale
    :exception Error: If the ``to`` argument is not a part of the :class:`Locale` enum.
    """

    if not isinstance(to, Locale):
      raise Error(f'Expected {to!r} to be a Locale enum')

    self.__locale = to


class BaseForecast(CustomizableBase):
  __slots__ = ('__inner',)

  def __init__(self, json: dict, unit: _Unit, locale: Locale):
    self.__inner = json

    super().__init__(unit, locale)

  @property
  def ultraviolet(self) -> UltraViolet:
    """The ultra-violet (UV) index."""

    return UltraViolet._new(int(self.__inner['uvIndex']))

  @property
  def feels_like(self) -> int:
    """What it felt like, in celcius or fahrenheit."""

    return int(self.__inner[f'FeelsLike{self._CustomizableBase__unit.temperature}'])

  @property
  def humidity(self) -> int:
    """The humidity value in percent."""

    return int(self.__inner['humidity'])

  @property
  def temperature(self) -> int:
    """The temperature in either celcius or Fahrenheit."""

    return int(self.__inner[f'temp_{self._CustomizableBase__unit.temperature}'])

  @property
  def precipitation(self) -> float:
    """The precipitation in either millimeters or inches."""

    return float(self.__inner[f'precip{self._CustomizableBase__unit.precipitation}'])

  @property
  def pressure(self) -> float:
    """The pressure in either pascal or inches."""

    return float(self.__inner[f'pressure{self._CustomizableBase__unit.pressure}'])

  @property
  def visibility(self) -> int:
    """The visibility distance in either kilometers or miles."""

    return int(self.__inner[f'visibility{self._CustomizableBase__unit.visibility}'])

  @property
  def wind_speed(self) -> int:
    """The wind speeds in either kilometers/hour or miles/hour."""

    return int(self.__inner[f'windspeed{self._CustomizableBase__unit.velocity}'])

  @property
  def wind_direction(self) -> WindDirection:
    """The wind direction."""

    return WindDirection._new(
      self.__inner['winddir16Point'], int(self.__inner['winddirDegree'])
    )

  @property
  def description(self) -> str:
    """The description regarding the forecast. This can be localized in different languages depending on the localization used."""

    description = (
      self.__inner['weatherDesc'][0]['value']
      if self._CustomizableBase__locale == Locale.ENGLISH
      else self.__inner[f'lang_{self._CustomizableBase__locale.value}'][0]['value']
    )

    return description.strip()

  @property
  def kind(self) -> Kind:
    """The kind of the forecast."""

    return Kind(int(self.__inner['weatherCode']))
