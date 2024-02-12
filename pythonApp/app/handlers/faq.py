from aiogram import Dispatcher, types

async def faq_start(message: types.Message):
    await message.answer('faq\n\n \
Сайты, с которых собираются данные: exchangerate-api.com, cb.rf, metaltorg.ru \
Список доступных валют можно посмотреть по ссылке: https://www.exchangerate-api.com/docs/supported-currencies \
главный разработчик @Artiom_Nosov')

def register_handlers_faq(dp: Dispatcher):
    dp.register_message_handler(faq_start, commands='faq', state='*')

