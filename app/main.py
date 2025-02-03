import logging
import asyncio
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from app.api import fetch_weather_data
from app.config import bot_settings as settings
from app.routers import location_router, help_router, other_text_messages_router, forecast_router
from app.utils import get_weather
from app.storage import get_city, get_all_users

bot = Bot(
    token=settings.TELEGRAM_BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)
dp = Dispatcher()


async def send_weather_update(user_id: int) -> None:
    city = await get_city(user_id)
    if not city:
        return

    data = await fetch_weather_data(settings.WEATHER_API_TOKEN, city=city)
    text = get_weather(data, city)

    await bot.send_message(
        chat_id=user_id,
        text=text,
    )


async def scheduled_weather_updates():
    while True:
        try:
            users = await get_all_users()
            await asyncio.sleep(3600)
            logging.info("Прохожусь по всем пользователям из базы данных.")
            for user_id in users:
                await send_weather_update(user_id)
                logging.info("Сообщение было отправлено пользователю.")

        except Exception as error:
            logging.error(f"Ошибка при отправке прогноза: {error}")
            await asyncio.sleep(60)


async def main() -> None:
    dp.include_routers(
        help_router,
        location_router,
        forecast_router,
        other_text_messages_router,
    )

    asyncio.create_task(scheduled_weather_updates())

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d - %(funcName)s()] - %(message)s",
        stream=sys.stdout,
    )
    logging.info("The bot has started working.")

    asyncio.run(main())
