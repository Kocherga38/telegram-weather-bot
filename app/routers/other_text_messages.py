import logging

from aiogram import Router, F
from aiogram.types import Message

from app.keyboard import main_kb

logger = logging.getLogger(__name__)
router = Router()


@router.message(F.text, ~F.state)
async def other_text_messages_handler(message: Message) -> None:
    await message.answer(
        text="Вы ввели не команду.\n\nС полным списком команд вы можете ознакомиться написав /help.",
        reply_markup=main_kb,
    )
    logger.info("other_text_messages_handler handler отработал.")
