from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder, ReplyKeyboardMarkup


def main_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()

    keyboard.add(types.KeyboardButton(text='📑 Пример\nвакансии'))
    keyboard.add(types.KeyboardButton(text='📔 Правила\nпубликации'))
    keyboard.add(types.KeyboardButton(text='✅Опубликовать вакансию'))

    keyboard.adjust(2)
    return keyboard.as_markup(resize_keyboard=True)


def vacancy_time_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()

    keyboard.add(types.KeyboardButton(text='1 Неделя'))
    keyboard.add(types.KeyboardButton(text='2 Недели'))
    keyboard.add(types.KeyboardButton(text='3 Недели'))
    keyboard.add(types.KeyboardButton(text='Месяц'))
    keyboard.add(types.KeyboardButton(text='Назад'))

    keyboard.adjust(2)
    return keyboard.as_markup(resize_keyboard=True)


def back_button() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()

    keyboard.add(types.KeyboardButton(text='Назад'))
    keyboard.adjust(1)
    return keyboard.as_markup(resize_keyboard=True)
