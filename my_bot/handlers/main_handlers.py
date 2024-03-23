import asyncio

import aioschedule
from aiogram import F, Router, types
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from bot import bot
from my_bot.config import config
from my_bot.constants import EXAMPLE, RULES_TEXT, THREAD_KEYWORDS, START_MESSAGE
from my_bot.keyboards import main_keyboard, vacancy_time_keyboard, back_button

router = Router()

last_vacancy_sent = 0


class VacancyForm(StatesGroup):
    ConfirmVacancy = State()
    change_timestamp = State()


@router.message(Command("start"))
async def start(message: types.Message):
    text = START_MESSAGE
    await message.answer(text, reply_markup=main_keyboard(), parse_mode=ParseMode.MARKDOWN_V2)


@router.message(lambda message: message.text == '📑 Пример\nвакансии')
async def send_vacancy_example(message: types.Message):
    text = EXAMPLE
    await message.answer(text, parse_mode=ParseMode.MARKDOWN_V2)


@router.message(lambda message: message.text == '📔 Правила\nпубликации')
async def send_rules(message: types.Message):
    text = RULES_TEXT
    await message.answer(text,  parse_mode=ParseMode.MARKDOWN_V2)


@router.message(lambda message: message.text == '✅Опубликовать вакансию')
async def publish_vacancy(message: types.Message, state: FSMContext):
    text = 'Выберете срок, на который вы хотите опубликовать вакансию'
    await message.answer(text, reply_markup=vacancy_time_keyboard())
    await state.set_state(VacancyForm.change_timestamp)


@router.message(VacancyForm.change_timestamp)
async def process_vacancy(message: types.Message, state: FSMContext):
    if message.text == 'Назад':
        await state.set_state(None)  # Очищаем состояние, возвращаемся в основное меню
        await start(message)
    else:
        selected_time = message.text
        await state.update_data(selected_time=selected_time)
        await state.set_state(VacancyForm.ConfirmVacancy)
        text = f'Срок публикации: <i><b>{selected_time}</b></i>. Введите текст вашей вакансии'
        await message.answer(text, reply_markup=back_button(), parse_mode=ParseMode.HTML)


@router.message(VacancyForm.ConfirmVacancy)
async def enter_vacancy_text(message: types.Message, state: FSMContext):
    if message.text == 'Назад':
        await state.set_state(VacancyForm.change_timestamp)
        await publish_vacancy(message, state)
    else:
        global last_vacancy_sent
        current_time = asyncio.get_event_loop().time()
        data = message.text
        vacancy_parts = data.split('\n\n')
        selected_time = (await state.get_data()).get("selected_time")

        hashtags = [part for part in vacancy_parts if part.startswith("#")]
        name_organisation = [part for part in vacancy_parts if 'Название организации' in part]
        responsibilities = [part for part in vacancy_parts if "Требования к кандидату" in part]
        conditions = [part for part in vacancy_parts if "Условия работы" in part]
        position = [part for part in vacancy_parts if "Должность" in part]
        salary = next((part for part in vacancy_parts if any(word in part.lower() for word in ["зп", "оклад"])), None)
        contacts = [part for part in vacancy_parts if "Контактные данные" in part]

        message_thread_id = None
        for thread_id, keywords in THREAD_KEYWORDS.items():
            for keyword in keywords:
                if keyword.lower() in data.lower() or any(
                        keyword.lower() in part.lower() for part in vacancy_parts):
                    message_thread_id = thread_id
                    break
            if message_thread_id:
                break

        if (message_thread_id and responsibilities and
                salary and position and hashtags and
                name_organisation and contacts):
            if current_time - last_vacancy_sent < 1800:  # 1800 seconds = 30 minutes
                await message.answer("Вы не можете отправлять вакансии чаще, чем раз в 30 минут.")
            else:
                formatted_vacancy = (
                    "\n\n".join(hashtags + name_organisation +
                                position + list(map(str, responsibilities)) +
                                conditions + [salary] + contacts)
                )
                vacancy = await bot.send_message(
                    chat_id=config.chat_id.get_secret_value(),
                    message_thread_id=message_thread_id,
                    text=formatted_vacancy
                )
                last_vacancy_sent = current_time
                if selected_time == 'Месяц':
                    aioschedule.every(4).weeks.do(delete_message, vacancy)
                elif selected_time == '3 Недели':
                    aioschedule.every(3).weeks.do(delete_message, vacancy)
                elif selected_time == '2 Недели':
                    aioschedule.every(2).weeks.do(delete_message, vacancy)
                else:
                    aioschedule.every(1).weeks.do(delete_message, vacancy)
                await state.clear()
                vacancy_link = f"{config.link.get_secret_value()}{message_thread_id}/{vacancy.message_id}"
                await message.answer(f"Ваша вакансия успешно опубликована🎉\n\n"
                                     f"[Можете посмотреть её по этой ссылке]({vacancy_link})",
                                     reply_markup=main_keyboard(),
                                     parse_mode=ParseMode.MARKDOWN_V2)
        else:
            await message.answer(
                "Вакансия не опубликована! Пожалуйста, отправьте вакансию в правильном формате.",
                reply_markup=main_keyboard()
            )


async def delete_message(vacancy):
    chat_id = vacancy.chat.id
    message_id = vacancy.message_id
    try:
        await bot.delete_message(chat_id=chat_id, message_id=message_id)
    except TelegramBadRequest as e:
        print(f"Ошибка при удалении сообщения: {e}")


@router.message()
async def message_handler(message: types.Message):
    text = "Чтобы опубликовать вакансию, нажмите кнопку '✅Опубликовать вакансию'"
    await message.answer(text, reply_markup=main_keyboard())
