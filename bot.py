import logging
import asyncio
from aiogram import Bot, Dispatcher

from vacancy_bot.my_bot import handlers
from vacancy_bot.my_bot.config import BOT_TOKEN

logging.basicConfig(level=logging.DEBUG)
bot = Bot(token=BOT_TOKEN)


async def main():
    dp = Dispatcher()
    dp.include_routers(handlers.router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()
