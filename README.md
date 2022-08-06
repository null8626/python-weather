# python-weather
A free and asynchronous weather API wrapper made in python, for python.

## Library Example
```py
# import the module
import python_weather
import asyncio
import os

async def getweather():
  # declare the client. format defaults to the metric system (celcius, km/h, etc.)
  async with python_weather.Client(format=python_weather.IMPERIAL) as client:

    # fetch a weather forecast from a city
    weather = await client.get("New York")
  
    # returns the current day's forecast temperature (int)
    print(weather.current.temperature)
  
    # get the weather forecast for a few days
    for forecast in weather.forecasts:
      print(forecast.date, forecast.astronomy)
  
      # hourly forecasts
      for hourly in forecast.hourly:
        print(f' --> {hourly!r}')

if __name__ == "__main__":
  # see https://stackoverflow.com/questions/45600579/asyncio-event-loop-is-closed-when-getting-loop
  # for more details
  if os.name == "nt":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

  asyncio.run(getweather())
```

If you're running debian, make sure to install `aiohttp` first:

```console
sudo apt install python3-aiohttp
```

Otherwise install the ones in `requirements.txt`:

```console
python -m pip install -r requirements.txt
```

Use [example.py](https://github.com/null8626/python-weather/blob/master/example.py) for a quick run ;\)