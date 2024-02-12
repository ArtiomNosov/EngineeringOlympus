import datetime

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from priceParser import main

from app.db.functions import *
max_str_length = 255

class FillСurrencies(StatesGroup):
    waiting_platform = State()
    waiting_material = State()

async def platform_inputted(message: types.Message, state: FSMContext):
    if len(message.text) > max_str_length:
        await message.answer('Пожалуйста, напишите название короче 255 символов')
        return
    await state.update_data(waiting_platform=message.text)

    await state.set_state(FillСurrencies.waiting_material.state)
    await message.answer('Теперь пришлите название материала: CASTIRON или STEEL')

async def get_material(message: types.Message, state: FSMContext):
    if len(message.text) > max_str_length:
        await message.answer('Пожалуйста, напишите название короче 255 символов')
        return
    await state.update_data(waiting_material=message.text)

    await state.set_state(FillСurrencies.waiting_material.state)

    user_data = await state.get_data()
    await print_exchange_rate(message, user_data.get('waiting_platform'), user_data.get('waiting_material'))
    await state.finish()

async def exchange_rate(message: types.Message, state: FSMContext):
    # print(user_exists_in_db(message.from_id))
    # if not user_exists_in_db(message.from_id):
    #     await message.answer('Вы ещё не заполняли анкету, сначала заполните анкету')
    #     await state.finish()
    #     return
    await message.answer('Напишите название платформы METALTORG или CBRF')
    await state.set_state(FillСurrencies.waiting_platform.state)


def register_handlers_materials(dp: Dispatcher):
    dp.register_message_handler(exchange_rate, commands='materials', state='*')
    dp.register_message_handler(platform_inputted, state=FillСurrencies.waiting_platform)
    dp.register_message_handler(get_material, state=FillСurrencies.waiting_material)

from app.exchange_rate_API.functions import *

async def test_get_exchange_rate_from_API(name1, name2):
    outer = main.Parser()
    return outer.parseOutside(name1, name2)

async def print_exchange_rate(message, currency1, currency2):
    exchange_rate = await test_get_exchange_rate_from_API(currency1, currency2)
    try:
        await message.answer(f"1 тонна {currency2} стоит {exchange_rate}$ согласно {currency1}", reply_markup=types.ReplyKeyboardRemove())
    except Exception as e:
        await message.answer(f"Ошибка: {e}", reply_markup=types.ReplyKeyboardRemove())
