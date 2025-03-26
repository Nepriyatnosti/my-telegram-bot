from aiogram import Bot, Dispatcher
from bot.loader import dp, bot
from bot.handlers import common, analysis, history
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="bot.log"
)

logger = logging.getLogger(__name__)

async def main():
    dp = Dispatcher()
    # Регистрируем все обработчики
    dp.include_router(common.router)
    dp.include_router(analysis.router)
    dp.include_router(history.router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())