import logging
import redis.exceptions

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message,
)

from app.config.bot import bot_settings as settings
from app.routers.states import WeatherStates
from app.storage import save_city_in_redis
from app.api import fetch_weather_data
from app.keyboard import main_kb
from app.utils import send_weather_from_the_city

logger = logging.getLogger(__name__)
router = Router()


@router.message(Command(commands=["start", "location"]))
async def start_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(WeatherStates.city)
    text = "Здравствуй.\n\nНапиши название города, из которого ты хочешь получать информацию о погоде."
    await message.answer(text=text, reply_markup=main_kb)
    logger.info("Start handler отработал.")


@router.message(WeatherStates.city)
async def save_city_name(message: Message, state: FSMContext) -> None:
    city = message.text.capitalize()
    data = await fetch_weather_data(settings.WEATHER_API_TOKEN, city=city)

    if data.get("code") == 404:
        await message.answer("Ты ввел нихуя не город, попробуй еще.")
        logger.info("Пользователь ввёл какую-то хуйню, а не название города.")
        return await state.set_state(WeatherStates.city)
    try:
        await save_city_in_redis(message.from_user.id, message.text)
    except redis.exceptions.ConnectionError:
        logger.error("Connection error.")

    await state.clear()
    await send_weather_from_the_city(message=message, city=city, data=data)
