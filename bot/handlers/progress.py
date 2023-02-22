"""
This module is responsible for displaying user progress.
"""
import logging

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from lexicon.russian import API_ERROR_LEXICON, PROGRESS_LEXICON
from misc.api import backend_api

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


async def user_porgress(message: Message, state: FSMContext) -> None:
    """Show user progress."""
    data = await backend_api.get_user_progress(user_tg_id=message.from_user.id)
    if isinstance(data, dict) and 'detail' in data:
        await message.answer(text=(f'{PROGRESS_LEXICON["title"]}'
                                   f'{API_ERROR_LEXICON[data["detail"]]}'))
    else:
        await message.answer(text=(
            f'{PROGRESS_LEXICON["title"]}'
            f'{PROGRESS_LEXICON["topics"]}{data["topics"]}\n'
            f'{PROGRESS_LEXICON["words"]}{data["words"]}\n'
            f'{PROGRESS_LEXICON["total_tasks"]}{data["total_tasks"]}\n'
            f'{PROGRESS_LEXICON["passed_tasks"]}{data["passed_tasks"]}'
        ))


def register_progress_handlers(dp: Dispatcher):
    """"Helper function to register progress handlers."""
    dp.register_message_handler(user_porgress, commands='progress')
