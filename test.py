from inspect import isgenerator
from sys import stdout
import python_weather
import traceback
import asyncio
import os

INDENTATION_LEVEL = 2

def test_properties(obj, indent_level = 0, generator_name = None, index = 0):
  for name in dir(obj.__class__):
    attr = getattr(obj.__class__, name)
    
    if isinstance(attr, property) and attr.fget:
      data = attr.fget(obj)
      
      try:
        if isgenerator(data):
          for i, each in enumerate(data):
            if not test_properties(each, indent_level + INDENTATION_LEVEL, f'{obj.__class__.__name__}#{name}', i):
              return False
          
          continue
        
        stdout.write(' ' * indent_level)
        
        if generator_name is not None:
          stdout.write(f'{generator_name}[{index}]: ')
        
        stdout.write(f'{obj.__class__.__name__}#{name} -> ')
        
        if getattr(data, '__module__', '').startswith('python_weather'):
          stdout.write('\n')
        
          if not test_properties(data, indent_level + INDENTATION_LEVEL):
            return False
        else:
          print(repr(data))
      except:
        print(f'error: cannot retrieve {obj.__class__.__name__}#{name}:\n\n{traceback.format_exc()}')
        
        return False
  
  return True

async def getweather():
  async with python_weather.Client(unit=python_weather.IMPERIAL) as client:
    if not test_properties(await client.get('New York')):
      exit(1)

if __name__ == '__main__':
  if os.name == 'nt':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
  
  asyncio.run(getweather())