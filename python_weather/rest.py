from asyncio import sleep
from xmltodict import parse
from aiohttp import ClientSession
from urllib.parse import quote
from .cache import Cache
from .response import Weather
from .exceptions import HTTPException

class HTTPClient:
    __slots__ = ('_session', '_query_params', 'cache')

    def __init__(self, max_cache_size: int, format: str, locale: str, session: "ClientSession" = None):
        self._session = session if isinstance(session, ClientSession) and (not session.closed) else ClientSession()
        self._query_params = f"?src=outlook&culture={quote(locale)}&weadegreetype={format}&weasearchstr=" + "{}"
        self.cache = Cache(max_cache_size)

    async def request(self, location: str) -> dict:
        url = "https://weather.service.msn.com/find.aspx" + self._query_params.format(quote(location))

        if url not in self.cache:
            resp = await self._session.get(url)
            self.cache[url] = await resp.text()
        
        parsed = parse(self.cache[url])
        error_message = parsed.get('string')
        if error_message:
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