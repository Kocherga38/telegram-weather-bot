import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from app.api import fetch_weather_data
from app.config import bot_settings as settings
from app.routers import router as location_router
from app.utils import weather_emojis

bot = Bot(
    token=settings.TELEGRAM_BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)
dp = Dispatcher()


async def send_weather_update(user_id: int) -> None:
    from app.storage import get_city

    city = await get_city(user_id)
    if not city:
        return

    data = await fetch_weather_data(settings.WEATHER_API_TOKEN, city=city)
    weather = data["weather"][0]
    emoji = weather_emojis.get(weather["main"].lower(), "❓")

    text = (
        f"Прогноз погоды в <b>{city}</b>:\n\n"
        f"<blockquote>"
        f"🌡 Температура: <b>{data['main']['temp']}℃</b>\n"
        f"🤔 Ощущается как: <b>{data['main']['feels_like']}℃</b>\n"
        f"{emoji} <b>{weather['description'].capitalize()}</b>\n"
        f"💨 Ветер: <b>{data['wind']['speed']} м/с</b>"
        f"</blockquote>"
    )

    await bot.send_message(chat_id=user_id, text=text)


async def scheduled_weather_updates():
    from storage import get_all_users

    while True:
        try:
            users = await get_all_users()
            logging.info("Прохожусь по всем пользователям из базы данных.")
            for user_id in users:
                await send_weather_update(user_id)
                logging.info("Сообщение было отправлено пользователю.")
            await asyncio.sleep(5)
        except Exception as error:
            logging.error(f"Ошибка при отправке прогноза: {error}")
            await asyncio.sleep(60)


async def main() -> None:
    dp.include_router(
        location_router,
    )

    asyncio.create_task(scheduled_weather_updates())

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
