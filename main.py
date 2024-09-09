import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from config import TOKEN
import keyboards as kb

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Обработчик команды /start
@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(f'Приветики, {message.from_user.first_name}', reply_markup=kb.main_menu)

# Обработчик кнопки "Привет"
@dp.message(F.text == "Привет")
async def greet(message: Message):
    await message.answer(f'Привет, {message.from_user.first_name}!')

# Обработчик кнопки "Пока"
@dp.message(F.text == "Пока")
async def farewell(message: Message):
    await message.answer(f'До свидания, {message.from_user.first_name}!')

# Обработчик команды /links
@dp.message(Command('links'))
async def send_links(message: Message):
    await message.answer('Ссылки:', reply_markup=kb.url_keyboard)

# Обработчик команды /dynamic
@dp.message(Command('dynamic'))
async def dynamic(message: Message):
    await message.answer('Динамическая клавиатура:', reply_markup=kb.dynamic_keyboard)

# Обработчик инлайн кнопки "Показать больше"
@dp.callback_query(F.data == 'show_more')
async def show_more(callback: CallbackQuery):
    await callback.message.edit_text('Выберите опцию:', reply_markup=kb.create_options())

# Обработчик для опций
@dp.callback_query(F.data.in_({'option_1', 'option_2'}))
async def handle_option(callback: CallbackQuery):
    option = callback.data
    if option == 'option_1':
        await callback.message.answer('Вы выбрали Опция 1')
    elif option == 'option_2':
        await callback.message.answer('Вы выбрали Опция 2')

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())