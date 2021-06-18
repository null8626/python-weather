# python-weather
A free and asynchronous weather API wrapper made in python.

## Library Example
```py
# import the module
import python_weather
import asyncio

async def getweather():
    # declare the client. format defaults to metric system (celcius, km/h, etc.)
    client = python_weather.Client(format=python_weather.IMPERIAL)

    # fetch a weather forecast from a city
    weather = await client.find("Washington DC")

    # returns the current day's forecast temperature (int)
    print(weather.current.temperature)

    # get the weather forecast for a few days
    for forecast in weather.forecasts:
        print(str(forecast.date), forecast.sky_text, forecast.temperature)

    # close the wrapper once done
    await client.close()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(getweather())
```

Use [example.py](https://github.com/vierofernando/python-weather/blob/master/example.py?raw=1) for a quick run ;\)

## Weather CLI
This package also contains a simple weather CLI for it.
To get all usage and supported flags, run:
```bash
$ weather -h
```

Examples:
```bash
$ weather washington dc -u f -c
$ weather washington dc -o file.json
```