from os import path
import sys

sys.path.insert(0, path.join(path.dirname(path.realpath(__file__)), '..'))


import pytest_asyncio
import typing
import pytest
import mock

import python_weather

from util import _test_attributes, RequestMock


def example_code(weather: python_weather.forecast.Forecast) -> None:
  print(weather.temperature)

  for daily in weather:
    print(daily)

    for hourly in daily:
      print(f' --> {hourly!r}')


@pytest_asyncio.fixture(params=[python_weather.METRIC, python_weather.IMPERIAL])
async def client(
  request: pytest.FixtureRequest,
) -> typing.AsyncGenerator[python_weather.Client, None]:
  client = python_weather.Client(unit=request.param)

  yield client
  await client.close()


@pytest.mark.parametrize(
  'mock_response_path', ('mock_response_1.json', 'mock_response_2.json')
)
@pytest.mark.asyncio
async def test_Client_works(
  monkeypatch: pytest.MonkeyPatch,
  client: python_weather.Client,
  mock_response_path: str,
) -> None:
  _test_attributes(client)

  with RequestMock(200, 'OK', mock_response_path) as request:
    monkeypatch.setattr('aiohttp.ClientSession.get', request)

    weather = await client.get('New York')

    example_code(weather)
    _test_attributes(weather)

    request.assert_called_once()


@pytest.mark.parametrize(
  'unit', (None, '', 'C', 'F', 'METRIC', 'IMPERIAL', python_weather.constants._Unit)
)
def test_Client_throws_invalid_unit_error(
  client: python_weather.Client, unit: typing.Any
) -> None:
  with pytest.raises(python_weather.Error, match='^Invalid measuring unit specified!$'):
    client.unit = unit


@pytest.mark.parametrize(
  'locale', (None, '', 'CHINESE_SIMPLIFIED', 'zh', python_weather.enums.Locale)
)
def test_Client_throws_invalid_locale_error(
  client: python_weather.Client, locale: typing.Any
) -> None:
  with pytest.raises(python_weather.Error, match='to be a Locale enum$'):
    client.locale = locale


@pytest.mark.asyncio
async def test_Client_throws_already_closed_error(
  monkeypatch: pytest.MonkeyPatch, client: python_weather.Client
) -> None:
  monkeypatch.setattr(
    'aiohttp.ClientSession.closed', mock.PropertyMock(return_value=True)
  )

  with pytest.raises(
    python_weather.Error, match='^Client session is already closed\\.$'
  ):
    await client.get('New York')


@pytest.mark.asyncio
@pytest.mark.parametrize('location', (None, '', 2, (), {}, []))
async def test_Client_throws_invalid_location_error(
  client: python_weather.Client, location: typing.Any
) -> None:
  with pytest.raises(TypeError, match='^Expected a proper location str, got '):
    await client.get(location)


@pytest.mark.asyncio
async def test_Client_throws_request_error(
  monkeypatch: pytest.MonkeyPatch, client: python_weather.Client
) -> None:
  with RequestMock(404, 'Not Found') as request:
    monkeypatch.setattr('aiohttp.ClientSession.get', request)

    with pytest.raises(python_weather.RequestError, match='^404: Not Found$'):
      await client.get('New York')

    assert request.call_count == (client._Client__max_retries + 1)
