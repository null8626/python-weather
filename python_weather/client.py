from aiohttp import ClientSession, ClientTimeout, TCPConnector
from urllib.parse import quote_plus
from typing import Optional
from asyncio import sleep
from enum import auto

from .constants import _Unit, METRIC
from .base import CustomizableBase
from .forecast import Forecast
from .errors import Error
from .enums import Locale


class Client(CustomizableBase):
  """
  The class that lets you interact with the API.

  :param unit: Whether to use the metric or imperial/customary system (``IMPERIAL``). Defaults to ``METRIC``.
  :type unit: Optional[:py:class:`enum.auto`]
  :param locale: Whether to use a different locale/language as the description for the returned forecast. Defaults to ``Locale.ENGLISH``.
  :type locale: Optional[Locale]
  :param session: Whether to use an existing aiohttp client session for requesting or not. Defaults to ``None`` (creates a new one instead)
  :type session: Optional[:class:`aiohttp.ClientSession`]

  :raises Error: If the ``unit`` argument is not ``None`` and it's also not ``METRIC`` or ``IMPERIAL``, or if the ``locale`` argument is not ``None`` and it's also not a part of the :class:`Locale` enum.
  """

  __slots__ = ('__session',)

  def __init__(
    self,
    *,
    unit: Optional[auto] = METRIC,
    locale: Optional[Locale] = Locale.ENGLISH,
    session: Optional[ClientSession] = None,
  ):
    super().__init__(unit, locale)

    self.__session = session or ClientSession(
      timeout=ClientTimeout(total=5000.0),
      connector=TCPConnector(verify_ssl=False),
    )

  def __repr__(self) -> str:
    return f'<{self.__class__.__name__} {self.__session!r}>'

  async def get(
    self,
    location: str,
    *,
    unit: Optional[auto] = None,
    locale: Optional[Locale] = None,
  ) -> Forecast:
    """
    Fetches a weather forecast for a specific location.

    :param location: The requested location name for said weather forecast.
    :type location: str
    :param unit: Overrides the metric or imperial/customary system (``IMPERIAL``) used by the :class:`Client` object. Defaults to ``None`` (uses the one from the :class:`Client`).
    :type unit: Optional[:py:class:`enum.auto`]
    :param locale: Overrides the locale/language used by the :class:`Client` object. Defaults to ``None`` (uses the one from the :class:`Client`).
    :type locale: Optional[Locale]

    :exception Error: If the aiohttp client session used by the :class:`Client` object is already closed, if the ``unit`` argument is not ``None`` and it's also not ``METRIC`` or ``IMPERIAL``, if the ``locale`` argument is not ``None`` and it's also not a part of the :class:`Locale` enum, or if the :class:`Client` cannot send a web request to the web server.

    :returns: The requested weather forecast.
    :rtype: Forecast
    """

    if (not isinstance(location, str)) or (not location):
      raise Error(f'Expected a proper location str, got {location!r}')
    elif self.__session.closed:
      raise Error('Client is already closed')

    if not isinstance(unit, _Unit):
      unit = self._CustomizableBase__unit

    if not isinstance(locale, Locale):
      locale = self._CustomizableBase__locale

    subdomain = f'{locale.value}.' if locale != Locale.ENGLISH else ''
    delay = 0

    while True:
      if delay != 0:
        await sleep(delay)
        delay *= 2

      async with self.__session.get(
        f'https://{subdomain}wttr.in/{quote_plus(location)}?format=j1'
      ) as resp:
        try:
          return Forecast(await resp.json(), unit, locale)
        except Exception as e:
          if delay == 4:
            raise e  # okay, that's too much requests - just raise the error
          elif delay == 0:
            delay = 0.5

  async def close(self):
    """Closes the :class:`Client` object. Nothing will happen if it's already closed."""

    if not self.__session.closed:
      await self.__session.close()

  async def __aenter__(self):
    return self

  async def __aexit__(self, *_, **__):
    await self.close()
