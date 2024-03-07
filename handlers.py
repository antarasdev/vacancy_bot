from aiogram import types, Dispatcher
from aiogram.filters.command import Command

from vacancy_bot.constants import ADMIN_ID
from vacancy_bot.main import bot

dp = Dispatcher()


@dp.message(Command("start"))
async def start(message: types.Message):
    text = "Добро пожаловать! Я могу помочь вам опубликовать вакансии"
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[[types.KeyboardButton(text="Пример заполнения вакансии")]],
        resize_keyboard=True
    )
    await message.answer(text, reply_markup=keyboard)


@dp.message((lambda message: message.text == 'Пример заполнения вакансии'))
async def send_vacancy_example(message: types.Message):
    vacancy_text = "#PythonDeveloper\n\nОбязанности:\n- Разработка и поддержка веб-приложений\n\nЗП: от 100 000 рублей"
    await message.answer(vacancy_text)


@dp.message()
async def process_vacancy(message: types.Message):
    vacancy_text = message.text
    vacancy_parts = vacancy_text.split('\n')

    hashtags = []
    responsibilities = []
    salary = None

    for part in vacancy_parts:
        if part.startswith("#"):
            hashtags.append(part)
        elif "Обязанности" in part:
            responsibilities.append(part)
        elif "ЗП" in part or "оклад" in part:
            salary = part

    if hashtags and responsibilities and salary:
        formatted_vacancy = "\n".join(hashtags + responsibilities + [salary])
        await bot.send_message(chat_id=ADMIN_ID, text=f"Новая вакансия:\n{formatted_vacancy}")
        await message.answer("Вакансия успешно отправлена администратору.")
    else:
        await message.answer("Вакансия должна содержать хэштеги, обязанности и информацию о зарплате! "
                             "Пожалуйста, отправьте вакансию в правильном формате.")
