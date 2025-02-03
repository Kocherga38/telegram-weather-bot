import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message


logger = logging.getLogger(__name__)
router = Router()


@router.message(Command("forecast"))
async def get_forecast(message: Message) -> None:
    from app.main import send_weather_update

    await send_weather_update(message.from_user.id)
    logger.info("Forecast handler отработал.")
