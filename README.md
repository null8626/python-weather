# python-weather
A free and asynchronous weather API wrapper made in python.

## Simple Usage
```py
# import the module
import python_weather

# declare the client. format defaults to metric system (celcius, km/h, etc.)
client = python_weather.Client(format=python_weather.IMPERIAL)

# fetch a weather forecast from a city
weather = await client.find("Washington DC")

# returns the current city temperature (int)
print(weather.current.temperature)

# get the weather forecast for a few days
for forecast in weather.forecast:
    print(str(forecast.date), forecast.sky_text, forecast.temperature)

# close the wrapper once done
await client.close()
```

Note:  Use example.py for quick run :)
