from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
)


main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="/location"), KeyboardButton(text="/forecast")],
    ],
    resize_keyboard=True,
    input_field_placeholder="Тапай, тапай нахуй.",
)

# inline_keyboard = InlineKeyboardMarkup(
#     inline_keyboard=[
#         [InlineKeyboardButton(text="Отдай мне свои деньги", url="https://www.youtube.com/")],
#         [InlineKeyboardButton(text="Отдай ещё своих деняккк", url="https://www.youtube.com/")],
#     ]
# )

# from aiogram.utils.keyboard import InlineKeyboardBuilder
# cars = ["1", "2", "3"]
# async def inline_cars():
#     keyboard = InlineKeyboardBuilder()
#     for car in cars:
#         keyboard.add(InlineKeyboardButton(text=car, callback_data=f"car_{car}"))
#     return keyboard.adjust(2).as_markup()
