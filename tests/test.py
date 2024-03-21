import unittest
from unittest.mock import AsyncMock

from aiogram import types
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from my_bot.handlers.main_handlers import router, VacancyForm


class TestHandlers(unittest.IsolatedAsyncioTestCase):

    async def test_start_handler(self):
        message = types.Message(text='/start')
        message.answer = AsyncMock()
        await router.process_message(message)
        message.answer.assert_awaited()

    async def test_send_vacancy_example_handler(self):
        message = types.Message(text='📑 Шаблон\nвакансии')
        message.answer = AsyncMock()
        await router.process_message(message)
        message.answer.assert_awaited()

    async def test_publish_vacancy_handler(self):
        message = types.Message(text='✅Опубликовать вакансию')
        message.answer = AsyncMock()
        message.set_state = AsyncMock()
        await router.process_message(message)
        message.answer.assert_awaited()
        message.set_state.assert_awaited_with(VacancyForm.ConfirmVacancy)

    async def test_process_vacancy_handler(self):
        message = types.Message(text='Your vacancy text here')
        message.answer = AsyncMock()
        message.text = 'Your vacancy text here'
        message.chat.id = 123456
        state = FSMContext(VacancyForm.ConfirmVacancy)
        state.set_state = AsyncMock()
        state.clear = AsyncMock()
        await router.process_message(message, state)
        message.answer.assert_awaited()
        state.set_state.assert_awaited()
        state.clear.assert_awaited()