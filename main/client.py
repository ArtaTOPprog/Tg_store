from aiogram import Router, F
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import Message, CallbackQuery
from main.keyboard import menu, clients_name, clients_phone, categories, back_to_categories
from aiogram.fsm.context import FSMContext

from main.database.request import set_user, update_user, get_card

client = Router()


#Старт и регистрация пользователя

@client.message(CommandStart())
async def start(message: Message, state: FSMContext):
    is_user = await set_user(message.from_user.id)
    if not is_user:
        await message.answer('Добро пожаловать!\nПройдите регистрацию', reply_markup=await clients_name(message.from_user.first_name))
        await state.set_state('reg_name')
    else:
        await message.answer('Добро пожаловать в интернет магазин\nИспользую кнопки ниже ознакомтесь с меню', reply_markup=menu)


@client.message(StateFilter('reg_name'))
async def reg_name(message: Message, state: FSMContext):
    if len(message.text) > 1:
        await state.update_data(name=message.text.capitalize())
    else:
        await message.answer('Введите правильное имя')
        await start()
    await message.answer('Введите ваш номер телефона!\n(От этого зависит получители вы заказ или нет)', reply_markup=await clients_phone())
    await state.set_state('reg_phone')

@client.message(F.contact, StateFilter('reg_phone'))
async def reg_phone(message: Message, state: FSMContext):
    await state.update_data(phone_number = message.contact.phone_number)
    data = await state.get_data()
    await update_user(message.from_user.id, data['name'], data['phone_number'])

    await message.answer('Регистрация прошла успешно\nДобро пожаловать в интернет магазин!', reply_markup=menu)

    await state.clear()

@client.message(StateFilter('reg_phone'))
async def reg_phone(message: Message, state: FSMContext):
    await state.update_data(phone_number = message.text)
    data = await state.get_data()
    await update_user(message.from_user.id, data['name'], data['phone_number'])

    await message.answer('Регистрация прошла успешно\nДобро пожаловать в интернет магазин!', reply_markup=menu)

    await state.clear()


#Каталог товаров

@client.callback_query(F.data == 'categories')
@client.message(F.text == 'Каталог')
async def catalog(event: Message | CallbackQuery):
    if isinstance(event, Message):
        await event.answer('Выберите категорию товаров', reply_markup = await categories())
    else:
        await event.answer('Вывернулись назад')
        await event.message.edit_text('Выберите категорию товаров', reply_markup= await categories())


@client.callback_query(F.data.startwith('category_'))
async def cards(callback: CallbackQuery):
    await callback.answer()
    category_id = callback.data.split('_')[1]

    await callback.message.edit_text('Выберите товар:',reply_markup = await cards(category_id))


@client.callback_query(F.data.startwith('card_'))
async def card_info(callback: CallbackQuery):
    await callback.answer()
    card_id = callback.data.split('_')[1]
    card = await get_card(card_id)
    await callback.message.delete()
    await callback.message.answer_photo(photo=card.image,caption=f'{card.name}\n\n{card.description}\n\n{card.price}RUB',
                                        reply_markup=await back_to_categories(card.category_id, card.id))
    
#Вспомогательные хендлеры

@client.message(F.photo)
async def get_id_photo(message: Message):
    await message.answer(message.photo[-1].file_id)
