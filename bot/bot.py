import asyncio
import logging

from aiogram import Bot, Dispatcher

from my_bot.config import config
from my_bot.handlers import main_handlers
from my_bot.schedulers import schedule_jobs

logging.basicConfig(level=logging.DEBUG)
bot = Bot(token=config.bot_token.get_secret_value())


async def main():
    dp = Dispatcher()
    dp.include_routers(main_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.create_task(schedule_jobs())
    loop.run_forever()
