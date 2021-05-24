from asyncio import sleep
from xmltodict import parse
from aiohttp import ClientSession
from urllib.parse import quote
from .constants import default_client_options, base_url
from .cache import Cache
from .response import Weather
from .exceptions import HTTPException

class HTTPClient:
    __slots__ = ('_session', '_format_query_string', 'cache')

    def __init__(self, session: "ClientSession" = None, max_cache_size: int = 15, options: dict = default_client_options):
        self._session = session if isinstance(session, ClientSession) and (not session.closed) else ClientSession()
        self._format_query_string = lambda location: ('?' + '&'.join(f'{k}={quote(v)}' for k, v in options.items())) + f"weasearchstr={quote(location)}"
        self.cache = Cache(max_cache_size)

    async def request(self, location: str) -> dict:
        url = base_url + self._format_query_string(location.lower())

        if url not in self.cache:
            resp = await self._session.get(url)
            self.cache[url] = await resp.text()
        
        parsed = parse(self.cache[url])
        if (error_message := parsed.get('string')):
            raise HTTPException(response, error_message['#text'])
        elif resp.status >= 400:
            raise HTTPException(response)
        
        resp.close()
        try:
            return Weather(parsed['weatherdata']['weather'][0])
        except KeyError:
            return Weather(parsed['weatherdata']['weather'])
    
    @property
    def closed(self) -> bool:
        """ Returns if the HTTPClient is closed. """
        return self._session.closed and not bool(self.cache)

    def __repr__(self) -> str:
        return f"<HTTPClient closed={self.closed}>"

    async def close(self):
        if not self._session.closed:
            await self._session.close()
        
        self.cache.clear()