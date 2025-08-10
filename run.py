from aiogram import Bot, Dispatcher
import asyncio
from main.client import client
from main.database.models import init_models


async def start_bot():
    await init_models() #Создание базы данных
    print('Бот запущен')

async def shotdown_bot():
    print('Выключение бота')



async def main():
    bot = Bot(token='8226303674:AAF6uW_CV--3JwM1mqKXbtdMn4Qh097iQXI')
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