import os

from dotenv import load_dotenv
from dataclasses import dataclass

load_dotenv()


@dataclass
class Settings:
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN")
    WEATHER_API_TOKEN: str = os.getenv("WEATHER_API_TOKEN")


settings = Settings()
