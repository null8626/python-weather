from .rest import HTTPClient
from .constants import default_client_options
from gc import collect

class Client:
    __slots__ = ('http',)

    def __init__(self, session=None, format: str = None, **options):
        if format.upper() not in ('C', 'F'):
            raise TypeError('Invalid format.')
        
        opt = {}
        for key in default_client_options.keys():
            opt[key] = options.get(key, default_client_options[key])
        
        if isinstance(format, str) and (format.upper() in ('C', 'F')):
            opt["weadegreetype"] = format

        self.http = HTTPClient(session, options.get('max_cache_size', 15), opt)

    async def find(self, location: str) -> "Weather":
        """ Finds a weather forecast from a location. """
        if not isinstance(location, str):
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