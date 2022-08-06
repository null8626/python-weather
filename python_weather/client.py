from aiohttp import ClientSession, ClientTimeout
from urllib.parse import quote_plus

from .constants import is_invalid_format, VALID_FORMATS
from .forecast import Weather
from .errors import Error, InvalidArg

class Client:
  __slots__ = ('__session', '__default_format')

  def __init__(self, format: str = None, session: ClientSession = None):
    """
    Creates the client instance.

    Args:
        format (str, optional): The default format to be used. Defaults to None.
        session (ClientSession, optional): An existing `ClientSession` instance to be used. Defaults to None.
    """

    self.__session = session or ClientSession(timeout=ClientTimeout(total=2000.0))
    self.__default_format = 'C' if is_invalid_format(format) else format
  
  def __repr__(self) -> str:
    """
    Returns:
        str: The string representation of said object.
    """

    return f'<Client {self.__session!r}>'

  async def get(self, location: str, format: str = None) -> Weather:
    """
    Fetches the weather for a specific location.

    Args:
        location (str): The location string.
        format (str, optional): The format - this will override the default if provided. Defaults to None.

    Raises:
        InvalidArg: Invalid `location` argument
        Error: Client is already closed
    
    Returns:
        Weather: The weather forecast for the given location.
    """

    if (not isinstance(location, str)) or (not location):
      raise InvalidArg('proper location str', location)
    elif self.__session.closed:
      raise Error('Client is already closed')

    if is_invalid_format(format):
      format = self.__default_format

    async with self.__session.get(f'https://wttr.in/{quote_plus(location)}?format=j1') as resp:
      return Weather(await resp.json(), format)

  @property
  def default_format(self) -> str:
    """
    Returns:
        str: The default format used.
    """

    return self.__default_format
  
  @default_format.setter
  def default_format(self, to: str):
    """
    Sets the default format used.

    Args:
        to (str): The new default format to be used. Must be `C` or `F`.

    Raises:
        InvalidArg: Invalid format.
    """

    if is_invalid_format(to):
      raise InvalidArg(VALID_FORMATS, to)
    
    self.__default_format = to

  async def close(self) -> None:
    """
    Closes the client instance. Nothing will happen if it's already closed.
    """

    if not self.__session.closed:
      await self.__session.close()