import logging

import redis.exceptions
from aiogram import F, Router
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message,
    ReplyKeyboardRemove,
)
from app.config.bot import bot_settings as settings

from app.storage import save_city_in_redis
from app.api import fetch_weather_data

logger = logging.getLogger(__name__)


class WeatherStates(StatesGroup):
    city = State()


router = Router()


@router.message(Command(commands=["start", "location"]))
async def start_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(WeatherStates.city)
    await message.answer(
        text="Здравствуй.\n\nНапиши название города, из которого ты хочешь получать информацию о погоде.",
        reply_markup=ReplyKeyboardRemove(),
    )


@router.message(Command("forecast"))
async def get_forecast(message: Message) -> None:
    from app.main import send_weather_update

    await send_weather_update(message.from_user.id)


@router.message(WeatherStates.city)
async def save_city_name(message: Message, state: FSMContext) -> None:
    data = await fetch_weather_data(settings.WEATHER_API_TOKEN, city=message.text)
    if data.get("code") == 404:
        await message.answer("Ты ввел нихуя не город, попробуй еще.")
        return await state.set_state(WeatherStates.city)

    try:
        await save_city_in_redis(message.from_user.id, message.text)
    except redis.exceptions.ConnectionError:
        logger.error("Connection error.")

    await state.clear()
    await message.answer(
        text=f"Отлично. Город «{message.text}» сохранен!",
        reply_markup=ReplyKeyboardRemove(),
    )


@router.message(F.text, ~F.state)
async def other_text_messages_handler(message: Message) -> None:
    await message.answer(
        text="Вы ввели не команду.\n\nС полным списком команд вы можете ознакомиться написав /help.",
        reply_markup=ReplyKeyboardRemove(),
    )
