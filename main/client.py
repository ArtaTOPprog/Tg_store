from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery

client = Router()

@client.message(CommandStart())
async def start(message: Message):
    await message.answer('Добро пожаловать!')