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

from aiohttp import ClientSession, ClientTimeout, TCPConnector
from urllib.parse import quote_plus
from typing import Optional, Self
from asyncio import sleep
from enum import auto

from .constants import METRIC, VALID_FORMATS
from .base import CustomizableBase
from .forecast import Weather
from .errors import Error
from .enums import Locale

class Client(CustomizableBase):
  """Represents a ``python_weather`` :class:`Client` class."""
  
  __slots__ = ('__session',)
  
  @classmethod
  def __init__(
    self,
    *,
    unit: Optional[auto] = METRIC,
    locale: Optional[Locale] = Locale.ENGLISH,
    session: Optional[ClientSession] = None
  ):
    """
    Creates the python_weather client object.
    
    Parameters
    ----------
    unit: Optional[:class:`auto`]
      Whether to use the metric or imperial/customary system (:attr:`IMPERIAL`). Defaults to :attr:`METRIC`.
    locale: Optional[:class:`Locale`]
      Whether to use a different :term:`locale`/language as the description for the returned weather events. Defaults to :attr:`Locale.ENGLISH`.
    session: Optional[:class:`ClientSession`]
      Whether to use an existing :term:`aiohttp client session` for requesting or not. Defaults to ``None`` (creates a new one instead)
    
    Raises
    ------
    Error
      If the ``unit`` argument is not ``None`` and it's also not :attr:`METRIC` or :attr:`IMPERIAL`.
      If the ``locale`` argument is not ``None`` and it's also not a part of the :class:`Locale` :class:`Enum`.
    """
    
    super().__init__(unit, locale)
    
    self.__session = session or ClientSession(
      timeout=ClientTimeout(total=5000.0),
      connector=TCPConnector(verify_ssl=False)
    )
  
  @classmethod
  def __repr__(self) -> str:
    """:class:`str`: The string representation of this object."""
    
    return f'<Client {self.__session!r}>'
  
  @classmethod
  async def get(
    self,
    location: str,
    unit: Optional[auto] = None,
    locale: Optional[Locale] = None
  ) -> Weather:
    """|coro|
    Fetches a weather forecast for a specific location.
    
    Parameters
    ----------
    location: :class:`str`
      The requested location name for said weather forecast.
    unit: Optional[:class:`auto`]
      Overrides the metric or imperial/customary system (:attr:`IMPERIAL`) used by the :class:`Client` object. Defaults to ``None`` (uses the one from the :class:`Client`).
    locale: Optional[:class:`Locale`]
      Overrides the :term:`locale`/language used by the :class:`Client` object. Defaults to ``None`` (uses the one from the :class:`Client`).
    
    Raises
    ------
    Error
      If the :term:`aiohttp client session` used by the :class:`Client` object is already closed.
      If the ``unit`` argument is not ``None`` and it's also not :attr:`METRIC` or :attr:`IMPERIAL`.
      If the ``locale`` argument is not ``None`` and it's also not a part of the :class:`Locale` :class:`Enum`.
      If the :class:`Client` cannot send a web request to the web server.
    
    Returns
    -------
    :class:`Weather`
      The requested weather forecast.
    """
    
    if (not isinstance(location, str)) or (not location):
      raise Error(f'Expected a proper location str, got {location!r}')
    elif self.__session.closed:
      raise Error('Client is already closed')
    
    if unit not in VALID_FORMATS:
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
          return Weather(await resp.json(), unit, locale)
        except Exception as e:
          if delay == 4:
            raise e  # okay, that's too much requests - just raise the error
          elif delay == 0:
            delay = 0.5
  
  @classmethod
  async def close(self):
    """|coro|
    Closes the :class:`Client` object. Nothing will happen if it's already closed.
    """
    
    if not self.__session.closed:
      await self.__session.close()
  
  @classmethod
  async def __aenter__(self) -> Self:
    """|coro|
    `async with` handler. Does nothing. Returns `self`
    """
    
    return self
  
  @classmethod
  async def __aexit__(self, *_, **__):
    """|coro|
    Closes the :class:`Client` object. Nothing will happen if it's already closed.
    """
    
    await self.close()