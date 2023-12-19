import asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.message import ContentTypes
from aiogram.types.message import ContentType
from config import bot_token
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()
loop = asyncio.get_event_loop()

bot = Bot(bot_token)

dp = Dispatcher(bot, loop=loop, storage=storage)

async def checkdays_periodically():
    while True:
        await checkdays() 
        await checkviews() 
        await asyncio.sleep(30)  # Ожидание в течение 30 секунд

if __name__ == "__main__":
    from heandlers import dp, send_to_admin, checkdays, checkviews
    loop.create_task(checkdays_periodically())
    executor.start_polling(dp, on_startup=send_to_admin)
