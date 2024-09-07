import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
import sqlite3
import logging
from config import TOKEN  # Импортируем ваш токен из файла config

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера с FSM-хранилищем
bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


# Инициализация базы данных
def init_db():
    conn = sqlite3.connect('school_data.db')
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        grade TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()


init_db()


# Определяем состояния для FSM
class StudentForm(StatesGroup):
    name = State()
    age = State()
    grade = State()


# Обработчик команды /start
@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await message.answer("Привет! Как тебя зовут?")
    await state.set_state(StudentForm.name)


# Обработчик для получения имени
@dp.message(StudentForm.name)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Сколько тебе лет?")
    await state.set_state(StudentForm.age)


# Обработчик для получения возраста
@dp.message(StudentForm.age)
async def get_age(message: Message, state: FSMContext):
    age = message.text
    if not age.isdigit():
        await message.answer("Пожалуйста, введите корректный возраст числом.")
        return
    await state.update_data(age=int(age))
    await message.answer("В каком классе ты учишься?")
    await state.set_state(StudentForm.grade)


# Обработчик для получения класса (grade)
@dp.message(StudentForm.grade)
async def get_grade(message: Message, state: FSMContext):
    await state.update_data(grade=message.text)
    user_data = await state.get_data()

    # Сохранение данных в базу данных
    conn = sqlite3.connect('school_data.db')
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO students (name, age, grade) VALUES (?, ?, ?)''',
                (user_data['name'], user_data['age'], user_data['grade']))
    conn.commit()
    conn.close()

    await message.answer(
        f"Спасибо, {user_data['name']}! Мы записали, что ты учишься в классе {user_data['grade']} и тебе {user_data['age']} лет.")

    # Очистка состояния
    await state.clear()


# Основная функция для запуска бота
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
