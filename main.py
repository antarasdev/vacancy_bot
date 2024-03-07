import logging
import asyncio
from aiogram import Bot, Dispatcher
from vacancy_bot.config import BOT_TOKEN

logging.basicConfig(level=logging.DEBUG)

bot = Bot(token=BOT_TOKEN)


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    from vacancy_bot.handlers import dp
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()
