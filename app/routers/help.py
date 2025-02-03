from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.keyboard import main_kb

router = Router()


@router.message(Command("help"))
async def help_command(message: Message):
    text = (
        "Полный список команд:\n\n"
        "/location - Чтобы изменить город, из которого вы желаете получать прогноз погоды.\n"
        "/forecast - Получить прогноз погоды.\n"
    )

    await message.answer(
        text=text,
        reply_markup=main_kb,
    )
