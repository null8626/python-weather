from inspect import isgenerator
from sys import stdout
import python_weather
import asyncio
import os

INDENTATION = 2

is_local = lambda data: getattr(data, '__module__', '').startswith('python_weather') # yapf: disable

def _test(obj, indent_level):
  for name in dir(obj.__class__):
    attr = getattr(obj.__class__, name)
    
    if isinstance(attr, property) and attr.fget:
      stdout.write(f'{" " * indent_level}{obj.__class__.__name__}.{name}')
      
      data = getattr(obj, name)
      
      if isgenerator(data):
        stdout.write('[0] -> ')
        
        for i, each in enumerate(data):
          if i > 0:
            stdout.write(
              f'{" " * indent_level}{obj.__class__.__name__}.{name}[{i}] -> '
            )
          
          print(repr(each))
          _test(each, indent_level + INDENTATION)
        
        continue
      
      print(f' -> {data!r}')
      
      if is_local(data):
        _test(data, indent_level + INDENTATION)

def test(obj):
  print(f'{obj!r} -> ')
  _test(obj, INDENTATION)

async def getweather():
  async with python_weather.Client(unit=python_weather.IMPERIAL) as client:
    test(await client.get('New York'))

if __name__ == '__main__':
  if os.name == 'nt':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
  
  asyncio.run(getweather())
