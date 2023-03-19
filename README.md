# [python-weather][pypi-url] [![pypi][pypi-image]][pypi-url] [![downloads][downloads-image]][pypi-url] [![Build Status][ci-image]][ci-url] [![languages][languages-image]][github-url] [![libraries.io dependents][libraries-io-dependents-image]][libraries-io-url] [![libraries.io score][libraries-io-score-image]][libraries-io-url] [![github code size][github-code-size-image]][github-url] [![license][github-license-image]][github-license-url] [![BLAZINGLY FAST!!!][blazingly-fast-image]][blazingly-fast-url]

[pypi-image]: https://img.shields.io/pypi/v/python-weather.svg?style=flat-square
[pypi-url]: https://pypi.org/project/python-weather/
[downloads-image]: https://img.shields.io/pypi/dm/python-weather?style=flat-square
[ci-image]: https://github.com/null8626/python-weather/workflows/CI/badge.svg
[ci-url]: https://github.com/null8626/python-weather/actions
[languages-image]: https://img.shields.io/github/languages/top/null8626/python-weather?style=flat-square
[libraries-io-dependents-image]: https://img.shields.io/librariesio/dependents/pypi/python-weather?style=flat-square
[libraries-io-score-image]: https://img.shields.io/librariesio/sourcerank/pypi/python-weather?style=flat-square
[libraries-io-url]: https://libraries.io/pypi/python-weather
[github-url]: https://github.com/null8626/python-weather
[github-code-size-image]: https://img.shields.io/github/languages/code-size/null8626/python-weather?style=flat-square
[github-license-image]: https://img.shields.io/github/license/null8626/python-weather?style=flat-square
[github-license-url]: https://github.com/null8626/python-weather/blob/main/LICENSE
[blazingly-fast-image]: https://img.shields.io/badge/speed-BLAZINGLY%20FAST!!!%20%F0%9F%94%A5%F0%9F%9A%80%F0%9F%92%AA%F0%9F%98%8E-brightgreen.svg?style=flat-square
[blazingly-fast-url]: https://twitter.com/acdlite/status/974390255393505280

A free and asynchronous weather API wrapper made in Python, for Python.

## Example

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
    print(weather.current.temperature)
    
    # get the weather forecast for a few days
    for forecast in weather.forecasts:
      print(forecast)
      
      # hourly forecasts
      for hourly in forecast.hourly:
        print(f' --> {hourly!r}')

if __name__ == '__main__':
  # see https://stackoverflow.com/questions/45600579/asyncio-event-loop-is-closed-when-getting-loop
  # for more details
  if os.name == 'nt':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
  
  asyncio.run(getweather())
```

If you're running Debian, make sure to install [`aiohttp`](https://github.com/aio-libs/aiohttp) first:

```shell
sudo apt install python3-aiohttp
```

Otherwise install the ones in `pyproject.toml` by running:

```shell
python -m pip install .
```
