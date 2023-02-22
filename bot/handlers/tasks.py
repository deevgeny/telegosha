"""
This module is responsible for handling /tasks command.

/tasks handler get active tasks from server and maps first task in the
response list to its specific handler.

Categories of tasks and sequence:
1. intro - introduction of new words
2. learn - learning new words
3. test - check new words knowledge
4. spell - check new words spelling
"""

import logging

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from lexicon.russian import API_ERROR_LEXICON, TASKS_LEXICON
from misc.api import backend_api

from .intro import intro_entry_point
from .learn import learn_entry_point
from .spelling import spelling_entry_point
from .test import test_entry_point

TASKS_MAP = {
    'intro': intro_entry_point,
    'learn': learn_entry_point,
    'test': test_entry_point,
    'spell': spelling_entry_point,
}

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


async def tasks_command(message: Message, state: FSMContext) -> None:
    """Handler for /tasks menu command."""
    data = await backend_api.get_user_tasks(user_tg_id=message.from_user.id)
    if isinstance(data, dict) and 'detail' in data:
        await message.answer(text=(f'{TASKS_LEXICON["title"]}'
                                   f'{API_ERROR_LEXICON[data["detail"]]}'))
    elif isinstance(data, list) and len(data) == 0:
        await message.answer(text=(f'{TASKS_LEXICON["title"]}'
                                   f'{TASKS_LEXICON["no_tasks"]}'))
    elif data[0]['category'] in TASKS_MAP:
        await TASKS_MAP[data[0]['category']](message, state, data[0])


def register_tasks_handlers(dp: Dispatcher):
    """"Helper function to register tasks handlers."""
    dp.register_message_handler(tasks_command, commands='tasks')
