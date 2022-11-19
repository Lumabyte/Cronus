import aiohttp
import asyncio
from cronus.plugin import Plugin, plugin, handler


WEATHER_URL = "https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&hourly=temperature_2m,relativehumidity_2m,windspeed_10m"


@plugin(name="weather", description="Fetching weather information")
class Weather(Plugin):

    @handler("discord", "message")
    async def get_weather(self, _: any, message: str):
        async with aiohttp.ClientSession() as session:
            async with session.get(WEATHER_URL) as response:
                weather = await response.json()
                print(weather)


if __name__ == "__main__":
    weather = Weather(None)
    func = weather.get_weather("source", "!weather cape_town")
    asyncio.run(func)

