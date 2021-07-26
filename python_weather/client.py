from .rest import HTTPClient
from gc import collect
from urllib.parse import unquote, quote
from re import search

class Client:
    __slots__ = ('http',)

    def __init__(self, session=None, format: str = 'C', locale: str = 'en-US', max_cache_size: int = 15):
        if format.upper() not in ('C', 'F'):
            raise TypeError('Invalid format.')
        
        self.http = HTTPClient(max_cache_size, format, locale, session)

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
    def cache(self) -> "Cache":
        """ Returns the cache. """
        if self.closed:
            return
        return self.http.cache
    
    @cache.setter
    def cache(self, new_cache: dict) -> None:
        """ Modifies the cache. """
        if self.closed:
            return
        elif new_cache is None:
            return self.cache.clear()
        elif not isinstance(new_cache, dict):
            raise TypeError('Invalid type for setting the client\'s cache.')

        new_is_empty = not len(new_cache.keys())
        for k, v in new_cache.items():
            self.http.cache[k] = v
        
        if new_is_empty:
            collect()

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