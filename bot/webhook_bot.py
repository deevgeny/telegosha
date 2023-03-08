import logging
import os

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils.executor import start_webhook
from dotenv import load_dotenv

from handlers.intro import register_intro_handlers
from handlers.learn import register_learn_handlers
from handlers.menu import register_menu_handlers
from handlers.progress import register_progress_handlers
from handlers.spelling import register_spelling_handlers
from handlers.tasks import register_tasks_handlers
from handlers.test import register_test_handlers
from keyboards.main_menu import set_main_menu

load_dotenv()

TG_API_TOKEN: str = os.getenv('TG_API_TOKEN', '')
WEBHOOK_HOST: str = os.getenv('WEBHOOK_HOST', '')
WEBHOOK_PATH: str = os.getenv('WEBHOOK_PATH', '')
WEBHOOK_URL: str = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"
WEBAPP_HOST: str = '0.0.0.0'
WEBAPP_PORT: int = 8000

logger: logging = logging.getLogger(__name__)
storage: MemoryStorage = MemoryStorage()
bot: Bot = Bot(token=TG_API_TOKEN, parse_mode=types.ParseMode.HTML)
dp: Dispatcher = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())


async def on_startup(dp):
    logging.info('Setting webhook...')
    await bot.set_webhook(WEBHOOK_URL)

    # Set up main menu
    logging.info('Setting main menu...')
    set_main_menu(dp)

    logging.info('Registering handlers...')
    # Register handlers
    register_menu_handlers(dp)
    register_learn_handlers(dp)
    register_test_handlers(dp)
    register_tasks_handlers(dp)
    register_spelling_handlers(dp)
    register_progress_handlers(dp)
    register_intro_handlers(dp)


async def on_shutdown(dp):
    logging.warning('Deleting webhook...')
    # Delete webhook
    await bot.delete_webhook()

    logging.warning('Closing storage connection...')
    # Close DB connection (if used)
    await dp.storage.close()
    await dp.storage.wait_closed()
    logging.warning('Closing bot...')
    await bot.close()
    logging.warning('Bye!')


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s '
               u'[%(asctime)s] - %(name)s - %(message)s')
    logger.info('Starting bot...')
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
