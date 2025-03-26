from aiogram import Bot
from aiogram.dispatcher.dispatcher import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import Config

# Инициализация бота
bot = Bot(token=Config.BOT_TOKEN, parse_mode="HTML")

# Хранилище состояний
storage = MemoryStorage()

# Диспетчер
dp = Dispatcher(storage=storage)