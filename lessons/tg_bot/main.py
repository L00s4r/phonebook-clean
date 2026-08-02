import asyncio
import sys

# ФИКС ДЛЯ WINDOWS
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

TOKEN = "ВАШ_ТОКЕН"

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Привет!")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())