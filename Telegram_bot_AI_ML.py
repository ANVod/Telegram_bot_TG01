import logging
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from config import TOKEN, AIML_API_KEY

AIML_API_URL = 'https://api.aimlapi.com/v1/chat'

logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

async def get_aiml_response(user_message: str) -> str:
    headers = {
        'Authorization': f'Bearer {AIML_API_KEY}',
        'Content-Type': 'application/json'
    }
    data = {
        'message': user_message
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(AIML_API_URL, headers=headers, json=data) as response:
            if response.status == 200:
                result = await response.json()
                return result.get('response', 'Извините, я не могу ответить на это сейчас.')
            else:
                return 'Ошибка при подключении к AIML API.'

@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Привет! Отправь мне сообщение, и я отвечу с использованием AIML API.")

@dp.message()
async def handle_message(message: Message):
    user_message = message.text
    response = await get_aiml_response(user_message)
    await message.answer(response)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())