.. python-weather documentation master file, created by
   sphinx-quickstart on Sat Feb 24 18:54:24 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

===============
python-weather_
===============

|pypi|_ |downloads|_ |codacy|_ |codecov|_ |ko-fi-brief|_

.. _python-weather: https://pypi.org/project/python-weather/
.. |pypi| image:: https://img.shields.io/pypi/v/python-weather.svg?style=flat-square
.. _pypi: https://pypi.org/project/python-weather/
.. |downloads| image:: https://img.shields.io/pypi/dm/python-weather?style=flat-square
.. _downloads: https://pypi.org/project/python-weather/
.. |codacy| image:: https://app.codacy.com/project/badge/Grade/0f7721b7e4314a748c75a04f0a7e0ce3
.. _codacy: https://app.codacy.com/gh/null8626/python-weather/dashboard
.. |codecov| image:: https://codecov.io/gh/null8626/python-weather/graph/badge.svg
.. _codecov: https://codecov.io/gh/null8626/python-weather
.. |ko-fi-brief| image:: https://img.shields.io/badge/donations-ko--fi-red?color=ff5e5b&style=flat-square
.. _ko-fi-brief: https://ko-fi.com/null8626
.. |ko-fi| image:: https://ko-fi.com/img/githubbutton_sm.svg
.. _ko-fi: https://ko-fi.com/null8626

A free and asynchronous weather Python API wrapper made in Python, for Python.

Getting started
---------------

Run the following command in your terminal:

.. code-block:: console

   pip install python-weather

Example
-------

.. code-block:: python

  # Import the module.
  import python_weather
  
  import asyncio
  
  
  async def main() -> None:

    # Declare the client. The measuring unit used defaults to the metric system (celcius, km/h, etc.)
    async with python_weather.Client(unit=python_weather.IMPERIAL) as client:
      
      # Fetch a weather forecast from a city.
      weather = await client.get('New York')
      
      # Fetch the temperature for today.
      print(weather.temperature)
      
      # Fetch weather forecast for upcoming days.
      for daily in weather:
        print(daily)
      
        # Each daily forecast has their own hourly forecasts.
        for hourly in daily:
          print(f' --> {hourly!r}')
  
  if __name__ == '__main__':
    asyncio.run(main())

Data source
___________

This library depends on `wttr.in`_, which uses data from the `World Weather Online API`_.

.. _wttr.in: https://wttr.in
.. _World Weather Online API: https://www.worldweatheronline.com/weather-api

Donations
---------

If you want to support this project, consider donating! ❤

|ko-fi|_

.. toctree::
   :maxdepth: 2
   :hidden:

   client
   forecast/index.rst
   changelog
   repository
   github-donate
   ko-fi-donate