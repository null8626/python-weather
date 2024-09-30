Changelog
=========

+---------+-------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Version | Release date      | Changes                                                                                                                                                        |
+=========+===================+================================================================================================================================================================+
| 0.2.1   | 10 January 2021   | - 🟩 Create ``python-weather``.                                                                                                                                |
+---------+-------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 0.2.3   | 11 January 2021   | - 🟦 Fix an :py:class:`IndexError` while initiating :class:`Weather`.                                                                                          |
|         |                   | - 🟥 Remove ``__getattribute__`` from :class:`Weather`.                                                                                                        |
+---------+-------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 0.3.0   | 24 May 2021       | - 🟦 Use properties instead of directly storing attributes.                                                                                                    |
|         |                   | - 🟩 Add built-in caching capabilities.                                                                                                                        |
|         |                   | - 🟥 Rename ``Weather.forecast`` to ``Weather.forecasts``.                                                                                                     |
|         |                   | - 🟩 Add an exception class ``HTTPException``.                                                                                                                 |
|         |                   | - 🟩 Add ``__slots__`` to class definitions.                                                                                                                   |
|         |                   | - 🟩 Add ``example.py`` in the project root directory.                                                                                                         |
|         |                   | - 🟦 Use python's walrus operator to clean up repetitive code.                                                                                                 |
|         |                   | - 🟦 Implement Python's inheritance rather than keeping everything in one class.                                                                               |
|         |                   | - 🟦 Separate ``Client`` from ``HTTPClient``.                                                                                                                  |
|         |                   | - 🟦 Improve the example in README.                                                                                                                            |
+---------+-------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 0.3.3   | 18 June 2021      | - 🟩 Add a bundled-in CLI.                                                                                                                                     |
|         |                   | - 🟩 Add ``Weather.format`` property.                                                                                                                          |
|         |                   | - 🟩 Add ``Weather.locale`` property.                                                                                                                          |
|         |                   | - 🟦 Improve the project's typings.                                                                                                                            |
|         |                   | - 🟩 Add ``.gitignore`` in the project's root to remove ``__pycache__`` from appearing.                                                                        |
|         |                   | - 🟦 Tweaks to the project's documentation.                                                                                                                    |
+---------+-------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 0.3.4   | 27 June 2021      | - 🟦 Fix backwards-compatibility for Python 3.7 users by removing all walrus operators.                                                                        |
+---------+-------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 0.3.5   | 29 June 2021      | - 🟦 Fix typo that causes a :py:class:`NameError`.                                                                                                             |
+---------+-------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 0.3.6   | 26 July 2021      | - 🟦 Fix bug that causes ``IMPERIAL`` to have no effect.                                                                                                       |
+---------+-------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 0.3.7   | 5 November 2021   | - 🟦 Fix bug that raises an exception when calling ``HTTPException.__repr__``.                                                                                 |
|         |                   | - 🟦 ``HTTPException`` now derives from the :py:class:`Exception` class.                                                                                       |
|         |                   | - 🟩 Add ``__slots__`` to the class definition for ``HTTPException``.                                                                                          |
+---------+-------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 0.3.8   | 28 June 2022      | - 🟥 Remove the bundled-in CLI.                                                                                                                                |
|         |                   | - 🟦 Fix potential :py:class:`NameError` bug.                                                                                                                  |
|         |                   | - 🟥 Remove all built-in caching capabilities.                                                                                                                 |
|         |                   | - 🟦 Update the example with a fix for all Windows systems.                                                                                                    |
|         |                   | - 🟩 Add GitHub workflows for testing.                                                                                                                         |
+---------+-------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 0.4.0   | 6 August 2022     | - 🟦 Migrate from using Microsoft's MSN API to ``wttr.in``.                                                                                                    |
|         |                   | - 🟦 Fix dependabot alerts.                                                                                                                                    |
|         |                   | - 🟩 Add ``async with`` support for the client instance.                                                                                                       |
|         |                   | - 🟩 Add additional installation instructions for debian users.                                                                                                |
+---------+-------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 0.4.1   | 8 August 2022     | - 🟦 Fix bug when retrieving ``CurrentForecast.local_time``.                                                                                                   |
+---------+-------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 0.4.2   | 9 September 2022  | - 🟥 Rename ``DailyForecast.average_temperature`` to ``DailyForecast.temperature``.                                                                            |
|         |                   | - 🟦 Printing the forecast result should no longer raise an :py:class:`AttributeError`.                                                                        |
|         |                   | - 🟦 ``Weather.location`` should not return ``None`` now, and should return floats insead of ints. (making it consistent to the type-hint)                     |
|         |                   | - 🟩 Add ``Mist`` property to the ``WeatherType`` enum.                                                                                                        |
|         |                   | - 🟩 Add an additional ``TCPConnector`` argument to the default ``ClientSession``.                                                                             |
|         |                   | - 🟥 Remove unused ``__slots__`` tuple member in the ``BaseForecast`` abstract class.                                                                          |
+---------+-------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 0.4.3   | 23 October 2022   | - 🟦 The ``HourlyForecast.time`` property should return a ``datetime`` ``time`` object instead of a raw API :py:class:`int`.                                   |
+---------+-------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 1.0.0   | 28 April 2023     | - 🟩 Add custom locale support.                                                                                                                                |
|         |                   | - 🟩 Add lots of new classes and enums, and improve inheritance use.                                                                                           |
|         |                   | - 🟩 Add code testing workflow on every commit.                                                                                                                |
|         |                   | - 🟩 Add code formatting workflow with ``yapf``.                                                                                                               |
|         |                   | - 🟩 Add dependabot to automatically bump dependencies weekly.                                                                                                 |
+---------+-------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 1.0.1   | 29 April 2023     | - 🟦 Fix backwards-compatibility for Python 3.7 users by removing the ``Self`` typing.                                                                         |
+---------+-------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 1.0.2   | 18 May 2023       | - 🟦 Fix ``tempC`` and ``tempF`` :py:class:`KeyError`.                                                                                                         |
|         |                   | - 🟦 Fix :class:`UltraViolet` enum returning incorrect values.                                                                                                 |
+---------+-------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 1.0.3   | 20 June 2023      | - 🟩 Add missing ``index`` property in the :class:`UltraViolet` enum.                                                                                          |
|         |                   | - 🟩 Add more helper methods.                                                                                                                                  |
|         |                   | - 🟦 Improve docstrings of several properties.                                                                                                                 |
+---------+-------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 1.1.0   | 23 November 2023  | - 🟩 Add support for Python 3.12 by upgrading the ``aiohttp`` dependency to v3.9.0.                                                                            |
|         |                   | - 🟥 The library no longer supports Python 3.7, which was discontinued in June 2023.                                                                           |
|         |                   | - 🟦 Removed several instances of copy-pasted code.                                                                                                            |
+---------+-------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 1.1.1   | 20 February 2024  | - 🟥 Rename ``chances_of_remdry`` to ``chances_of_remaining_dry`` in order to reduce confusion.                                                                |
|         |                   | - 🟦 Bump ``aiohttp`` dependency from v3.9.0 to v3.9.3.                                                                                                        |
+---------+-------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 1.1.2   | 25 February 2024  | - 🟩 Add official project documentation in https://python-weather.readthedocs.io/en/latest/.                                                                   |
+---------+-------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 2.0.0   | 18 March 2024     | - 🟥 Rename the main forecast's class name from ``Weather`` to :class:`Forecast`.                                                                              |
|         |                   | - 🟥 Merge ``CurrentForecast`` class' properties with :class:`Forecast`'s. Therefore the ``current`` property is removed.                                      |
|         |                   | - 🟥 Merge ``Area`` class' properties with :class:`Forecast`.                                                                                                  |
|         |                   | - 🟥 Rename ``Weather.forecasts`` to ``Forecast.daily_forecasts``.                                                                                             |
|         |                   | - 🟥 Rename ``Weather.location`` to ``Forecast.coordinates``. The former now returns the forecast location's name and the latter is no longer an optional type.|
|         |                   | - 🟥 Rename ``CurrentForecast.chances_of_hightemp`` to ``Forecast.chances_of_high_temperature``.                                                               |
|         |                   | - 🟥 Rename ``CurrentForecast.chances_of_remdry`` to ``Forecast.chances_of_remaining_dry``.                                                                    |
|         |                   | - 🟥 Rename ``CurrentForecast.date`` to ``Forecast.datetime``.                                                                                                 |
|         |                   | - 🟥 Rename ``DailyForecast.hourly`` to ``DailyForecast.hourly_forecasts``.                                                                                    |
|         |                   | - 🟥 Rename ``Ultraviolet`` to :class:`UltraViolet`.                                                                                                           |
|         |                   | - 🟩 ``HourlyForecast.heat_index`` now returns a convenience enum called :class:`HeatIndex`.                                                                   |
|         |                   | - 🟥 Merge ``Astronomy`` class' properties with :class:`DailyForecast`.                                                                                        |
|         |                   | - 🟥 Rename ``Astronomy.sun_rise`` to ``DailyForecast.sunrise``.                                                                                               |
|         |                   | - 🟥 Rename ``Astronomy.sun_set`` to ``DailyForecast.sunset``.                                                                                                 |
|         |                   | - 🟥 Rename ``Astronomy.moon_rise`` to ``DailyForecast.moonrise``.                                                                                             |
|         |                   | - 🟥 Rename ``Astronomy.moon_set`` to ``DailyForecast.moonset``.                                                                                               |
+---------+-------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 2.0.1   | 25 March 2024     | - 🟦 Migrate from ``yapf`` to ``ruff``.                                                                                                                        |
|         |                   | - 🟦 Fix potential :py:class:`NameError` while modifying forecast unit or locale.                                                                              |
|         |                   | - 🟦 Remove several unused imports.                                                                                                                            |
|         |                   | - 🟦 Fix potential :py:class:`NameError` on some typings.                                                                                                      |
+---------+-------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 2.0.2   | 25 April 2024     | - 🟩 Add a donation link over at https://ko-fi.com/null8626.                                                                                                   |
|         |                   | - 🟦 As of 19 April 2024, all GitHub commits sent to the repository (both manual and automated) will be GPG-signed.                                            |
+---------+-------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 2.0.3   | 5 May 2024        | - 🟦 Fix potential :py:class:`NameError` while accessing the ``Phase.emoji`` property.                                                                         |
|         |                   | - 🟦 Refactors on the request delay calculation.                                                                                                               |
|         |                   | - 🟦 Fix broken donations redirect in the documentation page.                                                                                                  |
+---------+-------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 2.0.4   | 30 September 2024 | - 🟦 The ``Client.close`` method now no longer closes the ``ClientSession`` if an existing ``ClientSession`` was provided in the constructor.                  |
|         |                   | - 🟩 HTTP exceptions are now wrapped under :class:`RequestError`.                                                                                              |
|         |                   | - 🟩 Add ``__iter__`` and ``__list__`` helper implementations for the forecast classes.                                                                        |
|         |                   | - 🟦 Bump the ``aiohttp`` dependency to be at least version ``3.10.8``.                                                                                        |
|         |                   | - 🟩 Add an additional ``raise_for_status`` argument to the default ``ClientSession``.                                                                         |
|         |                   | - 🟦 Refactor the regex retrieval for the ``Forecast.local_population`` property.                                                                              |
+---------+-------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+