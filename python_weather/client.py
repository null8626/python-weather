from .rest import HTTPClient
from urllib.parse import unquote, quote
from re import search

class Client:
  __slots__ = ('http',)

  def __init__(self, session=None, format: str = 'C', locale: str = 'en-US'):
    if format.upper() not in ('C', 'F'):
      raise TypeError('Invalid format.')
    
    self.http = HTTPClient(format, locale, session)

  @property
  def format(self) -> str:
    return search('&weadegreetype=([^&]+)', self.http._query_params)[0][15:]

  @format.setter
  def format(self, value: str) -> None:
    if value.upper() not in ('C', 'F'):
      raise TypeError('Invalid format.')
    self.http._query_params = self.http._query_params.replace(f'&weadegreetype={self.format}', f'&weadegreetype={value}')

  @property
  def locale(self) -> str:
    return unquote(search('&culture=([^&]+)', self.http._query_params))[0][9:]

  @locale.setter
  def locale(self, value: str) -> None:
    self.http._query_params = self.http._query_params.replace(f'&culture={self.locale}', f'&culture={quote(value)}')

  async def find(self, location: str) -> "Weather":
    """ Finds a weather forecast from a location. """
    if (not location) or (not isinstance(location, str)):
      raise TypeError('location must be a string.')
    return await self.http.request(location)

  @property
  def closed(self) -> bool:
    """ Returns if the client is closed or not. """
    return self.http.closed

  async def close(self) -> None:
    """ Closes the wrapper. """
    if not self.closed:
      await self.http.close()

  def __repr__(self) -> str:
    return f"<WeatherClient closed={self.closed}>"