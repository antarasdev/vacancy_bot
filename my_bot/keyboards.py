from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder, ReplyKeyboardMarkup


def main_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()

    keyboard.add(types.KeyboardButton(text='📑 Шаблон\nвакансии'))
    keyboard.add(types.KeyboardButton(text='📔 Правила\nпубликации'))
    keyboard.add(types.KeyboardButton(text='✅Опубликовать вакансию'))

    keyboard.adjust(2)
    return keyboard.as_markup(resize_keyboard=True)


def payment_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()

    keyboard.add(types.KeyboardButton(text="Открыть оплату", pay=True))

    keyboard.adjust(2)
    return keyboard.as_markup(resize_keyboard=True)
