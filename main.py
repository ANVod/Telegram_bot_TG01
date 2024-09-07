import asyncio
import random
import requests
from gtts import gTTS
import os
from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message, FSInputFile, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart, Command
from googletrans import Translator
from config import TOKEN, WEATHER_API_KEY

# Создаем папку для хранения фотографий, если она не существует
if not os.path.exists('img'):
    os.makedirs('img')

bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()

translator = Translator()  # Инициализация транслятора

# Создаем клавиатуру с кнопками для команд
keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="/start"), KeyboardButton(text="/help")],
        [KeyboardButton(text="/photos"), KeyboardButton(text="/video")],
        [KeyboardButton(text="/audio"), KeyboardButton(text="/training")],
    ],
    resize_keyboard=True
)

@router.message(CommandStart())
async def start_command(message: Message):
    await message.answer("Бот запущен. Введите команду /help для получения списка доступных команд.", reply_markup=keyboard)

@router.message(Command('help'))
async def help_command(message: Message):
    await message.answer(
        "Этот бот умеет выполнять команды:\n"
        "/start - Запуск бота\n"
        "/help - Помощь при использовании бота\n"
        "/photos - Загрузка фото\n"
        "/video - Получение видео\n"
        "/audio - Получение аудио\n"
        "/training - Ежедневная мини тренировка",
        reply_markup=keyboard
    )
def get_weather(city: str):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=ru"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        city = data['name']
        temp = data['main']['temp']
        description = data['weather'][0]['description']
        return f"Погода в городе {city}:\nТемпература: {temp}°C\nОписание: {description}"
    else:
        return "Не удалось получить данные о погоде. Проверьте название города."

@router.message(F.photo)
async def react_photo(message: Message):
    responses = ['Ого, какая фотка!', 'Непонятно, что это такое', 'Не отправляй мне такое больше']
    rand_answ = random.choice(responses)
    await message.answer(rand_answ)

    # Скачиваем фото и сохраняем в папке 'img'
    photo_file = message.photo[-1]
    file_info = await bot.get_file(photo_file.file_id)
    destination_path = f'img/{photo_file.file_id}.jpg'
    await bot.download(file_info, destination=destination_path)
    await message.answer(f"Фото сохранено как {destination_path}")

@router.message(Command('video'))
async def video_command(message: Message):
    video_file = FSInputFile('video.mp4')
    await bot.send_chat_action(message.chat.id, 'upload_video')
    await bot.send_video(message.chat.id, video_file)

@router.message(Command('audio'))
async def audio_command(message: Message):
    audio = FSInputFile('audio.mp3')  # Замените на ваш фактический аудиофайл
    await bot.send_chat_action(message.chat.id, 'upload_audio')
    await bot.send_audio(message.chat.id, audio)

@router.message(Command('voice'))
async def voice_command(message: Message):
    voice = FSInputFile("sample.ogg")
    await message.answer_voice(voice)

@router.message(Command('training'))
async def training_command(message: Message):
    training_list = [
        "Тренировка 1:\n1. Скручивания: 3 подхода по 15 повторений\n2. Велосипед: 3 подхода по 20 повторений (каждая сторона)\n3. Планка: 3 подхода по 30 секунд",
        "Тренировка 2:\n1. Подъемы ног: 3 подхода по 15 повторений\n2. Русский твист: 3 подхода по 20 повторений (каждая сторона)\n3. Планка с поднятой ногой: 3 подхода по 20 секунд (каждая нога)",
        "Тренировка 3:\n1. Скручивания с поднятыми ногами: 3 подхода по 15 повторений\n2. Горизонтальные ножницы: 3 подхода по 20 повторений\n3. Боковая планка: 3 подхода по 20 секунд (каждая сторона)"
    ]
    rand_tr = random.choice(training_list)
    await message.answer(f"Это ваша мини-тренировка на сегодня: {rand_tr}")

    # Генерируем аудио с помощью gTTS
    tts = gTTS(text=rand_tr, lang='ru')
    tts.save("training.ogg")
    audio = FSInputFile('training.ogg')
    await bot.send_voice(chat_id=message.chat.id, voice=audio)
    os.remove("training.ogg")

@router.message(Command('doc'))
async def doc_command(message: Message):
    doc = FSInputFile("chpora.pdf")
    await bot.send_document(message.chat.id, doc)

@router.message(F.text)
async def translate_text(message: Message):
    original_text = message.text
    translated = translator.translate(original_text, dest='en')
    await message.answer(f"Перевод на английский: {translated.text}")

async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
