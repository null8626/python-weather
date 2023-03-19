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
from typing import Optional
from asyncio import sleep
from enum import auto

from .constants import METRIC, VALID_FORMATS
from .forecast import Weather
from .errors import Error
from .enums import Locale

class Client:
  __slots__ = ('__session', '__default_format', '__locale')
  
  def __init__(self,
               format: Optional[auto] = METRIC,
               locale: Optional[Locale] = Locale.ENGLISH,
               session: Optional[ClientSession] = None):
    """
    Creates the client instance.

    Args:
      format (auto, optional): The default format to be used. Defaults to 'C' or METRIC.
      locale (Locale, optional): The default locale to be used. Defaults to Locale.ENGLISH.
      session (ClientSession, optional): An existing `ClientSession` instance to be used. Defaults to None.

    Raises:
      Error: Client is already closed, invalid `location` argument, or invalid `locale` argument.
    """
    
    self.__session = session or ClientSession(
        timeout=ClientTimeout(total=5000.0),
        connector=TCPConnector(verify_ssl=False))
    
    self.format = format or METRIC
    self.locale = locale or Locale.ENGLISH
  
  def __repr__(self) -> str:
    """
    Returns:
      str: The string representation of said object.
    """
    
    return f'<Client {self.__session!r}>'
  
  async def get(self,
                location: str,
                format: Optional[auto] = None,
                locale: Optional[Locale] = None) -> Weather:
    """
    Fetches the weather for a specific location.

    Args:
      location (str): The location string.
      format (auto, optional): The format - this will override the default if provided. Defaults to None.
      locale (Locale, optional): The format - this will override the default if provided. Defaults to None.

    Raises:
      Error: Client is already closed, or invalid `location` argument.

    Returns:
      Weather: The weather forecast for the given location.
    """
    
    if (not isinstance(location, str)) or (not location):
      raise Error(f'Expected a proper location str, got {location!r}')
    elif self.__session.closed:
      raise Error('Client is already closed')
    
    if format not in VALID_FORMATS:
      format = self.__default_format
    
    subdomain = self.__locale if isinstance(locale, Locale) else (
        f'{locale.value}.' if locale and locale != Locale.ENGLISH else '')
    delay = 0
    
    while True:
      if delay != 0:
        await sleep(delay)
        delay *= 2
      
      async with self.__session.get(
          f'https://{subdomain}wttr.in/{quote_plus(location)}?format=j1'
      ) as resp:
        try:
          return Weather(await resp.json(), format)
        except Exception as e:
          if delay == 4:
            raise e  # okay, that's too much requests - just raise the error
          elif delay == 0:
            delay = 0.5
  
  @property
  def format(self) -> str:
    """
    Returns:
      str: The default format used.
    """
    
    return self.__default_format
  
  @format.setter
  def format(self, to: auto):
    """
    Sets the default format used.

    Args:
      to (auto): The new default format to be used. Must be METRIC or IMPERIAL.

    Raises:
      Error: Invalid format.
    """
    
    if to not in VALID_FORMATS:
      raise Error('Invalid format specified!')
    
    self.__default_format = to
  
  @property
  def locale(self) -> Locale:
    """
    Returns:
      Locale: The default locale used.
    """
    
    return Locale(self.__locale[:-1] if self.__locale else 'en')
  
  @locale.setter
  def locale(self, to: Locale):
    """
    Sets the default locale used.

    Args:
      to (Locale): The new default locale to be used.

    Raises:
      Error: Not a part of the Locale enum.
    """
    
    if not isinstance(to, Locale):
      raise Error(f'Expected {to!r} to be a Locale enum')
    
    self.__locale = f'{to.value}.' if to != Locale.ENGLISH else ''
  
  async def close(self) -> None:
    """
    Closes the client instance. Nothing will happen if it's already closed.
    """
    
    if not self.__session.closed:
      await self.__session.close()
  
  async def __aenter__(self):
    """
    `async with` handler. Does nothing. Returns `self`
    """
    
    return self
  
  async def __aexit__(self, *_, **__):
    """
    Closes the client instance. Nothing will happen if it's already closed.
    """
    
    await self.close()
