import sys
from os import path

sys.path.insert(0, path.join(path.dirname(path.realpath(__file__)), '..'))


import pytest
from util import _test_attributes

import python_weather


@pytest.fixture(params=iter(python_weather.Phase))
def phase(request: pytest.FixtureRequest) -> python_weather.Phase:
  return request.param


@pytest.fixture(params=iter(python_weather.WindDirection))
def wind_direction_value(request: pytest.FixtureRequest) -> str:
  return request.param.value


@pytest.mark.parametrize('index', range(-5, 60, 2))
def test_HeatIndex_works(index: int) -> None:
  _test_attributes(python_weather.HeatIndex._new(index, 1))


@pytest.mark.parametrize(
  'kind_id',
  (
    113,
    116,
    119,
    122,
    125,
    128,
    131,
    134,
    137,
    140,
    143,
    146,
    149,
    152,
    155,
    158,
    161,
    176,
    179,
    182,
    185,
    200,
    227,
    230,
    248,
    260,
    263,
    266,
    281,
    284,
    293,
    296,
    299,
    302,
    305,
    308,
    311,
    314,
    317,
    320,
    323,
    326,
    329,
    332,
    335,
    338,
    350,
    353,
    356,
    359,
    362,
    365,
    368,
    371,
    374,
    377,
    386,
    389,
    392,
    395,
  ),
)
def test_Kind_works(kind_id: int) -> None:
  kind = python_weather.Kind(kind_id)

  _test_attributes(kind)

  assert isinstance(kind.emoji, str)


def test_Phase_works(phase: python_weather.Phase) -> None:
  _test_attributes(phase)

  assert isinstance(phase.emoji, str)


@pytest.mark.parametrize('index', range(-5, 20, 2))
def test_UltraViolet_works(index: int) -> None:
  _test_attributes(python_weather.UltraViolet._new(index))


@pytest.mark.parametrize('degrees', range(0, 360, 5))
def test_WindDirection_works(wind_direction_value: str, degrees: int) -> None:
  wind_direction = python_weather.WindDirection._new(wind_direction_value, degrees)

  _test_attributes(wind_direction)

  assert isinstance(degrees in wind_direction, bool)
  assert isinstance(wind_direction.emoji, str)
