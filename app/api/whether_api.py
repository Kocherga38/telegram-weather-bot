import asyncio

import aiohttp

from app.config.bot import bot_settings as settings

from pprint import pprint

async def fetch_weather_data(token: str, city: str) -> dict:
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": token, "units": "metric"}

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url=url, params=params, timeout=5) as response:
                response.raise_for_status()
                return await response.json()
        except aiohttp.ClientResponseError as error:
            return {"code": error.status, "message": error.message}
        except aiohttp.ClientError as error:
            return {"cod": "500", "message": f"Ошибка при соединении: {str(error)}"}

async def main():
    city = input("Enter city: ").strip() or "Нижнекамск"
    token = settings.WEATHER_API_TOKEN
    weather = await fetch_weather_data(token=token, city=city)
    if weather:
        pprint(weather)


if __name__ == "__main__":
    asyncio.run(main())
