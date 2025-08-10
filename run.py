from aiogram import Bot, Dispatcher
import asyncio
from main.client import client
from main.database.models import init_models
import os
from dotenv import load_dotenv


async def start_bot():
    await init_models() #Создание базы данных
    print('Бот запущен')

async def shotdown_bot():
    print('Выключение бота')



async def main():
    load_dotenv()
    bot = Bot(token=os.getenv('TOKEN'))
    dp = Dispatcher()
    dp.include_router(client)

    dp.startup.register(start_bot)
    dp.shutdown.register(shotdown_bot)

    await dp.start_polling(bot)


if __name__=='__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')