"""
This module is responsible for displaying a list of all user tasks.

Functionality:
- User can navigate over the tasks list by pressing inline keyboard bottons.
- During navigation, callback message is edited setting cursor to a selected
task.
- After pushing select button, user will be redirected to another module
handler responsible for a specific task handling.
"""

import logging

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from keyboards.user_keyboards import inline_keyboard
from lexicon.russian import TASKS_LEXICON
from services.api import backend_api

from . import callbacks
from .quiz_handlers import quiz_intro
from .spelling_handlers import spelling_intro

TASKS_MAP = {
    'quiz': quiz_intro,
    'spelling': spelling_intro,
}

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Tasks(StatesGroup):
    """Tasks FSM."""
    scroll = State()


def scroll_tasks_list(tasks: list, active_task: int = 0) -> str:
    """Create tasks scroll list message.

    Input: list of tasks
    Output:
      task 1
    > task 2 (active task with pointer)
      task 3
      ...
    """
    msg = ''
    for i in range(len(tasks)):
        if active_task == i:
            msg = msg + (f'{TASKS_LEXICON["pointer"]} '
                         f'<b>{TASKS_LEXICON[tasks[i]["category"]]} - '
                         f'{tasks[i]["topic"].lower()}</b>\n')
        else:
            msg = msg + (f'{TASKS_LEXICON["tab"]}'
                         f'{TASKS_LEXICON[tasks[i]["category"]]} - '
                         f'{tasks[i]["topic"].lower()}\n')
    return msg


async def tasks_command(message: Message, state: FSMContext) -> None:
    """Handler for /tasks menu command."""
    data = await backend_api.get_user_tasks(user_tg_id=message.from_user.id)
    if len(data) == 0:
        await message.answer(text=(f'{TASKS_LEXICON["title"]}'
                                   f'{TASKS_LEXICON["no_tasks"]}'))
    else:
        keyboard = inline_keyboard(
            buttons=[[TASKS_LEXICON['prev_button'], callbacks.PREV_TASK],
                     [TASKS_LEXICON['select_button'], callbacks.SELECT_TASK],
                     [TASKS_LEXICON['next_button'], callbacks.NEXT_TASK]],
            row_width=3
        )
        tasks_list = scroll_tasks_list(data)
        await state.update_data(tasks=data, active_task=0)
        await state.set_state(Tasks.scroll)
        await message.answer(text=f'{TASKS_LEXICON["title"]}{tasks_list}',
                             reply_markup=keyboard)


async def select_task(callback: CallbackQuery, state: FSMContext) -> None:
    """Select task handler."""
    data = await state.get_data()
    task = data['tasks'][data['active_task']]
    await state.reset_state()
    if task['category'] in TASKS_MAP:
        await TASKS_MAP[task['category']](callback, state, task)
        return
    await callback.answer(text=TASKS_LEXICON['error'])


async def previous_task(callback: CallbackQuery, state: FSMContext) -> None:
    """Previous task handler."""
    data = await state.get_data()
    if len(data['tasks']) == 1:
        await callback.answer()
        return
    active_task = (data['active_task'] - 1) % len(data['tasks'])
    tasks_list = scroll_tasks_list(tasks=data['tasks'],
                                   active_task=active_task)
    await state.update_data(active_task=active_task)
    await callback.message.edit_text(
        text=f'{TASKS_LEXICON["title"]}{tasks_list}',
        reply_markup=callback.message.reply_markup
    )


async def next_task(callback: CallbackQuery, state: FSMContext):
    """Next task handler."""
    data = await state.get_data()
    if len(data['tasks']) == 1:
        await callback.answer()
        return
    active_task = (data['active_task'] + 1) % len(data['tasks'])
    tasks_list = scroll_tasks_list(tasks=data['tasks'],
                                   active_task=active_task)
    await state.update_data(active_task=active_task)
    await callback.message.edit_text(
        text=f'{TASKS_LEXICON["title"]}{tasks_list}',
        reply_markup=callback.message.reply_markup
    )


def register_tasks_handlers(dp: Dispatcher):
    """"Helper function to register tasks handlers."""
    dp.register_message_handler(tasks_command, commands='tasks')
    dp.register_callback_query_handler(select_task, text=callbacks.SELECT_TASK,
                                       state=Tasks.scroll)
    dp.register_callback_query_handler(next_task, text=callbacks.NEXT_TASK,
                                       state=Tasks.scroll)
    dp.register_callback_query_handler(previous_task, text=callbacks.PREV_TASK,
                                       state=Tasks.scroll)
