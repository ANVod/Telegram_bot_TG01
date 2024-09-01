import asyncio
from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from config import TOKEN
import random

# Создаем экземпляр бота
bot = Bot(token=TOKEN)
# Создаем диспетчер
dp = Dispatcher()
# Создаем экземпляр Router
router = Router()

@dp.message(Command('photo'))
async def photo(message: Message):
    photos = [
        'https://cdn.lifehacker.ru/wp-content/uploads/2018/04/Kak-oboJti-blokirovku-Telegram_1523476695.jpg',
        'https://i.ytimg.com/vi/YLGWy-zI34E/maxresdefault.jpg',
        'https://1.bp.blogspot.com/-7VmgXfSkia8/WqEnhrcNnXI/AAAAAAAAHOE/m0Pq91OAmdUh1Oo6r8A6sXKw-xKIG5CHACLcBGAs/w1200-h630-p-k-no-nu/Telegram_veb_na_russkom_jazyke.jpg'
    ]
    rand_photo = random.choice(photos)
    print(f"Selected photo: {rand_photo}")  # Отладочное сообщение
    await message.answer_photo(photo=rand_photo, caption='Это супер крутая картинка')

@dp.message(F.photo)
async def react_photo(message: Message):
    responses = ['Ого, какая фотка!', 'Непонятно, что это такое', 'Не отправляй мне такое больше']
    rand_answ = random.choice(responses)
    await message.answer(rand_answ)

@dp.message(F.text == "что такое ИИ?")
async def aitext(message: Message):
    await message.answer('Искусственный интеллект — это свойство искусственных интеллектуальных систем выполнять творческие функции, которые традиционно считаются прерогативой человека; наука и технология создания интеллектуальных машин, особенно интеллектуальных компьютерных программ')

# Регистрируем хендлеры в роутере
@router.message(Command('help'))
async def help(message: Message):
    await message.answer("Этот бот умеет выполнять команды:\n/start\n/help")

@router.message(CommandStart())
async def start(message: Message):
    await message.answer("Приветики, я бот!")

async def main():
    # Включаем роутер в диспетчер
    dp.include_router(router)
    # Запускаем поллинг
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())