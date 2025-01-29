import os

from dotenv import load_dotenv
from dataclasses import dataclass

load_dotenv()


@dataclass
class Settings:
    TOKEN: str = os.getenv("TOKEN")


settings = Settings()
