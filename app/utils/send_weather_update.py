import asyncio
import logging

from app.api import fetch_weather_data
from app.utils import get_weather
from app.storage import get_city, get_all_users
from app.config import bot_settings as settings


async def send_weather_update(user_id: int) -> None | bool:
    from app.main import bot

    city = await get_city(user_id)
    if not city:
        return False

    data = await fetch_weather_data(settings.WEATHER_API_TOKEN, city=city)
    text = get_weather(data, city)

    await bot.send_message(chat_id=user_id, text=text)


async def scheduled_weather_updates() -> None:
    while True:
        try:
            users = await get_all_users()
            await asyncio.sleep(3600)
            logging.info("Прохожусь по всем пользователям из базы данных.")
            for user_id in users:
                await send_weather_update(user_id=user_id)
                logging.info("Сообщение было отправлено пользователю.")

        except Exception as error:
            logging.error(f"Ошибка при отправке прогноза: {error}")
            await asyncio.sleep(60)
