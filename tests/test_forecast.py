from datetime import time

import pytest

from python_weather.forecast import _parse_time


@pytest.mark.parametrize(
  ('timestring', 'expected'),
  (
    ('12:48 PM', time(12, 48)),
    ('12:00 PM', time(12, 0)),
    ('12:00 AM', time(0, 0)),
    ('01:15 PM', time(13, 15)),
  ),
)
def test_parse_time_handles_noon_and_midnight(
  timestring: str, expected: time
) -> None:
  assert _parse_time(timestring) == expected
