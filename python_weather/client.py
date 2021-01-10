from aiohttp import ClientSession
from urllib.parse import quote as _url
from .weather import Weather

class Client:
    DEFAULT_OPTIONS = {
        "src": "outlook",
        "culture": "en-US",
        "weadegreetype": "C"
    }

    def __repr__(self) -> str:
        options = " ".join([f"{option}={repr(Client.DEFAULT_OPTIONS[option])}" for option in Client.DEFAULT_OPTIONS.keys()]) if Client.DEFAULT_OPTIONS else "None"
        return f"<WeatherClient cached={hasattr(self, '_cache')} options=<{options}>>"

    def __init__(
        self,
        session=None,
        max_cache_size: int = 20,
        store_cache: bool = True,
        format: str = "C",
        **kwargs
    ) -> None:
        """ Main Client Object of python-weather. """
        self.session = session
        
        self._session_settings = kwargs.pop("session_settings", {})
        self._baseURL = "https://weather.service.msn.com/find.aspx"
        self._format = format
        self._max_cache_size = max_cache_size if store_cache else None
        assert ((not self._format) or self._format.lower() in ("c", "f")), "Invalid temperature format."
        
        if store_cache:
            self._cache = {}
        
        if kwargs:
            Client.DEFAULT_OPTIONS = kwargs
        else:
            Client.DEFAULT_OPTIONS["weadegreetype"] = self._format
        
    def clear_cache(self) -> None:
        if not hasattr(self, "_cache"):
            raise TypeError("Caching is already disabled.")
        self._cache = {}
    
    def _get_cache(self, location: str):
        _filtered = location.lower().replace(",", "").replace(" ", "")
        return self._cache.get(_filtered)
    
    def _store_cache(self, key, data):
        if not hasattr(self, "_cache"):
            return
        
        if len(self._cache.keys()) == 10:
            self._cache.pop(tuple(self._cache.keys())[::-1][0])
        
        _filtered = key.lower().replace(",", "").replace(" ", "")
        self._cache[_filtered] = data
    
    def _encode_parameters(self, parameters: dict, location: str) -> str:
        parameters["weasearchstr"] = location
        return ("?" + "&".join([f"{i}={_url(parameters[i])}" for i in parameters.keys() if parameters[i]]) if parameters else "")
    
    async def find(self, location: str, format=None, **kwargs):
        """ Fetches weather from a location. """
        if hasattr(self, "_cache"):
            cache = self._get_cache(location)
            if cache:
                return Weather(cache)
        
        if not self.session:
            self.session = ClientSession(**self._session_settings)
        
        assert (location and isinstance(location, str)), "Please add a location."
        format = format or self._format
        parameters = self._encode_parameters(kwargs if kwargs else Client.DEFAULT_OPTIONS, location)
        
        response = await self.session.get(self._baseURL + parameters)
        content = await response.text()
        response.close()
        
        self._store_cache(location, content)
        return Weather(content)
    
    async def close(self) -> None:
        """ Closes the client and clears the cache. """
        
        try:
            self.clear_cache()
        except TypeError:
            pass
        
        await self.session.close()
        del self._max_cache_size, self.session, self._baseURL, self._session_settings, self._format
        
        if hasattr(self, "_cache"):
            del self._cache