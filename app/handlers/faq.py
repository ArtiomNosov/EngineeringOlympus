from aiogram import Dispatcher, types

async def faq_start(message: types.Message):
    await message.answer('faq\n\n' \
                         'Список доступных валют можно посмотреть по ссылке: https://www.exchangerate-api.com/docs/supported-currencies')

def register_handlers_faq(dp: Dispatcher):
    dp.register_message_handler(faq_start, commands='faq', state='*')

