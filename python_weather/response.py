from datetime import datetime
from typing import List
from re import match

class BaseResponse:
    __slots__ = ('_get',)

    def __init__(self, response: dict):
        self._get = response.get
    
    def __getitem__(self, key: str):
        res = self._get(key)
        if res:
            return res
        raise KeyError(key)

class WeatherForecast(BaseResponse):
    def __init__(self, forecast_obj: dict):
        super().__init__(forecast_obj)

    def __repr__(self) -> str:
        return f"<WeatherForecast date={self.date!r} temperature={self.temperature} sky_text={self.sky_text} precip={self.precip}>"

    @property
    def low(self) -> int:
        """ Returns the lowest predicted temperature for the forecast. """
        temp = self._get('@low')
        return int(temp) if temp else None

    @property
    def high(self) -> int:
        """ Returns the highest predicted temperature for the forecast. """
        temp = self._get('@high')
        return int(temp) if temp else None

    @property
    def temperature(self) -> int:
        """ Returns the mean of the lowest and highest prediction. """
        return ((self.low or 0) + (self.high or 0)) // 2

    @property
    def sky_code_day(self) -> int:
        """ Returns the sky code day for the weather forecast. """
        code = self._get('@skycodeday')
        return int(code) if code else None

    @property
    def sky_text(self) -> str:
        """ Returns the sky text day string. """
        return self._get('@skytextday')

    @property
    def date(self) -> "datetime":
        """ Returns the weather forecast date. """
        try:
            return datetime(*tuple(map(int, self._get('@date').split('-'))))
        except:
            pass

    @property
    def day(self) -> str:
        """ Returns the day the where the forecast was predicted to happen. """
        return self._get('@day')
    
    @property
    def short_day(self) -> str:
        """ Returns the day the where the forecast was predicted to happen. (short version) """
        return self._get('@shortday')

    @property
    def precip(self) -> int:
        """ Returns the precipitation value. """
        val = self._get('@precip')
        return int(val) if val else None

class CurrentForecast(BaseResponse):
    def __init__(self, forecast_obj: dict):
        super().__init__(forecast_obj)
    
    def __repr__(self) -> str:
        return f"<CurrentForecast date={self.date!r} temperature={self.temperature} sky_text={self.sky_text} humidity={self.humidity} wind_speed={self.wind_speed}>"

    @property
    def temperature(self) -> int:
        """ Returns the current weather temperature. """
        temp = self._get('@temperature')
        return int(temp) if temp else None

    @property
    def sky_code(self) -> int:
        """ Returns the sky code for the current weather. """
        code = self._get('@skycode')
        return int(code) if code else None

    @property
    def sky_text(self) -> str:
        """ Returns the sky text for the current weather. """
        return self._get('@skytext')

    @property
    def date(self) -> "datetime":
        """ Returns the observation date for the current weather. """
        try:
            args = tuple(map(int, self._get('@date').split('-'))) + tuple(map(int, self._get('@observationtime').split(':')))
            return datetime(*args)
        except:
            pass

    @property
    def observation_point(self) -> str:
        """ Returns the observation point for the current weather. """
        return self._get('@observationpoint')

    @property
    def feels_like(self) -> int:
        """ Returns the temperature of what it feels like. """
        temp = self._get('@feelslike')
        return int(temp) if temp else None
    
    @property
    def humidity(self) -> int:
        """ Returns the humidity level. """
        temp = self._get('@humidity')
        return int(temp) if temp else None
    
    @property
    def wind_display(self) -> str:
        """ Returns the wind display string. """
        return self._get('@winddisplay')

    @property
    def day(self) -> str:
        """ Returns the day the current weather was recorded. """
        return self._get('@day')
    
    @property
    def short_day(self) -> str:
        """ Returns the day the current weather was recorded. (short version) """
        return self._get('@shortday')
    
    @property
    def wind_speed(self) -> int:
        """ Returns the wind speed """
        try:
            return int(match(r'(\d+) (\w+)', self._get('@windspeed') or '')[1])
        except:
            pass

class Weather(BaseResponse):
    def __init__(self, response: dict):
        super().__init__(response)
    
    def __repr__(self) -> str:
        return f"<Weather latitude={self.latitude} longitude={self.longitude} location_name={self.location_name} url={self.url}>"

    @property
    def current(self) -> "CurrentForecast":
        """ Returns the CurrentForecast object for the weather object. """
        current = self._get('current')
        return CurrentForecast(current) if current else None

    @property
    def forecasts(self) -> List[WeatherForecast]:
        """ Returns a list of forecasts for the weather object. """
        res = []
        for forecast in self._get('forecast', []):
            res.append(WeatherForecast(forecast))
        return res

    @property
    def location_code(self) -> str:
        """ Returns the weather location code. """
        return self._get('@weatherlocationcode')
    
    @property
    def location_name(self) -> str:
        """ Returns the weather location name. """
        return self._get('@weatherlocationname')
    
    @property
    def url(self) -> str:
        """ Returns the URL for the weather object. """
        return self._get('@url')
    
    @property
    def degree_type(self) -> str:
        """ Returns the format of the degree type. """
        return self._get('@degreetype')
    
    @property
    def provider(self) -> str:
        """ Returns the source provider for the weather forecast. """
        return self._get('@provider')
    
    @property
    def latitude(self) -> float:
        """ Returns the latitude of the weather's location. """
        lat = self._get('@lat')
        return float(lat) if lat else None
    
    @property
    def longitude(self) -> float:
        """ Returns the longitude of the weather's location. """
        long = self._get('@long')
        return float(long) if long else None
    
    @property
    def timezone_offset(self) -> int:
        """ Returns the timezone offset. """
        offset = self._get('@timezone')
        return int(offset) if offset else None
    
    @property
    def alert_message(self) -> str:
        """ Returns the alert message if available. """
        return self._get('@alert') or None
    
    @property
    def entity_id(self) -> int:
        """ Returns the entity ID for the weather forecast. """
        id = self._get('@entityid')
        return int(id) if id else None
    
    @property
    def provider_attribution(self) -> str:
        """ Returns the provider's attribution URL. """
        return self._get('@attribution')
