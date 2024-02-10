import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from app.config_reader import load_config
from app.handlers.exchange_rate import register_handlers_exchange_rate
from app.handlers.faq import register_handlers_faq
from app.handlers.support import register_handlers_support
from app.handlers.common import register_hendlers_common

# from app.db.functions import create_tables_if_not_exists, save_message_to_db, save_psychological_state_to_db, save_conditional_branch_to_db, get_psychological_state_id, get_chat_conditional_branches_from_db

logger = logging.getLogger(__name__)

async def set_commands(bot: Bot):
    commands = [
        # BotCommand(command='/form', description='Заполнить анкету'),
        # BotCommand(command='/edit', description='Отредактировать анкету'),
        BotCommand(command='/exchange_rate', description='Получить курсы валют и материалов'),
        BotCommand(command='/faq', description='Ответы на часто задаваемые вопросы'),
        BotCommand(command='/support', description='Техническая поддрежка'),
    ]
    await bot.set_my_commands(commands)

async def main():
    # Настройка логирования в stdout
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.error('Starting bot')

    # Парсинг файла конфигурации
    config = load_config('config/bot.ini')

    # Объявление и инициализация объектов бота и диспетчера
    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher(bot, storage=MemoryStorage())

    # Регистрация хэндлеров
    register_hendlers_common(dp, config.tg_bot.admin_id)
    register_handlers_exchange_rate(dp) # TODO
    register_handlers_faq(dp)
    register_handlers_support(dp)

    # Установка команд бота
    await set_commands(bot)
    # Запуск поллинга
    # await dp.skip_updates()  # пропуск накопившихся апдейтов (необязательно)
    await dp.start_polling()

if __name__ == '__main__':
    # create_tables_if_not_exists()
    asyncio.run(main())

# async def foo():
#     create_tables_if_not_exists()
#     await save_message_to_db('1', None, 'textbot', 'textuser', 'gpt-patient')
#     await save_psychological_state_to_db('name of state', 'super type', 'super description')
#     await save_conditional_branch_to_db(1, 'super branch name', 'много врёшь', 'будет плохо жить')
#     await save_conditional_branch_to_db(1, 'super branch name', 'много врёшь', 'будет плохо жить')
#     res1 = await get_psychological_state_id('name of state')
#     res2 = await get_chat_conditional_branches_from_db('name of state')
#     print(res1, res2)
#
# asyncio.run(foo())