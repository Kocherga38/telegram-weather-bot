from aiogram.fsm.state import StatesGroup, State


class WeatherStates(StatesGroup):
    city = State()
