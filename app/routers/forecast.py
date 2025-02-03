import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.utils import send_weather_update
from app.keyboard import main_kb

logger = logging.getLogger(__name__)
router = Router()


@router.message(Command("forecast"))
async def get_forecast(message: Message) -> None:
    result = await send_weather_update(user_id=message.from_user.id)
    if not result:
        text = "Вы ещё не вводили название города. Для того, чтобы ввести его, напишите /location."
        await message.answer(text=text, reply_markup=main_kb)
    logger.info("Forecast handler отработал.")
