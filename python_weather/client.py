from aiohttp import ClientSession, ClientTimeout, TCPConnector
from urllib.parse import quote_plus
from typing import Optional
from asyncio import sleep

from .constants import is_invalid_format, METRIC, VALID_FORMATS
from .forecast import Weather
from .errors import Error
from .enums import Locale

class Client:
  __slots__ = ('__session', '__default_format', '__locale')

  def __init__(
    self,
    format: str = 'C',
    locale: Locale = Locale.ENGLISH,
    session: Optional[ClientSession] = None
  ):
    """
    Creates the client instance.

    Args:
      format (str, optional): The default format to be used. Defaults to 'C' or METRIC.
      locale (Locale, optional): The default locale to be used. Defaults to Locale.ENGLISH.
      session (ClientSession, optional): An existing `ClientSession` instance to be used. Defaults to None.

    Raises:
      Error: Client is already closed, invalid `location` argument, or invalid `locale` argument.
    """

    self.__session = session or ClientSession(
      timeout=ClientTimeout(total=5000.0),
      connector=TCPConnector(verify_ssl=False)
    )

    self.format = format or METRIC
    self.locale = locale or Locale.ENGLISH

  def __repr__(self) -> str:
    """
    Returns:
      str: The string representation of said object.
    """

    return f'<Client {self.__session!r}>'

  async def get(self, location: str, format: Optional[str] = None, locale: Optional[Locale] = None) -> Weather:
    """
    Fetches the weather for a specific location.

    Args:
      location (str): The location string.
      format (str, optional): The format - this will override the default if provided. Defaults to None.
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

    if is_invalid_format(format):
      format = self.__default_format

    subdomain = self.__locale if isinstance(locale, Locale) else (f'{locale.value}.' if locale != Locale.ENGLISH else '')
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
  def format(self, to: str):
    """
    Sets the default format used.

    Args:
      to (str): The new default format to be used. Must be `C` or `F`.

    Raises:
      Error: Invalid format.
    """

    if is_invalid_format(to):
      raise Error(f'Expected {to!r} to be in {VALID_FORMATS!r}')

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