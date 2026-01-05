# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2021-2026 null8626

from aiohttp import ClientSession, ClientTimeout, ClientResponseError, TCPConnector
from urllib.parse import quote_plus
from asyncio import sleep

from .errors import Error, RequestError
from .constants import _Unit, METRIC
from .base import CustomizableBase
from .forecast import Forecast
from .version import VERSION
from .enums import Locale


class Client(CustomizableBase):
  """
  Interact with the API's endpoints.

  Examples:

  .. code-block:: python

    # Explicit cleanup
    client = python_weather.Client(unit=python_weather.IMPERIAL)

    # ...

    await client.close()

    # Implicit cleanup
    async with python_weather.Client(unit=python_weather.IMPERIAL) as client:
      # ...

  :param unit: Whether to use the metric or imperial/customary system (:data:`~.constants.IMPERIAL`). Defaults to :data:`~.constants.METRIC`.
  :type unit: ``_Unit``
  :param locale: Whether to use a different locale/language as the description for the returned forecast. Defaults to :attr:`.Locale.ENGLISH`.
  :type locale: :class:`.Locale`
  :param session: Whether to use an existing :class:`~aiohttp.ClientSession` for requesting or not. Defaults to :py:obj:`None` (creates a new one instead).
  :type session: :class:`~aiohttp.ClientSession` | :py:obj:`None`
  :param max_retries: Maximum amount of retries upon request failure before raising a :class:`.RequestError`.
                      Use ``-1`` to disable (NOT recommended). Defaults to 3 retries.
  :type max_retries: :class:`int` | :py:obj:`None`

  :exception Error: ``unit`` is not :data:`~.constants.METRIC` or :data:`~.constants.IMPERIAL` or ``locale`` is not a part of the :class:`.Locale` enum.
  """

  __slots__: tuple[str, ...] = '__own_session', '__session', '_max_retries'

  __own_session: bool
  __session: ClientSession
  _max_retries: int

  def __init__(
    self,
    *,
    unit: _Unit = METRIC,
    locale: Locale = Locale.ENGLISH,
    session: ClientSession | None = None,
    max_retries: int | None = None,
  ):
    super().__init__(unit, locale)

    self.__own_session = session is None
    self.__session = session or ClientSession(
      timeout=ClientTimeout(total=5000.0),
      connector=TCPConnector(ssl=False),
    )
    self._max_retries = max_retries or 3

  def __repr__(self) -> str:
    return f'<{__class__.__module__}.{__class__.__name__} {self.__session!r}>'

  async def get(
    self,
    location: str,
    *,
    unit: _Unit | None = None,
    locale: Locale | None = None,
  ) -> Forecast:
    """
    Fetches a weather forecast for a specific location.

    Example:

    .. code-block:: python

      weather = await client.get('New York')

    :param location: The requested location.
    :type location: :py:class:`str`
    :param unit: Overrides the unit used.
    :type unit: ``_Unit`` | :py:obj:`None`
    :param locale: Overrides the locale used.
    :type locale: :class:`.Locale` | :py:obj:`None`

    :exception TypeError: ``location`` is not a :py:class:`str` or is empty.
    :exception Error: The client is already closed.
    :exception RequestError: The client received a non-favorable response from the API.

    :returns: The requested weather forecast.
    :rtype: Forecast
    """

    if self.__session.closed:
      raise Error('Client session is already closed.')

    elif not isinstance(location, str) or not location:
      raise TypeError(f'Expected a proper location str, got {location!r}')

    if not isinstance(unit, _Unit):
      unit = self._unit

    if not isinstance(locale, Locale):
      locale = self._locale

    subdomain = f'{locale.value}.' if locale != Locale.ENGLISH else ''
    attempts = 0

    status = None
    reason = None

    while True:
      try:
        async with self.__session.get(
          f'https://{subdomain}wttr.in/{quote_plus(location)}?format=j1',
          headers={
            'Content-Type': 'application/json',
            'User-Agent': f'python_weather (https://github.com/null8626/python-weather {VERSION}) Python/',
          },
        ) as resp:
          status = resp.status
          reason = resp.reason

          resp.raise_for_status()

          return Forecast(await resp.json(), unit, locale)
      except ClientResponseError:
        if attempts == self._max_retries:
          raise RequestError(status, reason) from None

        await sleep(0.5 * (2**attempts))
        attempts += 1

  async def close(self) -> None:
    """
    Closes the :class:`.Client` object.

    Example:

    .. code-block:: python

      await client.close()
    """

    if self.__own_session and not self.__session.closed:
      await self.__session.close()

  async def __aenter__(self) -> 'Client':
    return self

  async def __aexit__(self, *_, **__) -> None:
    await self.close()
