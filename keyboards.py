from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

# Основное меню
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Привет")],
        [KeyboardButton(text="Пока")]
    ],
    resize_keyboard=True
)

# Инлайн-клавиатура с URL-ссылками
url_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Новости", url='https://www.rbc.ru/')],
    [InlineKeyboardButton(text="Музыка", url='https://music.yandex.ru/')],
    [InlineKeyboardButton(text="Видео", url='https://hd.kinopoisk.ru/')]
])

# Динамическая клавиатура
dynamic_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Показать больше", callback_data='show_more')]
])

# Функция для создания опций
def create_options():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Опция 1", callback_data='option_1')],
        [InlineKeyboardButton(text="Опция 2", callback_data='option_2')]
    ])