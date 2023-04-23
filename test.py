from inspect import isgenerator
from sys import stdout
import python_weather
import traceback
import asyncio
import os

INDENTATION = 2

def _test_properties(obj, indent_level=0, in_recursion=False):
  exists = not in_recursion
  
  for name in dir(obj.__class__):
    attr = getattr(obj.__class__, name)
    
    if isinstance(attr, property) and attr.fget:
      if not exists:
        print()
        exists = True
      
      stdout.write(f'{" " * indent_level}{obj.__class__.__name__}#{name}')
      
      data = attr.fget(obj)
      
      if isgenerator(data):
        stdout.write('[0] -> ')
        
        for i, each in enumerate(data):
          if i > 0:
            stdout.write(
              f'{" " * indent_level}{obj.__class__.__name__}#{name}[{i}] -> '
            )
          
          _test_properties(each, indent_level + INDENTATION, True)
        
        continue
      
      stdout.write(' -> ')
      
      if getattr(data, '__module__', '').startswith('python_weather'):
        _test_properties(data, indent_level + INDENTATION, True)
      else:
        print(repr(data))
  
  if not exists:
    print(repr(obj))

def test(obj):
  try:
    _test_properties(obj)
  except:
    print(f'\n\n{traceback.format_exc().rstrip()}')
    exit(1)

async def getweather():
  async with python_weather.Client(unit=python_weather.IMPERIAL) as client:
    test(await client.get('New York'))

if __name__ == '__main__':
  if os.name == 'nt':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
  
  asyncio.run(getweather())
