import aiohttp
import json

from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from app.config import settings
from app.api import fetch_weather_data

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message):
    await message.reply(
        f"Здравствуй. Я буду отправлять информацию о погоде в указанном тобой городе в то время, которое ты хочешь."
    )


@router.message(Command("get_weather"))
async def get_weather_handler(message: Message):
    city = "Нижнекамск"
    token = settings.WEATHER_API_TOKEN

    try:
        weather = await fetch_weather_data(token, city)
        dict_str = json.dumps(weather, ensure_ascii=False, indent=4)
        await message.answer(dict_str)
    except aiohttp.ClientError as error:
        print(error)
        await message.reply(f"Ошибка при получении данных: {error}")
