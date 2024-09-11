import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
import requests
from googletrans import Translator
from config import TOKEN, THE_CAT_API_KEY

bot = Bot(token=TOKEN)
dp = Dispatcher()
translator = Translator()

def get_cat_breeds():
    url = "https://api.thecatapi.com/v1/breeds"
    headers = {"x-api-key": THE_CAT_API_KEY}
    response = requests.get(url, headers=headers)
    return response.json()

def get_cat_image_by_breed(breed_id):
    url = f"https://api.thecatapi.com/v1/images/search?breed_ids={breed_id}"
    headers = {"x-api-key": THE_CAT_API_KEY}
    response = requests.get(url, headers=headers)
    data = response.json()
    return data[0]['url'] if data else None

def get_breed_info(breed_name):
    breeds = get_cat_breeds()
    for breed in breeds:
        if breed['name'].lower() == breed_name.lower():
            return breed
    return None

def translate_text(text, dest_language='en'):
    translated = translator.translate(text, dest=dest_language)
    return translated.text

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Привет! Какая кошка тебя интересует? \n"
                         "Напиши мне название породы кошки,\n"
                         "и я пришлю тебе её фото и описание.")

@dp.message()
async def send_cat_info(message: Message):
    # Переводим введенное сообщение на английский
    breed_name_en = translate_text(message.text, 'en')
    breed_info = get_breed_info(breed_name_en)

    if breed_info:
        cat_image_url = get_cat_image_by_breed(breed_info['id'])
        if cat_image_url:
            info = (
                f"Порода - {breed_info['name']}\n"
                f"Описание - {breed_info.get('description', 'Описание отсутствует')}\n"
                f"Продолжительность жизни - {breed_info.get('life_span', 'неизвестно')} лет"
            )
            # Переводим описание обратно на русский
            translated_info = translate_text(info, 'ru')
            await message.answer_photo(photo=cat_image_url, caption=translated_info)
        else:
            await message.answer("Изображение для этой породы не найдено.")
    else:
        await message.answer("Порода не найдена. Попробуйте еще раз.")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())