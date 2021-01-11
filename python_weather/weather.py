from xmltodict import parse as _xmltodict
from .forecast import Forecast

from urllib.parse import quote_plus as _encode_uri
from collections import OrderedDict as bad_dict
from io import BytesIO
from json import dumps

class WeatherException(Exception):
    def __init__(self, response: str, message: str):
        self.raw_response = response
        super().__init__(message)

class Weather(object):
    REPR_ATTRS = ("weather_location_name", "degree_type", "lat", "long")

    def __dict__(self) -> dict:
        return self.dict

    def __getitem__(self, key):
        if isinstance(key, int):
            return self.forecast[key]
    
        return self.dict[key]

    def __repr__(self) -> str:
        return f"<Weather {' '.join([f'{i}={getattr(self, i)}' for i in Weather.REPR_ATTRS])}>"

    def __init__(self, response: str):
        self._raw = response
        self._parsed = _xmltodict(self._raw)
        self.dict = self._parse(self._parsed)
        
        if self.dict.get("string"):
            raise WeatherException(self._raw, self.dict["string"])
        
        del self._parsed
        
        data = self.dict["weatherdata"]["weather"][0]
        self.weather_location_code = data.get("@weatherlocationcode")
        self.weather_location_name = data.get("@weatherlocationname")
        self.url                   = data.get("@url")
        self.image_relative_url    = data.get("@imagerelativeurl")
        self.degree_type           = data.get("@degreetype", "C")
        self.provider              = data.get("@provider")
        self.attribution           = (data.get("@attribution"), data.get("@attribution2")) if data.get("@attribution2") else data.get("@attribution")
        self.lat                   = float(data.get("@lat", 0))
        self.long                  = float(data.get("@long", 0))
        self.timezone              = int(data.get("@timezone", 0))
        self.alert                 = data.get("@alert")
        self.entity_id             = int(data.get("@entityid", 0))
        self.encoded_location_name = data.get("@encodedlocationname", (_encode_uri(self.weather_location_name or "")))
        self.current               = Forecast._current(data["current"])
        self.forecast              = []
        
        for forecast in data["forecast"]:
            self.forecast.append(Forecast(forecast))
    
    def save(self, file_or_buffer, xml=False) -> int:
        """ Saves the XML/JSON data = """
        file_format = ".xml" if xml else ".json"
        data = self._raw if xml else dumps(self.dict)
    
        if isinstance(file_or_buffer, BytesIO):
            return file_or_buffer.write(data.encode("utf-8"))
        with open((file_or_buffer if file_or_buffer.lower().endswith(file_format) else file_or_buffer + file_format), "w+", encoding="utf-8") as _file:
            _data = _file.write(data)
            _file.close()
            return _data
    
    def _parse(self, _dict) -> dict:
        _dict = dict(_dict)
        for key in _dict.keys():
            if isinstance(_dict[key], bad_dict):
                _dict[key] = self._parse(_dict[key]) # the power of recursion boiii
            elif isinstance(_dict[key], list):
                for i, v in enumerate(_dict[key]):
                    if isinstance(v, bad_dict):
                        _dict[key][i] = self._parse(v) # the power of recursion boiii
        return _dict