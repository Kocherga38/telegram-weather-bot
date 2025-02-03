import logging
import asyncio
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode


from app.config import bot_settings as settings
from app.routers import location_router, help_router, other_text_messages_router, forecast_router
from app.utils import scheduled_weather_updates

bot = Bot(
    token=settings.TELEGRAM_BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)
dp = Dispatcher()


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
