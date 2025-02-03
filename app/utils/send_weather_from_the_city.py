import logging

from aiogram.types import Message

from app.keyboard import main_kb
from app.utils import get_weather

logger = logging.getLogger(__name__)


async def send_weather_from_the_city(message: Message, city: str, data: dict) -> None:
    text = get_weather(data=data, city=city)
    await message.answer(text=f"Отлично. Город <b>«{city}»</b> сохранён!", reply_markup=main_kb)
    await message.answer(text=text, reply_markup=main_kb)
    logger.info("Город пользователя сохранен. Город - %s.", message.text)
