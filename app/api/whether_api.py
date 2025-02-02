import asyncio
import aiohttp

from app.config.bot import bot_settings as settings

from pprint import pprint


async def fetch_weather_data(token: str, city: str) -> dict:
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": token, "units": "metric"}

    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, params=params, timeout=5) as response:
            response.raise_for_status()
            return await response.json()


async def get_weather(token: str, city: str) -> dict:
    try:
        return await fetch_weather_data(token, city)

    except aiohttp.ClientError as error:
        print("Error: ", error)


async def main():
    city = input("Введите город: ").strip() or "Нижнекамск"
    token = settings.WEATHER_API_TOKEN
    weather = await get_weather(token=token, city=city)
    if weather:
        pprint(weather)


if __name__ == "__main__":
    asyncio.run(main())
