from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_start_keyboard():
    keyboard = ReplyKeyboardBuilder()

    keyboard.add(types.KeyboardButton(text='📑 Шаблон\nвакансии'))
    keyboard.add(types.KeyboardButton(text='📔 Правила\nоформления'))
    keyboard.add(types.KeyboardButton(text='Новая кнопка1'))
    keyboard.add(types.KeyboardButton(text='Новая кнопка2'))
    keyboard.adjust(2)
    return keyboard
