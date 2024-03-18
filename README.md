# [python-weather][pypi-url] [![pypi][pypi-image]][pypi-url] [![downloads][downloads-image]][pypi-url]

[pypi-image]: https://img.shields.io/pypi/v/python-weather.svg?style=flat-square
[pypi-url]: https://pypi.org/project/python-weather/
[downloads-image]: https://img.shields.io/pypi/dm/python-weather?style=flat-square

A free and asynchronous weather Python API wrapper made in Python, for Python.

## Installation

```console
$ pip install python-weather
```

## Example

For more information, please read the [documentation](https://python-weather.readthedocs.io/en/latest/).

```py
# import the module
import python_weather

import asyncio
import os

async def getweather():
  # declare the client. the measuring unit used defaults to the metric system (celcius, km/h, etc.)
  async with python_weather.Client(unit=python_weather.IMPERIAL) as client:
    # fetch a weather forecast from a city
    weather = await client.get('New York')
    
    # returns the current day's forecast temperature (int)
    print(weather.temperature)
    
    # get the weather forecast for a few days
    for daily in weather.daily_forecasts:
      print(daily)
      
      # hourly forecasts
      for hourly in daily.hourly_forecasts:
        print(f' --> {hourly!r}')

if __name__ == '__main__':
  # see https://stackoverflow.com/questions/45600579/asyncio-event-loop-is-closed-when-getting-loop
  # for more details
  if os.name == 'nt':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
  
  asyncio.run(getweather())
```
