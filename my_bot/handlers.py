import asyncio
import time

from aiogram import types, Dispatcher, F
from aiogram.filters.command import Command

from .constants import THREAD_ID
from .config import CHAT_ID
from vacancy_bot import bot
from .keyboards import get_start_keyboard

dp = Dispatcher()
last_vacancy_sent = 0


@dp.message(Command("start"))
async def start(message: types.Message):
    text = "Добро пожаловать! Я могу помочь вам опубликовать вакансии"
    keyboard = get_start_keyboard()
    await message.answer(text, reply_markup=keyboard.as_markup(resize_keyboard=True),)


@dp.message(lambda message: message.text == '📑 Шаблон\nвакансии')
async def send_vacancy_example(message: types.Message):
    text = ("#PythonDeveloper\n"
            "\nОбязанности:\n- Разработка и поддержка веб-приложений\n"
            "\nЗП: от 100 000 рублей")
    await message.answer(text)


@dp.message()
async def process_vacancy(message: types.Message):
    global last_vacancy_sent
    current_time = asyncio.get_event_loop().time()
    vacancy_text = message.text
    vacancy_parts = vacancy_text.split('\n')

    hashtags = [part for part in vacancy_parts if part.startswith("#")]
    responsibilities = [part for part in vacancy_parts if "Обязанности" in part]
    salary = next((part for part in vacancy_parts if any(word in part.lower() for word in ["зп", "оклад"])), None)
    message_thread_id = THREAD_ID.get(next((part for part in vacancy_parts if part.startswith("#")), None))

    if message_thread_id and len(hashtags) > 0 and responsibilities and salary:
        if current_time - last_vacancy_sent < 1800:  # 1800 seconds = 30 minutes
            await message.answer("Вы не можете отправлять вакансии чаще, чем раз в 30 минут.")
        else:
            formatted_vacancy = "\n\n".join(hashtags + responsibilities + [salary])
            await bot.send_message(
                chat_id=CHAT_ID,
                message_thread_id=message_thread_id,
                text=formatted_vacancy
            )
            last_vacancy_sent = current_time
            await message.answer("Вакансия успешно опубликована.")
    else:
        await message.answer("Вакансия должна содержать хэштеги, обязанности и информацию о зарплате! "
                             "Пожалуйста, отправьте вакансию в правильном формате.")
