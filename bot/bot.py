import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from data.config import Config, load_config
from handlers.intro import register_intro_handlers
from handlers.learn import register_learn_handlers
from handlers.menu import register_menu_handlers
from handlers.progress import register_progress_handlers
from handlers.spelling import register_spelling_handlers
from handlers.tasks import register_tasks_handlers
from handlers.test import register_test_handlers
from keyboards.main_menu import set_main_menu

logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s '
               u'[%(asctime)s] - %(name)s - %(message)s')
    logger.info('Starting bot')

    config: Config = load_config()
    storage: MemoryStorage = MemoryStorage()
    bot: Bot = Bot(token=config.tg_bot.token, parse_mode=types.ParseMode.HTML)
    dp: Dispatcher = Dispatcher(bot, storage=storage)

    # Set up main menu
    await set_main_menu(dp)

    # Register handlers
    register_menu_handlers(dp)
    register_learn_handlers(dp)
    register_test_handlers(dp)
    register_tasks_handlers(dp)
    register_spelling_handlers(dp)
    register_progress_handlers(dp)
    register_intro_handlers(dp)

    try:
        await dp.start_polling()
    finally:
        await bot.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error('Bot stopped!')
