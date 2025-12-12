from multidict import CIMultiDict, CIMultiDictProxy
from typing import Any, TYPE_CHECKING
from contextlib import nullcontext
from inspect import getmembers
from sys import stdout
from yarl import URL
from os import path
import aiohttp
import json
import mock

if TYPE_CHECKING:
  from io import TextIOWrapper


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
  names = getattr(obj.__class__, '__slots__', ()) + tuple(
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

  if obj_iter := getattr(obj, '__iter__', None):
    try:
      _ = next(obj_iter())

      stdout.write(f'{" " * indent_level}{obj.__class__.__name__}.__iter__[0] -> ')

      for i, each in enumerate(obj_iter()):
        if i > 0:
          stdout.write(
            f'{" " * indent_level}{obj.__class__.__name__}.__iter__[{i}] -> '
          )

        print(repr(each))
        _test_attributes_inner(each, indent_level + INDENTATION)
    except StopIteration:
      print(f'{" " * indent_level}{obj.__class__.__name__}.__iter__ -> {obj_iter()!r}')


def _test_attributes(obj: object) -> None:
  print(f'{obj!r} -> ')
  _test_attributes_inner(obj, INDENTATION)


class RequestMock:
  __slots__: tuple[str, ...] = (
    '__mock_response',
    '__mock_json_response',
  )

  __mock_response: mock.Mock
  __mock_json_response: 'TextIOWrapper | None'

  def __init__(self, status: int, reason: str, mock_response: str | None = None):
    self.__mock_response = mock.Mock(specs=aiohttp.ClientResponse)

    self.__mock_response.status = status
    self.__mock_response.reason = reason

    self.__mock_json_response = None

    if mock_response is not None:
      self.__mock_json_response = open(path.join(CURRENT_DIR, mock_response), 'r')
      self.__mock_response.json = mock.AsyncMock(
        return_value=json.loads(self.__mock_json_response.read())
      )

    raise_for_status_kwargs = {}

    if 200 <= status < 300:
      raise_for_status_kwargs['return_value'] = None
    else:
      raise_for_status_kwargs['side_effect'] = aiohttp.ClientResponseError(
        aiohttp.RequestInfo(
          url=URL('http://example.com'),
          method='GET',
          headers=CIMultiDictProxy(CIMultiDict()),
          real_url=URL('http://example.com'),
        ),
        (),
        status=status,
        message=reason,
      )

    self.__mock_response.raise_for_status = mock.Mock(**raise_for_status_kwargs)

  def __enter__(self) -> mock.Mock:
    return mock.Mock(return_value=nullcontext(self.__mock_response))

  def __exit__(self, *_: Any) -> None:
    if self.__mock_json_response is not None:
      self.__mock_json_response.close()
      self.__mock_json_response = None
