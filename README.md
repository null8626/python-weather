# [python-weather][pypi-url] [![pypi][pypi-image]][pypi-url] [![downloads][downloads-image]][pypi-url] [![codacy-badge][codacy-url]][codacy-image] [![ko-fi][ko-fi-brief-image]][ko-fi-url]

[pypi-image]: https://img.shields.io/pypi/v/python-weather.svg?style=flat-square
[pypi-url]: https://pypi.org/project/python-weather/
[downloads-image]: https://img.shields.io/pypi/dm/python-weather?style=flat-square
[ko-fi-brief-image]: https://img.shields.io/badge/donations-ko--fi-red?color=ff5e5b&style=flat-square
[codacy-url]: https://app.codacy.com/project/badge/Grade/0f7721b7e4314a748c75a04f0a7e0ce3
[codacy-image]: https://app.codacy.com/gh/null8626/python-weather/dashboard
[ko-fi-image]: https://ko-fi.com/img/githubbutton_sm.svg
[ko-fi-url]: https://ko-fi.com/null8626

A free and asynchronous weather Python API wrapper made in Python, for Python.

## Getting started

Run the following command in your terminal:

```console
$ pip install python-weather
```

## Example

For more information, please read the [documentation](https://python-weather.readthedocs.io/en/latest/).

```py
# Import the module.
import python_weather

import asyncio
import os


async def main() -> None:
  
  # Declare the client. The measuring unit used defaults to the metric system (celcius, km/h, etc.)
  async with python_weather.Client(unit=python_weather.IMPERIAL) as client:
    
    # Fetch a weather forecast from a city.
    weather = await client.get('New York')
    
    # Fetch the temperature for today.
    print(weather.temperature)
    
    # Fetch weather forecast for upcoming days.
    for daily in weather:
      print(daily)
    
      # Each daily forecast has their own hourly forecasts.
      for hourly in daily:
        print(f' --> {hourly!r}')

if __name__ == '__main__':
  
  # See https://stackoverflow.com/questions/45600579/asyncio-event-loop-is-closed-when-getting-loop
  # for more details.
  if os.name == 'nt':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
  
  asyncio.run(main())
```

## Data source

This library depends on [`wttr.in`](https://github.com/chubin/wttr.in), which uses data from the [World Weather Online API](https://www.worldweatheronline.com/weather-api/).

## Donations

If you want to support this project, consider donating! ❤

[![ko-fi][ko-fi-image]][ko-fi-url]
