# import the module
import python_weather
import asyncio


async def getweather():
    # declare the client. format defaults to metric system (celcius, km/h, etc.)
    client = python_weather.Client(format=python_weather.IMPERIAL)

    # fetch a weather forecast from a city
    weather = await client.find("Washington DC")

    # returns the current city temperature (int)
    print(weather.current.temperature)

    # await client.close()

    # get the weather forecast for a few days
    for forecast in weather.forecast:
        print(str(forecast.date), forecast.sky_text, forecast.temperature)

    # close the wrapper once done
    await client.close()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(getweather())

