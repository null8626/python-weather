from sys import stdout
import python_weather
import asyncio
import os

INDENTATION = 2


def is_local(data: object) -> bool:
  return getattr(data, '__module__', '').startswith('python_weather')


def _test_attributes(obj: object, indent_level: int) -> None:
  for name in obj.__class__.__slots__:
    stdout.write(f'{" " * indent_level}{obj.__class__.__name__}.{name}')
    data = getattr(obj, name)

    if isinstance(data, list):
      stdout.write('[0] -> ')

      for i, each in enumerate(data):
        if i > 0:
          stdout.write(f'{" " * indent_level}{obj.__class__.__name__}.{name}[{i}] -> ')

        print(repr(each))
        _test_attributes(each, indent_level + INDENTATION)

      continue

    print(f' -> {data!r}')

    if is_local(data):
      _test_attributes(data, indent_level + INDENTATION)


def test_attributes(weather: python_weather.forecast.Forecast) -> None:
  print(f'{weather!r} -> ')
  _test_attributes(weather, INDENTATION)


def example_code(weather: python_weather.forecast.Forecast) -> None:
  print(weather.temperature)

  for daily in weather:
    print(daily)

    for hourly in daily:
      print(f' --> {hourly!r}')


async def test(client: python_weather.Client) -> None:
  weather = await client.get('New York')

  example_code(weather)
  test_attributes(weather)


async def getweather() -> None:
  async with python_weather.Client(unit=python_weather.IMPERIAL) as client:
    await test(client)

  async with python_weather.Client(unit=python_weather.METRIC) as client:
    await test(client)


if __name__ == '__main__':
  if os.name == 'nt':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

  asyncio.run(getweather())
