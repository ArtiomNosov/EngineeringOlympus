from aiogram import Dispatcher, types

async def support_start(message: types.Message):
    await message.answer('Пишите @Artiom_Nosov в личные сообщения')

def register_handlers_support(dp: Dispatcher):
    dp.register_message_handler(support_start, commands='support', state='*')