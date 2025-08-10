from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from main.database.request import get_categories, get_cards_by_category

#Кнопки для старта и регистрации пользователя
menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Каталог')],
    [KeyboardButton(text='Контакты')]
], resize_keyboard=True, input_field_placeholder='Выберите пункт меню...')


async def clients_name(name):
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text=name)]
    ], resize_keyboard=True, input_field_placeholder='Введите имя или оставьте такое же')

async def clients_phone():
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='Поделиться контактом', request_contact=True)]
    ], resize_keyboard=True, input_field_placeholder='Введите номер телефона')


async def client_location():
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='Отправить локацию', request_location=True)]
    ], resize_keyboard=True, input_field_placeholder='Отправить геолокацию')


#Конопки для катагорий товара и самого товара
async def categories():
    keyboard = InlineKeyboardBuilder()
    all_categories = await get_categories()

    for category in all_categories:
        keyboard.add(InlineKeyboardButton(text=category.name, callback_data=f'category_{category.id}'))

    return keyboard.adjust(2).as_markup()


async def cards(category_id):
    keyboard = InlineKeyboardBuilder()
    all_cards = await get_cards_by_category(category_id)

    for card in all_cards:
        keyboard.row(InlineKeyboardButton(text=f'{card.name} | {card.price}RUB', callback_data=f'card_{card.id}'))
    
    keyboard.row(InlineKeyboardButton(text='Назад', callback_data='categories'))
    return keyboard.as_markup()


async def back_to_categories(category_id, card_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Купить', callback_data=f'buy_{card_id}')],
        [InlineKeyboardButton(text='Назад', callback_data=f'category_{category_id}')]
    ])