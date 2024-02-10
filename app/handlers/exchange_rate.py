import datetime

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from app.db.functions import *

max_str_length = 255

class FillСurrencies(StatesGroup):
    waiting_currency1 = State()
    waiting_currency2 = State()

async def currency1_inputted(message: types.Message, state: FSMContext):
    if len(message.text) > max_str_length:
        await message.answer('Пожалуйста, напишите имя валюты короче 255 символов')
        return
    await state.update_data(currency1=message.text)

    await state.set_state(FillСurrencies.waiting_currency2.state)
    await message.answer('Теперь пришлите название второй валюты')

async def get_currency2(message: types.Message, state: FSMContext):
    if len(message.text) > max_str_length:
        await message.answer('Пожалуйста, напишите имя валюты короче 255 символов')
        return
    await state.update_data(currency2=message.text)

    await state.set_state(FillСurrencies.waiting_currency2.state)

    user_data = await state.get_data()
    await print_exchange_rate(message, user_data.get('currency1'), user_data.get('currency2'))
    await state.finish()

async def exchange_rate(message: types.Message, state: FSMContext):
    # print(user_exists_in_db(message.from_id))
    # if not user_exists_in_db(message.from_id):
    #     await message.answer('Вы ещё не заполняли анкету, сначала заполните анкету')
    #     await state.finish()
    #     return
    await message.answer('Напишите первую валюту')
    await state.set_state(FillСurrencies.waiting_currency1.state)


def register_handlers_exchange_rate(dp: Dispatcher):
    dp.register_message_handler(exchange_rate, commands='exchange_rate', state='*')
    dp.register_message_handler(currency1_inputted, state=FillСurrencies.waiting_currency1)
    dp.register_message_handler(get_currency2, state=FillСurrencies.waiting_currency2)

from app.exchange_rate_API.functions import *

async def test_get_exchange_rate_from_API(currency1, currency2):
    amount = 1
    last_updated_datetime, exchange_rate = convert_currency_erapi(currency1, currency2, amount)
    print("Last updated datetime:", last_updated_datetime)
    print(f"{amount} {currency1} = {exchange_rate} {currency2}")
    return exchange_rate

async def print_exchange_rate(message, currency1, currency2):
    exchange_rate = await test_get_exchange_rate_from_API(currency1, currency2)
    try:
        await message.answer(f"1 {currency1} равно {exchange_rate} {currency2} согласно https://www.exchangerate-api.com/", reply_markup=types.ReplyKeyboardRemove())
    except Exception as e:
        await message.answer(f"Ошибка: {e}", reply_markup=types.ReplyKeyboardRemove())
