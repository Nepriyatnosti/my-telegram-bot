import os
from dotenv import load_dotenv

# Загрузка .env из корневой директории
load_dotenv()

class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")

    @classmethod
    def check_tokens(cls):
        if not all([cls.BOT_TOKEN, cls.RAPIDAPI_KEY]):
            raise ValueError("Отсутствуют обязательные переменные окружения!")