"""
The MIT License (MIT)

Copyright (c) 2021-2024 null8626

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from aiohttp import ClientSession, ClientTimeout, TCPConnector
from urllib.parse import quote_plus
from typing import Optional, Tuple
from asyncio import sleep

from .errors import Error, RequestError
from .constants import _Unit, METRIC
from .base import CustomizableBase
from .forecast import Forecast
from .enums import Locale


class Client(CustomizableBase):
  """
  The class that lets you interact with the API.

  :param unit: Whether to use the metric or imperial/customary system (``IMPERIAL``). Defaults to ``METRIC``.
  :type unit: ``_Unit``
  :param locale: Whether to use a different locale/language as the description for the returned forecast. Defaults to :attr:`.Locale.ENGLISH`.
  :type locale: :class:`.Locale`
  :param session: Whether to use an existing :class:`~aiohttp.ClientSession` for requesting or not. Defaults to :py:obj:`None` (creates a new one instead).
  :type session: Optional[:class:`~aiohttp.ClientSession`]
  :param max_retries: Maximum amount of retries upon receiving HTTP request failure before raising a :class:`.RequestError`. To have infinite retries, use ``-1`` (NOT recommended). Defaults to :py:obj:`None` (or 3 retries).
  :type max_retries: Optional[:class:`int`]

  :raises Error: If ``unit`` is not ``METRIC`` or ``IMPERIAL``, or if ``locale`` is not a part of the :class:`.Locale` enum.
  """

  __slots__: Tuple[str, ...] = ('__own_session', '__session', '__max_retries')

  def __init__(
    self,
    *,
    unit: _Unit = METRIC,
    locale: Locale = Locale.ENGLISH,
    session: Optional[ClientSession] = None,
    max_retries: Optional[int] = None,
  ):
    super().__init__(unit, locale)

    self.__own_session = session is None
    self.__session = session or ClientSession(
      timeout=ClientTimeout(total=5000.0),
      connector=TCPConnector(verify_ssl=False),
    )
    self.__max_retries = max_retries or 3

  def __repr__(self) -> str:
    return f'<{__class__.__name__} {self.__session!r}>'

  async def get(
    self,
    location: str,
    *,
    unit: Optional[_Unit] = None,
    locale: Optional[Locale] = None,
  ) -> Forecast:
    """
    Fetches a weather forecast for a specific location.

    :param location: The requested location name for said weather forecast.
    :type location: :py:class:`str`
    :param unit: Overrides the unit used by this object. Defaults to the one used by this object.
    :type unit: Optional[``_Unit``]
    :param locale: Overrides the locale used by this object. Defaults to the one used by this object.
    :type locale: Optional[:class:`.Locale`]

    :exception Error: If the `location` argument is not a :py:class:`str` or is empty.
    :exception RequestError: If the :class:`~aiohttp.ClientSession` used by the :class:`.Client` object is already closed, or if the :class:`.Client` cannot send a web request to the web server.

    :returns: The requested weather forecast.
    :rtype: Forecast
    """

    if (not isinstance(location, str)) or (not location):
      raise Error(f'Expected a proper location str, got {location!r}')

    if not isinstance(unit, _Unit):
      unit = self._CustomizableBase__unit

    if not isinstance(locale, Locale):
      locale = self._CustomizableBase__locale

    subdomain = f'{locale.value}.' if locale != Locale.ENGLISH else ''
    delay = 0.5
    attempts = 0

    while True:
      try:
        async with self.__session.get(
          f'https://{subdomain}wttr.in/{quote_plus(location)}?format=j1'
        ) as resp:
          resp.raise_for_status()

          return Forecast(await resp.json(), unit, locale)
      except Exception as err:
        if attempts == self.__max_retries:
          raise RequestError(err)

        await sleep(delay)
        attempts += 1
        delay *= 2

  async def close(self) -> None:
    """Closes the :class:`.Client` object. Nothing will happen if the client uses a pre-existing :class:`~aiohttp.ClientSession` or if the session is already closed."""

    if self.__own_session and not self.__session.closed:
      await self.__session.close()

  async def __aenter__(self) -> 'Client':
    return self

  async def __aexit__(self, *_, **__) -> None:
    await self.close()
