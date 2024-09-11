import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ParseMode
import requests
from config import TOKEN, NASA_API_KEY

# Инициализация бота и диспетчера
default_properties = types.DefaultBotProperties(parse_mode=ParseMode.HTML)
bot = Bot(token=TOKEN, default_bot_properties=default_properties)
dp = Dispatcher()

def get_recent_epic_images():
    url = f"https://api.nasa.gov/EPIC/api/natural/images?api_key={NASA_API_KEY}"
    response = requests.get(url)
    return response.json()

def get_image_url(image_data):
    date = image_data['date'].split(" ")[0]
    year, month, day = date.split("-")
    image_name = image_data['image']
    image_url = f"https://api.nasa.gov/EPIC/archive/natural/{year}/{month}/{day}/png/{image_name}.png?api_key={NASA_API_KEY}"
    return image_url

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Привет! Я бот, который предоставляет изображения Земли с помощью EPIC API. Отправьте команду /earth, чтобы получить последнее изображение.")

@dp.message(Command(commands=['earth']))
async def send_recent_earth_image(message: Message):
    images_data = get_recent_epic_images()
    if images_data:
        latest_image_data = images_data[0]
        image_url = get_image_url(latest_image_data)
        caption = (
            f"Дата: {latest_image_data['date']}\n"
            f"Позиция: {latest_image_data['centroid_coordinates']}\n"
            f"Луна: {'Да' if 'lunar_position' in latest_image_data and latest_image_data['lunar_position'] else 'Нет'}"
        )
        await message.answer_photo(photo=image_url, caption=caption)
    else:
        await message.answer("Не удалось получить изображение. Попробуйте позже.")

async def main():
    # Запуск поллинга
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())