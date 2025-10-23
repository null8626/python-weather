from contextlib import nullcontext
from inspect import getmembers
from typing import Any
from sys import stdout
from os import path
import aiohttp
import json
import mock


CURRENT_DIR = path.dirname(path.realpath(__file__))
INDENTATION = 2
BASIC_SPECIAL_METHOD_NAMES = (
  '__hash__',
  '__int__',
  '__float__',
  '__len__',
  '__str__',
  '__repr__',
)
COMPARISON_SPECIAL_METHOD_NAMES = (
  '__lt__',
  '__le__',
  '__gt__',
  '__ge__',
  '__eq__',
  '__ne__',
)


def is_local(data: object) -> bool:
  return getattr(data, '__module__', '').startswith('python_weather')


def _test_attributes_inner(obj: object, indent_level: int) -> None:
  names = obj.__class__.__slots__ + tuple(
    map(
      lambda pair: pair[0], getmembers(obj.__class__, lambda o: isinstance(o, property))
    )
  )

  for name in names:
    stdout.write(f'{" " * indent_level}{obj.__class__.__name__}.{name}')
    data = (
      getattr(obj, f'_{obj.__class__.__name__}{name}')
      if name.startswith('__')
      else getattr(obj, name)
    )

    if isinstance(data, list) and data:
      stdout.write('[0] -> ')

      for i, each in enumerate(data):
        if i > 0:
          stdout.write(f'{" " * indent_level}{obj.__class__.__name__}.{name}[{i}] -> ')

        print(repr(each))
        _test_attributes_inner(each, indent_level + INDENTATION)

      continue

    print(f' -> {data!r}')

    if is_local(data):
      _test_attributes_inner(data, indent_level + INDENTATION)

  for special_method_name in BASIC_SPECIAL_METHOD_NAMES:
    if special_method := getattr(obj, special_method_name, None):
      print(
        f'{" " * indent_level}{obj.__class__.__name__}.{special_method_name} -> {special_method()!r}'
      )

  for special_method_name in COMPARISON_SPECIAL_METHOD_NAMES:
    if special_method := getattr(obj, special_method_name, None):
      print(
        f'{" " * indent_level}{obj.__class__.__name__}.{special_method_name}(self) -> {special_method(obj)!r}'
      )

  if hasattr(obj, '__iter__'):
    try:
      _ = next(iter(obj))

      stdout.write(f'{" " * indent_level}{obj.__class__.__name__}.__iter__[0] -> ')

      for i, each in enumerate(obj):
        if i > 0:
          stdout.write(
            f'{" " * indent_level}{obj.__class__.__name__}.__iter__[{i}] -> '
          )

        print(repr(each))
        _test_attributes_inner(each, indent_level + INDENTATION)
    except StopIteration:
      print(f'{" " * indent_level}{obj.__class__.__name__}.__iter__ -> {iter(obj)!r}')


def _test_attributes(obj: object) -> None:
  print(f'{obj!r} -> ')
  _test_attributes_inner(obj, INDENTATION)


class RequestMock:
  __slots__: tuple[str, ...] = (
    '__mock_response',
    '__mock_json_response',
    '__mock_json_response_filename',
  )

  def __init__(self, status: int, reason: str, mock_response_filename: str = None):
    self.__mock_response = mock.Mock(specs=aiohttp.ClientResponse)

    self.__mock_response.status = status
    self.__mock_response.reason = reason

    raise_for_status_kwargs = {}

    if 200 <= status < 300:
      raise_for_status_kwargs['return_value'] = None

      self.__mock_json_response_filename = mock_response_filename
    else:
      raise_for_status_kwargs['side_effect'] = aiohttp.ClientResponseError(
        None, (), status=status, message=reason
      )

    self.__mock_response.raise_for_status = mock.Mock(**raise_for_status_kwargs)

  def __enter__(self) -> mock.Mock:
    if 200 <= self.__mock_response.status < 300:
      self.__mock_json_response = open(
        path.join(CURRENT_DIR, self.__mock_json_response_filename), 'r'
      )
      self.__mock_response.json = mock.AsyncMock(
        return_value=json.loads(self.__mock_json_response.read())
      )

    return mock.Mock(return_value=nullcontext(self.__mock_response))

  def __exit__(self, *_: Any) -> None:
    if 200 <= self.__mock_response.status < 300:
      self.__mock_json_response.close()
