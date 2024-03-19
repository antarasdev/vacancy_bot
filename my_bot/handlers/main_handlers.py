import asyncio

from aiogram import types, Router, F
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import ReplyKeyboardRemove

from vacancy_bot.my_bot.constants import THREAD_KEYWORDS, RULES_TEXT, EXAMPLE
from vacancy_bot.my_bot.config import config
from vacancy_bot.my_bot.keyboards import main_keyboard
from vacancy_bot.bot import bot


router = Router()

last_vacancy_sent = 0


class VacancyForm(StatesGroup):
    ConfirmVacancy = State()


@router.message(Command("start"))
async def start(message: types.Message):
    text = "Добро пожаловать! Я могу помочь вам опубликовать вакансии"
    await message.answer(text, reply_markup=main_keyboard())


@router.message(lambda message: message.text == '📑 Шаблон\nвакансии')
async def send_vacancy_example(message: types.Message):
    text = EXAMPLE
    await message.answer(text)


@router.message(lambda message: message.text == '📔 Правила\nпубликации')
async def send_rules(message: types.Message):
    text = RULES_TEXT
    await message.answer(text)


@router.message(lambda message: message.text == '✅Опубликовать вакансию')
async def publish_vacancy(message: types.Message, state: FSMContext):
    text = 'Напиши текст вашей вакансии по шаблону'
    await message.answer(text)
    await state.set_state(VacancyForm.ConfirmVacancy)


@router.message(VacancyForm.ConfirmVacancy)
async def process_vacancy(message: types.Message, state: FSMContext):
    global last_vacancy_sent
    current_time = asyncio.get_event_loop().time()
    data = message.text
    vacancy_parts = data.split('\n\n')

    hashtags = ([part for part in vacancy_parts if part.startswith("#")])
    name_organisation = [part for part in vacancy_parts if 'Название фирмы' in part]
    responsibilities = [part for part in vacancy_parts if "Требования к кандидату" in part]
    position = next((part for part in vacancy_parts if "Должность" in part), None)
    salary = next((part for part in vacancy_parts if any(word in part.lower() for word in ["зп", "оклад"])), None)
    contacts = [part for part in vacancy_parts if 'Контактные данные' in part]

    message_thread_id = None
    for thread_id, keywords in THREAD_KEYWORDS.items():
        for keyword in keywords:
            if keyword.lower() in data.lower() or any(
                    keyword.lower() in part.lower() for part in vacancy_parts):
                message_thread_id = thread_id
                break
        if message_thread_id:
            break

    if message_thread_id and responsibilities and salary and position and hashtags and name_organisation and contacts:
        if current_time - last_vacancy_sent < 1800:  # 1800 seconds = 30 minutes
            await message.answer("Вы не можете отправлять вакансии чаще, чем раз в 30 минут.")
        else:
            formatted_vacancy = (
                "\n\n".join(hashtags + name_organisation +
                            [position] + list(map(str, responsibilities)) +
                            [salary] + contacts)
                )
            await bot.send_message(chat_id=config.chat_id.get_secret_value(),
                                   message_thread_id=message_thread_id, text=formatted_vacancy)
            last_vacancy_sent = current_time
            await state.clear()
            await message.answer("Вакансия успешно опубликована.", reply_markup=main_keyboard())
    else:
        await message.answer(
            "Вакансия не опубликована! Пожалуйста, отправьте вакансию в правильном формате.",
            reply_markup=main_keyboard()
        )


@router.message()
async def message_handler(message: types.Message):
    text = "Чтобы опубликовать вакансию, нажмите кнопку '✅Опубликовать вакансию'"
    await message.answer(text, reply_markup=main_keyboard())
