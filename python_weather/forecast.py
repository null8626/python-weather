from datetime import datetime

class Forecast:
    
    def __repr__(self) -> str:
        if self.current:
            return f"<Forecast current=True temperature={self.temperature} sky_text='{self.sky_text}' date={repr(self.date)}>"
        return f"<Forecast current=False low={self.low} high={self.high} sky_text='{self.sky_text}' date={repr(self.date)} precip={self.precip}>"
    
    def __str__(self) -> str:
        return self.sky_text
    
    def __dict__(self) -> dict:
        return self._dict
    
    def __getitem__(self, key: str):
        if not key.startswith("@"): key = "@" + key
        return self._dict[key]

    def __init__(self, data: dict, _current: bool = False):
        """ Gets the forecast. """
        self._dict = data
        self.current = _current
    
        if _current:
            return
        
        self.low                 = int(data.get("@low", 0))
        self.high                = int(data.get("@high", 0))
        self.sky_code_day        = int(data.get("@skycodeday", 0))
        self.temperature         = (self.low + self.high) // 2
        self.sky_text            = data.get("@skytextday", "")
        self.day                 = data.get("@day")
        self.short_day           = data.get("@shortday")
        self.date                = datetime(*[int(i) for i in data["@date"].split("-")])
        self.time                = self.date # this is an alias
        self._date               = data["@date"]
        self.precipitation       = int(data["@precip"]) if data.get("@precip") else 0
        self.precip              = self.precipitation # this is an alias
    
    @staticmethod
    def _current(data: dict):
        _class = Forecast(None, _current=True)
        _class.temperature       = int(data.get("@temperature", 0))
        _class.sky_code          = int(data.get("@skycode", 0))
        _class.sky_text          = data.get("@skytext", "")
        _class.date              = datetime.strptime(f'{data["@date"]} {data["@observationtime"]}', "%Y-%d-%m %H:%M:%S")
        _class.time              = _class.date # this is an alias
        _class._date             = data["@date"]
        _class._observation_time = data["@observationtime"]
        _class.day               = data.get("@day")
        _class.short_day         = data.get("@shortday")
        _class.observation_point = data.get("@observationpoint")
        _class.feels_like        = int(data.get("@feelslike", 0))
        _class.humidity          = int(data["@humidity"] if data.get("humidity") else 0) # there are cases that this is an empty string.
        _class.wind_speed        = int(data.get("@windspeed", "0").split()[0])
        _class.wind_display      = data.get("@winddisplay", "")
        
        return _class